from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"comment": "Пользователи"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(comment="Имя")
    last_name: Mapped[str] = mapped_column(comment="Фамилия")
    surname: Mapped[str] = mapped_column(comment="Отчество", nullable=True)
    birthday: Mapped[datetime] = mapped_column(comment="Дата рождения", nullable=True)
    email: Mapped[str] = mapped_column(comment="Почта", index=True, unique=True)
    username: Mapped[str] = mapped_column(comment="Имя пользователя", index=True, unique=True)
    password: Mapped[str] = mapped_column(comment="Пароль")
    deleted: Mapped[bool] = mapped_column(comment="Удален ли пользователь", default=False)


