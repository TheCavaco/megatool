import sqlite3


import os
import ctypes
import platform

from exceptions.EventSelectError import EventSelectError


def create_hidden_directory(dir_name:str) -> str:
    """ Create a hidden directory and return its location.
    """
    # Determine the correct path based on the current working directory
    current_dir:str = os.getcwd()
    hidden_dir_path:str = os.path.join(current_dir, dir_name)

    # Check if the directory already exists
    if os.path.exists(hidden_dir_path):
        return hidden_dir_path

    # Check the operating system
    system_name = platform.system()

    if system_name == "Windows":
        # Create the directory
        os.makedirs(hidden_dir_path, exist_ok=True)
        # Set the hidden attribute
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(hidden_dir_path, FILE_ATTRIBUTE_HIDDEN)
        print(f"Hidden directory created at: {hidden_dir_path} on Windows")

    elif system_name in ["Linux", "Darwin"]:  # Darwin is for macOS
        # Prefix the directory name with a dot to make it hidden
        hidden_dir_path = os.path.join(current_dir, f".{dir_name}")
        os.makedirs(hidden_dir_path, exist_ok=True)
        print(f"Hidden directory created at: {hidden_dir_path} on {system_name}")

    else:
        print(f"Unsupported operating system: {system_name}")

    return hidden_dir_path



class ExcelDB:
    def __init__(self, name):
        directory:str = create_hidden_directory("tool_db")
        conn = sqlite3.connect(os.path.join(directory, name))
        self.current_table = ""
        self.setCursor(conn.cursor())

    
    def create_table(self, name:str):
        self.getCursor().execute(f'''
            CREATE TABLE IF NOT EXISTS {name} (
                mark TEXT PRIMARY KEY,
                reference INTEGER NOT NULL
            )
        ''')
        self.current_table = name
        self.getCursor().connection.commit()


    def add_entry(self, mark, reference):
        # Check if the mark already exists in the table
        if self.current_table == "":
            raise EventSelectError("No directory selected")

        self.getCursor().execute(f'''
            SELECT reference FROM invoice WHERE mark = ?
        ''', (mark,))
        result = self.getCursor().fetchone()

        if result is None:
            # No existing entry with the same mark, insert new entry
            print("inserting " + str(mark) + " " + str(reference) +" into table")
            self.getCursor().execute(f'''
                INSERT INTO {self.current_table} (mark, reference) VALUES (?, ?)
            ''', (mark, reference))
        elif result[0] != reference:
            # Mark exists but with a different reference, update the entry
            print("updating " + str(mark) + " " + str(reference) +" into table")
            self.getCursor().execute(f'''
                UPDATE {self.current_table} SET reference = ? WHERE mark = ?
            ''', (reference, mark))
        
        # Commit the changes to the database
        self.getCursor().connection.commit()

    
    def get_entry(self, mark:str) -> str:
        if self.current_table == "":
            raise EventSelectError("No directory selected")
        self.getCursor().execute(f'''
            SELECT reference FROM {self.current_table} WHERE mark = ?
        ''', (mark,))
        result = self.getCursor().fetchone()

        print("Fetched result: " + str(result))

        if result is None:
            return "X"
        else:
            return int(result[0])
    




    #----------------------------------------------------------------
    #-------------------------GETTERS--------------------------------
    #----------------------------------------------------------------

    def getCursor(self) -> sqlite3.Cursor:
        return self.cursor


    #----------------------------------------------------------------
    #-------------------------SETTERS--------------------------------
    #----------------------------------------------------------------

    def setCursor(self, cursor):
        self.cursor = cursor