from dataclasses import dataclass


@dataclass
class CamadaIntervalo:
    profundidade_inicial: float
    profundidade_final: float


def calcular_espessura(
    profundidade_inicial: float,
    profundidade_final: float,
) -> float:
    return round(
        profundidade_final - profundidade_inicial,
        2,
    )


def existe_sobreposicao(
    profundidade_inicial: float,
    profundidade_final: float,
    camadas: list[CamadaIntervalo],
) -> bool:

    for camada in camadas:

        if (
            profundidade_inicial < camada.profundidade_final
            and profundidade_final > camada.profundidade_inicial
        ):
            return True

    return False


def verificar_lacunas(
    camadas: list[CamadaIntervalo],
):

    camadas = sorted(
        camadas,
        key=lambda c: c.profundidade_inicial,
    )

    lacunas = []

    for atual, proxima in zip(
        camadas,
        camadas[1:],
    ):

        if (
            proxima.profundidade_inicial
            > atual.profundidade_final
        ):

            lacunas.append(
                (
                    atual.profundidade_final,
                    proxima.profundidade_inicial,
                )
            )

    return lacunas


def perfil_continuo(
    camadas: list[CamadaIntervalo],
) -> bool:

    return len(verificar_lacunas(camadas)) == 0