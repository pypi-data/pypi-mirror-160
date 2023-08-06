from typing import Any, Dict, Mapping, Optional

from pyspark.sql import Column, DataFrame
import pyspark.sql.functions as F

from aporia.core.context import get_context
from aporia.core.types.field import FieldCategory


def timestamp_to_iso8601(timestamp: Column) -> Column:
    value = F.date_format(timestamp, "yyyy-MM-dd'T'HH:mm:ss.SSSZ")
    return F.regexp_replace(value, r"\+0000", "+00:00")


def apply_dataset_schema(
    data: DataFrame,
    features: Dict[str, str],
    predictions: Dict[str, str],
    raw_inputs: Optional[Dict[str, str]] = None,
    labels: Optional[Dict[str, str]] = None,
    id_column: Optional[str] = None,
    timestamp_column: Optional[str] = None,
) -> DataFrame:
    select_params = []

    if id_column is not None:
        select_params.append(F.col(id_column).alias("id"))
    else:
        select_params.append(F.expr("uuid()").alias("id"))

    if timestamp_column is not None:
        select_params.append(F.col(timestamp_column).alias("timestamp"))
    else:
        select_params.append(F.current_timestamp().alias("timestamp"))

    feature_renames = [F.col(column).alias(name) for name, column in features.items()]
    select_params.append(F.struct(*feature_renames).alias("features"))

    prediction_renames = [F.col(column).alias(name) for name, column in predictions.items()]
    select_params.append(F.struct(*prediction_renames).alias("predictions"))

    if raw_inputs is not None:
        raw_input_renames = [F.col(column).alias(name) for name, column in raw_inputs.items()]
        select_params.append(F.struct(*raw_input_renames).alias("raw_inputs"))

    if labels is not None:
        label_renames = [F.col(column).alias(name) for name, column in labels.items()]
        select_params.append(F.struct(*label_renames).alias("actuals"))

    return data.select(*select_params)


def add_metadata_columns(
    data: DataFrame,
    model_id: str,
    version_name: str,
    version_id: str,
    environment: str,
    environment_id: str,
    add_occurred_at: bool,
) -> DataFrame:
    current_timestamp = timestamp_to_iso8601(F.current_timestamp())

    data = data.select(
        "*",
        F.lit(model_id).alias("model_id"),
        F.lit(version_name).alias("model_version"),
        F.lit(version_id).alias("model_version_id"),
        F.lit(environment).alias("environment"),
        F.lit(environment_id).alias("environment_id"),
        current_timestamp.alias("updated_at"),
        current_timestamp.alias("created_at"),
        F.date_format(data["timestamp"], "yyyy_MM").alias("date"),
    )

    if add_occurred_at:
        data = data.select("*", timestamp_to_iso8601(data["timestamp"]).alias("occurred_at"))

    return data


def log_batch_prediction(
    apr_model: Any,
    version_id: str,
    data: DataFrame,
    timestamp_column: Optional[str] = None,
    id_column: Optional[str] = None,
    features: Optional[Mapping[str, str]] = None,
    predictions: Optional[Mapping[str, str]] = None,
    raw_inputs: Optional[Mapping[str, str]] = None,
    labels: Optional[Mapping[str, str]] = None,
    spark_options: Optional[Mapping[str, str]] = None,
):
    # Fetch cluster and environment ID
    context = get_context()

    response = context.event_loop.run_coroutine(
        context.http_client.post(
            url="environments",
            data={"name": apr_model._config.environment},
        )
    )

    cluster_id =  response["cluster_id"]
    environment_id = response["environment_id"]

    # Fetch model version schema
    version_schema = apr_model._training.get_version_schema()

    # Apply default schema + overrides
    features = {
        **{field: field for field in version_schema[FieldCategory.FEATURES].keys()},
        **(features if features is not None else {}),
    }

    predictions = {
        **{field: field for field in version_schema[FieldCategory.PREDICTIONS].keys()},
        **(predictions if predictions is not None else {}),
    }

    if FieldCategory.RAW_INPUTS in version_schema:
        raw_inputs = {
            **{field: field for field in version_schema.get(FieldCategory.RAW_INPUTS, {}).keys()},
            **(raw_inputs if raw_inputs is not None else {}),
        }

    # Add types (e.g my_field -> numeric_my_field)
    features = {
        f"{version_schema[FieldCategory.FEATURES][key].value}_{key}": value
        for key, value in features.items()
    }
    predictions = {
        f"{version_schema[FieldCategory.PREDICTIONS][key].value}_{key}": value
        for key, value in predictions.items()
    }

    if labels is not None:
        labels = {
            f"{version_schema[FieldCategory.PREDICTIONS][key].value}_{key}": value
            for key, value in labels.items()
        }

    if raw_inputs is not None:
        raw_inputs = {
            f"{version_schema[FieldCategory.RAW_INPUTS][key].value}_{key}": value
            for key, value in raw_inputs.items()
        }

    data = apply_dataset_schema(
        data=data,
        id_column=id_column,
        timestamp_column=timestamp_column,
        features=features,
        predictions=predictions,
        raw_inputs=raw_inputs,
        labels=labels,
    )

    data = add_metadata_columns(
        data=data,
        model_id=apr_model.model_id,
        version_name=apr_model.model_version,
        version_id=version_id,
        environment=apr_model._config.environment,
        environment_id=environment_id,
        add_occurred_at=(predictions is not None),
    )

    base_index = f"aporia_{cluster_id}_pred_{apr_model.model_id}_{version_id}_{environment_id}"

    options = {
        "es.nodes.wan.only": "true",
        "es.port": str(apr_model._config.port),
        "es.nodes": str(apr_model._config.host),
        "es.net.http.header.Authorization": f"Bearer {apr_model._config.token}",
        "es.nodes.path.prefix": "/v1/es/",
        "es.resource": f"{base_index}_{{date}}",
        "es.write.operation": "index"
        if features is not None and predictions is not None
        else "upsert",
        "es.mapping.id": "id",
        "es.mapping.exclude": "id,timestamp,date",
        "es.batch.write.refresh": "false",
        "es.net.ssl": "true" if apr_model._config.port == 443 else "false",
        "es.net.ssl.cert.allow.self.signed": "false" if apr_model._config.verify_ssl else "true",
        **(spark_options if spark_options is not None else {}),
    }

    data.write.format("org.elasticsearch.spark.sql").options(**options).mode("append").save()
