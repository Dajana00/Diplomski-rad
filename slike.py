import os
import numpy as np
import pydicom
import cv2

current_directory = os.path.dirname(__file__)
dicom_directory = os.path.join(current_directory, "AllDICOMs")
output_directory_png = os.path.join(current_directory, "ALLPNG")

if not os.path.exists(output_directory_png):
    os.makedirs(output_directory_png)



def save_dicom_as_png(dicom_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(dicom_folder):
        if filename.endswith('.dcm'):
            dicom_path = os.path.join(dicom_folder, filename)
            dicom_data = pydicom.dcmread(dicom_path)
            image = dicom_data.pixel_array
            image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
            image = image.astype(np.uint8)
            png_path = os.path.join(output_folder, filename.replace('.dcm', '.png'))
            cv2.imwrite(png_path, image)

dicom_folder = 'AllDICOMs'
output_folder = 'AllPNG'
save_dicom_as_png(dicom_folder, output_folder)

def main():
    for file in os.listdir(dicom_directory):
        if file.endswith('.dcm'):
            # Izvuci prvi niz brojeva pre prve pojave "_"
            base_name = os.path.splitext(file)[0]  # Bez ekstenzije
            first_number = ''.join([c for c in base_name if c.isdigit()])  # Izvuci sve brojeve
            if "_" in base_name:
                first_number = base_name.split('_')[0]  # Prvi deo pre "_"
            
            dicom_path = os.path.join(dicom_directory, file)
            output_filename = f'{first_number}.png'  # Postavi novo ime fajla
            output_path = os.path.join(output_directory_png, output_filename)
            
            save_dicom_as_png(dicom_path, output_path)
            print(f'Sačuvana slika: {output_filename}')

if __name__ == "__main__":
    main()
