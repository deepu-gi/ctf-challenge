import base64

text = "WEARE"

print("Base64 :", base64.b64encode(text.encode()).decode())
print("Hex    :", text.encode().hex())
