#!/usr/bin/env python3

import subprocess
from flask import Flask, jsonify, request
from importlib import import_module

app = Flask(__name__)

@app.route("/holehe/<email>")
def holehe_check(email):
    try:
        result = subprocess.run(
            ["holehe", email, "--only-used"],
            capture_output=True,
            text=True,
            timeout=180
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/maigret/<user>")
def maigret_check(user):
    try:
        result = subprocess.run(
            ["docker", "run", "-i", "soxoj/maigret", user],
            capture_output=True,
            text=True,
            timeout=180
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sherlock/<user>")
def sherlock_check(user):
    try:
        result = subprocess.run(
            ["docker", "run", "-i", "sherlock/sherlock", user],
            capture_output=True,
            text=True,
            timeout=180  # Aumenta el timeout aquí
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
