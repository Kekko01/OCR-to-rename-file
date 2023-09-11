# OCR to rename file

![Logo](https://francescociociola.it/assets/images/OCR-to-rename-file.png "OCR to rename file")

 Read a PDF file and rename the file with INFO in the page

[![GitHub issues](https://img.shields.io/github/issues/Kekko01/OCR-to-rename-file)](https://github.com/Kekko01/OCR-to-rename-file/issues)
[![GitHub forks](https://img.shields.io/github/forks/Kekko01/OCR-to-rename-file)](https://github.com/Kekko01/OCR-to-rename-file/network)
[![GitHub stars](https://img.shields.io/github/stars/Kekko01/OCR-to-rename-file)](https://github.com/Kekko01/OCR-to-rename-file/stargazers)
[![GitHub license](https://img.shields.io/github/license/Kekko01/OCR-to-rename-file)](https://github.com/Kekko01/OCR-to-rename-file/blob/main/LICENSE)
[![Twitter](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FKekko01%2FOCR-to-rename-file)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FKekko01%2FOCR-to-rename-file)

## What is it?

OCR to rename file is software that allows you to open pdf files, read the contents of those files, and rename the file according to the contents of the document.

## What does it do?

The software reads the configuration, then reads the .pdf files within the input folder, turns page x into an image, the various pieces to be read are cropped, an OCR scan is done, and then with the results it had, renames and moves the .pdf file with the read data.

## How to clone software and setup

1. Download last software release from: <https://github.com/Kekko01/OCR-to-rename-file/releases>

2. Extract it and open folder

3. Installs the required libraries with the  **requirements.txt**:

    ```bash
    pip install -r requirements.txt
    ```

4. Edit the **config-EDITME.json** file and rename it **config.json**, with this structure::

    ```JSON
    {
        "configs":
        [
            {
                "name": "Config 1",
                "description": "Description 1",
                "in_dir": "dir\\in\\files",
                "out_dir": "dir\\out\\files",
                "dpi": 150,
                "languages": ["it"],
                "filename": "{FIELD1} {field2} - {Field3} some text.pdf",
                "fields": [
                    {"name": "FIELD1", "left": 194, "top": 138, "right": 548, "bottom": 173},
                    {"name": "field2", "left": 549, "top": 141, "right": 1146, "bottom": 164},
                    {"name": "Field3", "left": 849, "top": 179, "right": 877, "bottom": 205}
                ]
            }
            
            ,

            {
                "name": "Config 2",
                "description": "Description 2",
                "in_dir": "dir\\in\\files",
                "out_dir": "dir\\out\\files",
                "dpi": 150,
                "languages": ["fr", "en"],
                "page": 1,
                "filename": "{FIELD1} {field2} - {Field3} some text.pdf",
                "fields": [
                    {"name": "FIELD1", "left": 194, "top": 138, "right": 548, "bottom": 173},
                    {"name": "field2", "left": 549, "top": 141, "right": 1146, "bottom": 164},
                    {"name": "Field3", "left": 849, "top": 179, "right": 877, "bottom": 205}
                ]
            }
        ]
    }
    ```

5. Start the main.py software:

    ```bash
    python main.py
    ```

### Compiled software (Beta)

You could skip some of these steps (2, 3, 5) and avoid installing Python by downloading the precompiled .exe package from the [Releases](https://github.com/Kekko01/OCR-to-rename-file/releases) page. It doesn't work everywhere and doesn't work as perfectly as the guide explained earlier, however, if you are on Windows you might try it.
The package was done with pyinstaller, and I don't know why a virus is detected, probably [False Positive](https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184).

------------

# FAQ

## How to install Python?

Go here: <https://www.python.org/downloads/> and install the verson for yout PC

## Have you problems?

Don't worry, please you can found or create a issue here: <https://github.com/Kekko01/OCR-to-rename-file/issues>

## I would like to contribute, how can I do that?

You can fork the repository and then submit a pull request. If you don't know how to do that, you can read the [Github forking guide](https://guides.github.com/activities/forking/).
