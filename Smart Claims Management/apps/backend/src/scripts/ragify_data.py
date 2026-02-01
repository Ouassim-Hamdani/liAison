import os
from services.ragify import RagifyPipe

if __name__ == "__main__":
    ragify = RagifyPipe()
    FOLDER = "C:\\Projects\\Hack in saclay\\Repo\\data\\files"
    for category_folder in os.listdir(FOLDER):
        folder_path = os.path.join(FOLDER, category_folder)
        
        print(os.listdir(folder_path))
        if category_folder!="health":
            continue
        for file in os.listdir(folder_path):
            print(f"Ragifying file: {file} in category: {category_folder}")
            try:
                ragify(os.path.join(folder_path, file), category_folder)
            except Exception as e:
                print(f"Error ragifying file {file}: {e}")
                continue #04-2023_CG VALANT NI_AN_EVIN_323 V2.pdf