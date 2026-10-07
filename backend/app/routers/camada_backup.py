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
            detail="Furo de sondagem não encontrado.",
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
            detail="Furo de sondagem não encontrado.",
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
            detail="Camada não encontrada.",
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
            detail="Camada não encontrada.",
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
            detail="Camada não encontrada.",
        )

    db.delete(camada)
    db.commit()

    return None
