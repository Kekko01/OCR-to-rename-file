#!/usr/bin/env python
'''
@author  Francesco Ciociola - https://kekko01.altervista.org/blog/
'''

import sys, json, os, tempfile

def check_configs(configs):
    for config in configs:
        if not os.path.exists(config['in_dir']):
            print(f"Error with {config['name']} configuration: input directory does not exist. Directory: {config['in_dir']}")
            return False
        if 'dpi' in config and (not isinstance(config['dpi'], int) or config['dpi'] <= 0):
            print(f"Error with {config['name']} configuration: invalid value for dpi. Value: {config['dpi']}")
            return False
        lang_list = ['bn','as','mni', 'ru','rs_cyrillic','be','bg','uk','mn','abq','ady','kbd',
                    'ava','dar','inh','che','lbe','lez','tab','tjk','hi','mr','ne','bh','mai','ang',
                    'bho','mah','sck','new','gom','sa','bgc','th','ch_sim','ch_tra','ja','ko','ta','te','kn']
        if 'languages' in config and not isinstance(config['languages'], list):
            print(f"Error with {config['name']} configuration: invalid value for languages, languages must be a list! Value: {config['languages']}")
            return False
        for lang in config['languages']:
            if lang not in lang_list:
                print(f"Error with {config['name']} configuration: invalid value for language, check if language is supported. Value: {lang}")
                if input('Do you want to open the page where there are all the supported languages? (y/n): ') == 'y':
                    os.system(
                        "open https://www.jaided.ai/easyocr/#:~:text=languages%20and%20expanding.-,Supported%20Languages,-Language"
                    )
                return False
        for field in config['fields']:
            if not isinstance(field['left'], int) or field['left'] < 0:
                print(f"Error with {config['name']} configuration: invalid value for left. Value: {field['left']}")
                return False
            if not isinstance(field['top'], int) or field['top'] < 0:
                print(f"Error with {config['name']} configuration: invalid value for top. Value: {field['top']}")
                return False
            if not isinstance(field['right'], int) or field['right'] < 0:
                print(f"Error with {config['name']} configuration: invalid value for right. Value: {field['right']}")
                return False
            if not isinstance(field['bottom'], int) or field['bottom'] < 0:
                print(f"Error with {config['name']} configuration: invalid value for bottom. Value: {field['bottom']}")
                return False
            if field['left'] >= field['right']:
                print(f"Error with {config['name']} configuration: the left value cannot be larger than the right value!. Value left: {field['left']} Value right: {field['right']}")
                return False
            if field['top'] >= field['bottom']:
                print(f"Error with {config['name']} configuration: the top value cannot be larger than the bottom value!. Value top: {field['top']} Value bottom: {field['bottom']}")
                return False
    return True

def pdf_to_image(file_in, file_out, dpi=150, page=0):
    try:
        import fitz  # PyMuPDF
        if not os.path.exists(file_in):
            print(f"Error with {file_in}: file does not exist!")
            return False
        pdf_document = fitz.open(file_in)
        if page >= len(pdf_document):
            print(f"Error with {file_in}: page {page} does not exist!")
            return False
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
        print("Error: could not load config.json, please make sure it exists JSON.")
        input()
        sys.exit(1)

    """
    Check configuration
    """
    if not check_configs(configs):
        input()
        sys.exit(1)

    print("Welcome to OCR to rename file!\n")
    use_gpu = bool(sys.argv[2]) if len(sys.argv) > 2 else True
    if len(sys.argv) > 1:
        try:
            current_config = configs[int(sys.argv[1])]
        except:
            print("Error: could not find configuration for", sys.argv[1], "in config.json, please make sure it exists and is valid JSON.")
            input()
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
            input()
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
            if os.path.exists(os.path.join(current_config['out_dir'], new_name)):
                print(f"Error: file already exists. Filename: {file}")
                continue
            if not os.path.exists(os.path.join(current_config['out_dir'])):
                os.makedirs(os.path.join(current_config['out_dir']))
                print(f"Directory created: {current_config['out_dir']}")
            os.rename(os.path.join(current_config['in_dir'], file), os.path.join(current_config['out_dir'], new_name))
            print(f"File saved in: {current_config['out_dir']}")
        except:
            print(f"Error: could not rename file. Filename: {file}")

        os.remove(image_to_scan)

    print("All files processed!")
    input()
    sys.exit(0)
            