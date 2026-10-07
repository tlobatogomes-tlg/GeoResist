from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Projeto(Base):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cliente: Mapped[str | None] = mapped_column(String(150), nullable=True)
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estado: Mapped[str | None] = mapped_column(String(2), nullable=True)

    endereco: Mapped[str | None] = mapped_column(String(250), nullable=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    furos: Mapped[list["Furo"]] = relationship(
        "Furo",
        back_populates="projeto",
        cascade="all, delete-orphan",
    )
