import Tkinter as tk
import tkFileDialog
from ccat import subjects
import sys
from itertools import islice
from multiprocessing import Process
from threading import Thread
from Queue import Queue, Empty

run = True

class NewModel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Set the frames for the page layout
        name_frame = tk.Frame(self)
        mx_frame = tk.Frame(self)
        csv_frame = tk.Frame(self)
        button_frame = tk.Frame(self)

        # Pack the frames in the correct shape
        name_frame.pack(anchor=tk.W)
        mx_frame.pack(anchor=tk.W)
        csv_frame.pack(anchor=tk.W)
        button_frame.pack(anchor=tk.E)

        # Filename
        self.fname_label_text = tk.StringVar()
        self.fname_label = tk.Label(
            name_frame, text="Choose a project name and location")
        self.fname_entry = tk.Entry(
            name_frame, state=tk.DISABLED, textvariable=self.fname_label_text)
        self.fname_button = tk.Button(
            name_frame, text="Browse...", command=self.get_fname)

        # Subject directory
        self.sdir_label_text = tk.StringVar()
        self.sdir_label = tk.Label(
            mx_frame, text="Select the connection matrices")
        self.sdir_entry = tk.Entry(
            mx_frame, state=tk.DISABLED, textvariable=self.sdir_label_text)
        self.sdir_button = tk.Button(
            mx_frame, text="Browse...", command=self.get_sdir)

        # CSV File
        self.csv_label_text = tk.StringVar()
        self.csv_label = tk.Label(
            csv_frame, text="Select the CSV for the data (Leave blank if none)")
        self.csv_entry = tk.Entry(
            csv_frame, state=tk.DISABLED, textvariable=self.csv_label_text)
        self.csv_button = tk.Button(
            csv_frame, text="Browse...", command=self.get_csv)

        # Button
        self.submit_button = tk.Button(
            button_frame, text="Submit", command=self.submit_behaviour)
        self.back_button = tk.Button(
            button_frame, text="Back", command=lambda: self.controller.show_frame("OptionsPage"))
        self.close_button = tk.Button(
            button_frame, text="Close", command=self.quit)

        # Loading text
        self.loading_status = tk.Text(self)

        # View layout
        self.fname_label.pack(side=tk.RIGHT)
        self.fname_entry.pack(side=tk.RIGHT)
        self.fname_button.pack(side=tk.RIGHT)

        self.sdir_label.pack(side=tk.RIGHT)
        self.sdir_entry.pack(side=tk.RIGHT)
        self.sdir_button.pack(side=tk.RIGHT)

        self.csv_label.pack(side=tk.RIGHT)
        self.csv_entry.pack(side=tk.RIGHT)
        self.csv_button.pack(side=tk.RIGHT)

        self.close_button.pack(side=tk.LEFT)
        self.back_button.pack(side=tk.LEFT)
        self.submit_button.pack(side=tk.LEFT)

        # Loading view
        self.loading_status.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def get_fname(self):
        fname = tkFileDialog.asksaveasfilename()
        self.fname_label_text.set(fname)

    def get_sdir(self):
        subject_directory = tkFileDialog.askdirectory()
        self.sdir_label_text.set(subject_directory)

    def get_csv(self):
        csv_directory = tkFileDialog.askopenfilename()
        self.csv_label_text.set(csv_directory)

    def submit_behaviour(self):
        self.fname_button['state'] = tk.DISABLED
        self.sdir_button['state'] = tk.DISABLED
        self.submit_button['state'] = tk.DISABLED
        self.back_button['state'] = tk.DISABLED
    
        directory = self.sdir_label_text.get()
        fname = self.fname_label_text.get()
        # csv = self.csv_lable_text.get()

        # if type(csv) != type(None):
            # self.controller.subject_model = subjects.Subject(directory, fname, csv=csv)
        self.controller.subject_model = subjects.Subject(directory, fname)
        sbj = self.controller.subject_model

        # Define the job to be done and the queue to signal.
        q = Queue()
        fn = SubjectJob(sbj, q)

        # Redirect stdout
        sys.stdout = NewStdout(self.loading_status, q)
        
        # Define and start the thread
        thread = Thread(target=fn.job)
        thread.daemon = True
        thread.start()

        # Stop Tkinter from using the main loop.
        while True:
            self.update_idletasks()
            self.update()

            if q.empty():
                # return stdout to Normal
                sys.stdout = sys.__stdout__

                # Show the analysis page
                self.controller.show_frame("AnalysisPage")

                # Exit the temporary main loop
                return

class NewStdout(object):
    def __init__(self, variable, q):
        self.variable = variable
        self.q = q
    def write(self, string):
        if self.q.empty() is not True:
            self.variable.insert(tk.END, string)
            self.variable.see(tk.END)

class SubjectJob:
    def __init__(self, sbj, q):
        self.q = q
        self.sbj = sbj

    def job(self):
        self.q.put(True)
        self.sbj.default_pipeline()
        self.q.get()
        self.q.task_done()
