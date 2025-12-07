#!/usr/bin/env python3

import subprocess
import shutil
import logging
import os
from flask import Flask, jsonify, request

# Configure logging
# Configure logging
log_file = os.path.join(os.path.dirname(__file__), 'social-api.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def run_command(command_list, timeout=180):
    """Ejecutar un comando de forma segura y encontrar correctamente la ruta del ejecutable."""
    try:
        cmd_name = command_list[0]
        # Resolver la ruta del ejecutable
        executable = shutil.which(cmd_name)
        if not executable:
             logger.error(f"Ejecutable {cmd_name} no encontrado en el PATH.")
             return None, f"Ejecutable {cmd_name} no encontrado en el PATH."

        command_list[0] = executable
        logger.info(f"Ejecutando comando: {' '.join(command_list)}")
        
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            logger.info(f"Ejecución del comando {cmd_name} exitosa.")
            return result.stdout, None
        else:
            logger.warning(f"El comando {cmd_name} falló con código de retorno {result.returncode}.")
            logger.debug(f"Stderr: {result.stderr}")
            return result.stdout, result.stderr

    except Exception as e:
        logger.exception(f"Ocurrió una excepción al ejecutar {command_list}: {str(e)}")
        return None, str(e)

@app.route("/holehe/<email>")
def holehe_check(email):
    logger.info(f"Recibida petición holehe para: {email}")
    output, error = run_command(["holehe", email, "--only-used"])
    if error:
         return jsonify({"error": error}), 500
    return jsonify({"output": output})

@app.route("/maigret/<user>")
def maigret_check(user):
    logger.info(f"Recibida petición maigret para: {user}")
    output, error = run_command(["maigret", user])
    if error:
         return jsonify({"error": error}), 500
    return jsonify({"output": output})

@app.route("/sherlock/<user>")
def sherlock_check(user):
    logger.info(f"Recibida petición sherlock para: {user}")
    output, error = run_command(["sherlock", user])
    if error:
         return jsonify({"error": error}), 500
    return jsonify({"output": output})

if __name__ == "__main__":
    host = os.environ.get("SOCIAL_API_HOST", "127.0.0.1")
    port = int(os.environ.get("SOCIAL_API_PORT", 8000))
    debug = os.environ.get("SOCIAL_API_DEBUG", "False").lower() == "true"
    
    logger.info(f"Iniciando Social API en {host}:{port}")
    app.run(host=host, port=port, debug=debug)
