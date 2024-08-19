import XmlToTxt
import slike
import DataSets
import yaml
import os
from ultralytics import YOLO

def run():
    # XmlToTxt.main()  # Pravi .txt za detekciju i za segmentaciju
    # slike.main()     # Pretvara slike u PNG i cuva u ALLPNG
    # DataSets.main()  # Kreira dataset i YAML fajl

    # Putanja do YAML fajla
    #yaml_path = 'datasetSegmentation.yaml'
    yaml_path = 'datasetDetection.yaml'

    # Učitavanje YAML fajla
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)

    # Definišite konfiguraciju modela
    model_config = {
        'model': 'yolov8s.pt',  # 'yolov8n.pt', 'yolov8m.pt', 'yolov8l.pt', itd.
        'epochs': 10,                # Broj epoha
        'batch': 32                  # Veličina serije (batch size)
    }

    # Kreiranje modela
    model = YOLO(model_config['model'])

    # Treniranje modela
    results = model.train(data=yaml_path, epochs=model_config['epochs'], batch=model_config['batch'])

    # Predikcija na test setu
    test_images_path = data['test']  # putanja do test slika definisana u YAML fajlu
    predictions = model.predict(source=test_images_path, save=True)  # Rezultati će biti sačuvani

    # Prikazivanje rezultata predikcije
    print("Predikcija završena na test setu.")

if __name__ == "__main__":
    run()
