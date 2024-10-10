from pathlib import Path
import shutil


DOWNLOADS_FOLDER = Path.home() / "Downloads"
TARGET_FOLDER = Path.home() / "Desktop" / "Organized"


FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
}

def create_folders():
    
    for folder in FILE_CATEGORIES.keys():
        folder_path = TARGET_FOLDER / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"Created folder: {folder_path}")

def move_files():
    
    print(f"Scanning {DOWNLOADS_FOLDER} for files...")

    # List all files in the Downloads folder
    for file_path in DOWNLOADS_FOLDER.iterdir():
        if file_path.is_file():
            file_extension = file_path.suffix.lower()
            print(f"Found file: {file_path.name}, extension: {file_extension}")

            # Move the file to the corresponding folder
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if file_extension in extensions:
                    target_path = TARGET_FOLDER / category / file_path.name
                    shutil.move(str(file_path), str(target_path))
                    print(f"Moved {file_path.name} to {category}")
                    moved = True
                    break

            # If no category matches, move it to 'Other'
            if not moved:
                other_folder = TARGET_FOLDER / "Other"
                if not other_folder.exists():
                    other_folder.mkdir(parents=True, exist_ok=True)
                    print(f"Created 'Other' folder: {other_folder}")
                target_path = other_folder / file_path.name
                shutil.move(str(file_path), str(target_path))
                print(f"Moved {file_path.name} to Other")
        else:
            print(f"Skipping directory: {file_path.name}")

if __name__ == "__main__":
    create_folders()  
    move_files()      