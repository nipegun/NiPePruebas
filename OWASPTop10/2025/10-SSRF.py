#!/usr/bin/env python3
# Vulnerabilidad simulada: Server-Side Request Forgery (SSRF). El endpoint /fetch solicita la
# URL indicada por el usuario y devuelve su contenido sin validarla, permitiendo acceder a
# recursos internos o metadatos. La debilidad es permitir que el servidor haga peticiones
# arbitrarias. Para explotarla, se puede llamar a /fetch?url=http://127.0.0.1:25009/login para
# alcanzar servicios internos o endpoints de administración no expuestos.
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/fetch")
def fFetch():
  vURL = request.args.get("url","http://127.0.0.1")
  # VULN: SSRF sin validación
  r = requests.get(vURL)
  return f"<pre>{r.text}</pre>"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25010, debug=True)
