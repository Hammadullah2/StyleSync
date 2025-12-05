import os
import glob
import sys

def patch_chroma():
    # Locate the file in the venv
    # We look for .venv relative to current dir, or in standard locations
    patterns = [
        ".venv/lib/python3.*/site-packages/chromadb/segment/impl/metadata/sqlite.py",
        "venv/lib/python3.*/site-packages/chromadb/segment/impl/metadata/sqlite.py",
        "/home/ubuntu/StyleSync/.venv/lib/python3.11/site-packages/chromadb/segment/impl/metadata/sqlite.py"
    ]
    
    target_file = None
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            target_file = matches[0]
            break
    
    if not target_file:
        print("Could not find chromadb/segment/impl/metadata/sqlite.py")
        print("Please ensure you are running this from the project root and the venv is set up.")
        sys.exit(1)
        
    print(f"Patching {target_file}...")
    
    with open(target_file, "r") as f:
        content = f.read()
        
    # The function to patch is _decode_seq_id
    # We want to handle the case where seq_id_bytes is already an int
    
    func_def = "def _decode_seq_id(seq_id_bytes):"
    patch_code = """
    if isinstance(seq_id_bytes, int):
        return seq_id_bytes"""
        
    if func_def in content:
        if "if isinstance(seq_id_bytes, int):" in content:
            print("File already patched.")
        else:
            new_content = content.replace(func_def, func_def + patch_code)
            with open(target_file, "w") as f:
                f.write(new_content)
            print("Successfully patched _decode_seq_id.")
    else:
        print("Could not find function definition to patch.")
        sys.exit(1)

if __name__ == "__main__":
    patch_chroma()
