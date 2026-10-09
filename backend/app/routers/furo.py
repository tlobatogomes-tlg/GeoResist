from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.camada import Camada
from app.models.furo import Furo
from app.models.projeto import Projeto
from app.schemas.furo import FuroCreate, FuroResponse, FuroUpdate


router = APIRouter(
    prefix="/furos",
    tags=["Furos de Sondagem"],
)


@router.post(
    "/",
    response_model=FuroResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_furo(dados: FuroCreate, db: Session = Depends(get_db)):
    projeto = db.get(Projeto, dados.projeto_id)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado.",
        )

    furo = Furo(**dados.model_dump())

    db.add(furo)
    db.commit()
    db.refresh(furo)

    return furo


@router.get("/", response_model=list[FuroResponse])
def listar_furos(db: Session = Depends(get_db)):
    return db.query(Furo).order_by(Furo.id).all()


@router.get("/{furo_id}", response_model=FuroResponse)
def buscar_furo(furo_id: int, db: Session = Depends(get_db)):
    furo = db.get(Furo, furo_id)

    if furo is None:
        raise HTTPException(
            status_code=404,
            detail="Furo de sondagem não encontrado.",
        )

    return furo


@router.patch("/{furo_id}", response_model=FuroResponse)
def atualizar_furo(
    furo_id: int,
    dados: FuroUpdate,
    db: Session = Depends(get_db),
):
    furo = db.get(Furo, furo_id)

    if furo is None:
        raise HTTPException(
            status_code=404,
            detail="Furo de sondagem não encontrado.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    nova_profundidade_final = alteracoes.get(
        "profundidade_final",
        furo.profundidade_final,
    )

    if (
        "profundidade_final" in alteracoes
        and nova_profundidade_final is not None
    ):
        maior_profundidade_camada = (
            db.query(Camada.profundidade_final)
            .filter(Camada.furo_id == furo.id)
            .order_by(Camada.profundidade_final.desc())
            .first()
        )

        if (
            maior_profundidade_camada is not None
            and nova_profundidade_final < maior_profundidade_camada[0]
        ):
            raise HTTPException(
                status_code=422,
                detail=(
                    "A profundidade final do furo não pode ser menor que "
                    "a profundidade final de uma camada cadastrada."
                ),
            )

    for campo, valor in alteracoes.items():
        setattr(furo, campo, valor)

    db.commit()
    db.refresh(furo)

    return furo


@router.delete("/{furo_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_furo(furo_id: int, db: Session = Depends(get_db)):
    furo = db.get(Furo, furo_id)

    if furo is None:
        raise HTTPException(
            status_code=404,
            detail="Furo de sondagem não encontrado.",
        )

    db.delete(furo)
    db.commit()

    return None
