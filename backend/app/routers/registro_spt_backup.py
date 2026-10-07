from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.furo import Furo
from app.models.registro_spt import RegistroSPT
from app.schemas.registro_spt import (
    RegistroSPTCreate,
    RegistroSPTResponse,
    RegistroSPTUpdate,
)


router = APIRouter(
    prefix="/spt",
    tags=["Registros SPT"],
)


@router.post(
    "/",
    response_model=RegistroSPTResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_registro_spt(
    dados: RegistroSPTCreate,
    db: Session = Depends(get_db),
):
    furo = db.get(Furo, dados.furo_id)

    if furo is None:
        raise HTTPException(
            status_code=404,
            detail="Furo de sondagem não encontrado.",
        )

    registro = RegistroSPT(**dados.model_dump())

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro


@router.get("/", response_model=list[RegistroSPTResponse])
def listar_registros_spt(db: Session = Depends(get_db)):
    return (
        db.query(RegistroSPT)
        .order_by(RegistroSPT.furo_id, RegistroSPT.profundidade)
        .all()
    )


@router.get("/furo/{furo_id}", response_model=list[RegistroSPTResponse])
def listar_spt_do_furo(
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
        db.query(RegistroSPT)
        .filter(RegistroSPT.furo_id == furo_id)
        .order_by(RegistroSPT.profundidade)
        .all()
    )


@router.get("/{registro_id}", response_model=RegistroSPTResponse)
def buscar_registro_spt(
    registro_id: int,
    db: Session = Depends(get_db),
):
    registro = db.get(RegistroSPT, registro_id)

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Registro SPT não encontrado.",
        )

    return registro


@router.patch("/{registro_id}", response_model=RegistroSPTResponse)
def atualizar_registro_spt(
    registro_id: int,
    dados: RegistroSPTUpdate,
    db: Session = Depends(get_db),
):
    registro = db.get(RegistroSPT, registro_id)

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Registro SPT não encontrado.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    for campo, valor in alteracoes.items():
        setattr(registro, campo, valor)

    db.commit()
    db.refresh(registro)

    return registro


@router.delete(
    "/{registro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_registro_spt(
    registro_id: int,
    db: Session = Depends(get_db),
):
    registro = db.get(RegistroSPT, registro_id)

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Registro SPT não encontrado.",
        )

    db.delete(registro)
    db.commit()

    return None
