from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from jsonschema.exceptions import SchemaError
from jsonschema.validators import Draft202012Validator
from kilroy_ws_client_py_sdk import JSON
from pydantic import BaseModel


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


class PostRequest(BaseModel):
    post: JSON


class PostReply(BaseModel):
    postId: UUID


class ScoreRequest(BaseModel):
    postId: UUID


class ScoreReply(BaseModel):
    score: float


class ScrapRequest(BaseModel):
    limit: Optional[int] = None
    before: Optional[datetime] = None
    after: Optional[datetime] = None


class ScrapReply(BaseModel):
    postId: UUID
    post: JSON
