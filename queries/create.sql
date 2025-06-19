CREATE TABLE IF NOT EXISTS esporte {
    id_esporte INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id_esporte)
};

CREATE TABLE IF NOT EXISTS campeonatos {
    id_campeonato INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL UNIQUE,
    url_logo VARCHAR(255) NULL,
    id_esporte INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    PRIMARY KEY (id_campeonato),
    FOREIGN KEY (id_esporte) REFERENCES esporte(id_esporte)
};

CREATE TABLE IF NOT EXISTS times {
    id_time INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    url_logo VARCHAR(255) NULL,
    PRIMARY KEY (id_time)
};

CREATE TABLE IF NOT EXISTS inscricoes {
    id_inscricao INT NOT NULL AUTO_INCREMENT,
    id_campeonato INT NOT NULL,
    id_time INT NOT NULL,
    PRIMARY KEY (id_inscricao),
    FOREIGN KEY (id_campeonato) REFERENCES campeonatos(id_campeonato),
    FOREIGN KEY (id_time) REFERENCES times(id_time)
};

CREATE TABLE IF NOT EXISTS partidas {
    id_partida INT NOT NULL AUTO_INCREMENT,
    id_campeonato INT NOT NULL,
    rodada INT NOT NULL,
    id_time_a INT NULL,
    id_time_b INT NULL,
    placar_time_a INT NULL,
    placar_time_b INT NULL,
    data_hora DATETIME NULL,
    PRIMARY KEY (id_partida),
    FOREIGN KEY (id_campeonato) REFERENCES campeonatos(id_campeonato),
    FOREIGN KEY (id_time_a) REFERENCES times(id_time),
    FOREIGN KEY (id_time_b) REFERENCES times(id_time)
};