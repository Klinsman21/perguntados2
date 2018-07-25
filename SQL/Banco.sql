CREATE DATABASE Perguntados;

CREATE TABLE Jogador (Player serial,UserName varchar(255) ,email varchar(255) ,senha varchar(255) ,PRIMARY KEY (Player));


CREATE TABLE Partidas (ID serial,horario time,Player1 int ,Player2 int ,vencedor int,Pontos1 int ,Pontos2 int ,PRIMARY KEY (ID),FOREIGN KEY (Player1) REFERENCES Jogador(Player),FOREIGN KEY (Player2) REFERENCES Jogador(Player),FOREIGN KEY (vencedor) REFERENCES Jogador(Player));



CREATE TABLE Resultado (ID serial,Jogador int,Partida int,Pergunta int,Acerto BOOLEAN,PRIMARY KEY (ID),FOREIGN KEY (Jogador) REFERENCES Jogador(Player),FOREIGN KEY (Partida) REFERENCES Partidas(ID),FOREIGN KEY (Pergunta) REFERENCES Perguntas(ID));


CREATE TABLE Perguntas (ID serial,Pergunta varchar(255),Resposta1 varchar(255),Resposta2 varchar(255),Resposta3 varchar(255),Correta varchar(255),Categoria int,PRIMARY KEY (ID),FOREIGN KEY (Categoria) REFERENCES Categorias(ID));



CREATE TABLE Categorias (ID serial,Categoria varchar(255),PRIMARY KEY (ID));

insert into categorias (Categoria) values ('Ciência');
insert into categorias (Categoria) values ('Geografia');
insert into categorias (Categoria) values ('Arte');
insert into categorias (Categoria) values ('Esporte');
insert into categorias (Categoria) values ('Entretenimento');
insert into categorias (Categoria) values ('História');


