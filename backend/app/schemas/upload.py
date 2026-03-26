from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    filename: str
    path: str
    is_valid_format: bool


class FileContentResponse(BaseModel):
    path: str
    content: str
