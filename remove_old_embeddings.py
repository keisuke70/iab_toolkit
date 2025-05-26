import os

# Remove old embedding files to force regeneration
files_to_remove = [
    r"final\data\tier1_embeddings.npy",
    r"final\data\tier1_domains.json",
    r"data\tier1_embeddings.npy", 
    r"data\tier1_domains.json"
]

for file_path in files_to_remove:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed: {file_path}")
    else:
        print(f"Not found: {file_path}")

print("✅ Old embedding files removed - will regenerate with cleaner format")
