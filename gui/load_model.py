import Tkinter as tk
import tkFileDialog
import pickle

class LoadModel(tk.Frame):
    """
    This window allows the user to load a previously produced subject model.
    """
    def __init__(self, parent, controller):
        # Init the class as a frame with the parent being the root window.
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Init the frames for the layout
        path_frame = tk.Frame(self)
        path_frame.pack()

        # Init the widgets to get the model path
        self.lmodel_label_text = tk.StringVar()
        self.lmodel_label = tk.Label(path_frame, text="Load a saved model")
        self.lmodel_entry = tk.Entry(path_frame, state=tk.DISABLED, textvariable=self.lmodel_label_text)
        self.lmodel_button = tk.Button(path_frame, text="Browse...", command=self.get_lmodel)
        
        # Init the frame to hold the widgets
        button_frame = tk.Frame(self)
        button_frame.pack(anchor=tk.E)

        # Init the button widgets
        self.submit_button = tk.Button(button_frame, text="Submit", command=self.submit_behaviour)
        self.back_button = tk.Button(button_frame, text="Back", command=lambda:self.controller.show_frame("OptionsPage"))
        self.close_button = tk.Button(button_frame, text="Close", command=self.quit)

        # Pack the load model widgets
        self.lmodel_label.pack(side=tk.LEFT)
        self.lmodel_entry.pack(side=tk.LEFT)
        self.lmodel_button.pack(side=tk.LEFT)

        # Display the button widgets
        self.close_button.pack(side=tk.LEFT)
        self.back_button.pack(side=tk.LEFT)
        self.submit_button.pack(side=tk.LEFT)

    def get_lmodel(self):
        """
        This is the event handler which is triggered when the user clicks on 
        the browse button. It sets the path to the previously produced subject
        model.
        """
        # Open file dialog
        path = tkFileDialog.askopenfilename() 
        # Set the chosen path
        self.lmodel_label_text.set(path) 

    def submit_behaviour(self):
        """
        This is the event handler bound to the submit button. it loads the 
        subject model using pickle and assigns it to the controllers subject
        model variable. Once the subject model is loaded the analysis page is
        shown.
        """
        # Store the path in a more readible local variable
        path = self.lmodel_label_text.get()

        print "Loading..."

        with open(path, 'rb') as f:
            print "Starting..."
            # Load the subject model with pickle
            self.controller.subject_model = pickle.load(f)

        print "Loaded!"
        # Show the analysis page
        self.controller.show_frame("AnalysisPage")
