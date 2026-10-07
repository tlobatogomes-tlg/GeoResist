from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CondicaoSPT = Literal[
    "normal",
    "peso_haste",
    "peso_martelo",
    "sem_avanco",
    "nao_executado",
]


class RegistroSPTBase(BaseModel):
    profundidade: float = Field(ge=0)

    golpes_1: int | None = Field(default=None, ge=0)
    penetracao_1: float | None = Field(default=None, ge=0)
    condicao_1: CondicaoSPT = "normal"

    golpes_2: int | None = Field(default=None, ge=0)
    penetracao_2: float | None = Field(default=None, ge=0)
    condicao_2: CondicaoSPT = "normal"

    golpes_3: int | None = Field(default=None, ge=0)
    penetracao_3: float | None = Field(default=None, ge=0)
    condicao_3: CondicaoSPT = "normal"

    registro_campo: str | None = None
    observacoes: str | None = None


class RegistroSPTCreate(RegistroSPTBase):
    furo_id: int = Field(gt=0)


class RegistroSPTUpdate(BaseModel):
    profundidade: float | None = Field(default=None, ge=0)

    golpes_1: int | None = Field(default=None, ge=0)
    penetracao_1: float | None = Field(default=None, ge=0)
    condicao_1: CondicaoSPT | None = None

    golpes_2: int | None = Field(default=None, ge=0)
    penetracao_2: float | None = Field(default=None, ge=0)
    condicao_2: CondicaoSPT | None = None

    golpes_3: int | None = Field(default=None, ge=0)
    penetracao_3: float | None = Field(default=None, ge=0)
    condicao_3: CondicaoSPT | None = None

    registro_campo: str | None = None
    observacoes: str | None = None


class RegistroSPTResponse(RegistroSPTBase):
    id: int
    furo_id: int

    model_config = ConfigDict(from_attributes=True)
