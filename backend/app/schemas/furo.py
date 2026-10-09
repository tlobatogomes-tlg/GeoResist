from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FuroBase(BaseModel):
    identificacao: str = Field(min_length=1, max_length=50)

    sistema: Literal["manual", "mecanizado"]

    coordenada_x: float | None = None
    coordenada_y: float | None = None
    sistema_coordenadas: str | None = None

    cota_boca: float | None = None
    referencia_nivel: str | None = None

    data_inicio: date | None = None
    data_termino: date | None = None

    profundidade_final: float | None = Field(
        default=None,
        ge=0,
        allow_inf_nan=False,
    )

    sondador: str | None = None
    observacoes: str | None = None


class FuroCreate(FuroBase):
    projeto_id: int


class FuroUpdate(BaseModel):
    identificacao: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    sistema: Literal["manual", "mecanizado"] | None = None

    coordenada_x: float | None = None
    coordenada_y: float | None = None
    sistema_coordenadas: str | None = None

    cota_boca: float | None = None
    referencia_nivel: str | None = None

    data_inicio: date | None = None
    data_termino: date | None = None

    profundidade_final: float | None = Field(
        default=None,
        ge=0,
        allow_inf_nan=False,
    )

    sondador: str | None = None
    observacoes: str | None = None


class FuroResponse(FuroBase):
    id: int
    projeto_id: int

    model_config = ConfigDict(from_attributes=True)
