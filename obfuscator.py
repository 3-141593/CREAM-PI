import base64

# Simple XOR cipher for an extra layer
def xor(text, key=42):
    return ''.join(chr(ord(c) ^ key) for c in text)

# Your original code to obfuscate (put it here or read from a file)
original_code = """
print("This is my secret Python script!")
for i in range(3):
    print(f"Number: {i}")
"""

# Step 1: XOR encode the code
xor_encoded = xor(original_code)

# Step 2: Base64 encode the XOR result
b64_encoded = base64.b64encode(xor_encoded.encode()).decode()

# Loader template that will be in the output file
loader_template = """
import base64
def x(t, k=42):
    return ''.join(chr(ord(c) ^ k) for c in t)
exec(x(base64.b64decode('{}').decode()))
"""

# Create the final obfuscated script
obfuscated_code = loader_template.format(b64_encoded)

# Write to a new file
with open("hidden.py", "w") as f:
    f.write(obfuscated_code)

print("Obfuscated file 'hidden.py' created! Run it with 'python hidden.py'.")