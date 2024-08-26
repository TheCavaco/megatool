import hashlib
import string

from tkinter import filedialog, messagebox

from database.excel_db import ExcelDB
from excel.excel_tool import ExcelTool

from exceptions.EventSelectError import EventSelectError
from exceptions.EventSelectSuccess import EventSelectSuccess

# Function to trim text to fit within the label
def trim_text(text, max_length):
    if len(text) > max_length:
        return text[-max_length:]
    return text


def generate_directory_hash(directory: str) -> str:
    # Create a hash object using SHA-256
    hash_object = hashlib.sha256(directory.encode())

    # Get the hexadecimal digest of the hash
    hex_digest = hash_object.hexdigest()

    # Define a set of allowed characters (alphabet only, lowercase and uppercase)
    allowed_chars = string.ascii_letters  # a-z + A-Z

    # Convert the hexadecimal digest to an integer
    hex_int = int(hex_digest, 16)

    # Create a list to store the resulting characters
    hash_chars = []

    # Loop to generate 5 characters
    for _ in range(5):
        # Get the character index using modulo with the number of allowed characters
        index = hex_int % len(allowed_chars)
        hash_chars.append(allowed_chars[index])

        # Reduce hex_int for the next iteration
        hex_int //= len(allowed_chars)

    # Join the list into a string
    return ''.join(hash_chars)


# Function to handle directory selection
def select_directory(dir_label, dir_dictionary: dict, database:ExcelDB):
    dir_path = filedialog.askdirectory()
    if dir_path:
        dir_dictionary["directory"] = dir_path
        database.create_table(generate_directory_hash(dir_path))
        dir_label.config(text=trim_text(dir_path, 20), width=20, anchor='e', bg="white")
    else:
        dir_label.config(text="No directory selected", bg="red")


def fill_db_with_directory(dir_dictionary: dict, reader: ExcelTool, database: ExcelDB):
    if dir_dictionary["directory"] == "":
        raise EventSelectError("No directory selected!")
    else:
        reader.read_values(dir_dictionary["directory"],database,True)
        raise EventSelectSuccess("All values read successfully!")



def populate_file(dir_dictionary: dict, reader: ExcelTool, database: ExcelDB):
    if dir_dictionary["file"] == "":
        raise EventSelectError("No file selected!")

    else:
        #TODO: populate file with db contents
        reader.load_workbook(dir_dictionary["file"], True, dir_dictionary["old_version"])
        # TODO: change library for excel sheets to an older one
        reader.populate(dir_dictionary["file"], database)
        raise EventSelectSuccess("New file populated!")




def select_file(file_label, file_dictionary:dict):
    filename = filedialog.askopenfilename()
    if ".xls" in filename:
        file_dictionary["file"] = filename
        file_dictionary["old_version"] = True
        file_label.config(text=trim_text(filename, 20), width=20, anchor='e', bg="white")
    elif ".xlsx" in filename:
        file_dictionary["file"] = filename
        file_dictionary["old_version"] = False
        file_label.config(text=trim_text(filename, 20), width=20, anchor='e', bg="white")
    else:
        file_label.config(text="No file selected", bg="red")
