from flask import Flask, request, jsonify, send_from_directory
import yaml
import base64
import json
import os
import zlib
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.htm')

@app.route('/convert_to_yaml', methods=['POST'])
def convert_to_yaml():
    try:
        # Get JSON data from the request
        json_data = request.json
        # Convert JSON to YAML
        yaml_data = yaml.dump(json_data)
        # Encode YAML to Base64
        compressed_yaml = zlib.compress(yaml_data.encode())
        # Encode compressed YAML to Base64
        base64_yaml = base64.b64encode(compressed_yaml).decode()
        return jsonify({"zlib_yaml": base64_yaml}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/convert_to_json', methods=['POST'])
def convert_to_json():
    try:
        # Get Base64 YAML data from the request
        base64_yaml = request.json.get('zlib_yaml')
        # Decode Base64 to compressed YAML
        compressed_yaml = base64.b64decode(base64_yaml)
        # Decompress YAML data using zlib
        yaml_data = zlib.decompress(compressed_yaml).decode()
        # Convert YAML to JSON
        json_data = yaml.load(yaml_data, Loader = yaml.Loader)
        return jsonify(json_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)