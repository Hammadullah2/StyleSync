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
        lines = f.readlines()
        
    new_lines = []
    patched = False
    already_patched = False
    
    for line in lines:
        new_lines.append(line)
        if "def _decode_seq_id" in line:
            # Check if next line is already our patch
            # We need to be careful with reading the next line in the loop, 
            # but since we are appending, we can just set a flag to check the next lines?
            # Simpler: just check if the file content already has the patch string
            pass

    # Re-read content to check for existence
    content = "".join(lines)
    if "if isinstance(seq_id_bytes, int):" in content:
        print("File already patched.")
        return

    # Apply patch
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if "def _decode_seq_id" in line:
            print(f"Found function at: {line.strip()}")
            new_lines.append("    if isinstance(seq_id_bytes, int):\n")
            new_lines.append("        return seq_id_bytes\n")
            patched = True
            
    if patched:
        with open(target_file, "w") as f:
            f.writelines(new_lines)
        print("Successfully patched _decode_seq_id.")
    else:
        print("Could not find function definition 'def _decode_seq_id' in file.")
        # Print first few lines to debug
        print("First 20 lines of file:")
        for i, line in enumerate(lines[:20]):
            print(f"{i}: {line.strip()}")
        sys.exit(1)

if __name__ == "__main__":
    patch_chroma()
