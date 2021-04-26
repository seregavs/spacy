# coding: utf-8
import spacy
import mysql.connector
import os
import datetime
from constants import *
from progressbar import *
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm

cursor = None

sql_select_block = ("SELECT block, filename FROM alpine.block WHERE block < 6 ORDER BY block")

sql_insert_spacynlp = (
    "INSERT INTO `alpine`.`spacynlp` (`block`, `line`, `token_index`, `token_text`, `token_lemma`, `token_pos`, `token_tag`, `token_dep`)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
sql_delete_spacynlp = (
    "DELETE FROM `alpine`.`spacynlp` WHERE (`block` = %s)")

# clear terminal before report run
os.system('cls' if os.name == 'nt' else 'clear')

cnx = mysql.connector.connect(user=LC_DBUSER, database=LC_DATABASE, host=LC_DBHOST, password=LC_DBPASS, port=LC_DBPORT)
if not cnx:
    print('No connection made')
    quit()

print('Connected: ' + str(cnx))
cursor = cnx.cursor()
cursor.execute(sql_select_block)
blocks = cursor.fetchall()
nlp = spacy.load('ru_core_news_lg')
cnx.close()
pbar_corpus = tqdm(total=len(blocks))

begin_time = datetime.datetime.now().replace(microsecond=0)

def nlp_corpus(block):
    blockid = 0
    cnx = None
    cnx = mysql.connector.connect(user=LC_DBUSER, database=LC_DATABASE, host=LC_DBHOST, password=LC_DBPASS, port=LC_DBPORT)
    if not cnx:
        print('No connection made')
        quit()
    
    blockid = int(block[0])
    sql_data_delete_spacynlp = (blockid, )
    cursor = cnx.cursor()
    cursor.execute(sql_delete_spacynlp, sql_data_delete_spacynlp)
    cnx.commit()
    blockfile = 'corpus/' + block[1].strip()

    lines = None
    with open(blockfile, encoding="utf-8") as f:
        lines = (line.rstrip() for line in f)
        lines = list(line for line in lines if line)
    for index, line in enumerate(lines):
        doc = nlp(line)
        for token_index, token in enumerate(doc):
            sql_data_insert_spacynlp = (blockid, index, token_index, token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
            if cursor:
                cursor.execute(sql_insert_spacynlp, sql_data_insert_spacynlp)
        if index%LC_COMMIT_EVERY_N_ROWS == 0:
            cnx.commit()
    cnx.commit()
    cnx.close()
    pbar_corpus.update(1)

pool = ThreadPool(4)
results = pool.map(nlp_corpus, blocks)
pool.close()
pool.join()

# https://zetcode.com/python/multiprocessing/
print('All done. Duration is ' + str(datetime.datetime.now().replace(microsecond=0) - begin_time))