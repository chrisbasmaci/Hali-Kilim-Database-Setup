#! /usr/bin/env python3

#installing all used packages
    #source: https://stackoverflow.com/questions/17271444/how-to-install-a-missing-python-package-from-inside-the-script-that-needs-it

import sys, csv, psycopg2
from collections import Counter
import collections
import itertools

db_host = sys.argv[-5]
db_port = sys.argv[-4]
db_name = sys.argv[-3]
db_user = sys.argv[-2]
db_password = sys.argv[-1]

#names of the csv files which contain the data
kilimler_csv_name = sys.argv[1]#'kilimler.csv'
halilar_csv_name = sys.argv[2]#'halilar.csv'
photos_csv_name = sys.argv[3]#'photos.csv'





#------------------------------------------------------------------------------------------------------------------------------------------

#HELP:
'''
---Insertion to database:
   cur.execute('INSERT INTO Table1 (col1, col2) VALUES(%s, %s)', (value1, value2))

---Fetching from database:-----------------------------------------------------------------------------------------------------------------
   cur.execute(query)
   resultSet = cur.fetchall() - to fetch the whole result set
   reultSet = cur.fetchone() - to fetch a single row(does not mean only the first row, it means one row at a time)
-------------------------------------------------------------------------------------------------------------------------------------------
'''


def csv_to_list(csv_name):
#gets data from the csv file and puts it into a list of lists
#for accessing the data: data_list[row_number][column_number]
    data_list = []
    with open(csv_name, 'r', encoding='utf-8') as csvfile:
      data_squads = csv.reader(csvfile)
      
      for row in data_squads:
        #to remove all the ', to have no collisions in the code later on
        new_row = []
        for element in row:
          if isinstance(element, str):
            element = element.replace("'", "`")
          new_row.append(element)
        #print(new_row)
            
        data_list.append(new_row)
      #deletes the first row, which contains the table heads
      #optional:uncomment if this makes working with the data easier for you
      #del data_list[0]
    return data_list

def semicolon_string_to_list(string):
#interprets all ; of the given string as separator of elements
#returns a list of strings
    return string.split(';')

#------------------------------------------------------------------------------------------------------------------------------------------

#Lists from csvs
kilimler_list = csv_to_list(kilimler_csv_name)
halilar_list = csv_to_list(halilar_csv_name)
photos_list = csv_to_list(photos_csv_name)


#pop the names
kilimler_list.pop(0)
halilar_list.pop(0)
photos_list.pop(0)



#-------------------KILIMLER--------------------------

#----------------------KILIMER----------------------#




#---------------------INSTITUTIONS--------------------------#


#-----------------------------------------------------#


#SQL connection
sql_con = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
#cursor, for DB operations
cur = sql_con.cursor()
#----------------------------------------------------------Schema Setup-----------------------------------------------------------------------#
cur.execute("DROP TABLE IF EXISTS Kilimler, Halilar, Photos;")
cur.execute("DROP TABLE IF EXISTS Countries, Institutions, Persons, Theses, Conferences, Journals, Papers, AuthPapers;")
cur.execute("CREATE TABLE Kilimler (K_Key INT PRIMARY KEY, ORIGIN VARCHAR(256) NOT NULL, WIDTH INT NOT NULL, LENGTH INT NOT NULL, M2 FLOAT NOT NULL, PRICE INT NOT NULL);")
cur.execute("CREATE TABLE Halilar (H_Key INT PRIMARY KEY, ORIGIN VARCHAR(256) NOT NULL, WIDTH INT NOT NULL, LENGTH INT NOT NULL, M2 FLOAT NOT NULL, PRICE INT NOT NULL);")
cur.execute("CREATE TABLE Photos (P_Key INT PRIMARY KEY, Link VARCHAR(256) NOT NULL, K_Key INT REFERENCES Kilimler, H_Key INT REFERENCES Halilar, CHECK((K_Key IS NOT NULL AND H_Key IS NULL) OR (K_Key IS NULL AND H_Key IS NOT NULL)));")

#---------------------------------------------INSERTING----------------------------------------------------------------------------------------#

#--------------------------------------------KILIMLER------------------------------------------------------------------#
for bang in kilimler_list:
    k_key, origin, width, length, m2, price = bang[1], bang[2], bang[3], bang[4], bang[5], bang[6]
    k_key_num = k_key.replace("K-", "")
    
 

    cur.execute("""
    INSERT INTO kilimler (
        k_key, origin, width, length, m2, price
    ) VALUES (
        %(k_key_val)s, %(origin_val)s, %(width_val)s, %(length_val)s, %(m2_val)s, %(price_val)s
    )""", {
        "k_key_val": k_key_num,
        "origin_val": origin,
        "width_val": width,
        "length_val": length,
        "m2_val": m2,
        "price_val": price
    })
#--------------------------------------------------HALILAR---------------------------------------------------------#
for bang in halilar_list:
    h_key, origin, width, length, m2, price = bang[1], bang[2], bang[3], bang[4], bang[5], bang[6]
    h_key_num = h_key.replace("H-", "")
    
 

    cur.execute("""
    INSERT INTO halilar (
        h_key, origin, width, length, m2, price
    ) VALUES (
        %(h_key_val)s, %(origin_val)s, %(width_val)s, %(length_val)s, %(m2_val)s, %(price_val)s
    )""", {
        "h_key_val": h_key_num,
        "origin_val": origin,
        "width_val": width,
        "length_val": length,
        "m2_val": m2,
        "price_val": price
    })

#---------------------------Photos-------------------------------#
for bang in photos_list:
    p_key, link, kh_key = bang[0], bang[1], bang[2]
    p_key_num = p_key.replace("P-", "")
    k_key = kh_key.replace("K-", "") if kh_key[0].lower() == "k" else None
    h_key = kh_key.replace("H-", "") if kh_key[0].lower() == "h" else None

    cur.execute("""
    INSERT INTO photos (
        p_key, link, k_key, h_key
    ) VALUES (
        %(p_key_val)s, 
        %(link_val)s, 
        %(k_key_val)s, 
        %(h_key_val)s
    )""", {
        "p_key_val": p_key_num,
        "link_val": link,
        "k_key_val": k_key,
        "h_key_val": h_key,
    })




#----------------------------------------------------------------------------------------#
#commit the changes, this makes the database persistent
sql_con.commit()

#close connections
cur.close()
sql_con.close()
