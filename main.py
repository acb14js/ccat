#!/usr/bin/python2
from gui import options_page, load_model, new_model, analysis_page 
# import gui.options_page, gui.load_model, gui.new_model, gui.analysis_page
# from gui import *
import os
import Tkinter as tk


class ConnectomeAnalysisGUI(tk.Tk):
    """
    This is the root of the tkinter GUI hierachy. Run this script to show the
    GUI. The window title and icon are defined here in the __init__ function.
    The show frame function is used by other windows in the hierachy to switch
    to other windows within the GUI.
    """
    def __init__(self, master):
        root = tk.Frame(master)

        # Initialising the model to be used in the application
        self.subject_model = None

        # Setting the window title
        master.title("CCAT - Connectome Clustering Analysis Tool")

        # Setting the application icon
        imgicon = tk.PhotoImage(file=os.path.join('gui/icon.gif'))
        master.tk.call('wm', 'iconphoto', master._w, imgicon)  

        root.pack(side="top", fill="both", expand=True)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (options_page.OptionsPage, load_model.LoadModel, new_model.NewModel, analysis_page.AnalysisPage):
            page_name = F.__name__
            frame = F(root, self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("OptionsPage")

    def show_frame(self, cont):
        """
        This function is used to switch windows in the GUI. 

        Parameters
        ----------
        cont : str
            The name of the frame to switch to.
        """
        # Reset the layout to allow resizing
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        frame.grid()

        frame.tkraise()
        frame.update()

        # Window size is specified frame by frame
        frame.winfo_toplevel().geometry("")

        # Bind a show frame event
        frame.event_generate("<<ShowFrame>>")

    def get_page(self, page_class):
        return self.frames[page_class]

root = tk.Tk()
app = ConnectomeAnalysisGUI(root)
# root.protocol("WM_DELETE_WINDOW", app.quit)
tk.mainloop()
