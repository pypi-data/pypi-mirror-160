"""
tessaract ocr pipeline
"""
import os
import json
import zipfile
import pytesseract
from pytesseract import Output
from PIL import Image, ImageSequence
from pdf2image import convert_from_path
# from config import OUTPUT_PATH
# from config import EXTENSION_LIST

OUTPUT_PATH = '/home/sourav/sam_setup/DataAdapters/src/json_dir'
EXTENSION_LIST = ['.png', '.jpg', '.jpeg']

class TessaractOcr:
    """
    tesseract ocr
    """

    def extract_text_from_image(self, image, file_name, index):
        """
        extracting text from images

        Args:
            image (object): image object
            file_name (str): name of file
            index (int): index no of pages
        """
        # removing extension from input file name for output file initial name
        output_filename = os.path.splitext(file_name)[0]
        # processing image using Tessaract Ocr
        process_image = pytesseract.image_to_data(
            image, output_type=Output.DICT)
        # writing output to json file
        with open(OUTPUT_PATH + output_filename+str(index) + '.json', 'w') as f:
            output_json = {os.path.basename(file_name):
                           [{'Confidence Score': conf, 'Text': text,
                             'Line no.': line_no, 'Top': top, 'Left':
                             left, } for conf, text, line_no,
                            top, left in zip(process_image['conf'],
                                             process_image['text'],
                                             process_image['line_num'],
                                             process_image['top'],
                                             process_image['left'])]}
            json.dump(output_json, f, indent=4)

    def image_processing(self, input_file):
        """
        image processing

        Args:
            input_file (str): input file name
        """

        file_name = Image.open(input_file)
        # processing image using Tessaract Ocr
        for index, page in enumerate(ImageSequence.Iterator(file_name)):
            # page.save("Page%d.png" % i)
            self.extract_text_from_image(page, input_file, index)

    def pdf_processing(self, input_file):
        """
        pdf processing

        Args:
            input_file (str): input file name
        """
        pdf_pages = convert_from_path(
            input_file, 500)  # getting total no. of pages inside pdf
        # iterating over each page of pdf
        for index, page in enumerate(pdf_pages):
            self.extract_text_from_image(page, input_file, index)

    def zip_processing(self, input_file):
        """
        zip processing

        Args:
            input_file (str): input file name
        """
        inp_file = input_file
        # reading zip file
        with zipfile.ZipFile(inp_file, mode="r") as file_list:
            # getting list of file inside zip
            # iterating over each file of zip
            for file in file_list.namelist():
                file_list.extract(file, "")  # saving file
                # getting extension of file
                extension = os.path.splitext(file)[-1].lower()
                # if extesnion is image then calling image processing
                if extension in EXTENSION_LIST:
                    self.image_processing(file)
                   # else calling pdf procssing
                else:
                    self.pdf_processing(file)





