from fastapi import FastAPI

from app.database import Base, engine
from app.models.projeto import Projeto
from app.models.furo import Furo
from app.models.registro_spt import RegistroSPT
from app.routers.projeto import router as projeto_router
from app.routers.furo import router as furo_router
from app.routers.registro_spt import router as registro_spt_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GeoResist API",
    description="Tecnologia em Obras de Terra",
    version="0.1.0",
)


app.include_router(projeto_router)
app.include_router(furo_router)
app.include_router(registro_spt_router)


@app.get("/")
def inicio():
    return {
        "sistema": "GeoResist",
        "descricao": "Tecnologia em Obras de Terra",
        "versao": "0.1.0",
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
