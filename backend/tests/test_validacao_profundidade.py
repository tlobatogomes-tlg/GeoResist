import math

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models.camada import Camada
from app.models.furo import Furo
from app.models.projeto import Projeto
from app.models.registro_spt import RegistroSPT  # noqa: F401
from app.routers.camada import atualizar_camada, criar_camada
from app.routers.furo import atualizar_furo
from app.schemas.camada import CamadaCreate, CamadaUpdate
from app.schemas.furo import FuroUpdate


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def criar_furo_teste(
    db: Session,
    profundidade_final: float | None,
) -> Furo:
    projeto = Projeto(nome="Projeto de teste")
    db.add(projeto)
    db.flush()

    furo = Furo(
        projeto_id=projeto.id,
        identificacao="F-01",
        sistema="manual",
        profundidade_final=profundidade_final,
    )
    db.add(furo)
    db.commit()
    db.refresh(furo)
    return furo


def dados_camada(
    furo_id: int,
    profundidade_inicial: float,
    profundidade_final: float,
) -> CamadaCreate:
    return CamadaCreate(
        furo_id=furo_id,
        profundidade_inicial=profundidade_inicial,
        profundidade_final=profundidade_final,
        descricao_material="Argila arenosa",
        origem="ATERRO",
    )


@pytest.mark.parametrize("campo", ["profundidade_inicial", "profundidade_final"])
@pytest.mark.parametrize("valor", [math.nan, math.inf, -math.inf])
def test_camada_create_rejeita_profundidade_nao_finita(campo, valor):
    dados = {
        "furo_id": 1,
        "profundidade_inicial": 0.0,
        "profundidade_final": 1.0,
        "descricao_material": "Argila arenosa",
    }
    dados[campo] = valor

    with pytest.raises(ValidationError):
        CamadaCreate.model_validate(dados)


@pytest.mark.parametrize("campo", ["profundidade_inicial", "profundidade_final"])
@pytest.mark.parametrize("valor", [math.nan, math.inf, -math.inf])
def test_camada_update_rejeita_profundidade_nao_finita(campo, valor):
    with pytest.raises(ValidationError):
        CamadaUpdate.model_validate({campo: valor})


@pytest.mark.parametrize(
    ("inicial", "final"),
    [(-0.01, 1.0), (0.0, 0.0), (1.0, 0.5), (1.0, 1.0)],
)
def test_camada_create_rejeita_intervalo_invalido(inicial, final):
    with pytest.raises(ValidationError):
        CamadaCreate(
            furo_id=1,
            profundidade_inicial=inicial,
            profundidade_final=final,
            descricao_material="Argila arenosa",
        )


def test_camada_aceita_inicio_zero_e_intervalo_positivo():
    camada = CamadaCreate(
        furo_id=1,
        profundidade_inicial=0.0,
        profundidade_final=0.01,
        descricao_material="Argila arenosa",
    )

    assert camada.profundidade_inicial == 0.0
    assert camada.profundidade_final == 0.01


def test_criacao_de_camada_respeita_limite_do_furo(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=2.0)

    camada = criar_camada(dados_camada(furo.id, 1.0, 2.0), db_session)

    assert camada.profundidade_final == 2.0


def test_criacao_de_camada_nao_ultrapassa_limite_do_furo(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=2.0)

    with pytest.raises(HTTPException) as erro:
        criar_camada(dados_camada(furo.id, 1.0, 2.01), db_session)

    assert erro.value.status_code == 422
    assert db_session.query(Camada).count() == 0


def test_atualizacao_de_camada_nao_ultrapassa_limite_do_furo(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=2.0)
    camada = criar_camada(dados_camada(furo.id, 0.0, 1.0), db_session)

    with pytest.raises(HTTPException) as erro:
        atualizar_camada(
            camada.id,
            CamadaUpdate(profundidade_final=2.01),
            db_session,
        )

    assert erro.value.status_code == 422
    assert db_session.get(Camada, camada.id).profundidade_final == 1.0


