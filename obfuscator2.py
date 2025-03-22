import base64
import sys
import os

# Simple XOR cipher for an extra layer
def xor(text, key=42):
    return ''.join(chr(ord(c) ^ key) for c in text)

# Loader template for decryption and execution
loader_template = """
import base64
def x(t, k=42):
    return ''.join(chr(ord(c) ^ k) for c in t)
exec(x(base64.b64decode('{}').decode()))
"""

def obfuscate_file(input_file):
    # Step 1: Read and encrypt the original script
    with open(input_file, "r") as f:
        original_code = f.read()

    # First encryption: XOR then Base64
    xor_encoded = xor(original_code)
    b64_encoded = base64.b64encode(xor_encoded.encode()).decode()
    first_encrypted = loader_template.format(b64_encoded)

    # Step 2: Add a few lines of dummy code followed by empty lines
    dummy_lines = [
        "print('Initializing...')",
        "print('Loading modules...')",
        "print('Checking system...')",
        "print('Verifying integrity...')",
        "print('Starting process...')"
    ]  # 5 lines of dummy code
    dummy_code = "\n".join(dummy_lines)
    
    # Calculate how many empty lines are needed to reach line 100
    # 5 dummy lines + 1 for the encrypted line = 6, so 94 empty lines
    empty_lines = "\n" * 94
    combined_code = f"{dummy_code}{empty_lines}{first_encrypted}"

    # Step 3: Encrypt the entire thing again
    xor_encoded_combined = xor(combined_code)
    b64_encoded_combined = base64.b64encode(xor_encoded_combined.encode()).decode()
    final_encrypted = loader_template.format(b64_encoded_combined)

    # Generate output filename
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}-encrypted{ext}"

    # Write to the output file
    with open(output_file, "w") as f:
        f.write(final_encrypted)

if __name__ == "__main__":
    # Check if an input file is provided
    if len(sys.argv) < 2:
        print("Usage: python obfuscator.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    obfuscate_file(input_file)
