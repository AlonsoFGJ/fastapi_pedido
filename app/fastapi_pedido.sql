DROP TABLE pedido;

CREATE TABLE pedido(
    id_pedido NUMBER(8) PRIMARY KEY,
    rut_usuario VARCHAR2(10) NOT NULL,
    descripcion_carrito VARCHAR2(2000) NOT NULL,
    precio_total NUMBER(15) NOT NULL,
    pago_comprobado VARCHAR2(30) NOT NULL
);

INSERT INTO pedido VALUES('1','10033190-k','2x Cemento Polpaico (8,700), 1x Destornillador (4,990), 3x Yeso 5kg (7,770), 5x Yeso 1kg (3,450)',24910,'Pendiente');

COMMIT;


