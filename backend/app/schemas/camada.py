from pydantic import BaseModel, ConfigDict, Field, model_validator


class CamadaBase(BaseModel):
    profundidade_inicial: float = Field(ge=0)
    profundidade_final: float = Field(gt=0)

    origem: str | None = None
    descricao_material: str = Field(min_length=2, max_length=250)
    cor: str | None = None
    complementos: str | None = None
    observacoes: str | None = None

    @model_validator(mode="after")
    def validar_intervalo(self):
        if self.profundidade_final <= self.profundidade_inicial:
            raise ValueError(
                "A profundidade final deve ser maior que a profundidade inicial."
            )
        return self


class CamadaCreate(CamadaBase):
    furo_id: int = Field(gt=0)


class CamadaUpdate(BaseModel):
    profundidade_inicial: float | None = Field(default=None, ge=0)
    profundidade_final: float | None = Field(default=None, gt=0)

    origem: str | None = None
    descricao_material: str | None = Field(
        default=None,
        min_length=2,
        max_length=250,
    )
    cor: str | None = None
    complementos: str | None = None
    observacoes: str | None = None


class CamadaResponse(CamadaBase):
    id: int
    furo_id: int

    model_config = ConfigDict(from_attributes=True)
