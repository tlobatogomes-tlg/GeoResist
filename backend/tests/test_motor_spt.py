from app.calculations.spt.motor import calcular_n_spt


def test_spt_normal():
    r = calcular_n_spt(
        "manual",
        2, 15, "normal",
        3, 15, "normal",
        4, 15, "normal",
    )
    assert r.calculavel is True
    assert r.n_spt == 7
    assert r.status == "calculado"


def test_spt_penetracoes_irregulares():
    r = calcular_n_spt(
        "manual",
        3, 17, "normal",
        4, 14, "normal",
        5, 15, "normal",
    )
    assert r.calculavel is True
    assert r.n_spt == 9


def test_ph_50():
    r = calcular_n_spt(
        "manual",
        None, 50, "peso_haste",
        None, None, "nao_executado",
        None, None, "nao_executado",
    )
    assert r.calculavel is False
    assert r.n_spt is None
    assert r.status == "penetracao_estatica"


def test_pm_70():
    r = calcular_n_spt(
        "manual",
        None, 70, "peso_martelo",
        None, None, "nao_executado",
        None, None, "nao_executado",
    )
    assert r.calculavel is False
    assert r.n_spt is None
    assert r.status == "penetracao_estatica"


def test_5_0_sem_avanco():
    r = calcular_n_spt(
        "manual",
        5, 0, "sem_avanco",
        None, None, "nao_executado",
        None, None, "nao_executado",
    )
    assert r.calculavel is False
    assert r.status == "sem_avanco"


def test_manual_31_golpes_interrompe():
    r = calcular_n_spt(
        "manual",
        5, 15, "normal",
        31, 10, "normal",
        None, None, "normal",
    )
    assert r.calculavel is False
    assert r.status == "cravacao_interrompida"


def test_manual_30_golpes_nao_ultrapassa():
    r = calcular_n_spt(
        "manual",
        5, 15, "normal",
        30, 10, "normal",
        None, None, "normal",
    )
    assert r.status != "cravacao_interrompida"


def test_mecanizado_35_golpes_nao_ultrapassa():
    r = calcular_n_spt(
        "mecanizado",
        5, 15, "normal",
        35, 10, "normal",
        None, None, "normal",
    )
    assert r.status != "cravacao_interrompida"


def test_1_58():
    r = calcular_n_spt(
        "manual",
        1, 58, "normal",
        None, None, "normal",
        None, None, "normal",
    )
    assert r.calculavel is False
    assert r.n_spt is None
    assert r.status == "penetracao_excepcional"


def test_1_33_1_20():
    r = calcular_n_spt(
        "manual",
        1, 33, "normal",
        1, 20, "normal",
        None, None, "normal",
    )
    assert r.calculavel is False
    assert r.n_spt is None
    assert r.status == "penetracao_excepcional"
