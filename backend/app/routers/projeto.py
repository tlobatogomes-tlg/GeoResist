from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.projeto import Projeto
from app.schemas.projeto import ProjetoCreate, ProjetoResponse, ProjetoUpdate


router = APIRouter(
    prefix="/projetos",
    tags=["Projetos"],
)


@router.post(
    "/",
    response_model=ProjetoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_projeto(dados: ProjetoCreate, db: Session = Depends(get_db)):
    projeto = Projeto(**dados.model_dump())

    db.add(projeto)
    db.commit()
    db.refresh(projeto)

    return projeto


@router.get("/", response_model=list[ProjetoResponse])
def listar_projetos(db: Session = Depends(get_db)):
    return db.query(Projeto).order_by(Projeto.id.desc()).all()


@router.get("/{projeto_id}", response_model=ProjetoResponse)
def buscar_projeto(projeto_id: int, db: Session = Depends(get_db)):
    projeto = db.get(Projeto, projeto_id)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado.",
        )

    return projeto


@router.patch("/{projeto_id}", response_model=ProjetoResponse)
def atualizar_projeto(
    projeto_id: int,
    dados: ProjetoUpdate,
    db: Session = Depends(get_db),
):
    projeto = db.get(Projeto, projeto_id)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado.",
        )

    alteracoes = dados.model_dump(exclude_unset=True)

    for campo, valor in alteracoes.items():
        setattr(projeto, campo, valor)

    db.commit()
    db.refresh(projeto)

    return projeto


@router.delete("/{projeto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_projeto(projeto_id: int, db: Session = Depends(get_db)):
    projeto = db.get(Projeto, projeto_id)

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado.",
        )

    db.delete(projeto)
    db.commit()

    return None
