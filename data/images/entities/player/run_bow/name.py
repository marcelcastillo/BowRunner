import os

# Folder containing your images
folder = "."   # "." = current directory; change if needed

for filename in os.listdir(folder):
    if filename.startswith("BR-run - ") and filename.endswith(".png"):
        # Strip the prefix
        new_name = filename.replace("BR-run - ", "")
        
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        
        print(f"Renaming: {filename} -> {new_name}")
        os.rename(old_path, new_path)

print("Done.")
