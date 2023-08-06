from datetime import datetime
from enum import Enum
from typing import Annotated, Dict, List, Literal, Union
from uuid import UUID

from jsonschema.exceptions import SchemaError
from jsonschema.validators import Draft202012Validator
from kilroy_ws_client_py_sdk import JSON
from pydantic import BaseModel, Field


class JSONSchema(dict):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, schema: JSON) -> JSON:
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as e:
            raise ValueError(
                "Schema is not a valid JSON Schema 2020-12."
            ) from e
        if "type" not in schema:
            raise ValueError("Schema should have a type field.")
        elif schema["type"] != "object":
            raise ValueError("Only object types are allowed.")
        return schema


class PostSchema(BaseModel):
    postSchema: JSONSchema


class StatusEnum(str, Enum):
    loading = "loading"
    ready = "ready"


class Status(BaseModel):
    status: StatusEnum


class StatusNotification(BaseModel):
    old: Status
    new: Status


class Config(BaseModel):
    config: JSON


class ConfigSchema(BaseModel):
    configSchema: JSONSchema


class ConfigNotification(BaseModel):
    old: Config
    new: Config


class ConfigSetRequest(BaseModel):
    set: Config


class ConfigSetReply(BaseModel):
    old: Config
    new: Config


class GenerateRequest(BaseModel):
    numberOfPosts: int


class GenerateReply(BaseModel):
    postNumber: int
    postId: UUID
    post: JSON


class FitPostsRequest(BaseModel):
    postNumber: int
    post: JSON


class FitPostsReply(BaseModel):
    success: Literal[True]


class PostScore(BaseModel):
    postId: UUID
    score: float


class FitScoresRequest(BaseModel):
    scores: List[PostScore]


class FitScoresReply(BaseModel):
    success: Literal[True]


class StepRequest(BaseModel):
    pass


class StepReply(BaseModel):
    success: Literal[True]


class MetricTypeEnum(str, Enum):
    series = "series"
    timeseries = "timeseries"


class BaseMetricInfo(BaseModel):
    label: str


class BaseSeriesMetricInfo(BaseMetricInfo):
    stepLabel: str
    valueLabel: str


class SeriesMetricInfo(BaseSeriesMetricInfo):
    type: Literal[MetricTypeEnum.series] = MetricTypeEnum.series
    stepType: Literal["int", "float"]
    valueType: Literal["int", "float"]


class TimeseriesMetricInfo(BaseSeriesMetricInfo):
    type: Literal[MetricTypeEnum.timeseries] = MetricTypeEnum.timeseries
    valueType: Literal["int", "float"]


MetricInfo = Annotated[
    Union[
        SeriesMetricInfo,
        TimeseriesMetricInfo,
    ],
    Field(discriminator="type"),
]


class MetricsInfo(BaseModel):
    metrics: Dict[str, MetricInfo]


class SeriesMetricNotificationData(BaseModel):
    type: Literal[MetricTypeEnum.series] = MetricTypeEnum.series
    step: float
    value: float


class TimeseriesMetricNotificationData(BaseModel):
    type: Literal[MetricTypeEnum.timeseries] = MetricTypeEnum.timeseries
    step: datetime = Field(default_factory=datetime.utcnow)
    value: float


MetricNotificationData = Annotated[
    Union[
        SeriesMetricNotificationData,
        TimeseriesMetricNotificationData,
    ],
    Field(discriminator="type"),
]


class MetricsNotification(BaseModel):
    name: str
    data: MetricNotificationData
