-- DROP DES TABLES EXISTANTES
DROP TABLE IF EXISTS eleve;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS professeur_classe;
DROP TABLE IF EXISTS classe;
DROP TABLE IF EXISTS professeur;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS matiere;

-- CREATION DES TABLES

CREATE TABLE classe (
    nom_classe TEXT PRIMARY KEY
);

CREATE TABLE eleve (
    id_utilisateur VARCHAR(100) PRIMARY KEY,
    nom_classe TEXT,
    lv2 TEXT,
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY(nom_classe) REFERENCES classe(nom_classe)
);

CREATE TABLE professeur (
    id_utilisateur VARCHAR(100) PRIMARY KEY,
    nom_matiere VARCHAR(100),
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY(nom_matiere) REFERENCES matiere(nom_matiere)
);

CREATE TABLE matiere (
    nom_matiere VARCHAR(100) PRIMARY KEY
);

CREATE TABLE utilisateur (
    id_utilisateur VARCHAR(100) PRIMARY KEY,
    nom_utilisateur TEXT NOT NULL,
    prenom_utilisateur TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role_utilisateur VARCHAR(100),
    tentatives_echouees INTEGER DEFAULT 0,
    verrouillage_until TIMESTAMP
);

CREATE TABLE note (
    nom_note TEXT,
    date_note DATE,
    id_utilisateur VARCHAR(100),
    nom_matiere VARCHAR(100),
    valeur_note FLOAT,
    coefficient FLOAT,
    PRIMARY KEY(nom_note, date_note, id_utilisateur, nom_matiere),
    FOREIGN KEY(nom_matiere) REFERENCES matiere(nom_matiere),
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    CHECK(valeur_note >= 0 AND valeur_note <= 20)
);

CREATE TABLE professeur_classe (
    id_utilisateur VARCHAR(100),
    nom_classe TEXT,
    FOREIGN KEY(id_utilisateur) REFERENCES professeur(id_utilisateur),
    FOREIGN KEY(nom_classe) REFERENCES classe(nom_classe),
    PRIMARY KEY(id_utilisateur, nom_classe)
);

---------------------------------------------------------------------
-- INSERTIONS

-- Matières (4 matières différentes)
INSERT INTO matiere (nom_matiere) VALUES ('physique chimie');
INSERT INTO matiere (nom_matiere) VALUES ('allemand');
INSERT INTO matiere (nom_matiere) VALUES ('mathématiques');
INSERT INTO matiere (nom_matiere) VALUES ('espagnol');

-- Classes (4 classes)
INSERT INTO classe (nom_classe) VALUES ('3A');
INSERT INTO classe (nom_classe) VALUES ('3B');
INSERT INTO classe (nom_classe) VALUES ('3C');
INSERT INTO classe (nom_classe) VALUES ('3D');

---------------------------------------------------------------------
-- PROFESSEURS

-- Pour ces INSERT, la valeur pour nom_utilisateur devient le prénom et prenom_utilisateur devient le nom.
INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Didier.Lopez', 'Lopez', 'Didier', '41143e3410ebb1c0d755bb978d6cde09ce7a5f88d744c709201fb2afc9b0b3a3', 'professeur');

INSERT INTO professeur (id_utilisateur, nom_matiere)
VALUES ('Didier.Lopez', 'physique chimie');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Hans.Baeur', 'Baeur', 'Hans', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'professeur');

INSERT INTO professeur (id_utilisateur, nom_matiere)
VALUES ('Hans.Baeur', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Alice.Wonder', 'Wonder', 'Alice', '8c954cd9b6c8f8180a05f1de66ee555f0c44b4c6738120785d827521bb8d54df', 'professeur');

INSERT INTO professeur (id_utilisateur, nom_matiere)
VALUES ('Alice.Wonder', 'mathématiques');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Bob.Builder', 'Builder', 'Bob', '0b04e64c490eb7b9c61f84b36697239b28c65728b28f07ad70ca23191246c9b4', 'professeur');

INSERT INTO professeur (id_utilisateur, nom_matiere)
VALUES ('Bob.Builder', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Eve.Adams', 'Adams', 'Eve', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professeur');

INSERT INTO professeur (id_utilisateur, nom_matiere)
VALUES ('Eve.Adams', 'physique chimie');

---------------------------------------------------------------------
-- Affectation des professeurs aux classes

INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Didier.Lopez', '3A');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Didier.Lopez', '3B');

INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Hans.Baeur', '3A');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Hans.Baeur', '3B');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Hans.Baeur', '3C');

INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Alice.Wonder', '3C');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Alice.Wonder', '3D');

INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Bob.Builder', '3B');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Bob.Builder', '3D');

INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Eve.Adams', '3A');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Eve.Adams', '3C');
INSERT INTO professeur_classe (id_utilisateur, nom_classe) VALUES ('Eve.Adams', '3D');

---------------------------------------------------------------------
-- ÉLÈVES

-- Classe 3A (10 élèves)
INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Max.Costo', 'Costo', 'Max', '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Max.Costo', '3A', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Jessie.Spike', 'Spike', 'Jessie', 'f2d81a260dea8a100dd517984e53c56a7523d96942a834b9cdc249bd4e8c7aa9', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Jessie.Spike', '3A', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Leon.Cordelius', 'Cordelius', 'Leon', '1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Leon.Cordelius', '3A', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('John.Doe', 'Doe', 'John', '280d44ab1e9f79b5cce2dd4f58f5fe91f0fbacdac9f7447dffc318ceb79f2d02', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('John.Doe', '3A', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Jane.Doe', 'Doe', 'Jane', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Jane.Doe', '3A', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Mark.Twain', 'Twain', 'Mark', 'e4ad93ca07acb8d908a3aa41e920ea4f4ef4f26e7f86cf8291c5db289780a5ae', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Mark.Twain', '3A', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Luke.Skywalker', 'Skywalker', 'Luke', 'a941a4c4fd0c01cddef61b8be963bf4c1e2b0811c037ce3f1835fddf6ef6c223', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Luke.Skywalker', '3A', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Leia.Organa', 'Organa', 'Leia', 'a9c43be948c5cabd56ef2bacffb77cdaa5eec49dd5eb0cc4129cf3eda5f0e74c', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Leia.Organa', '3A', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Han.Solo', 'Solo', 'Han', '6382deaf1f5dc6e792b76db4a4a7bf2ba468884e000b25e7928e621e27fb23cb', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Han.Solo', '3A', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Peter.Parker', 'Parker', 'Peter', '000c285457fc971f862a79b786476c78812c8897063c6fa9c045f579a3b2d63f', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Peter.Parker', '3A', 'espagnol');

---------------------------------------------------------------------
-- Classe 3B (10 élèves)
INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Tom.Cruise', 'Cruise', 'Tom', '0bb09d80600eec3eb9d7793a6f859bedde2a2d83899b70bd78e961ed674b32f4', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Tom.Cruise', '3B', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Brad.Pitt', 'Pitt', 'Brad', 'fc613b4dfd6736a7bd268c8a0e74ed0d1c04a959f59dd74ef2874983fd443fc9', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Brad.Pitt', '3B', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Angelina.Jolie', 'Jolie', 'Angelina', '73cd1b16c4fb83061ad18a0b29b9643a68d4640075a466dc9e51682f84a847f5', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Angelina.Jolie', '3B', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Johnny.Dep', 'Dep', 'Johnny', '203b70b5ae883932161bbd0bded9357e763e63afce98b16230be33f0b94c2cc5', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Johnny.Dep', '3B', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Will.Smith', 'Smith', 'Will', '27cc6994fc1c01ce6659c6bddca9b69c4c6a9418065e612c69d110b3f7b11f8a', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Will.Smith', '3B', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Keanu.Reeves', 'Reeves', 'Keanu', '13b1f7ec5beaefc781e43a3b344371cd49923a8a05edd71844b92f56f6a08d38', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Keanu.Reeves', '3B', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Tom.Hanks', 'Hanks', 'Tom', '85738f8f9a7f1b04b5329c590ebcb9e425925c6d0984089c43a022de4f19c281', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Tom.Hanks', '3B', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Morgan.Freeman', 'Freeman', 'Morgan', 'a01edad91c00abe7be5b72b5e36bf4ce3c6f26e8bce3340eba365642813ab8b6', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Morgan.Freeman', '3B', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Robert.Downey', 'Downey', 'Robert', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Robert.Downey', '3B', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Chris.Evans', 'Evans', 'Chris', 'daaad6e5604e8e17bd9f108d91e26afe6281dac8fda0091040a7a6d7bd9b43b5', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Chris.Evans', '3B', 'italien');

