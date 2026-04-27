---
name: pdf-processing
description: Used to extract text, tables and images from PDF files. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
license: MIT
---

# What I do
Analyze and extract information from PDFs. The information you can extract are text, tables and images.

## Software you can use
- `pdfimages` for image extraction.
- `pdfplumber` for text, table and image extraction.
    - You can use it directly as a CLI command.
    - You can use the [python script](./scripts/pdf_processing.py) inside the `scripts` folder.
        - To run the python script you need the following package :
            - `csv`
            - `json`
            - `numpy`
            - `pandas`
            - `os`
            - `PIL`
            - `pdfplumber`
- `pdftotext` for text extraction.
- `pdftoppm` To convert PDF pages into images.
- `camelot`
- All the `cli` command installed by default to find file, create folder etc

Try to complete your task with the software you installed. If you specifically need a missing software, ask permission before installing it.
If none of the above software is installed, specify that you cannot complete your task.
As a last resort, If you find the current software list too limited for the task at hand, please suggest updates.

## Text extraction
Preferably, use a CLI tool. Use Python scripts only if specifically requested by the user, or the CLI tools will fail.

## Images extraction
Preferably, use a CLI tool. Use Python scripts only if specifically requested by the user, or the CLI tools will fail.

## Table extraction
Preferably, use a CLI tool. Use Python scripts only if specifically requested by the user, or the CLI tools will fail.
As a last resort, if specifically requested by the user, and you have the capabilities, you can directly analyze the entire file yourself and extract the tables.

## Metadata extraction
Preferably, use a CLI tool. Use Python scripts only if specifically requested by the user, or the CLI tools will fail.
This are optional informations, e.g. number of figures, pages size etc.
Extract this information only if it is useful to the current task

## File summary
By default produce a summary of the file(s) analyzed. See the [next section](#save-information) for more information on how these summary files should be structured.
To produce the summary, preferably extract the text using the tools at your disposal, save it to files and work with those files.
If specifically requested by the user, and you have the capabilities, you can directly analyze the entire `pdf` file yourself and summarize it.
Don't produce a summary file if the user asks for something more specific (e.g., extract only images).

## Save information
The information extracted should be saved, by default, in a directory called `pdf_summary` with the following structure :
```
pdf_summary/
├── images/
├── tables/
├── raw_text/
├── summaries/
├── list_of_images.csv
├── list_of_tables.csv
└── summary.md
```
You can use a different folder name and structure if you receive specific instructions in this regard.

### Notes on files to produce during the analysis
- By default, save images as `png`. Change the extension only if specifically requested.
- By default, save tables as `csv`. Change the extension only if specifically requested.
- By default, save text as `txt`. Change the extension only if specifically requested.
- `list_of_images.csv` is a `csv` file with a summary of all the images found. For each image you must save :
    - The path to the file containing the extracted image.
    - The dimensions of the extracted image must be saved.
    - The page number from which the image was extracted.
    - OPTIONAL. The original `pdf` file it was extracted from in case you are analyzing more than one file
    - OPTIONAL. If you have image analysis capability, a short description
- `list_of_tables.csv` is a `csv` file with a summary of all the tables found. For each table you must save :
    - The path to the file containing the extracted table.
    - The page number from which the table was extracted.
    - OPTIONAL. The original `pdf` file it was extracted from in case you are analyzing more than one file.
    - OPTIONAL. A description of the table.
- `summary.md` must contain the summary of the file(s) analyzed.
    - If you analyze only a single file then produce a summary of that file. Use [Template Summary Single file](./template_summary_single_file.md) as template, unless otherwise specified.
    - If you analyze more than 1 files then the summary files must contain a list of all the files analyzed. For each file analyzed insert the name, a very brief summary and a hyperlink to the summary of that specific file. Use [Template Summary Multiple file](./template_summary_multiple_files.md) as template, unless otherwise specified.
- `summaries` is an OPTIONAL folder that must be created if you analyze more than 1 file. Inside this folder you need to create a `md` file for each analyzed `pdf` file.
    - Use [Template Summary Single file](./template_summary_single_file.md) as template for each summary files, unless otherwise specified.
    - Each of the summary should be named `summary_[name original file].pdf`, unless otherwise specified.

# When to use me
- When you are asked to analyze one or more PDF documents
- When you are asked to summarize one or more PDF documents
- When you are asked to extract information (text, tables, images) from one or more PDF documents

# What you can't do
- Installing new software without permission. Even for the software mentioned in the [What I do](#what-i-do) section you have to ask if they are not already installed.
- Create and execute new scripts without permission
- Create new folders outside your currently working folder
- Create new files outside your currently working folder
