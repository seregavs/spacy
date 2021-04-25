# coding: utf-8
import spacy
import mysql.connector

# constants begin
blockid     =   0
cursor      = None

sql_select_block = ( "SELECT block, filename FROM alpine.block")

sql_insert_spacynlp = (
    "INSERT INTO `alpine`.`spacynlp` (`block`, `line`, `token_index`, `token_text`, `token_lemma`, `token_pos`, `token_tag`, `token_dep`)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
sql_delete_spacynlp = ( 
    "DELETE FROM `alpine`.`spacynlp` WHERE (`block` = %s)")

# constants end 

cnx = mysql.connector.connect(user='ALPINE', database='alpine', host='127.0.0.1', password='Init$12345', port = 3306)
if cnx is None:
    print('No connection made')
    quit()

print(cnx)    
cursor = cnx.cursor()
cursor.execute(sql_select_block)
blocks = cursor.fetchall()
nlp =  spacy.load('ru_core_news_lg')

for block in blocks:
    blockid = int(block[0])
    sql_data_delete_spacynlp = (blockid , )
    cursor.execute(sql_delete_spacynlp, sql_data_delete_spacynlp)
    cnx.commit()
    blockfile   = 'corpus/' + block[1].strip()
    with open(blockfile, encoding="utf-8") as f:
        lines = (line.rstrip() for line in f) 
        lines = list(line for line in lines if line)

    for index, line in enumerate(lines):
        # print(index, line)
        doc = nlp(line)
        for token_index, token in enumerate(doc):
            sql_data_insert_spacynlp = (blockid, index, token_index, token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
            # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
            if cursor:
                cursor.execute(sql_insert_spacynlp, sql_data_insert_spacynlp)
                # print(cursor.lastrowid)
                cnx.commit()
        print('block ', blockid, ' line ', index, ' handled')
    print('block ', blockid, ' done')
cnx.close()   
print('All done')
