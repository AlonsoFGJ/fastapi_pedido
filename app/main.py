from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.pedido import router as pedido_router


app = FastAPI(
    title= "API de gestión de pedido",
    version= "1.0.0",
    description= "API para gestionar pedido"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["*"] si quieres permitir todo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Traeremos los de las rutas (routers)
app.include_router(pedido_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}