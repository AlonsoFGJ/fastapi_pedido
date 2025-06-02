from fastapi import APIRouter, HTTPException
from app.database import get_conexion
from pydantic import BaseModel

#vamos a crear la variable para las rutas:
router = APIRouter(
    prefix="/pedido",
    tags=["pedido"]
)

class PedidoModel(BaseModel):    
    rut_usuario: str
    descripcion_carrito: str
    precio_total: int
    pago_comprobado: str

    class Config:
        from_attributes = True

#endpoints: GET, GET, POST, PUT, DELETE, PATCH
@router.get("/")
def obtener_pedidos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT id_pedido,rut_usuario,descripcion_carrito,precio_total,pago_comprobado FROM pedido")
        pedidos = []
        for id_pedido,rut_usuario,descripcion_carrito,precio_total,pago_comprobado in cursor:
            pedidos.append({
                "id_pedido": id_pedido,
                "rut_usuario": rut_usuario,
                "descripcion_carrito": descripcion_carrito,
                "precio_total": precio_total,
                "pago_comprobado": pago_comprobado
            })
        cursor.close()
        cone.close()
        return pedidos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_buscar}")
def obtener_pedido(id_buscar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT id_pedido,rut_usuario,descripcion_carrito,precio_total,pago_comprobado FROM pedido WHERE id_pedido = :id_pedido"
                       ,{"id_pedido": id_buscar})
        pedidoESP = cursor.fetchone()
        cursor.close()
        cone.close()
        if not pedidoESP:
            raise HTTPException(status_code=404, detail="pedido no encontrado")
        return {
            "id_pedido": id_buscar,
            "rut_usuario": pedidoESP[0],
            "descripcion_carrito": pedidoESP[1],
            "precio_total": pedidoESP[2],
            "pago_comprobado": pedidoESP[3]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/")
@router.post("/")
def agregar_pedido(pedido: PedidoModel):
    try:
        cone = get_conexion()
        cursor = cone.cursor()

        # Obtener el último id_pedido
        cursor.execute("SELECT MAX(id_pedido) FROM pedido")
        ultimo_id = cursor.fetchone()[0]
        nuevo_id = 1 if ultimo_id is None else ultimo_id + 1

        # Insertar con el nuevo id
        cursor.execute("""
            INSERT INTO pedido (id_pedido, rut_usuario, descripcion_carrito, precio_total, pago_comprobado)
            VALUES (:id_pedido, :rut_usuario, :descripcion_carrito, :precio_total, :pago_comprobado)
        """, {
            "id_pedido": nuevo_id,
            "rut_usuario": pedido.rut_usuario,
            "descripcion_carrito": pedido.descripcion_carrito,
            "precio_total": pedido.precio_total,
            "pago_comprobado": pedido.pago_comprobado
        })

        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Pedido agregado con éxito", "id_pedido": nuevo_id}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id_actualizar}")
def actualizar_pedido(id_pedido:int, rut_usuario:str, descripcion_carrito:str,precio_total:int, pago_comprobado:str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
                UPDATE pedido
                SET rut_usuario = :rut_usuario,descripcion_carrito = :descripcion_carrito,precio_total = :precio_total,pago_comprobado = :pago_comprobado
                WHERE id_pedido = :id_pedido
        """, {"id_pedido":id_pedido,"rut_usuario":rut_usuario,"descripcion_carrito":descripcion_carrito,"precio_total":precio_total,"pago_comprobado":pago_comprobado})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="pedido no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "pedido actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{id_eliminar}")
def eliminar_pedido(id_eliminar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM pedido WHERE id_pedido = :id_pedido"
                       ,{"id_pedido": id_eliminar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="pedido no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "pedido eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


from typing import Optional

@router.patch("/{id_actualizar}")
def actualizar_parcial(id_actualizar:int, rut_usuario:Optional[str]=None, descripcion_carrito:Optional[str]=None,precio_total:Optional[int]=None, pago_comprobado:Optional[int]=None):
    try:
        if not rut_usuario and not descripcion_carrito and not precio_total and not pago_comprobado:
            raise HTTPException(status_code=400, detail="Debe enviar al menos 1 dato")
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"id_pedido": id_actualizar}
        if rut_usuario:
            campos.append("rut_usuario = :rut_usuario")
            valores["rut_usuario"] = rut_usuario
        if descripcion_carrito:
            campos.append("descripcion_carrito = :descripcion_carrito")
            valores["descripcion_carrito"] = descripcion_carrito
        if precio_total:
            campos.append("precio_total = :precio_total")
            valores["precio_total"] = precio_total
        if pago_comprobado:
            campos.append("pago_comprobado = :pago_comprobado")
            valores["pago_comprobado"] = pago_comprobado

        cursor.execute(f"UPDATE pedido SET {', '.join(campos)} WHERE id_pedido = :id_pedido"
                       ,valores)
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="pedido no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "pedido actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
