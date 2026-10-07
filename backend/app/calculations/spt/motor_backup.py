from dataclasses import dataclass


@dataclass
class ResultadoSPT:
    n_spt: int | None
    calculavel: bool
    status: str
    mensagem: str


def calcular_n_spt(
    sistema: str,
    golpes_1: int | None,
    penetracao_1: float | None,
    condicao_1: str,
    golpes_2: int | None,
    penetracao_2: float | None,
    condicao_2: str,
    golpes_3: int | None,
    penetracao_3: float | None,
    condicao_3: str,
) -> ResultadoSPT:

    if sistema not in ("manual", "mecanizado"):
        return ResultadoSPT(
            None,
            False,
            "sistema_invalido",
            "Sistema deve ser manual ou mecanizado.",
        )

    condicoes = [condicao_1, condicao_2, condicao_3]

    if any(c in ("peso_haste", "peso_martelo") for c in condicoes):
        return ResultadoSPT(
            None,
            False,
            "penetracao_estatica",
            "Registro PH/PM: apresentar a relação de penetração sem calcular N automaticamente.",
        )

    if "sem_avanco" in condicoes:
        return ResultadoSPT(
            None,
            False,
            "sem_avanco",
            "Cravação sem avanço: apresentar golpes/penetração.",
        )

    if "nao_executado" in condicoes:
        return ResultadoSPT(
            None,
            False,
            "nao_executado",
            "Ensaio ou trecho identificado como não executado.",
        )

    golpes = [golpes_1, golpes_2, golpes_3]
    penetracoes = [penetracao_1, penetracao_2, penetracao_3]

    limite_golpes = 30 if sistema == "manual" else 40

    # Verifica primeiro os trechos que realmente foram executados.
    # Um trecho posterior pode estar vazio porque a cravação
    # já foi interrompida anteriormente.
    for golpe, penetracao in zip(golpes, penetracoes):
        if golpe is None and penetracao is None:
            continue

        if golpe is None or penetracao is None:
            return ResultadoSPT(
                None,
                False,
                "incompleto",
                "Trecho possui golpes ou penetração sem o respectivo valor.",
            )

        if golpe > limite_golpes:
            return ResultadoSPT(
                None,
                False,
                "cravacao_interrompida",
                (
                    f"Cravação interrompida: trecho ultrapassou "
                    f"{limite_golpes} golpes no sistema {sistema}."
                ),
            )

    # Para calcular N automaticamente precisamos dos três
    # registros de cravação.
    if any(g is None for g in golpes) or any(p is None for p in penetracoes):
        return ResultadoSPT(
            None,
            False,
            "cravacao_incompleta",
            "Cravação encerrada antes do registro completo dos três trechos.",
        )

    penetracao_total = sum(penetracoes)

    if penetracao_total < 45:
        return ResultadoSPT(
            None,
            False,
            "penetracao_inferior_45",
            "Cravação inferior a 45 cm: manter a relação golpes/penetração.",
        )

    n_spt = golpes_2 + golpes_3

    return ResultadoSPT(
        n_spt,
        True,
        "calculado",
        "N calculado pela soma dos golpes da segunda e terceira etapas.",
    )
