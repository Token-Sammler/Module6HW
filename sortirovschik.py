import os
import shutil
import sys
from pathlib import Path

#IMAGE = ('JPEG', 'PNG', 'JPG', 'SVG')
#VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
#DOCUMENT = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
#MUSIC = ('MP3', 'OGG', 'WAV', 'AMR')
#ARCHIVE = ('ZIP', 'GZ', 'TAR')
#OTHER = ()
#ALL = (IMAGE, VIDEO, DOCUMENT, MUSIC, ARCHIVE, OTHER)
FOLDERS = ('Image', 'Video', 'Document', 'Music', 'Archive', 'Other')

def normalize(text):
    translit = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye',
                'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L',
                'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
                'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ю': 'Yu',
                'Я': 'Ya', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e',
                'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
                'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ю': 'iu', 'я': 'ia'}
    result = ''
    for char in text:
        # перевірка, чи символ - літера латинського алфавіту чи цифра
        if char.isdecimal() or char.isalpha():
            # символ залишається як є
            result += char
        else:
            # символ транслітерується, якщо можливо
            if char in translit:
                result += translit[char]
            else:
                # символ замінюється на '_'
                result += '_'
    return result

def clean_empty_folders(path):
    path = Path(path)
    print(path)
    for folder in path.iterdir():
        if folder.is_dir() and not any(folder.iterdir()) and folder.name not in FOLDERS:
            print(f"Deleting empty folder: {folder}")
            folder.rmdir()

def create_folders(directory):
    for dir in FOLDERS:
        create_dir = os.path.join(directory, dir)
        os.makedirs(create_dir, exist_ok=True)

destination = []

def organize_files(directory):
    destination.append(directory)
    first_dest = destination[0]
    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name in FOLDERS:
            continue
        if os.path.isdir(file_path):
            clean_empty_folders(file_path)
            organize_files(file_path)

        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            normalized_name = normalize(os.path.splitext(file_name)[0])
            full_name = normalized_name + file_extension

            if file_extension in ('.jpg', '.jpeg', '.png', '.gif'):
                final_dest = os.path.join(first_dest, 'Image', full_name)
                os.replace(file_path, final_dest)
            elif file_extension in ('.doc', '.docx', '.pdf', '.txt'):
                final_dest = os.path.join(first_dest, 'Document', full_name)               
                os.replace(file_path, final_dest)
            elif file_extension in ('.mp3', '.wav', '.flac'):
                final_dest = os.path.join(first_dest, 'Music', full_name)              
                os.replace(file_path, final_dest)
            elif file_extension in ('.mp4', '.avi', '.mov', '.mkv'):
                final_dest = os.path.join(first_dest, 'Video', full_name)            
                os.replace(file_path, final_dest)
            elif file_extension in ('.zip', '.rar'):
                final_dest = os.path.join(first_dest, 'Archive', full_name)            
                shutil.unpack_archive(file_path, final_dest)
                os.remove(file_path)
            else:
                final_dest = os.path.join(first_dest, 'Other', full_name)           
                os.replace(file_path, final_dest)
    
    clean_empty_folders(destination[-1])
    del destination[-1]
#organize_files(r'C:/Users/Максим Степанец/Desktop/Розібрати')    
def main(directory):
    create_folders(directory)
    organize_files(directory)
 
sort = input('Введіть шлях до теки в якій необхідно відсортувати файли: ')
sort_r = r'' + sort
main((sort_r))
