#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def fHome():
  return "<h1>Inicio</h1><p><a href='/admin'>Panel Admin</a></p>"

@app.route("/admin")
def fAdmin():
  # VULN: No comprueba si el usuario está logueado
  return "<h1>Panel de Administración</h1><p>Acceso otorgado sin control.</p>"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001, debug=True)
