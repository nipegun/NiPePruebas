#!/usr/bin/env python3

# Vulnerabilidad simulada: Security Misconfiguration.
# La ruta principal muestra todas las variables de entorno y el servidor se ejecuta en modo debug, exponiendo secretos y trazas.
# La falla proviene de configuraciones inseguras y falta de hardening.
# Para explotarla sólo hay que visitar la raíz y leer los valores sensibles o forzar errores para ver información adicional.

from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def fIndex():
  # VULN: Exposición de variables de entorno
  return f"<pre>{os.environ}</pre>"

if __name__ == "__main__":
  # Debug + información sensible
  app.run(host="0.0.0.0", port=25005, debug=True)
