#!/usr/bin/env python3

import subprocess
import shutil
from flask import Flask, jsonify, request

app = Flask(__name__)

def run_command(command_list, timeout=180):
    """Running a command securely and correctly finding the executable path."""
    try:
        # Resolve the executable path (handles venv binaries if PATH is set correctly)
        executable = shutil.which(command_list[0])
        if not executable:
             return None, f"Executable {command_list[0]} not found in PATH."

        command_list[0] = executable
        
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return output, None
    except Exception as e:
        return None, str(e)

@app.route("/holehe/<email>")
def holehe_check(email):
    output, error = run_command(["holehe", email, "--only-used"])
    if error:
         return jsonify({"error": error}), 500
    return jsonify({"output": output})

@app.route("/maigret/<user>")
def maigret_check(user):
    # Native call: maigret <user>
    output, error = run_command(["maigret", user])
    if error:
         return jsonify({"error": error}), 500
    return jsonify({"output": output})

@app.route("/sherlock/<user>")
def sherlock_check(user):
    # Native call: sherlock <user>
    output, error = run_command(["sherlock", user])
    if error:
         return jsonify({"error": error}), 500
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
