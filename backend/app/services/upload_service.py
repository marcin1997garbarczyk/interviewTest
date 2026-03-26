from fastapi import UploadFile

from app.schemas.upload import FileContentResponse, FileUploadResponse
from app.services.file_service import FileService


class UploadService:
    def __init__(self, file_service: FileService) -> None:
        self.file_service = file_service

    async def upload_file(self, file: UploadFile) -> FileUploadResponse:
        if not self.file_service.validate_format(file.filename):
            raise ValueError("Unsupported file format")
        stored_path = await self.file_service.upload_file(file)
        return FileUploadResponse(filename=file.filename, path=str(stored_path), is_valid_format=True)

    def read_uploaded_file(self, path: str) -> FileContentResponse:
        try:
            content = self.file_service.read_file_content(path)
        except FileNotFoundError as exc:
            raise LookupError("File not found") from exc
        return FileContentResponse(path=path, content=content)
