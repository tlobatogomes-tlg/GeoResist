from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.furo import Furo
from app.models.camada import Camada
from app.schemas.camada import (
    CamadaCreate,
    CamadaResponse,
    CamadaUpdate,
)


router = APIRouter(
    prefix="/camadas",
    tags=["Camadas / Estratigrafia"],
)


def verificar_sobreposicao(
    db: Session,
    furo_id: int,
    profundidade_inicial: float,
    profundidade_final: float,
    ignorar_camada_id: int | None = None,
):
    consulta = (
        db.query(Camada)
        .filter(Camada.furo_id == furo_id)
        .filter(Camada.profundidade_inicial < profundidade_final)
        .filter(Camada.profundidade_final > profundidade_inicial)
    )

    if ignorar_camada_id is not None:
        consulta = consulta.filter(Camada.id != ignorar_camada_id)

    sobreposta = consulta.first()

    if sobreposta is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "O intervalo informado sobrepoe uma camada existente: "
                f"{sobreposta.profundidade_inicial:.2f} m a "
                f"{sobreposta.profundidade_final:.2f} m."
            ),
        )


@router.post(
    "/",
    response_model=CamadaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_camada(
    dados: CamadaCreate,
    db: Session = Depends(get_db),
):
    furo = db.get(Furo, dados.furo_id)

    if furo is None:
        raise HTTPException(
            status_code=404,
            detail="Furo de sondagem nao encontrado.",
        )

    verificar_sobreposicao(
        db=db,
        furo_id=dados.furo_id,
        profundidade_inicial=dados.profundidade_inicial,
        profundidade_final=dados.profundidade_final,
    )

    camada = Camada(**dados.model_dump())

    db.add(camada)
    db.commit()
    db.refresh(camada)

    return camada


@router.get("/", response_model=list[CamadaResponse])
def listar_camadas(db: Session = Depends(get_db)):
    return (
        db.query(Camada)
        .order_by(Camada.furo_id, Camada.profundidade_inicial)
        .all()
    )


@router.get(
    "/furo/{furo_id}",
    response_model=list[CamadaResponse],
)
def listar_camadas_do_furo(
    furo_id: int,
    db: Session = Depends(get_db),
):
    furo = db.get(Furo, furo_id)

    if furo is None:
        raise HTTPException(
            status_code=404,
            detail="Furo de sondagem nao encontrado.",
        )

    return (
        db.query(Camada)
        .filter(Camada.furo_id == furo_id)
        .order_by(Camada.profundidade_inicial)
        .all()
    )


@router.get(
    "/{camada_id}",
    response_model=CamadaResponse,
)
def buscar_camada(
    camada_id: int,
    db: Session = Depends(get_db),
):
    camada = db.get(Camada, camada_id)

    if camada is None:
        raise HTTPException(
            status_code=404,
            detail="Camada nao encontrada.",
        )

    return camada


@router.patch(
    "/{camada_id}",
    response_model=CamadaResponse,
)
def atualizar_camada(
    camada_id: int,
    dados: CamadaUpdate,
    db: Session = Depends(get_db),
):
    camada = db.get(Camada, camada_id)

    if camada is None:
        raise HTTPException(
            status_code=404,
            detail="Camada nao encontrada.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    nova_inicial = alteracoes.get(
        "profundidade_inicial",
        camada.profundidade_inicial,
    )

    nova_final = alteracoes.get(
        "profundidade_final",
        camada.profundidade_final,
    )

    if nova_final <= nova_inicial:
        raise HTTPException(
            status_code=422,
            detail="A profundidade final deve ser maior que a profundidade inicial.",
        )

    verificar_sobreposicao(
        db=db,
        furo_id=camada.furo_id,
        profundidade_inicial=nova_inicial,
        profundidade_final=nova_final,
        ignorar_camada_id=camada.id,
    )

    for campo, valor in alteracoes.items():
        setattr(camada, campo, valor)

    db.commit()
    db.refresh(camada)

    return camada


@router.delete(
    "/{camada_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_camada(
    camada_id: int,
    db: Session = Depends(get_db),
):
    camada = db.get(Camada, camada_id)

    if camada is None:
        raise HTTPException(
            status_code=404,
            detail="Camada nao encontrada.",
        )

    db.delete(camada)
    db.commit()

    return None
