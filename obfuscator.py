import base64
import sys

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

def obfuscate_file(input_file, output_file="hidden.py"):
    try:
        # Read the original code from the input file
        with open(input_file, "r") as f:
            original_code = f.read()

        # Step 1: XOR encode the code
        xor_encoded = xor(original_code)

        # Step 2: Base64 encode the XOR result
        b64_encoded = base64.b64encode(xor_encoded.encode()).decode()

        # Create the obfuscated script using the loader template
        obfuscated_code = loader_template.format(b64_encoded)

        # Write to the output file
        with open(output_file, "w") as f:
            f.write(obfuscated_code)

        print(f"Obfuscated file '{output_file}' created! Run it with 'python {output_file}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    # Check if an input file is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python obfuscator.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    obfuscate_file(input_file)