def test_atualizacao_de_camada_valida_intervalo_com_valor_existente(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=5.0)
    camada = criar_camada(dados_camada(furo.id, 0.0, 1.0), db_session)

    with pytest.raises(HTTPException) as erro:
        atualizar_camada(
            camada.id,
            CamadaUpdate(profundidade_inicial=1.0),
            db_session,
        )

    assert erro.value.status_code == 422


def test_atualizacao_de_camada_orfa_retorna_furo_nao_encontrado(db_session):
    camada = Camada(
        furo_id=999,
        profundidade_inicial=0.0,
        profundidade_final=1.0,
        descricao_material="Argila arenosa",
    )
    db_session.add(camada)
    db_session.commit()
    db_session.refresh(camada)

    with pytest.raises(HTTPException) as erro:
        atualizar_camada(
            camada.id,
            CamadaUpdate(descricao_material="Areia fina"),
            db_session,
        )

    assert erro.value.status_code == 404
    assert erro.value.detail == "Furo de sondagem não encontrado."


def test_atualizacao_de_furo_nao_fica_abaixo_de_camada_existente(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=5.0)
    criar_camada(dados_camada(furo.id, 0.0, 2.0), db_session)

    with pytest.raises(HTTPException) as erro:
        atualizar_furo(
            furo.id,
            FuroUpdate(profundidade_final=1.99),
            db_session,
        )

    assert erro.value.status_code == 422
    assert db_session.get(Furo, furo.id).profundidade_final == 5.0


def test_profundidade_final_do_furo_pode_igualar_final_da_camada(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=5.0)
    criar_camada(dados_camada(furo.id, 0.0, 2.0), db_session)

    furo_atualizado = atualizar_furo(
        furo.id,
        FuroUpdate(profundidade_final=2.0),
        db_session,
    )

    assert furo_atualizado.profundidade_final == 2.0


def test_furo_sem_profundidade_final_nao_limita_camada(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=None)

    camada = criar_camada(dados_camada(furo.id, 0.0, 1000.0), db_session)

    assert camada.profundidade_final == 1000.0


def test_furo_sem_limite_pode_receber_limite_acima_das_camadas(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=None)
    criar_camada(dados_camada(furo.id, 0.0, 1000.0), db_session)

    furo_atualizado = atualizar_furo(
        furo.id,
        FuroUpdate(profundidade_final=1000.0),
        db_session,
    )

    assert furo_atualizado.profundidade_final == 1000.0


def test_atualizacao_de_profundidade_de_furo_sem_camadas(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=None)

    furo_atualizado = atualizar_furo(
        furo.id,
        FuroUpdate(profundidade_final=3.0),
        db_session,
    )

    assert furo_atualizado.profundidade_final == 3.0
    assert db_session.query(Camada).filter(Camada.furo_id == furo.id).count() == 0


def test_atualizacao_de_furo_pode_limpar_limite(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=2.0)
    criar_camada(dados_camada(furo.id, 0.0, 2.0), db_session)

    furo_atualizado = atualizar_furo(
        furo.id,
        FuroUpdate(profundidade_final=None),
        db_session,
    )

    assert furo_atualizado.profundidade_final is None


def test_rota_de_camada_rejeita_sobreposicao(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=5.0)
    criar_camada(dados_camada(furo.id, 0.0, 1.0), db_session)

    with pytest.raises(HTTPException) as erro:
        criar_camada(dados_camada(furo.id, 0.5, 1.5), db_session)

    assert erro.value.status_code == 409
    assert db_session.query(Camada).filter(Camada.furo_id == furo.id).count() == 1


def test_rota_de_camada_permite_adjacencia(db_session):
    furo = criar_furo_teste(db_session, profundidade_final=5.0)
    criar_camada(dados_camada(furo.id, 0.0, 1.0), db_session)

    camada_adjacente = criar_camada(
        dados_camada(furo.id, 1.0, 2.0),
        db_session,
    )

    assert camada_adjacente.profundidade_inicial == 1.0
    assert db_session.query(Camada).filter(Camada.furo_id == furo.id).count() == 2


@pytest.mark.parametrize("valor", [math.nan, math.inf, -math.inf])
def test_furo_rejeita_profundidade_final_nao_finita(valor):
    with pytest.raises(ValidationError):
        FuroUpdate(profundidade_final=valor)
