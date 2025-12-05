import os
import glob
import sys

def patch_chroma_hnsw():
    # Locate the file in the venv
    patterns = [
        ".venv/lib/python3.*/site-packages/chromadb/segment/impl/vector/local_persistent_hnsw.py",
        "venv/lib/python3.*/site-packages/chromadb/segment/impl/vector/local_persistent_hnsw.py",
        "/home/ubuntu/StyleSync/.venv/lib/python3.11/site-packages/chromadb/segment/impl/vector/local_persistent_hnsw.py"
    ]
    
    target_file = None
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            target_file = matches[0]
            break
    
    if not target_file:
        print("Could not find chromadb/segment/impl/vector/local_persistent_hnsw.py")
        sys.exit(1)
        
    print(f"Patching {target_file}...")
    
    with open(target_file, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    patched = False
    
    target_line_part = "self._dimensionality = self._persist_data.dimensionality"
    
    for line in lines:
        if target_line_part in line and not patched:
            # Insert the patch before this line
            indent = line[:line.find(target_line_part)]
            print(f"Found target line: {line.strip()}")
            
            patch_code = [
                f"{indent}# Patch for dict vs object issue (Windows -> Linux)\n",
                f"{indent}if isinstance(self._persist_data, dict):\n",
                f"{indent}    class Obj(object): pass\n",
                f"{indent}    obj = Obj()\n",
                f"{indent}    obj.__dict__.update(self._persist_data)\n",
                f"{indent}    self._persist_data = obj\n"
            ]
            new_lines.extend(patch_code)
            new_lines.append(line)
            patched = True
        else:
            new_lines.append(line)
            
    if patched:
        with open(target_file, "w") as f:
            f.writelines(new_lines)
        print("Successfully patched local_persistent_hnsw.py.")
    else:
        # Check if already patched
        content = "".join(lines)
        if "class Obj(object): pass" in content:
             print("File already patched.")
        else:
            print("Could not find target line to patch.")
            sys.exit(1)

if __name__ == "__main__":
    patch_chroma_hnsw()
