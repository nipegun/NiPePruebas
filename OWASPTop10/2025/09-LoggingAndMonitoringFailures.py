#!/usr/bin/env python3
# Vulnerabilidad simulada: Logging and Monitoring Failures. El flujo de login no registra intentos
# exitosos ni fallidos ni genera alertas, impidiendo detectar bruteforce o accesos indebidos. La
# debilidad es la ausencia de telemetría y monitoreo. Para explotarla, un atacante puede probar
# credenciales masivamente en /login?u=admin&p=... sin riesgo de ser detectado por logs.

from flask import Flask, request

app = Flask(__name__)

@app.route("/login")
def fLogin():
  # VULN: No logging, no detección
  u = request.args.get("u","")
  p = request.args.get("p","")

  if u == "admin" and p == "admin":
    return "OK"
  else:
    return "Fallo (sin logs, sin alertas)"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25009, debug=True)
