import os
import shutil
import random

# Postavljanje putanja ka direktorijumima
current_directory = os.path.dirname(__file__)
directory_DataSetDL = os.path.join(current_directory, "DataSetDL")
directory_png = os.path.join(current_directory, "ALLPNG")
directory_txtDL = os.path.join(current_directory, "ALLTXTDL")
img_testdl = os.path.join(directory_DataSetDL, "images", "test")
img_validdl = os.path.join(directory_DataSetDL, "images", "valid")
img_traindl = os.path.join(directory_DataSetDL, "images", "train")
label_testdl = os.path.join(directory_DataSetDL, "labels", "test")
label_validdl = os.path.join(directory_DataSetDL, "labels", "valid")
label_traindl = os.path.join(directory_DataSetDL, "labels", "train")

directory_DataSetSL = os.path.join(current_directory, "DataSetSL")
directory_txtSL = os.path.join(current_directory, "ALLTXTSL")
img_testsl = os.path.join(directory_DataSetSL, "images", "test")
img_validsl = os.path.join(directory_DataSetSL, "images", "valid")
img_trainsl = os.path.join(directory_DataSetSL, "images", "train")
label_testsl = os.path.join(directory_DataSetSL, "labels", "test")
label_validsl = os.path.join(directory_DataSetSL, "labels", "valid")
label_trainsl = os.path.join(directory_DataSetSL, "labels", "train")


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
    for img_dir in [img_traindl, img_validdl, img_testdl, img_trainsl, img_validsl, img_testsl]:
        os.makedirs(img_dir, exist_ok=True)
    for label_dir in [label_traindl, label_validdl, label_testdl, label_trainsl, label_validsl, label_testsl]:
        os.makedirs(label_dir, exist_ok=True)


create_directories()


def copy_files(source_directory, txt_directory, img_train_directory, img_valid_directory, img_test_directory,
               label_train_directory, label_valid_directory, label_test_directory):
    # Učitavanje imena datoteka iz oba foldera
    files_allpng = set(os.listdir(source_directory))
    files_alltxt = set(os.listdir(txt_directory))

    # Pronalaženje zajedničkih datoteka (bez ekstenzija)
    common_files = {os.path.splitext(file)[0] for file in files_allpng}.intersection(
        {os.path.splitext(file)[0] for file in files_alltxt})

    # Pretvaranje zajedničkih datoteka u listu i mešanje
    common_files = list(common_files)
    random.shuffle(common_files)

    # Izračunavanje broja datoteka za svaki folder
    total_files = len(common_files)
    num_70 = int(0.7 * total_files)
    num_20 = int(0.2 * total_files)
    num_10 = total_files - num_70 - num_20

    # Razdvajanje datoteka na 70%, 20%, i 10%
    files_70 = common_files[:num_70]
    files_20 = common_files[num_70:num_70 + num_20]
    files_10 = common_files[num_70 + num_20:]

    # Kopiranje datoteka u odgovarajuće foldere
    for file in files_70:
        # Kopiranje slika
        src_png = os.path.join(source_directory, f"{file}.png")
        dst_png_train = os.path.join(img_train_directory, f"{file}.png")
        if os.path.exists(src_png):
            shutil.copy(src_png, dst_png_train)
        else:
            print(f"Slika nije pronađena: {src_png}")

        # Kopiranje tekstualnih datoteka
        src_txt = os.path.join(txt_directory, f"{file}.txt")
        dst_txt_train = os.path.join(label_train_directory, f"{file}.txt")
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt_train)
        else:
            print(f"Tekstualna datoteka nije pronađena: {src_txt}")

    for file in files_20:
        # Kopiranje slika
        src_png = os.path.join(source_directory, f"{file}.png")
        dst_png_valid = os.path.join(img_valid_directory, f"{file}.png")
        if os.path.exists(src_png):
            shutil.copy(src_png, dst_png_valid)
        else:
            print(f"Slika nije pronađena: {src_png}")

        # Kopiranje tekstualnih datoteka
        src_txt = os.path.join(txt_directory, f"{file}.txt")
        dst_txt_valid = os.path.join(label_valid_directory, f"{file}.txt")
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt_valid)
        else:
            print(f"Tekstualna datoteka nije pronađena: {src_txt}")

    for file in files_10:
        # Kopiranje slika
        src_png = os.path.join(source_directory, f"{file}.png")
        dst_png_test = os.path.join(img_test_directory, f"{file}.png")
        if os.path.exists(src_png):
            shutil.copy(src_png, dst_png_test)
        else:
            print(f"Slika nije pronađena: {src_png}")

        # Kopiranje tekstualnih datoteka
        src_txt = os.path.join(txt_directory, f"{file}.txt")
        dst_txt_test = os.path.join(label_test_directory, f"{file}.txt")
        if os.path.exists(src_txt):
            shutil.copy(src_txt, dst_txt_test)
        else:
            print(f"Tekstualna datoteka nije pronađena: {src_txt}")

    print("Datoteke su uspešno kopirane.")


def main():
    # Brisanje postojećih datoteka u tren, valid, i test direktorijumima
    clear_directory(img_validsl)
    clear_directory(img_trainsl)
    clear_directory(img_testsl)
    clear_directory(label_validsl)
    clear_directory(label_trainsl)
    clear_directory(label_testsl)
    clear_directory(img_validdl)
    clear_directory(img_traindl)
    clear_directory(img_testdl)
    clear_directory(label_validdl)
    clear_directory(label_traindl)
    clear_directory(label_testdl)
    print("Svi fajlovi iz navedenih foldera su izbrisani.")

    # Kopiranje datoteka za DataSetDL
    copy_files(directory_png, directory_txtDL, img_traindl, img_validdl, img_testdl, label_traindl, label_validdl,
               label_testdl)

    # Kopiranje datoteka za DataSetSL
    copy_files(directory_png, directory_txtSL, img_trainsl, img_validsl, img_testsl, label_trainsl, label_validsl,
               label_testsl)

    # Ispis broja datoteka u svakom direktorijumu
    num_files = count_files(label_trainsl)
    print(f"Label train SL: {num_files}")
    num_files = count_files(label_traindl)
    print(f"Label train DL: {num_files}")
    num_files = count_files(img_trainsl)
    print(f"Img train SL: {num_files}")
    num_files = count_files(img_traindl)
    print(f"Img train DL: {num_files}")

    num_files = count_files(img_validdl)
    print(f"Img valid DL: {num_files}")
    num_files = count_files(img_validsl)
    print(f"Img valid SL: {num_files}")

    num_files = count_files(img_testdl)
    print(f"Img test DL: {num_files}")
    num_files = count_files(img_testsl)
    print(f"Img test SL: {num_files}")

    num_files = count_files(label_validsl)
    print(f"Label valid SL: {num_files}")
    num_files = count_files(label_validdl)
    print(f"Label valid DL: {num_files}")

    num_files = count_files(label_testsl)
    print(f"Label test SL: {num_files}")
    num_files = count_files(label_testdl)
    print(f"Label test DL: {num_files}")


if __name__ == "__main__":
    main()
