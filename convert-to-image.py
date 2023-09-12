if __name__ == '__main__':
    import os

    in_file = input('Enter the full address of the file to be converted here:')
    if not os.path.exists(in_file):
        print('File does not exist!')
        exit()

    dpi = int(input('Enter DPI of the output image here: '))
    if dpi <= 0:
        print('DPI must be a positive integer!')
        exit()

    page = int(input('Enter the page number of the PDF file to be converted here: '))
    if page <= 0:
        print('Page number must be a positive integer!')
        exit()

    import fitz  # PyMuPDF

    pdf_document = fitz.open(in_file)
    pix = pdf_document[page].get_pixmap(dpi=dpi)
    pix.save(in_file.replace('.pdf', '.jpg'))
    pdf_document.close()
    print('Conversion complete! Check the output file in the same directory as the input file.')
    exit()
