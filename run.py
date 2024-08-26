from UI.window import init_ui


from database.excel_db import ExcelDB


from excel.excel_tool import ExcelTool

def init_info(info:dict):
    info["directory"] = ""
    info["file"] = ""








if __name__ == '__main__':

    # INFO
    info = {}

    init_info(info)

    # Database
    db = ExcelDB("entradas.db")

    
    # Excel Reader
    reader = ExcelTool()


    # UI
    init_ui(info, reader, db)
    
    print("hello")