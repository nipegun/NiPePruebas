#!/usr/bin/env python3

from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/login")
def fLogin():
  vPass = request.args.get("p","")
  # VULN: Contraseña hardcodeada
  if vPass == "1234":
    return redirect("/panel?session=admin")
  return "Login incorrecto"

@app.route("/panel")
def fPanel():
  # VULN: Sesión manipulable desde URL
  vSession = request.args.get("session","guest")
  return f"<h1>Panel de usuario: {vSession}</h1>"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25007, debug=True)
