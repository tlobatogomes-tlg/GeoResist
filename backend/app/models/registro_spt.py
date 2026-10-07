from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RegistroSPT(Base):
    __tablename__ = "registros_spt"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    furo_id: Mapped[int] = mapped_column(
        ForeignKey("furos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Profundidade inicial do ensaio
    profundidade: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # 1º trecho
    golpes_1: Mapped[int | None] = mapped_column(Integer, nullable=True)
    penetracao_1: Mapped[float | None] = mapped_column(Float, nullable=True)
    condicao_1: Mapped[str] = mapped_column(
        String(20),
        default="normal",
        nullable=False,
    )

    # 2º trecho
    golpes_2: Mapped[int | None] = mapped_column(Integer, nullable=True)
    penetracao_2: Mapped[float | None] = mapped_column(Float, nullable=True)
    condicao_2: Mapped[str] = mapped_column(
        String(20),
        default="normal",
        nullable=False,
    )

    # 3º trecho
    golpes_3: Mapped[int | None] = mapped_column(Integer, nullable=True)
    penetracao_3: Mapped[float | None] = mapped_column(Float, nullable=True)
    condicao_3: Mapped[str] = mapped_column(
        String(20),
        default="normal",
        nullable=False,
    )

    # Registro original e observações de campo
    registro_campo: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    furo: Mapped["Furo"] = relationship(
        "Furo",
        back_populates="registros_spt",
    )
