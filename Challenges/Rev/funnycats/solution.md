Identify that it's actually a PyInstaller program, pycdc, deobfs source code. Realise that it uses a variant of stego to store a generated key that's been RSA encrypted which is used by blowfish (ala WannaCryptor), with the RSA pem stored in cat 1, the encrypted key stored in cat 2 and the blowfish encrypted contents of passwd stored in cat 3.

Flag: `blahaj{STEGANOKITTIES}`