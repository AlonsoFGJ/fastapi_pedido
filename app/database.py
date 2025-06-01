import cx_Oracle
import oracledb


def get_conexion():
    try:
        conexion = oracledb.connect(
            user="fastapi_pedido",
            password="fastapi_pedido",
            dsn="localhost:1521/xe"  # Ajusta si usas otro SID o IP
        )
        print("¡Conexión exitosa!")
        return conexion
    except Exception as e:
        print(f"Error de conexión: {e}")
        raise

# Probar la conexión y consultar datos
try:
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedido")
    for row in cursor:
        print(row)
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error al consultar: {e}")