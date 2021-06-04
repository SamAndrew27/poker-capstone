import psycopg2 as pg2
from sqlalchemy import create_engine

conn = pg2.connect(database="hand_results", user="postgres", password="galvanize", host="localhost", port="5432")

engine = create_engine("postgresql://postgres:galvanize@localhost:5432/hand_results")

cur = conn.cursor()

num = 5

cur.execute(
    f'''CREATE TABLE test{num}(
        name VARCHAR,
        whatever INT,
        something TEXT    
        );
        ''')
conn.commit()
cur.execute(
    f'''INSERT INTO test{num}(name, whatever, something)
    VALUES ('sam', 5, 'Hello?')'''
)
conn.commit()
cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cur.fetchall():
    print(table)
    print(type(table[0]))