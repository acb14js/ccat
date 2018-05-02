import Tkinter as tk
import numpy as np
import ttk

# Matplotlib imports
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Global settings for matplotlib
matplotlib.rcParams.update({'font.size': 9 })
matplotlib.use('TkAgg')

# Globale settings for the analysis page
COLORS =  ['white', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']


class AnalysisPage(tk.Frame):
    """
    This window displays the information found by the clustering analysis. The
    information is presented in 3 treeview tables, 2 matplotlib figures and a
    entry which extracts the information stored in the subject model for the 
    currently selected scan. The
    """
    def __init__(self, parent, controller, options=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # The group that the selected subject is assigned.
        self.group = None

        #  Stops the frame initializing at the initialisation of the root frame
        self.bind('<<ShowFrame>>', self.on_show_frame)

    def on_show_frame(self, event):
        """
        This function is run when the window is shown. This prevents the page
        from initialising the tables when the starting window is run. This is
        because Tkinter will run all the __init__ functions of all the root 
        windows children. This function has been bound to the 'ShowFrame' 
        event in this classes __init__ function.
        """

        # Will throw an error if ran before the subject is loaded
        self.sbj = self.controller.subject_model

        # Split the frame into a left and right frame
        l_frm = tk.Frame(self, height=100)
        r_frm = tk.Frame(self)
        l_frm.pack(side=tk.LEFT, fill='x')
        r_frm.pack(side=tk.RIGHT, fill='x')

        # The frame for the main table of subjects
        sbj_frm = tk.Frame(l_frm)
        sbj_frm.pack()

        # Frame for the similar subjects table
        sim_frm = tk.Frame(l_frm)
        sim_frm.pack()

        # Frame for the disimiliar subjects
        dissim_frm = tk.Frame(l_frm)
        dissim_frm.pack()

        # Titles for the tables
        sbj_lbl = tk.Label(sbj_frm, text='Current Scan')
        sim_lbl = tk.Label(sim_frm, text='Similar Scan')
        dissim_lbl = tk.Label(dissim_frm, text='Dissimilar Scan')
        sbj_lbl.pack()
        sim_lbl.pack()
        dissim_lbl.pack()

        # Frame for the selected subject frame
        inf_frm = tk.Frame(r_frm, relief=tk.GROOVE, borderwidth=2)
        inf_frm.pack()

        # Frame for the data figures
        self.fig_frm = tk.Frame(r_frm)
        self.fig_frm.pack()

        # Frame for the buttons
        button_frame = tk.Frame(r_frm)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.E)

        # The button to save the current model
        model_save = tk.Button(
            button_frame, text='Save Model', command=self.sbj.save_model)
        model_save.pack(side=tk.RIGHT, anchor=tk.E)

        back_btn = tk.Button(button_frame, text='Close', command=self.quit)
        back_btn.pack(side=tk.RIGHT)

        # Titles for the selected subject frame.
        fig_lbl = tk.Label(self.fig_frm)
        fig_lbl.pack()
        inf_lbl = tk.Label(inf_frm, text='Subject Information')
        inf_lbl.pack()

        sbj_inf_frm = tk.Frame(inf_frm)
        sbj_inf_frm.pack()

        label_frm = tk.Frame(sbj_inf_frm)
        label_frm.pack(side=tk.LEFT)

        # The titles for the selected subject fields
        file_lbl = tk.Label(label_frm, text='The File Name:')
        num_lbl = tk.Label(label_frm, text='Subject Number:')
        asig_lbl = tk.Label(label_frm, text='The Assigned Group:')
        pseu_lbl = tk.Label(label_frm, text='The Latent Group:')
        file_lbl.pack(anchor=tk.E)
        num_lbl.pack(anchor=tk.E)
        asig_lbl.pack(anchor=tk.E)
        pseu_lbl.pack(anchor=tk.E)

        inf_display_frm = tk.Frame(sbj_inf_frm)
        inf_display_frm.pack(side=tk.RIGHT)

        # The text is contained in class variables so they can be modified.
        self.file_var = tk.StringVar()
        self.num_var  = tk.StringVar()
        self.asig_var = tk.StringVar()
        self.pseu_var = tk.StringVar()
        file_entry = tk.Label(inf_display_frm, textvariable=self.file_var)
        num_entry = tk.Label(inf_display_frm, textvariable=self.num_var)
        asig_entry = tk.Label(inf_display_frm, textvariable=self.asig_var)
        pseu_entry = tk.Label(inf_display_frm, textvariable=self.pseu_var)
        file_entry.pack(anchor=tk.E)
        num_entry.pack(anchor=tk.E)
        asig_entry.pack(anchor=tk.E)
        pseu_entry.pack(anchor=tk.E)

        edit_sbj_frm = tk.Frame(inf_frm)
        edit_sbj_frm.pack(side=tk.BOTTOM)

        # The command to verify the entry to the classification field.
        vcmd = (self.register(self.validate_group), '%P')
        # The entry for the chosen group classification
        clsfy_entry = tk.Entry(inf_frm, validate='key', validatecommand=vcmd)
        # The button to classify the selected subject.
        sbj_clsfy_btn = tk.Button(
            inf_frm, text='Classify', command=self.classify_event)
        clsfy_entry.pack(side=tk.LEFT)
        sbj_clsfy_btn.pack(side=tk.LEFT)

        def init_tables(treeview):
            """
            This code generalises the initialisation of the tables. all the 
            tables share the same headers.
            
            Parameters
            ----------
            treeview : ttk.Treeview
                The treeview object representing the table to be initialised.
            """
            treeview['columns'] = ('file_name', 'subject_number',
                                'expert_labels', 'pseudo_labels',)
            treeview.heading('subject_number', text='Subject Number')
            treeview.heading('file_name', text='File Name')
            treeview.heading('pseudo_labels', text='Predicted Group')
            treeview.heading('expert_labels', text='Allocated Group')
            # This hides the index column
            treeview['show'] = 'headings'

        # Init the table for storing the subject information
        self.all_sbj = ttk.Treeview(sbj_frm, selectmode='browse')
        self.all_sbj.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.all_sbj.bind('<ButtonRelease-1>', self.click_all_sbj)

        # Add a scrollbar to the table showing all the subjects
        sbj_scrollbar = tk.Scrollbar(sbj_frm)
        sbj_scrollbar.config(command = self.all_sbj.yview)
        sbj_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Call the generalised function to load in the subject data
        init_tables(self.all_sbj)

        # Init the table for the similiar subjects
        self.sim_sbj = ttk.Treeview(sim_frm, selectmode='browse')
        self.sim_sbj.pack(fill=tk.Y, expand=True)

        # Call the generalised function to load in the subject data
        init_tables(self.sim_sbj)

        # Init the table for the disimiliar subjects
        self.notsim_sbj = ttk.Treeview(dissim_frm, selectmode='browse')
        self.notsim_sbj.pack(fill=tk.Y, expand=True)

        # Call the generalised function to load in the subject data
        init_tables(self.notsim_sbj)

        # Choose an initial selection
        self.selected = len(self.sbj.data_frame['Expert Labels'].values)-1
        self.selected_sbj = self.sbj.data_frame.loc[self.selected]

        # Add data to the tables and information frame
        self.load_tables()
        self.load_inf()

        def init_pie(data):
            """
            This function initialises the figures. It is generalised to reduce
            repeated code.

            Parameters
            ----------
            data : list
                A list containing the data to be plotted to the figures.
            """

            figure = Figure(figsize=(4,2.5))
            ax = figure.add_subplot(111)

            plot_pie(ax, data)

            pie = FigureCanvasTkAgg(figure, self.fig_frm)
            pie.draw()

            self.update()
            return pie, ax

        # Init and Plot the information on the pie charts
        data = self.sbj.data_frame['Pseudo Labels'].values
        # Store the figures and axes in a class variable 
        self.group_pie, self.group_ax = init_pie(data)
        self.group_pie._tkcanvas.pack()

        data = self.sbj.data_frame['Expert Labels'].values
        self.assigned_pie, self.assigned_ax = init_pie(data)
        self.assigned_pie._tkcanvas.pack()

    def load_tables(self):
        """
        The function to extract the data from the selected subject. The 
        controller subject model stores the data. This function is called at
        initialisation and when a new subject is selected.
        """
        # Clear old data
        self.sim_sbj.delete(*self.sim_sbj.get_children())
        self.notsim_sbj.delete(*self.notsim_sbj.get_children())
        self.all_sbj.delete(*self.all_sbj.get_children())

        # The tuple format makes adding to the treeview widget simpler
        data = map(tuple, self.sbj.data_frame.values) 
        # Load the data for the main table
        populate_table(self.all_sbj, data)

        # Restore the selection to match the selection before it was cleared
        all_items = self.all_sbj.get_children()[::-1]
        item = all_items[self.selected]
        self.all_sbj.selection_set(item)

        # Get the disimiliar and similiar subjects
        top_10, last_10 = self.sbj.return_relevant_subjects(self.selected)

        # Add the similiar subjects to the table
        data = map(tuple, self.sbj.data_frame.values[top_10])
        populate_table(self.sim_sbj, data)

        # Add the disimiliar subjects to the table
        data = map(tuple, self.sbj.data_frame.values[last_10])
        populate_table(self.notsim_sbj, data)


    def load_inf(self):
        """
        The function to load the information regarding the selected subject.
        This function is called every time a new 
        """
        sbj = tuple(self.selected_sbj.values)
        file_name, subject_number, assigned_group, latent_group = sbj

        self.file_var.set(file_name)
        self.num_var.set(subject_number)
        self.asig_var.set(assigned_group)
        self.pseu_var.set(latent_group)

    def validate_group(self, ins_text):
        """
        The function to check the contents of the classify entry. The validate
        function refuses to set the entry to anything but a number. The number
        represents the particular class the expert is classifying the subject
        with. The function will allow numbers between 0-9.

        This function is bound to the classify entry.

        The validate function based upon this stack overflow answer:
        goo.gl/fYXBmX

        Parameters
        ----------
        ins_text : str
            The text which is being entered into the classify entry by the user.
            Accepted text will be integers between 0-9.
        """

        # Act sensibly if the entry is empty
        if not ins_text:
            self.group = None
            return True

        try:
            tmp = int(ins_text)
            # If the text is an integer between 0 and 9 accept
            if 1<= tmp <=9:
                self.group = tmp
                return True
            else:
                return False
        # Silence any value errors and reject the input
        except ValueError:
            return False

    def classify_event(self):
        """
        It stores the group chosen by the user in the subject model and calls
        all the functions to update the information in the GUI. This function
        is bound to the classify button. 
        """
        # Store the group chosen by the user in the subject model
        self.sbj.data_frame['Expert Labels'].values[self.selected] = self.group

        # Refresh the tables
        self.load_tables()
        # Refresh the selected subject information entry
        self.load_inf()
        # Refresh the figures
        self.load_pie()

    def load_pie(self):
        """
        This function clears the previous figures, loads the new data and 
        passes this data to the function which plots the data. Once that has
        returned the figures are drawn onto the GUI. It is an event handler 
        for the classify GUI event.
        """
        # Clear the outdated figures
        self.group_ax.clear()
        self.assigned_ax.clear()

        # Extract the new data
        group_plot_data = self.sbj.data_frame['Pseudo Labels'].values
        assigned_plot_data = self.sbj.data_frame['Expert Labels'].values

        # Plot the data
        plot_pie(self.group_ax, group_plot_data)
        plot_pie(self.assigned_ax, assigned_plot_data)

        # Show the new figures
        self.group_pie.draw()
        self.assigned_pie.draw()

    def click_all_sbj(self, event):
        """
        This function is an event handler for the mouse click event on the 
        table containing all the subjects.

        Parameters
        ----------
        event : tk.Event
            The mouse click event has to be passed to this event handler 
            function
        """
        # Get the inforation of the selected subject
        item = self.all_sbj.selection()[0]
        i_clicked = self.all_sbj.item(item)['values'][1]

        # Store the index of the selected subject in the class variable
        self.selected = i_clicked
        # Store the selected subject in the class variable
        self.selected_sbj = self.sbj.data_frame.loc[self.selected]

        # Refresh the data
        self.load_tables()
        self.load_inf()


# Module Specific Functions ---------------------------------------------------

def populate_table(treeview, data):
    """
    This function populate ALL the tables with the data stored in the 
    subject model. This function is called when the window is initialised,
    when a new subject is selected and when a subject has been classified.

    This function also contains the code to color the rows depending upon 
    the subjects assigned class. A global color variable is used so that 
    the colors are consistent throughout the GUI.

    Parameters
    ----------
    treeview : ttk.Treeview
        The treeview object representing the table to the data is inserted
        to.
    data : list
        A list of tuples containing the data to be added to the tables
    """
    # Get the global color definition
    global COLORS

    # The groups set tracks the number of groups the user has assigned
    groups = set()
    for values in data:
        # The expert assigned group
        i = str(values[2])
        # Store the assign
        groups.add(i)
        # Tag the row with the group so that it can be colored later
        treeview.insert('', 0, values=values, tag=i)

    # Convert to list to make iteration simpler
    groups = list(groups)

    # The 0 group represents unclassified subjects
    if len(groups)>1:
        groups = sorted(groups)[1:]

        # Color the rows using the tags defined previously
        count = 1
        for group in groups:
            treeview.tag_configure(group, background=COLORS[count])
            count += 1

def plot_pie(ax, data):
    """
    This function plots the figures in the GUI. It is general so that code
    is not repeated.

    Parameters
    ----------
    ax : 
        The axis the function should plot the pie chart on.
    data : list
        The data to be plotted on the axis.
    """
    # Count the occurance of each group label
    to_plot = np.bincount(data)

    # Init the labels, group 0 represents unclassified subjects
    labels = ['No group'] 
    # group numbering to the labels so that the display is more informative
    labels += ['group ' + str(x) for x in range(len(to_plot))][1:]

    # Copy the global variable locally so that it is not mutated
    global COLORS
    clrs = COLORS

    # No need to plot the 'no group' labels if there are none
    if to_plot[0] == 0:
        # Set remove the 'no group' data from the plot parameters
        to_plot = to_plot[1:]
        labels = labels[1:]
        clrs = clrs[1:]

    # Plot the data
    ax.pie(to_plot, labels=labels, autopct='%1.1f%%',
            colors=clrs, shadow=True)

    ax.axis('equal')
