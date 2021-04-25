 CREATE TABLE `spacynlp` (
  `block` int NOT NULL,
  `line` int NOT NULL,
  `token_index` int NOT NULL,
  `token_text` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `token_lemma` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `token_pos` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `token_tag` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `token_dep` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`block`,`line`,`token_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

CREATE TABLE `block` (
  `block` int NOT NULL,
  `filename` varchar(45) NOT NULL,
  PRIMARY KEY (`block`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

DELETE FROM `alpine`.`block` WHERE block >= 1; -- because of safe mode in SQL Workbench
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('1', '01_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('2', '01_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('3', '02_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('4', '02_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('5', '03_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('6', '03_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('7', '04_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('8', '04_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('9', '05_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('10', '05_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('11', '06_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('12', '06_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('13', '07_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('14', '07_spivak.txt');

SELECT DISTINCT block, token_text, token_lemma FROM alpine.spacynlp
 WHERE token_tag = 'VERB'
   AND  
     (( substring(token_lemma,-2,2) = 'ть' ) OR
        ( substring(token_lemma,-4,4) = 'ться') OR 
        ( substring(token_lemma,-2,2) = 'ти') OR 
        ( substring(token_lemma,-2,2) = 'чь' ))
 ORDER BY block, token_lemma ASC;

 -- total number of verbs by block
SELECT block, count(*) as cnt_VERB
  FROM alpine.spacynlp
 WHERE token_tag = 'VERB'
 GROUP BY block;