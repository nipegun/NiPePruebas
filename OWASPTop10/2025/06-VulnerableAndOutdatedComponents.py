#!/usr/bin/env python3
# Vulnerabilidad simulada: Vulnerable and Outdated Components. La página anuncia que la app usa
# una librería obsoleta (SuperLib 0.1) sin parchear. La debilidad es depender de componentes con
# fallos conocidos. Para explotarla, un atacante buscaría CVEs públicos de esa versión y lanzaría
# el exploit correspondiente contra el servicio o el entorno que lo usa.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def fIndex():
  return """
  <h1>Componentes vulnerables</h1>
  <p>Esta app usa una librería obsoleta y vulnerable (simulado).</p>
  <p>Version vulnerable: SuperLib 0.1</p>
  """

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25006, debug=True)
