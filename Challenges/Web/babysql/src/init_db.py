import sqlite3
import hashlib

connection=sqlite3.connect("database.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

cur=connection.cursor()

cur.execute("INSERT INTO priv_users (username,password,is_admin) VALUES (?,?,?)",
            ("Leon",hashlib.sha256("securepassword".encode()).hexdigest(),1)
            )

cur.execute("INSERT INTO priv_users (username,password,is_admin) VALUES (?,?,?)",
            ("Rigby",hashlib.sha256("knightrider".encode()).hexdigest(),1)
            )


cur.execute("INSERT INTO priv_users (username,password,is_admin) VALUES (?,?,?)",
            ("Cisco",hashlib.sha256("test101".encode()).hexdigest(),1)
            )

cur.execute("INSERT INTO products (description,price) VALUES (?,?)",("Blahaj","$4000"))
cur.execute("INSERT INTO products (description,price) VALUES (?,?)",("Blahaj but bigger","$10000"))
cur.execute("INSERT INTO products (description,price) VALUES (?,?)",("Blahaj but half the price","$2000"))

connection.commit()
connection.close()