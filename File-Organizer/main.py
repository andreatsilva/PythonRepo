from pathlib import Path
import shutil
import ctypes



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
    file_count = 0
    # List all files in the Downloads folder
    for file_path in DOWNLOADS_FOLDER.iterdir():
        if file_path.is_file():
            file_count += 1
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

    if file_count == 0:
        print("0 files found.")

def is_recycle_bin_empty():
    """Check if the Recycle Bin is empty."""
    num_items = ctypes.c_uint(0)
    result = ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(num_items))
    return num_items.value == 0

def clean_recycle_bin():
    if is_recycle_bin_empty():
        print("Recycle Bin is already empty.")
    else:
        answer = input("Do you want to empty the Recycle Bin?")
        if answer == "y":
        # Constants for Recycle Bin cleanup (SHERB_NOCONFIRMATION disables confirmation dialog)
            SHERB_NOCONFIRMATION = 0x00000001
            SHERB_NOPROGRESSUI = 0x00000002
            SHERB_NOSOUND = 0x00000004

            # Call Windows API to empty Recycle Bin
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND)
            
            print("Recycle Bin has been emptied.")
        else:
            print("Recycle Bin was not emptied.")

if __name__ == "__main__":
    create_folders()  
    move_files()
    clean_recycle_bin()