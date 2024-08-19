import os
import shutil
import random

# Postavljanje putanja ka direktorijumima
current_directory = os.path.dirname(__file__)
directory_DataSetDL = os.path.join(current_directory, "DataSetDL")
directory_png = os.path.join(current_directory, "ALLPNG")
directory_txtDL = os.path.join(current_directory, "ALLTXTDL")
img_validdl = os.path.join(directory_DataSetDL, "images", "valid")
img_traindl = os.path.join(current_directory, "DataSetDL/images/train")  # corrected this path
label_validdl = os.path.join(directory_DataSetDL, "labels", "valid")
label_traindl = os.path.join(current_directory, "DataSetDL/labels/train")  # corrected this path

directory_DataSetSL = os.path.join(current_directory, "DataSetSL")
directory_txtSL = os.path.join(current_directory, "ALLTXTSL")
img_validsl = os.path.join(directory_DataSetSL, "images", "valid")
img_trainsl = os.path.join(current_directory, "DataSetSL/images/train")  # corrected this path
label_validsl = os.path.join(directory_DataSetSL, "labels", "valid")
label_trainsl = os.path.join(current_directory, "DataSetSL/labels/train")  # corrected this path

def clear_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Brisanje fajla
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Brisanje direktorijuma
            except Exception as e:
                print(f'Greška prilikom brisanja {file_path}. Razlog: {e}')
                
def count_files(directory):
    return sum(1 for entry in os.scandir(directory) if entry.is_file())

# Kreiranje potrebnih direktorijuma ako ne postoje
def create_directories():
    for img_dir in [img_traindl, img_validdl, img_trainsl, img_validsl]:
        os.makedirs(img_dir, exist_ok=True)
    for label_dir in [label_traindl, label_validdl, label_trainsl, label_validsl]:
        os.makedirs(label_dir, exist_ok=True)

create_directories()

def copy_files(source_directory, txt_directory, img_train_directory, img_valid_directory, label_train_directory, label_valid_directory):
    # Učitavanje imena datoteka iz oba foldera
    files_allpng = set(os.listdir(source_directory))
    files_alltxt = set(os.listdir(txt_directory))

    print(f"Datoteke u {source_directory}: {files_allpng}")
    print(f"Datoteke u {txt_directory}: {files_alltxt}")

    # Pronalaženje zajedničkih datoteka (bez ekstenzija)
    common_files = {os.path.splitext(file)[0] for file in files_allpng}.intersection(
                    {os.path.splitext(file)[0] for file in files_alltxt})

    print(f"Zajedničke datoteke: {common_files}")

    # Pretvaranje zajedničkih datoteka u listu i mešanje
    common_files = list(common_files)
    random.shuffle(common_files)

    # Izračunavanje broja datoteka za svaki folder
    total_files = len(common_files)
    num_80 = int(0.8 * total_files)
    num_20 = total_files - num_80

    print(f"Ukupan broj datoteka: {total_files}")
    print(f"Broj datoteka za train: {num_80}")
    print(f"Broj datoteka za valid: {num_20}")

    # Razdvajanje datoteka na 80% i 20%
    files_80 = common_files[:num_80]
    files_20 = common_files[num_80:]

    # Kopiranje datoteka u odgovarajuće foldere
    for file in files_80:
        # Kopiranje slika
        src_png = os.path.join(source_directory, f"{file}.png")
        dst_png_train = os.path.join(img_train_directory, f"{file}.png")
        if os.path.exists(src_png):
            try:
                shutil.copy2(src_png, dst_png_train)
                print(f"Slika kopirana: {src_png} -> {dst_png_train}")
            except Exception as e:
                print(f"Greška prilikom kopiranja slike {src_png} -> {dst_png_train}. Razlog: {e}")
        else:
            print(f"Slika nije pronađena: {src_png}")

        # Kopiranje tekstualnih datoteka
        src_txt = os.path.join(txt_directory, f"{file}.txt")
        dst_txt_train = os.path.join(label_train_directory, f"{file}.txt")
        if os.path.exists(src_txt):
            try:
                shutil.copy2(src_txt, dst_txt_train)
                print(f"Tekstualna datoteka kopirana: {src_txt} -> {dst_txt_train}")
            except Exception as e:
                print(f"Greška prilikom kopiranja tekstualne datoteke {src_txt} -> {dst_txt_train}. Razlog: {e}")
        else:
            print(f"Tekstualna datoteka nije pronađena: {src_txt}")

    for file in files_20:
        # Kopiranje slika
        src_png = os.path.join(source_directory, f"{file}.png")
        dst_png_valid = os.path.join(img_valid_directory, f"{file}.png")
        if os.path.exists(src_png):
            try:
                shutil.copy2(src_png, dst_png_valid)
                print(f"Slika kopirana: {src_png} -> {dst_png_valid}")
            except Exception as e:
                print(f"Greška prilikom kopiranja slike {src_png} -> {dst_png_valid}. Razlog: {e}")
        else:
            print(f"Slika nije pronađena: {src_png}")

        # Kopiranje tekstualnih datoteka
        src_txt = os.path.join(txt_directory, f"{file}.txt")
        dst_txt_valid = os.path.join(label_valid_directory, f"{file}.txt")
        if os.path.exists(src_txt):
            try:
                shutil.copy2(src_txt, dst_txt_valid)
                print(f"Tekstualna datoteka kopirana: {src_txt} -> {dst_txt_valid}")
            except Exception as e:
                print(f"Greška prilikom kopiranja tekstualne datoteke {src_txt} -> {dst_txt_valid}. Razlog: {e}")
        else:
            print(f"Tekstualna datoteka nije pronađena: {src_txt}")

    print("Datoteke su uspešno kopirane.")

def main():
    clear_directory(img_validsl)
    clear_directory(img_trainsl)
    clear_directory(label_validsl)
    clear_directory(label_trainsl)
    clear_directory(img_validdl)
    clear_directory(img_traindl)
    clear_directory(label_validdl)
    clear_directory(label_traindl)
    print("Svi fajlovi iz navedenih foldera su izbrisani.")
    
    # Kopiranje datoteka za DataSetDL
    copy_files(directory_png, directory_txtDL, img_traindl, img_validdl, label_traindl, label_validdl)
    
    # Kopiranje datoteka za DataSetSL
    copy_files(directory_png, directory_txtSL, img_trainsl, img_validsl, label_trainsl, label_validsl)
    
    num_files = count_files(label_trainsl)
    print(f"Label train SL: {num_files}")
    num_files = count_files(label_traindl)
    print(f"Label train DL: {num_files}")
    num_files = count_files(img_trainsl)
    print(f"img train SL: {num_files}")
    num_files = count_files(img_traindl)
    print(f"img train DL: {num_files}")
    
    num_files = count_files(img_validsl)
    print(f"img valid SL: {num_files}")
    num_files = count_files(img_validdl)
    print(f"img valid DL: {num_files}")
    
    num_files = count_files(label_validsl)
    print(f"label valid SL: {num_files}")
    num_files = count_files(label_validdl)
    print(f"label valid DL: {num_files}")

if __name__ == "__main__":
    main()
