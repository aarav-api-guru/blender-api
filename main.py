from flask import Flask, request, send_file
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OUTPUT_FILE = "output.glb"

@app.route('/')
def home():
    return "✅ Blender API is running. Use /generate?shape=cube"

@app.route('/generate', methods=['GET'])
def generate():
    shape = request.args.get('shape', 'cube')
    allowed = ['cube', 'uv_sphere', 'cylinder']

    if shape not in allowed:
        return f"Invalid shape: {shape}", 400

    script = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_{shape}_add()
bpy.ops.export_scene.gltf(filepath=r'{OUTPUT_FILE}', export_format='GLB')
"""
    with open("gen.py", "w") as f:
        f.write(script)

    subprocess.run(["blender", "--background", "--python", "gen.py"])
    return send_file(OUTPUT_FILE, as_attachment=True, download_name=f"{shape}.glb")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)