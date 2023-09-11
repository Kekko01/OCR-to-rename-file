#!/usr/bin/env python
'''
@author  Francesco Ciociola - https://kekko01.altervista.org/blog/
'''

import sys, json, os, tempfile

def pdf_to_image(file_in, file_out, dpi=150, page=0):
    try:
        import fitz  # PyMuPDF
        pdf_document = fitz.open(file_in)
        pix = pdf_document[page].get_pixmap(dpi=dpi)
        pix.save(file_out)
        pdf_document.close()
        return True
    except:
        return False

    
def crop_image(image, left, top, right, bottom):
    try:
        from PIL import Image
        im = Image.open(image)
        cropped = im.crop((left, top, right, bottom))
        new_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False).name
        cropped.save(new_image)
        return new_image
    except:
        return None

def get_text(image, languages=None, use_gpu=True):
    if languages is None:
        languages = ['en']
    try:
        import easyocr
        reader = easyocr.Reader(languages, gpu=use_gpu)
        result = reader.readtext(image, detail = 0)
        return result[0]
    except:
        return None
    

if __name__ == '__main__':
    """
    Load configuration from config.json
    """
    try:
        configs = json.load(open('config.json'))['configs']
    except:
        print("Error: could not load config.json, please make sure it exists and is valid JSON.")
        sys.exit(1)
    print("Welcome to OCR to rename file!\n")
    use_gpu = bool(sys.argv[2]) if len(sys.argv) > 2 else True
    if len(sys.argv) > 1:
        try:
            current_config = configs[int(sys.argv[1])]
        except:
            print("Error: could not find configuration for", sys.argv[1], "in config.json, please make sure it exists and is valid JSON.")
            sys.exit(1)
    else:
        print("Please select a configuration:")
        for i, config in enumerate(configs):
            print(f"{i}) {config['name']}: {config['description']}")
        print("Enter the number of the configuration you want to use:")
        try:
            current_config = configs[int(input())]
        except:
            print("Error: invalid input, please enter a valid number.")
            sys.exit(1)
    print(f"Loaded configuration: {current_config['name']}: {current_config['description']}")

    """
    Process files
    """
    for file in os.listdir(current_config['in_dir']):
        fields_for_filename = {}
        print(f"Processing {file}...")

        """
        Convert PDF to image for OCR
        """
        image_to_scan = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False).name
        if not pdf_to_image(os.path.join(current_config['in_dir'], file), image_to_scan, current_config['dpi'] if 'dpi' in current_config else 150, current_config['page'] if 'page' in current_config else 0):
            print(f"Error: could not convert PDF to image. Filename: {file}")
            continue

        """
        Crop image to images smaller for analysis
        """
        for field in current_config['fields']:
            if field_image := crop_image(
                image_to_scan,
                field['left'],
                field['top'],
                field['right'],
                field['bottom'],
            ):
                """
                Run OCR
                """
                languages = current_config['languages'] if 'languages' in current_config else ['eng']
                if field_text := get_text(field_image, languages, use_gpu):
                    fields_for_filename[field['name']] = field_text
                else:
                    print(f"Field {field['name']} is empty.")
                    fields_for_filename[field['name']] = ' '
                os.remove(field_image)
            else:
                print(f"Error: could not crop image. Filename: {file}, field: {field['name']}")

        """
        Rename file
        """
        try:
            new_name = current_config['filename']
            for field in current_config['fields']:

                """
                Check if change field in UPPER, LOWER or CAPITALIZED
                """
                if field['name'].isupper():
                    fields_for_filename[field['name']] = fields_for_filename[field['name']].upper()
                elif field['name'].islower():
                    fields_for_filename[field['name']] = fields_for_filename[field['name']].lower()
                elif field['name'].istitle():
                    fields_for_filename[field['name']] = fields_for_filename[field['name']].title()
                

                new_name = new_name.replace("{" + field['name'] + "}", fields_for_filename[field['name']])
            print(f"New filename: {new_name}")
            try:
                os.rename(os.path.join(current_config['in_dir'], file), os.path.join(current_config['out_dir'], new_name))
                print(f"File saved in: {current_config['out_dir']}")
            except:
                print(f"Error: could not convert image to PDF. Filename: {file}")
        except:
            print(f"Error: could not rename file. Filename: {file}")

        os.remove(image_to_scan)
            
            