---------------------------------------------------------------------
-- Classe 3C (10 élèves)
INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Harry.Potter', 'Potter', 'Harry', '1532e76dbe9d43d0dea98c331ca5ae8a65c5e8e8b99d3e2a42ae989356f6242a', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Harry.Potter', '3C', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Hermione.Granger', 'Granger', 'Hermione', '3a120dc1589bb2f0cb023b28ec75328be3fc5333ef0707285b31f47ad268dfd3', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Hermione.Granger', '3C', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Ron.Weasley', 'Weasley', 'Ron', '74fca0325b5fdb3a34badb40a2581cfbd5344187e8d3432952a5abc0929c1246', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Ron.Weasley', '3C', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Draco.Malfoy', 'Malfoy', 'Draco', 'c0a4942143e872cd1ae29fc759e04526de2e909ac1732734d38550a29c2e2516', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Draco.Malfoy', '3C', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Luna.Lovegood', 'Lovegood', 'Luna', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Luna.Lovegood', '3C', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Neville.Longbottom', 'Longbottom', 'Neville', 'c06b0cfe0cc5e900c57784484094331f095bf441995c3c31ea6c75691c786c35', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Neville.Longbottom', '3C', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Cedric.Diggory', 'Diggory', 'Cedric', '7499aced43869b27f505701e4edc737f0cc346add1240d4ba86fbfa251e0fc35', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Cedric.Diggory', '3C', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Cho.Chang', 'Chang', 'Cho', 'fcfd075cbe367c158d5cfaa31fa06656a3e68f626388d96ee81b35dda4310b58', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Cho.Chang', '3C', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Seamus.Finnigan', 'Finnigan', 'Seamus', '04e77bf8f95cb3e1a36a59d1e93857c411930db646b46c218a0352e432023cf2', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Seamus.Finnigan', '3C', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Dean.Thomas', 'Thomas', 'Dean', '3113c9e45ff0b8e19f06e443deaa361cedb08d420b0e63606219cd5881f5fa27', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Dean.Thomas', '3C', 'allemand');

---------------------------------------------------------------------
-- Classe 3D (10 élèves)
INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Tony.Stark', 'Stark', 'Tony', 'e83664255c6963e962bb20f9fcfaad1b570ddf5da69f5444ed37e5260f3ef689', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Tony.Stark', '3D', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Steve.Rogers', 'Rogers', 'Steve', '308738b8195da46d65c96f4ee3909032e27c818d8a079bccb5a1ef62e8daaa45', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Steve.Rogers', '3D', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Bruce.Banner', 'Banner', 'Bruce', '2406f46e506c14b5a93679beacf9a89f6878521a444455866726d7a4ea9f6fe9', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Bruce.Banner', '3D', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Natasha.Romanoff', 'Romanoff', 'Natasha', '25b21a90ee740137306992158852f5d051dd98d70e907e3d0d4859ca6e31c587', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Natasha.Romanoff', '3D', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Clint.Barton', 'Barton', 'Clint', '43999461d22f67840fcd9b8824293eaa4f18146e57b2c651bcd925e3b3e4e429', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Clint.Barton', '3D', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Wanda.Maximoff', 'Maximoff', 'Wanda', '846f6a76ffc111552f1c9ca3a06d989d0c9c9b79c4fc25ff67f6207be512955c', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Wanda.Maximoff', '3D', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Vision.Nocturne', 'Nocturne', 'Vision', 'eaa2bded32cc585d3f37c5319abe8890ad28a697ed66d5823f10536cc9c0fdb9', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Vision.Nocturne', '3D', 'italien');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Peter.Quill', 'Quill', 'Peter', 'f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Peter.Quill', '3D', 'espagnol');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Gamora.Riche', 'Riche', 'Gamora', '44de3ed43a38bbf73a9e4d5ea79f0b06ab29f5d003984a335cd3f79781c04e51', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Gamora.Riche', '3D', 'allemand');

INSERT INTO utilisateur (id_utilisateur, nom_utilisateur, prenom_utilisateur, mot_de_passe, role_utilisateur)
VALUES ('Drax.Jean', 'Jean', 'Drax', '885ccdcc9119306a9dd59a8a85b9a5548ecd312981c3adde82a5ff7766e7bf08', 'eleve');
INSERT INTO eleve (id_utilisateur, nom_classe, lv2) VALUES ('Drax.Jean', '3D', 'italien');
