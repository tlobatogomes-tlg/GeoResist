from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Camada(Base):
    __tablename__ = "camadas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    furo_id: Mapped[int] = mapped_column(
        ForeignKey("furos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Intervalo da camada
    profundidade_inicial: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    profundidade_final: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Origem geotécnica do material
    # Exemplos: aterro, solo_residual, solo_transportado,
    # saprolito, rocha_alterada etc.
    origem: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # Descrição tátil-visual
    # Exemplo: Argila silto-arenosa
    descricao_material: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    cor: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Informações complementares:
    # fragmentos, pedregulhos, matéria orgânica etc.
    complementos: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    furo: Mapped["Furo"] = relationship(
        "Furo",
        back_populates="camadas",
    )
