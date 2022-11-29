CREATE TABLE IF NOT EXISTS devoir
(
    id             INT          NOT NULL AUTO_INCREMENT,
    date           DATE         NOT NULL,
    matiere        VARCHAR(255) NOT NULL,
    devoir         VARCHAR(255) NOT NULL,
    infoImportante VARCHAR(255) NOT NULL,
    salonDiscord   VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
