from pydantic import BaseModel, ConfigDict, Field, model_validator


def validar_intervalo_profundidade(
    profundidade_inicial: float,
    profundidade_final: float,
) -> None:
    if profundidade_final <= profundidade_inicial:
        raise ValueError(
            "A profundidade final deve ser maior que a profundidade inicial."
        )


class CamadaBase(BaseModel):
    profundidade_inicial: float = Field(ge=0, allow_inf_nan=False)
    profundidade_final: float = Field(gt=0, allow_inf_nan=False)

    origem: str | None = None
    descricao_material: str = Field(min_length=2, max_length=250)
    cor: str | None = None
    complementos: str | None = None
    observacoes: str | None = None

    @model_validator(mode="after")
    def validar_intervalo(self):
        validar_intervalo_profundidade(
            self.profundidade_inicial,
            self.profundidade_final,
        )
        return self


class CamadaCreate(CamadaBase):
    furo_id: int = Field(gt=0)


class CamadaUpdate(BaseModel):
    profundidade_inicial: float | None = Field(
        default=None,
        ge=0,
        allow_inf_nan=False,
    )
    profundidade_final: float | None = Field(
        default=None,
        gt=0,
        allow_inf_nan=False,
    )

    origem: str | None = None
    descricao_material: str | None = Field(
        default=None,
        min_length=2,
        max_length=250,
    )
    cor: str | None = None
    complementos: str | None = None
    observacoes: str | None = None

    @model_validator(mode="after")
    def validar_intervalo_quando_completo(self):
        if (
            "profundidade_inicial" in self.model_fields_set
            and self.profundidade_inicial is None
        ) or (
            "profundidade_final" in self.model_fields_set
            and self.profundidade_final is None
        ):
            raise ValueError("As profundidades da camada não podem ser nulas.")

        if (
            self.profundidade_inicial is not None
            and self.profundidade_final is not None
        ):
            validar_intervalo_profundidade(
                self.profundidade_inicial,
                self.profundidade_final,
            )
        return self


class CamadaResponse(CamadaBase):
    id: int
    furo_id: int

    model_config = ConfigDict(from_attributes=True)
