#!/usr/bin/env python3

from flask import Flask, request
import importlib.util, os

app = Flask(__name__)
cPlugins = "plugins"

os.makedirs(cPlugins, exist_ok=True)

@app.route("/upload", methods=["GET","POST"])
def fUpload():
  if request.method == "GET":
    return """
    <form method='POST' enctype='multipart/form-data'>
      Plugin (.py): <input type='file' name='f'><br>
      <input type='submit'>
    </form>
    """
  vF = request.files["f"]
  vPath = os.path.join(cPlugins, vF.filename)
  vF.save(vPath)

  # VULN: Ejecuta código Python subido por el usuario
  spec = importlib.util.spec_from_file_location("plugin", vPath)
  plugin = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(plugin)

  return "Plugin ejecutado"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=25008, debug=True)
