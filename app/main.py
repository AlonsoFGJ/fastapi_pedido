from fastapi import FastAPI
from app.routers.pedido import router as pedido_router


app = FastAPI(
    title= "API de gestión de pedido",
    version= "1.0.0",
    description= "API para gestionar pedido"
)

#Traeremos los de las rutas (routers)
app.include_router(pedido_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}