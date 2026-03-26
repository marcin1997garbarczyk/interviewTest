from pathlib import Path

from fastapi import UploadFile


class FileService:
    allowed_suffixes = {".txt", ".md", ".json", ".csv"}

    def __init__(self, base_storage_path: str = "app/storage") -> None:
        self.storage_path = Path(base_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file: UploadFile) -> Path:
        file_path = self.storage_path / file.filename
        content = await file.read()
        file_path.write_bytes(content)
        return file_path

    def read_file_content(self, path: str) -> str:
        file_path = Path(path)
        return file_path.read_text(encoding="utf-8")

    def validate_format(self, filename: str) -> bool:
        suffix = Path(filename).suffix.lower()
        return suffix in self.allowed_suffixes
