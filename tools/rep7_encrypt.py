import base64

text="WEARETHELAST"

# Reverse

step1=text[::-1]

# Caesar

step2=""

for c in step1:

    step2+=chr(ord(c)+3)

# Hex

step3=step2.encode().hex()

# Base64

step4=base64.b64encode(step3.encode()).decode()

# Reverse Again

cipher=step4[::-1]

print(cipher)
