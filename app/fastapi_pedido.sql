DROP TABLE pedido;

CREATE TABLE pedido(
    id_pedido NUMBER(8) PRIMARY KEY,
    descripcion_pedido varchar2(2000) NOT NULL,
    rut_usuario VARCHAR2(10) NOT NULL,
    pago_comprobado VARCHAR2(30) NOT NULL
);


COMMIT;