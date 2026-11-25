CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL,
    logradouro VARCHAR(80) NOT NULL,
    numero INTEGER NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    cep VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente_telefone (
    id_telefone SERIAL PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    id_cliente INTEGER REFERENCES cliente (id_cliente)
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido SERIAL PRIMARY KEY,
    data_feita DATE NOT NULL,
    data_prevista DATE NOT NULL,
    data_entregue DATE
);

CREATE TABLE IF NOT EXISTS tipo_doce (
    id_tipo SERIAL PRIMARY KEY,
    sabor VARCHAR(30) NOT NULL,
    tipo VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS doce (
    id_doce SERIAL PRIMARY KEY,
    preco NUMERIC(10, 2) NOT NULL,
    id_tipo INTEGER REFERENCES tipo_doce (id_tipo)
);

CREATE TABLE IF NOT EXISTS item_pedido (
    id_pedido INTEGER REFERENCES pedido (id_pedido),
    id_doce INTEGER REFERENCES doce (id_doce),
    id_cliente INTEGER REFERENCES cliente (id_cliente),
    total_pago NUMERIC(10, 2) NOT NULL,
    troco NUMERIC(10, 2),
    PRIMARY KEY (id_pedido, id_doce, id_cliente)
);

CREATE TABLE IF NOT EXISTS solicitacao (
    id_cliente INTEGER REFERENCES cliente (id_cliente),
    id_pedido INTEGER REFERENCES pedido (id_pedido),
    PRIMARY KEY (id_cliente, id_pedido)
);