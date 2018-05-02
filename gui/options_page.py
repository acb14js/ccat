import Tkinter as tk
from PIL import ImageTk, Image


class OptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        title_frame = tk.Frame(self)
        body_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        title_frame.pack()
        body_frame.pack()
        bottom_frame.pack(anchor=tk.E)

        welcome_text = "Welcome to the Connectome Clustering Analysis Tool - CCAT"
        title = tk.Label(title_frame, text=welcome_text, font='Helvetica 14 bold')
        title.pack()

        img_path = "gui/welcome_icon.png"
        img_open = Image.open(img_path)
        img = img_open.resize((250, 250), Image.ANTIALIAS)
        # TODO get the image to show
        img_show = ImageTk.PhotoImage(img)
        image_label = tk.Label(body_frame, image=img_show)
        image_label.image = img_show
        image_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        body_txt_frame = tk.Frame(body_frame)
        body_txt_frame.pack()

        body_title = tk.Label(body_txt_frame, text="Important Information", font='Helvetica 12')
        body_title.pack(anchor=tk.S)

        pipeline_info = """
        Before using this tool to analyse MRI images make sure that your pipeline converts the MRI scans into connectomes. 
        """
        pipeline_text = tk.Label(body_txt_frame, text=pipeline_info, wraplength=220, justify=tk.LEFT)
        pipeline_text.pack(anchor=tk.NE)

        cpac_info = """
        For further information see the C-PAC page at: https://github.com/FCP-INDI/C-PAC
        """

        cpac_text = tk.Label(body_txt_frame, text=cpac_info, wraplength=220, justify=tk.LEFT)
        cpac_text.pack()

        button_frame = tk.Frame(bottom_frame)
        button_frame.pack(side=tk.RIGHT, anchor=tk.E)

        close_button = tk.Button(
            button_frame, text="Close", command=self.quit)
        load_model = tk.Button(button_frame, text="Load a model",
            command=lambda:self.controller.show_frame("LoadModel"))
        new_model = tk.Button(button_frame, text="New model",
            command=lambda:self.controller.show_frame("NewModel"))
        
        # View layour
        close_button.pack(side=tk.LEFT)
        load_model.pack(side=tk.LEFT)
        new_model.pack(side=tk.LEFT)

        version_frame = tk.Frame(bottom_frame)
        version_frame.pack(side=tk.LEFT, anchor=tk.W)
        version = tk.Label(version_frame, text="Version 0.1")
        version.pack()
        

