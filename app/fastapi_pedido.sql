DROP TABLE pedido;

CREATE TABLE pedido(
    id_pedido NUMBER(8) PRIMARY KEY,
    id_carrito NUMBER(8) NOT NULL,
    rut_usuario VARCHAR2(10) NOT NULL,
    pago_comprobado VARCHAR2(30) NOT NULL
);

COMMIT;

