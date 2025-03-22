import base64
import sys
import os

# Simple XOR cipher for an extra layer
def xor(text, key=42):
    return ''.join(chr(ord(c) ^ key) for c in text)

# Loader template for the obfuscated output file
loader_template = """
import base64
def x(t, k=42):
    return ''.join(chr(ord(c) ^ k) for c in t)
exec(x(base64.b64decode('{}').decode()))
"""

def obfuscate_file(input_file):
    try:
        # Step 1: Read and encrypt the original script
        with open(input_file, "r") as f:
            original_code = f.read()

        # First encryption: XOR then Base64
        xor_encoded = xor(original_code)
        b64_encoded = base64.b64encode(xor_encoded.encode()).decode()
        first_encrypted = loader_template.format(b64_encoded)

        # Step 2: Add a few lines of dummy code that looks functional but doesn't execute
        dummy_lines = [
            "def initialize_system():",
            "    config = {'mode': 'secure', 'level': 5}",
            "    if False:  # This block never executes",
            "        settings = config.get('mode')",
            "        for i in range(config['level']):",
            "            temp = i * 42",
            "            settings += str(temp)"
        ]  # 7 lines of realistic-looking but non-executing code
        
        dummy_code = "\n".join(dummy_lines)
        
        # Add 100 empty lines
        empty_lines = "\n" * 100
        
        # Combine dummy code, empty lines, and first encrypted code
        combined_code = f"{dummy_code}{empty_lines}{first_encrypted}"

        # Step 3: Encrypt the entire thing again
        xor_encoded_combined = xor(combined_code)
        b64_encoded_combined = base64.b64encode(xor_encoded_combined.encode()).decode()
        final_encrypted = loader_template.format(b64_encoded_combined)

        # Generate the output filename
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}-encrypted{ext}"

        # Write to the output file
        with open(output_file, "w") as f:
            f.write(final_encrypted)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    # Check if an input file is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python obfuscator_v2.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    obfuscate_file(input_file)
