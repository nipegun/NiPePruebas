#!/usr/bin/env python3

# Vulnerabilidad simulada: Broken Access Control.
# La vista /admin no comprueba sesión ni rol alguno, permitiendo que cualquiera acceda a funciones administrativas.
# La vulnerabilidad consiste en la ausencia de controles de autorización.
# Para explotarla basta con solicitar directamente http://host:25001/admin sin autenticarse.

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
  app.run(host="0.0.0.0", port=25001, debug=True)
