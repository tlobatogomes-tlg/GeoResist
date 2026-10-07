from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Furo(Base):
    __tablename__ = "furos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    projeto_id: Mapped[int] = mapped_column(
        ForeignKey("projetos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Identificação da sondagem
    identificacao: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Sistema previsto na NBR 6484:2020
    sistema: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # Locação
    coordenada_x: Mapped[float | None] = mapped_column(Float, nullable=True)
    coordenada_y: Mapped[float | None] = mapped_column(Float, nullable=True)
    sistema_coordenadas: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # Referência altimétrica
    cota_boca: Mapped[float | None] = mapped_column(Float, nullable=True)
    referencia_nivel: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    # Execução
    data_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_termino: Mapped[date | None] = mapped_column(Date, nullable=True)

    profundidade_final: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sondador: Mapped[str | None] = mapped_column(String(150), nullable=True)

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    projeto: Mapped["Projeto"] = relationship(
        "Projeto",
        back_populates="furos",
    )

    registros_spt: Mapped[list["RegistroSPT"]] = relationship(
        "RegistroSPT",
        back_populates="furo",
        cascade="all, delete-orphan",
        order_by="RegistroSPT.profundidade",
    )
    camadas: Mapped[list["Camada"]] = relationship(
        "Camada",
        back_populates="furo",
        cascade="all, delete-orphan",
        order_by="Camada.profundidade_inicial",
    )

