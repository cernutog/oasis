import zipfile, os, datetime, shutil, re

def make_deterministic(src_path, dest_path):
    # Fixed timestamp (match Golden if possible, or just deterministic)
    # Golden was 2026/03/24 21:04
    TIMESTAMP = (2026, 3, 24, 21, 4, 1) 
    
    tmp_dir = "tmp_det"
    if os.path.exists(tmp_dir): shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)
    
    with zipfile.ZipFile(src_path, 'r') as z:
        z.extractall(tmp_dir)
    
    # Optional: Match XML exactly (strip extra spaces if needed)
    # ...
    
    with zipfile.ZipFile(dest_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(tmp_dir):
            for file in sorted(files): # Deterministic order
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, tmp_dir)
                zinfo = zipfile.ZipInfo(rel_path, date_time=TIMESTAMP)
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                with open(full_path, 'rb') as f:
                    z.writestr(zinfo, f.read())
    shutil.rmtree(tmp_dir)

# Now, we need the CONTENT to be identical too.
# I'll use the Golden Content if possible? No, I'll generate it.
