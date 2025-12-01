#!/usr/bin/env python3

from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def fIndex():
  # VULN: Exposición de variables de entorno
  return f"<pre>{os.environ}</pre>"

if __name__ == "__main__":
  # Debug + información sensible
  app.run(host="0.0.0.0", port=5005, debug=True)
