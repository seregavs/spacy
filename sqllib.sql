SELECT DISTINCT token_text, token_lemma FROM alpine.spacynlp
 WHERE token_tag = 'VERB'
   AND  
     (( substring(token_lemma,-2,2) = 'ть' ) OR
        ( substring(token_lemma,-4,4) = 'ться') OR 
        ( substring(token_lemma,-2,2) = 'ти') OR 
        ( substring(token_lemma,-2,2) = 'чь' ))
 ORDER BY token_lemma ASC;
