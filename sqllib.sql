UPDATE `alpine`.`block` SET `filename` = '01_rosman.txt' WHERE (`block` = '1');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('2', '01_spivak.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('3', '02_rosman.txt');
INSERT INTO `alpine`.`block` (`block`, `filename`) VALUES ('4', '02_spivak.txt');


SELECT DISTINCT token_text, token_lemma FROM alpine.spacynlp
 WHERE token_tag = 'VERB'
   AND  
     (( substring(token_lemma,-2,2) = 'ть' ) OR
        ( substring(token_lemma,-4,4) = 'ться') OR 
        ( substring(token_lemma,-2,2) = 'ти') OR 
        ( substring(token_lemma,-2,2) = 'чь' ))
 ORDER BY token_lemma ASC;
