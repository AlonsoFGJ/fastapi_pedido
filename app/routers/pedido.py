from fastapi import APIRouter, HTTPException
from app.database import get_conexion
from pydantic import BaseModel
from typing import Optional

# Ruta para el recurso "pedido"
router = APIRouter(
    prefix="/pedido",
    tags=["pedido"]
)

# Modelo de datos
class PedidoModel(BaseModel):
    id_carrito: int
    rut_usuario: str
    pago_comprobado: str

    class Config:
        from_attributes = True

# Obtener todos los pedidos
@router.get("/")
def obtener_pedidos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_pedido, id_carrito, rut_usuario, pago_comprobado 
            FROM pedido
        """)
        pedidos = []
        for id_pedido, id_carrito, rut_usuario, pago_comprobado in cursor:
            pedidos.append({
                "id_pedido": id_pedido,
                "id_carrito": id_carrito,
                "rut_usuario": rut_usuario,
                "pago_comprobado": pago_comprobado
            })
        cursor.close()
        cone.close()
        return pedidos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Obtener un pedido por ID
@router.get("/{id_pedido}")
def obtener_pedido(id_pedido: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_carrito, rut_usuario, pago_comprobado 
            FROM pedido WHERE id_pedido = :id_pedido
        """, {"id_pedido": id_pedido})
        pedido = cursor.fetchone()
        cursor.close()
        cone.close()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return {
            "id_pedido": id_pedido,
            "id_carrito": pedido[0],
            "rut_usuario": pedido[1],
            "pago_comprobado": pedido[2]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/por-rut/{rut_usuario}")
def obtener_pedido_por_rut(rut_usuario: str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_carrito, pago_comprobado 
            FROM pedido 
            WHERE rut_usuario = :rut_usuario
        """, {"rut_usuario": rut_usuario})
        pedidos = cursor.fetchall()
        cursor.close()
        cone.close()
        if not pedidos:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return [
            {
                "rut_usuario": rut_usuario,
                "id_carrito": p[0],
                "pago_comprobado": p[1]
            } for p in pedidos
        ]
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Agregar un nuevo pedido
@router.post("/")
def agregar_pedido(pedido: PedidoModel):
    try:
        cone = get_conexion()
        cursor = cone.cursor()

        # Obtener el nuevo ID
        cursor.execute("SELECT MAX(id_pedido) FROM pedido")
        ultimo_id = cursor.fetchone()[0]
        nuevo_id = 1 if ultimo_id is None else ultimo_id + 1

        # Insertar pedido
        cursor.execute("""
            INSERT INTO pedido (id_pedido, id_carrito, rut_usuario, pago_comprobado)
            VALUES (:id_pedido, :id_carrito, :rut_usuario, :pago_comprobado)
        """, {
            "id_pedido": nuevo_id,
            "id_carrito": pedido.id_carrito,
            "rut_usuario": pedido.rut_usuario,
            "pago_comprobado": pedido.pago_comprobado
        })

        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Pedido agregado con éxito", "id_pedido": nuevo_id}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Actualizar completamente un pedido
@router.put("/{id_pedido}")
def actualizar_pedido(id_pedido: int,  pedido: PedidoModel):
    try:
        cone = get_conexion()
        cursor = cone.cursor()

        # 1. Obtener valores actuales del pedido
        cursor.execute("""
            SELECT id_carrito, rut_usuario, pago_comprobado 
            FROM pedido WHERE id_pedido = :id_pedido
        """, {"id_pedido": id_pedido})
        pedido_actual = cursor.fetchone()

        if not pedido_actual:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        # 2. Usar los valores nuevos o mantener los antiguos
        id_carrito = pedido.id_carrito or pedido_actual[0]
        rut_usuario = pedido.rut_usuario or pedido_actual[1]
        pago_comprobado = pedido.pago_comprobado or pedido_actual[2]

        # 3. Actualizar con los valores definitivos
        cursor.execute("""
            UPDATE pedido 
            SET id_carrito = :id_carrito,
                rut_usuario = :rut_usuario,
                pago_comprobado = :pago_comprobado
            WHERE id_pedido = :id_pedido
        """, {
            "id_pedido": id_pedido,
            "id_carrito": id_carrito,
            "rut_usuario": rut_usuario,
            "pago_comprobado": pago_comprobado
        })

        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Pedido actualizado con éxito"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Eliminar un pedido
@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM pedido WHERE id_pedido = :id_pedido", {"id_pedido": id_pedido})
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Pedido eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Actualización parcial de un pedido
@router.patch("/{id_pedido}")
def actualizar_parcial(
    id_pedido: int,
    id_carrito: Optional[int] = None,
    rut_usuario: Optional[str] = None,
    pago_comprobado: Optional[str] = None
):
    try:
        if not any([id_carrito, rut_usuario, pago_comprobado]):
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un campo para actualizar")

        campos = []
        valores = {"id_pedido": id_pedido}
        if id_carrito is not None:
            campos.append("id_carrito = :id_carrito")
            valores["id_carrito"] = id_carrito
        if rut_usuario is not None:
            campos.append("rut_usuario = :rut_usuario")
            valores["rut_usuario"] = rut_usuario
        if pago_comprobado is not None:
            campos.append("pago_comprobado = :pago_comprobado")
            valores["pago_comprobado"] = pago_comprobado

        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute(f"""
            UPDATE pedido SET {', '.join(campos)} 
            WHERE id_pedido = :id_pedido
        """, valores)

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Pedido actualizado parcialmente con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

