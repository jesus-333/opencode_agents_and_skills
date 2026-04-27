"""
Support for PDF processing, including text extraction and metadata retrieval.

Authors
-------
Alberto (Jesus) Zancanaro
"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports

import os
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
import pdfplumber

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_all_pdf_files_in_directory(directory_path : str) -> list :
    """
    Get a list of all PDF files in a specified directory.

    Parameters
    ----------
    directory_path : str
        The path to the directory to search for PDF files.

    Returns
    -------
    pdf_files : list
        A list of file paths for all PDF files found in the specified directory.
    """
    
    # List to store the paths of PDF files
    pdf_files = []
    
    # Walk through the directory and its subdirectories to find PDF files
    for root, _, files in os.walk(directory_path) :
        for file in files :
            if file.lower().endswith(".pdf") :
                pdf_files.append(os.path.join(root, file))

    return pdf_files

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Extract information from PDF documents

def get_number_of_pages(pdf_path : str) -> int :
    """
    Return the number of pages in the PDF document.

    Parameters
    ----------
    pdf_path : str
        The path to the PDF file.

    Returns
    -------
    int
        The number of pages in the PDF document.

    """
    with pdfplumber.open(pdf_path) as pdf : return len(pdf.pages)

def extract_metadata_from_pdf(pdf_path : str) -> dict :
    """
    Extract metadata from a PDF document.

    Parameters
    ----------
    pdf_path : str
        The path to the PDF file.

    Returns
    -------
    dict
        A dictionary containing the metadata of the PDF document.

    """
    with pdfplumber.open(pdf_path) as pdf :
        return pdf.metadata

def check_page_range(start_page : int, end_page : int, pdf) -> tuple :
    """
    Check the validity of the specified page range and return the adjusted start and end page numbers.
    Function created because this operation is repeated in all the extraction functions.

    The range is defined as [start_page, end_page], where start_page and end_page are inclusive.
    - If range is not specified (i.e., both start_page and end_page are None), it will return the range for the entire document.
    - If start page is defined and end_page is None, it will extract all the text from start_page to the end of the document.
    - If start_page is None and end_page is defined, it will extract all the text from the beginning of the document to end_page.
    - If start_page is greater than end_page, a ValueError will be raised indicating an invalid page range.
    - If start_page is negative or zero, a ValueError will be raised indicating that page numbers must be positive integers.
    - If end_page is greater than the total number of pages in the document, a ValueError will be raised indicating that end_page cannot exceed the total number of pages in the document.
    """

    # Check the range
    if start_page is None : start_page = 1
    if end_page is None : end_page = len(pdf.pages)
    if start_page > end_page : raise ValueError(f"Invalid page range: start_page ({start_page}) cannot be greater than end_page ({end_page}).")
    if start_page <= 0 : raise ValueError(f"Invalid page range: start_page ({start_page}) must be a positive integer.")
    if end_page > len(pdf.pages) : raise ValueError(f"Invalid page range: end_page ({end_page}) cannot exceed the total number of pages in the document ({len(pdf.pages)}).")

    return start_page, end_page

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Exttact text from PDF documents

def extract_text_from_pdf(pdf_path : str, start_page : int = None, end_page : int = None) -> str :
    """
    Extract text from a PDF document in a specified page range.
    See the docstring of the check_page_range function for details on how the page range is defined and handled.

    To extract text of a specific page, set start_page and end_page to the same value (e.g., start_page = 2, end_page = 2 to extract text from page 2).
    If start_page is greater than end_page, a ValueError will be raised indicating an invalid page range.

    Note that page numbers are 1-based, meaning that the first page of the document is page 1.
    This choice is made to align with common user expectations, as opposed to 0-based indexing used in programming.

    Parameters
    ----------
    pdf_path : str
        The path to the PDF file.
    start_page : int, optional
        The page number to start extraction from (default is 1).
    end_page : int, optional
        The page number to end extraction at (default is None, which means extract until the end of the document).

    Returns
    -------
    text : str
        The extracted text from the specified pages of the PDF document.

    """

    with pdfplumber.open(pdf_path) as pdf :
        # Define the page range
        start_page, end_page = check_page_range(start_page, end_page, pdf)

        # Extract text from the specified page range
        text = ""
        for page in pdf.pages[start_page - 1 : end_page] :
            text += page.extract_text() + "\n"

        return text.strip()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Tables

def extract_tables_from_pdf(pdf_path : str, start_page : int = None, end_page : int = None) -> list :
    """
    Extract tables from a PDF document in a specified page range.
    See the docstring of the check_page_range function for details on how the page range is defined and handled.

    Note that page numbers are 1-based, meaning that the first page of the document is page 1.
    This choice is made to align with common user expectations, as opposed to 0-based indexing used in programming.

    Parameters
    ----------
    pdf_path : str
        The path to the PDF file.
    start_page : int, optional
        The page number to start extraction from (default is 1).
    end_page : int, optional
        The page number to end extraction at (default is None, which means extract until the end of the document).

    Returns
    -------
    tables : list
        A list of tables extracted from the specified pages of the PDF document. Each table is represented as a list of rows, where each row is a list of cell values.

    """
    with pdfplumber.open(pdf_path) as pdf :
        # Define the page range
        start_page, end_page = check_page_range(start_page, end_page, pdf)

        # Extract tables from the specified page range
        tables = []
        for page in pdf.pages[start_page - 1 : end_page] :
            tables.extend(page.extract_tables())

        return tables

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Images

def extract_images_from_pdf(pdf_path : str, start_page : int = None, end_page : int = None) -> list :
    """
    Extract images and their information from a PDF document in a specified page range and return them as a list of PIL Image objects and a list of dictionaries containing the information of each image.
    See the docstring of the check_page_range function for details on how the page range is defined and handled.

    Note that page numbers are 1-based, meaning that the first page of the document is page 1.
    This choice is made to align with common user expectations, as opposed to 0-based indexing used in programming.

    Parameters
    ----------
    pdf_path : str
        The path to the PDF file.
    start_page : int, optional
        The page number to start extraction from (default is 1).
    end_page : int, optional
        The page number to end extraction at (default is None, which means extract until the end of the document).

    Returns
    -------
    images_list : list
        A list of PIL Image objects representing the images extracted from the specified pages of the PDF document.
    images_information : list
        A list of dictionaries containing the information of each image extracted from the specified pages of the PDF document. Each dictionary includes details such as page number, width, height, colorspace, bits per component, raw bytes length, and position on the page.
        The position is represented as a tuple of coordinates (x0, top, x1, bottom) which define the bounding box of the image on the page, where (x0, top) is the upper-left corner and (x1, bottom) is the lower-right corner.
    """

    with pdfplumber.open(pdf_path) as pdf:
        # Define the page range
        start_page, end_page = check_page_range(start_page, end_page, pdf)
        
        # List to save the extracted images and their information
        images_list = []
        images_information = []

        for page in pdf.pages[start_page - 1 : end_page] :
            for image_obj in page.images :

                # Get raw bytes from the stream
                stream = image_obj['stream']
                raw_bytes = stream.get_data()  # pdfminer decodes filters (FlateDecode etc.) for you

                # Reconstruct image from raw bytes
                width, height = image_obj['srcsize']
                colorspace = image_obj['colorspace'][0].name  # e.g. 'DeviceRGB'
                bits = image_obj['bits']  # bits per component

                if colorspace == 'DeviceRGB':
                    mode = 'RGB'
                    channels = 3
                elif colorspace == 'DeviceGray':
                    mode = 'L'
                    channels = 1
                elif colorspace == 'DeviceCMYK':
                    mode = 'CMYK'
                    channels = 4
                else:
                    raise ValueError(f"Unsupported colorspace: {colorspace}")

                # Raw bytes → numpy array → PIL Image
                dtype = np.uint16 if bits == 16 else np.uint8
                arr = np.frombuffer(raw_bytes, dtype = dtype)
                arr = arr.reshape((height, width, channels)) if channels > 1 else arr.reshape((height, width))
                img = Image.fromarray(arr, mode = mode)
                
                # Save image
                images_list.append(img)

                # Save image information
                image_info = {
                    "page_number" : page.page_number,
                    "width" : width,
                    "height" : height,
                    "colorspace" : colorspace,
                    "bits_per_component" : bits,
                    "raw_bytes_length" : len(raw_bytes),
                    "position" : (image_obj['x0'], image_obj['top'], image_obj['x1'], image_obj['bottom'])
                }
                images_information.append(image_info)

                # Note for position: (x0, top, x1, bottom) are the coordinates of the bounding box of the image on the page, 
                # - where (x0, top) is the upper-left corner
                # - (x1, bottom) is the lower-right corner.

        return images_list, images_information

def save_images_from_pdf(images_list : list, path_to_save : str, names_list : list = None, extension : str = 'png') -> None :
    """
    Save a list of PIL Image objects to a specified directory with optional custom names and file extension.

    Parameters
    ----------
    images_list : list
        A list of PIL Image objects to be saved, as obtained from the extract_images_from_pdf function.
    path_to_save : str
        The directory path where the images will be saved. If the directory does not exist, it will be created.
    names_list : list, optional
        A list of custom names for the images (without file extension). If not provided, images will be named sequentially as 'image_1', 'image_2', etc.
        If provided, must have the same length as images_list, otherwise a ValueError will be raised.
    extension : str, optional
        The file extension to use when saving the images (default is 'png'). Supported extensions are `png`, `jpg`, `jpeg`, `eps` and `pdf`.
    """

    # Check if path_to_save exists, if not create it
    if not os.path.exists(path_to_save) : os.makedirs(path_to_save)

    # Check names_list
    if names_list is not None :
        # If provided, check that it has the same length as images_list
        if len(names_list) != len(images_list) : raise ValueError(f"Length of names_list ({len(names_list)}) must be the same as length of images_list ({len(images_list)}).")
    else :
        # If not provided, create default names
        names_list = [f"image_{i + 1}" for i in range(len(images_list))]
    
    # Check extension
    supported_extensions = ['png', 'jpg', 'jpeg', 'eps', 'pdf']
    if extension.lower() not in supported_extensions : raise ValueError(f"Unsupported file extension: {extension}. Supported extensions are: {supported_extensions}")

    # Save images
    for img, name in zip(images_list, names_list) :
        img.save(os.path.join(path_to_save, f"{name}.{extension}"))
