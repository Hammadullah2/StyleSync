import os
import glob
import sys

def patch_chroma_final():
    # Locate the file
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
        print("Could not find local_persistent_hnsw.py")
        sys.exit(1)
        
    print(f"Patching {target_file}...")
    
    with open(target_file, "r") as f:
        lines = f.readlines()
        
    target_line_part = "self._dimensionality = self._persist_data.dimensionality"
    
    obj_patch_marker = "class Obj(object): pass"
    dim_patch_marker = "if self._dimensionality is None:"
    
    # Check current content
    content = "".join(lines)
    
    # Patch 1: Dict vs Object (Apply if missing)
    if obj_patch_marker not in content:
        print("Applying Dict vs Object patch...")
        temp_lines = []
        for line in lines:
            if target_line_part in line:
                indent = line[:line.find(target_line_part)]
                temp_lines.append(f"{indent}# Patch 1: Fix dict vs object\n")
                temp_lines.append(f"{indent}if isinstance(self._persist_data, dict):\n")
                temp_lines.append(f"{indent}    class Obj(object): pass\n")
                temp_lines.append(f"{indent}    obj = Obj()\n")
                temp_lines.append(f"{indent}    obj.__dict__.update(self._persist_data)\n")
                temp_lines.append(f"{indent}    self._persist_data = obj\n")
                temp_lines.append(line)
            else:
                temp_lines.append(line)
        lines = temp_lines
    else:
        print("Dict vs Object patch already present.")

    # Patch 2: None Dimensionality (Apply if missing)
    content = "".join(lines) # Update content check
    if dim_patch_marker not in content:
        print("Applying None Dimensionality patch...")
        temp_lines = []
        for line in lines:
            temp_lines.append(line)
            if target_line_part in line:
                indent = line[:line.find(target_line_part)]
                temp_lines.append(f"{indent}# Patch 2: Force dimensionality\n")
                temp_lines.append(f"{indent}if self._dimensionality is None:\n")
                temp_lines.append(f"{indent}    self._dimensionality = 512\n")
        lines = temp_lines
    else:
        print("None Dimensionality patch already present.")
        
    with open(target_file, "w") as f:
        f.writelines(lines)
    print("Patching complete.")

if __name__ == "__main__":
    patch_chroma_final()
