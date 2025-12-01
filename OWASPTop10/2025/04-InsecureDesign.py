#!/usr/bin/env python3
# Vulnerabilidad simulada: Insecure Design. El precio de la compra se recibe desde la URL y se
# usa directamente para completar el pago, sin reglas de negocio ni validaciones. La debilidad
# es confiar en datos del cliente para lógica crítica. Para explotarla, basta con invocar
# /buy?price=1 o incluso valores negativos para modificar el coste final.

from flask import Flask, request

app = Flask(__name__)

@app.route("/buy")
def fBuy():
  vPrecio = request.args.get("price","100")
  # VULN: El precio viene del cliente
  return f"<h1>Compra realizada por {vPrecio} euros</h1>"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25004, debug=True)
