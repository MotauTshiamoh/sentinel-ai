from pydantic import BaseModel, Field


class SecurityEvent(BaseModel):
    source_ip: str
    destination_ip: str
    source_port: int = Field(ge=1, le=65535)
    destination_port: int = Field(ge=1, le=65535)
    protocol: str
    bytes_sent: int = Field(ge=0)