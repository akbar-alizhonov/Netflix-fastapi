from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class File(Base):
    __tablename__ = 'file'
    __table_args__ = {"comment": "Файлы S3 хранилища"}

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    bucket_name: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    content_type: Mapped[str]