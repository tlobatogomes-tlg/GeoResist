from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjetoBase(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    cliente: str | None = None
    municipio: str | None = None
    estado: str | None = Field(default=None, min_length=2, max_length=2)
    endereco: str | None = None
    descricao: str | None = None


class ProjetoCreate(ProjetoBase):
    pass


class ProjetoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=150)
    cliente: str | None = None
    municipio: str | None = None
    estado: str | None = Field(default=None, min_length=2, max_length=2)
    endereco: str | None = None
    descricao: str | None = None


class ProjetoResponse(ProjetoBase):
    id: int
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)
