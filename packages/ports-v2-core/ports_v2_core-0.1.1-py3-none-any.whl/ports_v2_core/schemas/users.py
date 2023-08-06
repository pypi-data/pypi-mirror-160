from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from uuid import UUID


class EUserStatus(Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"


class UserSchema(BaseModel):
    """
    User pydantic schema.
    Represent user retrieved from UserService
    """

    id: UUID
    email: EmailStr
    name: str
    hashed_password: str
    mfa_enabled: bool = False
    status: EUserStatus
    created_at: datetime
    updated_at: datetime


class CreateUserSchema(BaseModel):
    email: EmailStr
    name: str
    password: str
    mfa_enabled: bool = False


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class SecretsSchema(BaseModel):
    id: str
    secret: str


class MfaVerifySchema(BaseModel):
    record_uuid: str
    mfa_code: str


class SessionSecretsSchema(BaseModel):
    session_id: str
    secret: str
