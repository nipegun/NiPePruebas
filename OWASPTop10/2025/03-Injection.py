#!/usr/bin/env python3
# Vulnerabilidad simulada: Inyección SQL. Los parámetros u y p se concatenan directamente en la
# consulta de autenticación sin usar parámetros preparados, permitiendo alterar la query. La
# vulnerabilidad consiste en no depurar ni parametrizar entradas controladas por el usuario. Se
# explota enviando valores como u=admin&p=' OR '1'='1 para saltar el login y enumerar datos.

import sqlite3
from flask import Flask, request

app = Flask(__name__)
cDB = "inj.db"

def fInit():
  conn = sqlite3.connect(cDB)
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT)")
  cur.execute("INSERT INTO users VALUES ('admin','admin123')")
  conn.commit()
  conn.close()

@app.route("/login", methods=["GET","POST"])
def fLogin():
  if request.method == "GET":
    return """
    <form method='POST'>
      User:<input name='u'><br>
      Pass:<input name='p'><br>
      <input type='submit'>
    </form>
    """
  vU = request.form.get("u","")
  vP = request.form.get("p","")
  conn = sqlite3.connect(cDB)
  cur = conn.cursor()

  # VULN SQLi
  query = f"SELECT user FROM users WHERE user='{vU}' AND pass='{vP}'"
  cur.execute(query)
  row = cur.fetchone()
  conn.close()

  if row:
    return f"Logged in como {row[0]}<br><pre>{query}</pre>"
  return f"Fallo<br><pre>{query}</pre>"

if __name__ == "__main__":
  fInit()
  app.run(host="0.0.0.0", port=25003, debug=True)
