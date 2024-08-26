import tkinter as tk
from tkinter import TOP, BOTH, LEFT, RIGHT
from tkinter import messagebox

from UI.events import select_directory, select_file, fill_db_with_directory, populate_file

from exceptions.EventSelectError import EventSelectError
from exceptions.EventSelectSuccess import EventSelectSuccess

event_list: list[str] = ["SELECT_DIR", "SELECT_FILE", "FILL_DB", "POPULATE_FILE"]


def pick_event(event:str, **kwargs):
    try:
        if event == event_list[0]:
            select_directory(kwargs["label_top"], kwargs["info"], kwargs["db"])
        elif event == event_list[1]:
            fill_db_with_directory(kwargs["info"], kwargs["reader"], kwargs["db"])
        elif event == event_list[2]:
            select_file(kwargs["label_bottom"], kwargs["info"])
        elif event == event_list[3]:
            populate_file(kwargs["info"], kwargs["reader"], kwargs["db"])
    except EventSelectSuccess as e:
        messagebox.showinfo("Success", e)
    except EventSelectError as e:
        messagebox.showerror("Failure", e)





def create_main_window(name:str, width:int, height:int)-> tk.Tk:
    root = tk.Tk()
    root.title(name)
    root.geometry(str(width)+"x"+str(height))
    return root

def create_label(window:tk.Tk, text:str, bg:str) -> tk.Label:
    return tk.Label(window ,text=text, bg=bg)

def create_button(window:tk.Tk, text:str, command)-> tk.Button:
    return tk.Button(window, text=text, command=command)


def init_ui(info:dict, reader, db):
    width = 900
    height = 800
    main_window = create_main_window("Organizador Excel", width, height)



    # Create the top frame
    top_frame = tk.Frame(main_window, bd=1, relief="solid")
    top_frame.pack(fill=tk.BOTH, expand=True)

    label_top = create_label(top_frame, text="No directory selected", bg="red")

    button_top = create_button(top_frame, "Select directory", command=lambda: pick_event("SELECT_DIR", label_top=label_top, info=info, db=db))
    button_top.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a label and a button in the top frame
    label_top.pack(side=tk.LEFT, padx=10, pady=10)

    

    # Create the big button in the top frame
    big_button_top = tk.Button(top_frame, text="Fill DB", height=2, width=20, command=lambda: pick_event("SELECT_FILE", info=info, reader=reader, db=db))
    big_button_top.pack(side=tk.LEFT, pady=10)



    

    # Create the bottom frame
    bottom_frame = tk.Frame(main_window, bd=1, relief="solid")
    bottom_frame.pack(fill=tk.BOTH, expand=True)

    label_bottom = create_label(bottom_frame,text="No file selected", bg="red")
    

    button_bottom = tk.Button(bottom_frame, text="Select file", command=lambda: pick_event("FILL_DB", label_bottom=label_bottom, info=info))
    button_bottom.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a label and a button in the bottom frame
    label_bottom.pack(side=tk.LEFT, padx=10, pady=10)

    

    # Create the big button in the bottom frame
    big_button_bottom = tk.Button(bottom_frame, text="Fill File", height=2, width=20, command=lambda: pick_event("POPULATE_FILE", info=info, reader=reader, db=db))
    big_button_bottom.pack(side=tk.LEFT,pady=10)




    main_window.mainloop()



