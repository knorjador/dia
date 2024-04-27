
/* 

    BDD foodly 

    > Création des tables aliment && utilisateur 
    > Insertion de données dans les tables 

*/

CREATE TABLE IF NOT EXISTS aliment (
    id SERIAL,
    nom varchar(100) NOT NULL,
    marque varchar(100) DEFAULT NULL,
    sucre float DEFAULT NULL,
    calories int NOT NULL,
    graisses float DEFAULT NULL,
    proteines float DEFAULT NULL,
    bio smallint DEFAULT '0',
    PRIMARY KEY (id)
);

INSERT INTO 
    aliment (nom, marque, sucre, calories, graisses, proteines, bio)
VALUES
    ('pomme','sans marque',19.1,72,0.2,0.4,0),
    ('poire','sans marque',27.5,134,0.2,1.1,1),
    ('banane','chiquita',24,101,0.3,1.1,0),
    ('jambon','herta',0.2,34,0.8,6.6,0),
    ('compote','andros',11,51,0,0.5,0),
    ('steak haché','charal',0.8,68,4.8,4.8,0),
    ('saumon','guyader',0,206,12.3,22.1,0),
    ('haricots verts','bonduelle',5.8,25,0.1,1.5,0),
    ('riz','oncle benz',28.2,130,0.3,2.7,0),
    ('pâtes completes','barilla',64,353,2.7,14,1),
    ('blanc de dinde','père dodu',0.6,98,0.9,22,0),
    ('filet de poulet','le gaulois',0,121,1.8,26.2,0),
    ('muesli','bjorg',26.5,170,5,3.5,1),
    ('café','carte noire',0,0,0,0,0),
    ('jus d''orange','innocent',16,74,0,1.6,0),
    ('jus de pomme','andros',24,100,0.2,0.2,1),
    ('pomme de terre','doréac',21.1,104,0.2,2.8,0),
    ('oeuf','naturalia',0.4,74,5.1,6.5,1),
    ('baguette','sans marque',36.1,185,1.2,7.5,0),
    ('lait d''amande','bjorg',6.1,80,5.3,1.5,1);

CREATE TABLE IF NOT EXISTS utilisateur (
    id SERIAL,
    nom varchar(100) DEFAULT NULL,
    prenom varchar(100) DEFAULT NULL,
    email varchar(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE(email)
);

INSERT INTO 
    utilisateur (nom, prenom, email)
VALUES 
    ('durantay','quentin','qentin@gmail.com'),
    ('dupont','marie','marie@hotmail.fr'),
    ('miller','vincent','vm@yahoo.com'),
    ('zuckerberg','marc','marc@gmail.com'),
    ('paul','pierre','pp@orange.fr'),
    ('de vauclerc','lisa','lisadv@gmail.com'),
    ('gluntig','éléonore','glunt@sfr.com'),
    ('cavill','henry','henry@outlook.fr'),
    ('hopper','lionel','hpp@gmail.com'),
    ('tember','fabienne','fabienne@yopmail.com');


/*

    CRUD -> create 

    Insérez le tableau suivant.

    nom             marque      calories    sucre   graisses    proteines   bio
    haricots verts  Monoprix    25          3       0           1.7         0

*/


INSERT INTO 
    aliment (nom, marque, sucre, calories, graisses, proteines, bio)
VALUES
    ('haricots verts','Monoprix',25,3,0,1.7,0);


/*

    CRUD -> read 

    Lister tous les noms et les calories associées pour chaque aliment présent.

*/


SELECT nom, calories FROM aliment;


/*

    CRUD -> update 

    Préciser le type de pomme vendue, il s'agit d'une pomme golden.

*/


UPDATE aliment SET nom = 'pomme golden' WHERE nom = 'pomme';


/*

    CRUD -> delete 

    Supprimer définitivement la pomme golden.

*/


DELETE FROM aliment WHERE nom = 'pomme golden';


/*

    CRUD -> read 

    Retrouver tous les aliments qui ne sont pas bio, classés par ordre décroissant de contenance en protéines.

*/


SELECT * 
FROM aliment 
WHERE bio = 0
ORDER BY proteines DESC;


/*

    CRUD -> read 

    Tester MIN et SUM

*/


SELECT MIN(calories)  AS "Nombre de calories minimum"
FROM aliment; 

SELECT ROUND(SUM(graisses)) AS "Total graisse des aliments avec calories supérieur à 100"
FROM aliment 
WHERE calories > 100;


/*

    CRUD -> create 

    Créer une vue des aliments non bio, classés par contenance en protéines (de manière décroissante).

*/


CREATE VIEW aliments_non_bio_proteines_desc AS 
    (   
        SELECT * 
        FROM aliment 
        WHERE bio = 0
        ORDER BY proteines DESC
    );


/*

    Création de nouvelles tables et de relations pour l'utilisation de jointures.

*/


CREATE TABLE IF NOT EXISTS langue (
    id SERIAL,
    nom varchar(100) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO 
    langue (nom)
VALUES
    ('français'),
    ('anglais');

ALTER TABLE utilisateur
    ADD COLUMN IF NOT EXISTS langue_id int;

ALTER TABLE utilisateur 
    ADD CONSTRAINT fk_langue_id FOREIGN KEY (langue_id) REFERENCES langue (id) ON DELETE CASCADE;

UPDATE utilisateur set langue_id = (SELECT x FROM (VALUES (1), (2)) v(x) LIMIT 1);

CREATE TABLE utilisateur_aliment (
    utilisateur_id int NOT NULL,
    aliment_id int NOT NULL,
    PRIMARY KEY (utilisateur_id, aliment_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (aliment_id) REFERENCES aliment (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT INTO 
    utilisateur_aliment (utilisateur_id, aliment_id)
VALUES 
    (1,7),
    (1,3),
    (1,5),
    (2,2),
    (2,19),
    (2,14),
    (3,4),
    (3,15),
    (3,12),
    (1,17),
    (4,5),
    (4,4),
    (4,7),
    (5,2),
    (5,18),
    (5,3),
    (6,2),
    (6,12),
    (6,6),
    (7,16),
    (7,19),
    (7,2),
    (8,3),
    (8,5),
    (9,18),
    (9,9),
    (9,14),
    (10,16),
    (10,3);


/*

    Jointure : 

    Retrouver tous les noms de famille des utilisateurs ayant sélectionné le français. 

*/


SELECT DISTINCT utilisateur.nom
FROM utilisateur
JOIN langue
ON utilisateur.langue_id = (SELECT id FROM langue WHERE nom = 'français');


/*

    Jointure : 

    Retrouver tous les aliments sélectionnés par les utilisateurs dont l’adresse e-mail et une adresse Gmail. 

*/


SELECT *
FROM aliment
JOIN utilisateur_aliment ON (aliment.id = utilisateur_aliment.aliment_id)
JOIN utilisateur ON (utilisateur.id = utilisateur_aliment.utilisateur_id AND utilisateur.email ILIKE '%gmail%');

