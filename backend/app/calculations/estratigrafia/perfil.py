from dataclasses import dataclass


@dataclass
class CamadaPerfil:
    profundidade_inicial: float
    profundidade_final: float
    origem: str
    descricao_material: str
    cor: str | None = None
    complementos: str | None = None


@dataclass
class PerfilEstratigrafico:
    camadas: list[CamadaPerfil]
