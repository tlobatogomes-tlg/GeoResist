from app.calculations.estratigrafia.motor import (
    CamadaIntervalo,
    calcular_espessura,
    existe_sobreposicao,
    verificar_lacunas,
    perfil_continuo,
)


def test_espessura_145():
    assert calcular_espessura(0.00, 1.45) == 1.45


def test_espessura_100():
    assert calcular_espessura(0.45, 1.45) == 1.00


def test_sem_sobreposicao():
    camadas = [
        CamadaIntervalo(0.45, 1.45),
    ]

    assert (
        existe_sobreposicao(
            1.45,
            2.45,
            camadas,
        )
        is False
    )


def test_com_sobreposicao():
    camadas = [
        CamadaIntervalo(0.45, 1.45),
    ]

    assert (
        existe_sobreposicao(
            1.20,
            1.80,
            camadas,
        )
        is True
    )


def test_perfil_continuo():
    camadas = [
        CamadaIntervalo(0.00, 0.45),
        CamadaIntervalo(0.45, 1.45),
        CamadaIntervalo(1.45, 2.45),
    ]

    assert perfil_continuo(camadas) is True


def test_perfil_com_lacuna():
    camadas = [
        CamadaIntervalo(0.00, 0.45),
        CamadaIntervalo(0.60, 1.45),
    ]

    assert perfil_continuo(camadas) is False


def test_detecta_lacuna():
    camadas = [
        CamadaIntervalo(0.00, 0.45),
        CamadaIntervalo(0.60, 1.45),
    ]

    assert verificar_lacunas(camadas) == [
        (0.45, 0.60),
    ]


def test_varias_camadas_continuas():
    camadas = [
        CamadaIntervalo(0.00, 0.45),
        CamadaIntervalo(0.45, 1.45),
        CamadaIntervalo(1.45, 2.45),
        CamadaIntervalo(2.45, 3.45),
    ]

    assert perfil_continuo(camadas) is True