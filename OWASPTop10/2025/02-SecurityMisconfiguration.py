#!/usr/bin/env python3
# Vulnerabilidad simulada: Security Misconfiguration. El servidor corre con debug habilitado,
# lo que expone información sensible y rutas públicas como /static/passwords.txt. La
# vulnerabilidad surge por configuraciones inseguras en producción. Para explotarla, basta con
# navegar a la raíz para ver el listado filtrado o provocar errores y revisar el traceback de
# Flask en el navegador.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def fIndex():
  return """
  <h1>Misconfiguration</h1>
  <p>Debug activo, exposición de info sensible y listado simulado:</p>
  <pre>
  /static/
    passwords.txt
    config_backup.zip
  </pre>
  """

if __name__ == "__main__":
  # VULN: Debug activo en producción
  app.run(host="0.0.0.0", port=25002, debug=True)
