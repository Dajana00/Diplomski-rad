import os
import numpy as np
import matplotlib.pyplot as plt
import pydicom
from skimage.draw import polygon
import plistlib
from lxml import etree


current_directory = os.path.dirname(__file__)
xml_directory = os.path.join(current_directory, "AllXML")
dicom_directory = os.path.join(current_directory, "AllDICOMs")
output_directory_dl = os.path.join(current_directory, "ALLTXTDL")
output_directory_sl = os.path.join(current_directory, "ALLTXTSL")

if not os.path.exists(output_directory_dl):
        os.makedirs(output_directory_dl)
if not os.path.exists(output_directory_sl):
    os.makedirs(output_directory_sl)
    
# Mapiranje tipova lezija na brojeve
lesion_type_mapping = {
    "UNNAMED" : 0,
    "" : 0,
    "Cluster": 1,
    "Calcification": 2,
    "Mass": 3,
    "Distortion": 4,
    "Asimmetry": 5,
    "Spiculated Region": 6
}

def load_inbreast_mask(mask_path, imshape):
    def load_point(point_string):
        x, y = tuple([float(num) for num in point_string.strip('()').split(',')])
        return y, x

    mask = np.zeros(imshape)
    rois = []
    lesion_types = []
    with open(mask_path, 'rb') as mask_file:
        plist_dict = plistlib.load(mask_file, fmt=plistlib.FMT_XML)['Images'][0]
        numRois = plist_dict['NumberOfROIs']
        rois_dict = plist_dict['ROIs']
        assert len(rois_dict) == numRois
        for roi_dict in rois_dict:
            numPoints = roi_dict['NumberOfPoints']
            points = roi_dict['Point_px']
            lesion_type = roi_dict['Name']
            assert numPoints == len(points)
            points = [load_point(point) for point in points]
            lesion_types.append(lesion_type)
            rois.append(points)
            if len(points) > 2:
                x, y = zip(*points)
                x, y = np.array(x), np.array(y)
                poly_x, poly_y = polygon(x, y, shape=imshape)
                mask[poly_x, poly_y] = 1
            else:
                for point in points:
                    mask[int(point[0]), int(point[1])] = 1
    return mask, rois, lesion_types

def find_dicom_file(directory, base_name):
    for file in os.listdir(directory):
        if file.startswith(base_name) and file.endswith('.dcm'):
            return os.path.join(directory, file)
    return None

def bounding_boxes_detection(rois, imshape):
    boxes = []
    for points in rois:
        mask = np.zeros(imshape)
        if len(points) <= 2:
            for point in points:
                mask[int(point[0]), int(point[1])] = 1
        else:
            x, y = zip(*points)
            x, y = np.array(x), np.array(y)
            poly_x, poly_y = polygon(x, y, shape=imshape)
            mask[poly_x, poly_y] = 1

        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        boxes.append((xmin, xmax, ymin, ymax))
    return boxes


def get_dicom_dimensions(dicom_path):
    dcm_data = pydicom.dcmread(dicom_path)
    return dcm_data.Rows, dcm_data.Columns
    plt.show()


def save_detection_format(txt_path, boxes, imshape, lesion_types):
    with open(txt_path, 'w') as file:
        for (xmin, xmax, ymin, ymax), lesion_type in zip(boxes, lesion_types):
            lesion_number = lesion_type_mapping.get(lesion_type, -1)  # -1 ako tip lezije nije pronađen
            x_center = (xmin + xmax) / 2 / imshape[1]
            y_center = (ymin + ymax) / 2 / imshape[0]
            width = (xmax - xmin) / imshape[1]
            height = (ymax - ymin) / imshape[0]
            file.write(f"{lesion_number} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def save_segmentation_format(txt_path, rois, lesion_types, imshape):
    with open(txt_path, 'w') as file:
        for points, lesion_type in zip(rois, lesion_types):
            lesion_number = lesion_type_mapping.get(lesion_type, -1)  # -1 ako tip lezije nije pronađen
            normalized_coords = ' '.join([f"{x/imshape[1]:.3f} {y/imshape[0]:.3f}" for y, x in points])
            file.write(f"{lesion_number} {normalized_coords}\n")
                
def display_image_with_bboxes_dect(image_path, boxes):
    if image_path.endswith('.dcm'):
        dcm_data = pydicom.dcmread(image_path)
        image = dcm_data.pixel_array
    else:
        image = plt.imread(image_path)

    plt.imshow(image, cmap='gray')
    for xmin, xmax, ymin, ymax in boxes:
        plt.gca().add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                          edgecolor='red', facecolor='none', linewidth=2))
    plt.show()
    
def display_image_with_bboxes_segm(image_path, rois):
    if image_path.endswith('.dcm'):
        dcm_data = pydicom.dcmread(image_path)
        image = dcm_data.pixel_array
    else:
        image = plt.imread(image_path)

    plt.imshow(image, cmap='gray')
    for points in rois:
        x, y = zip(*points)
        plt.plot(y, x, linestyle='-', linewidth=2, color='red')
    #plt.show()
    print('Početak')
            

def main():
    
    for xml_filename in os.listdir(xml_directory):
        if xml_filename.endswith('.xml'):
            xml_path = os.path.join(xml_directory, xml_filename)
            
            try:
                dicom_file_base_name = xml_filename.split('.')[0]
                dicom_file_path = find_dicom_file(dicom_directory, dicom_file_base_name)

                if xml_path and dicom_file_path:
                    dicom_shape = get_dicom_dimensions(dicom_file_path)
                    mask, rois, lesion_types = load_inbreast_mask(xml_path, dicom_shape)
                    boxes = bounding_boxes_detection(rois, dicom_shape)
                
            
                    txt_filename = os.path.splitext(os.path.basename(xml_path))[0] + '.txt'
                    
                    txt_path = os.path.join(output_directory_dl, txt_filename)
                    #save_detection_format(txt_path, boxes, dicom_shape, lesion_types)

                    
                    txt_path = os.path.join(output_directory_sl, txt_filename)
                    #save_segmentation_format(txt_path, rois, lesion_types, dicom_shape)
                    display_image_with_bboxes_dect(dicom_file_path, boxes)
                    #display_image_with_bboxes_segm(dicom_file_path, rois)
                    print(f'Obrađen fajl: {xml_filename}')
                else:
                    if not xml_path:
                        print(f"XML datoteka {xml_path} ne postoji.")
                    if not dicom_file_path:
                        print(f"DICOM datoteka za {dicom_file_base_name} nije pronađena.")
            except FileNotFoundError:
                print(f'Fajl nije pronađen: {xml_path}')
            except etree.XMLSyntaxError:
                print(f'Greška u parsiranju XML fajla: {xml_filename}')
            except Exception as e:
                print(f'Došlo je do greške: {e}')
if __name__ == "__main__":
    main()
