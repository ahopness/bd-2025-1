from flask import Flask
from app import app

import pymysql
from config import *

@app.cli.command('setup-db')
def setup_db():
    try:
        DB_CONFIG_COPY = DB_CONFIG.copy()
        db_name = DB_CONFIG_COPY.pop('database', 'gestor_campeonatos')

        connection = pymysql.connect(**DB_CONFIG_COPY)
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        connection.close()

        print(f"Database '{db_name}' criada.")
    except Exception as e:
        return print(f'Erro ao conectar com o servidor MySQL ou criar o banco de dados: {e}')

    try:
        connection = pymysql.connect(**DB_CONFIG)
    except Exception as e:
        return print(f'Erro ao conectar com o banco de dados: {e}')
    
    try:
        with connection.cursor() as cursor:
            for query in query_create.split(';'):
                if query.strip(): cursor.execute(query)
            
            connection.commit()
            return print("Banco de dados inicializado com sucesso e populado com dados padrão.")
    except Exception as e:
        connection.rollback()
        return print(f"SQL Error: {str(e)}")
    finally:
        if connection.open:
            connection.close()

query_create = """
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE IF NOT EXISTS esportes (
    id_esporte INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id_esporte)
);

CREATE TABLE IF NOT EXISTS campeonatos (
    id_campeonato INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao VARCHAR(500) NOT NULL DEFAULT '',
    url_logo VARCHAR(255) NOT NULL DEFAULT '',
    id_esporte INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    PRIMARY KEY (id_campeonato),
    FOREIGN KEY (id_esporte) 
        REFERENCES esportes(id_esporte) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    FOREIGN KEY (id_usuario) 
        REFERENCES usuarios(id_usuario) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS times (
    id_time INT NOT NULL AUTO_INCREMENT,
    id_campeonato INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    url_logo VARCHAR(255) NULL,
    PRIMARY KEY (id_time),
    FOREIGN KEY (id_campeonato) 
        REFERENCES campeonatos(id_campeonato)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS partidas (
    id_partida INT NOT NULL AUTO_INCREMENT,
    id_campeonato INT NOT NULL,
    rodada INT NOT NULL,
    data_hora DATETIME NULL,
    id_time_a INT NULL,
    id_time_b INT NULL,
    placar_time_a INT NULL,
    placar_time_b INT NULL,
    PRIMARY KEY (id_partida),
    FOREIGN KEY (id_campeonato) 
        REFERENCES campeonatos(id_campeonato)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (id_time_a) 
        REFERENCES times(id_time)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    FOREIGN KEY (id_time_b) 
        REFERENCES times(id_time)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);


INSERT INTO usuarios (nome, email, senha)
VALUES
('Fulano de Tal', 'fulano@email.com', 'senha'),
('Sicrano de Tal', 'Sicrano@email.com', 'senha'),
('Beltrano de Tal', 'Beltrano@email.com', 'senha');

INSERT INTO esportes (nome)
VALUES
('Futebol'), 
('Vôlei'), 
('Tênis'), 
('Hóquei'), 
('Natação'), 
('Skate'), 
('Surfe'), 
('Judô'), 
('Capoeira');

INSERT INTO campeonatos (nome, id_usuario, descricao, url_logo, id_esporte, data_inicio, data_fim)
VALUES
('Copa do Mundo de Clubes da FIFA 2025', (SELECT id_usuario FROM usuarios WHERE nome = 'Fulano de Tal'),
'Um torneio quadrienal internacional de futebol organizado pela Federação Internacional de Futebol (FIFA), disputado por 32 clubes das seis confederações continentais.',
'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/2025_FIFA_Club_World_Cup.svg/200px-2025_FIFA_Club_World_Cup.svg.png',
(SELECT id_esporte FROM esportes WHERE nome = 'Futebol'), '2025-06-14', '2025-07-13'),

('Campeonato Mundial de Hóquei no Gelo Ed. 86', (SELECT id_usuario FROM usuarios WHERE nome = 'Sicrano de Tal'),
'Torneio anual disputado pelas melhores seleções de hóquei no gelo. O torneio é organizado pela Federação Internacional de Hóquei no Gelo.',
'https://upload.wikimedia.org/wikipedia/en/thumb/9/96/2025_IIHF_World_Championship_logo.png/250px-2025_IIHF_World_Championship_logo.png',
(SELECT id_esporte FROM esportes WHERE nome = 'Hóquei'), '2025-05-09', '2025-05-25');

INSERT INTO times (nome, id_campeonato, url_logo)
VALUES
('Sociedade Esportiva Palmeiras', (SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'),
'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/250px-Palmeiras_logo.svg.png'),
('Futebol Clube do Porto', (SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'),
'https://upload.wikimedia.org/wikipedia/pt/thumb/c/c5/F.C._Porto_logo.png/120px-F.C._Porto_logo.png'),
('Botafogo de Futebol e Regatas', (SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'),
'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Botafogo_de_Futebol_e_Regatas_logo.svg/250px-Botafogo_de_Futebol_e_Regatas_logo.svg.png'),
('Seattle Sounders Football Club', (SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'),
'https://upload.wikimedia.org/wikipedia/pt/thumb/7/7c/Seattle_Sounders_FC.png/250px-Seattle_Sounders_FC.png'),
('Clube de Regatas do Flamengo', (SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'),
'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Flamengo_braz_logo.svg/250px-Flamengo_braz_logo.svg.png'),
('Espérance Sportive de Tunis', (SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'),
'https://upload.wikimedia.org/wikipedia/pt/thumb/4/49/Esp%C3%A9rance_Sportive_de_Tunis.png/250px-Esp%C3%A9rance_Sportive_de_Tunis.png');

INSERT INTO partidas (id_campeonato, rodada, data_hora, id_time_a, id_time_b, placar_time_a, placar_time_b)
VALUES
((SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'), 
'1', '2025-06-15 19:00:00', 
(SELECT id_time FROM times WHERE nome = 'Sociedade Esportiva Palmeiras'), (SELECT id_time FROM times WHERE nome = 'Futebol Clube do Porto'), 
'0', '0'),

((SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'), 
'1', '2025-06-15 23:00:00', 
(SELECT id_time FROM times WHERE nome = 'Botafogo de Futebol e Regatas'), (SELECT id_time FROM times WHERE nome = 'Seattle Sounders Football Club'), 
'2', '1'),

((SELECT id_campeonato FROM campeonatos WHERE nome = 'Copa do Mundo de Clubes da FIFA 2025'), 
'2', '2025-06-16 22:00:00', 
(SELECT id_time FROM times WHERE nome = 'Clube de Regatas do Flamengo'), (SELECT id_time FROM times WHERE nome = 'Espérance Sportive de Tunis'), 
'2', '0');
"""
