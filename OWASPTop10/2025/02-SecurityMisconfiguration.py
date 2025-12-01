#!/usr/bin/env python3
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
  app.run(host="0.0.0.0", port=5002, debug=True)
