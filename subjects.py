"""\
Consensus Clustering method for connectomes.
"""
import numpy as np
import pandas as pd
from glob import glob
import pickle
import natsort
from difflib import SequenceMatcher
import sys

# Local packages
import consensus

class Subject:
    """
    This is the subject model class which stores information about the set of 
    subjects. Code to manipulate the set of subjects is kept general and 
    seperate so that it can be easily maintained.
    """
    def __init__(self, directory, f_name, csv=None):
        self.f_name = f_name
        self.directory = directory
        self.csv = None
        if csv != None:
            try:
                self.csv = pd.read_csv(csv)
            except(IOError):
                print("Invalid csv path")
        
    def load_connectivity_mx(self):
        """
        This function loads the connectivity matrices from the chosen 
        directory. The csv file is then searched for a column which matches 
        the filenames in the directory. This assumes that the filenames have
        been given meaningful names. The order of the loaded filenames is 
        rearranged to match the order in the csv file. This is so that the 
        latent group information can be appended to the csv. Finally the data
        is loaded from the files and stored in class variables
        """
        print("Finding the  directory...")
        # Load the file names
        fnames_paths = glob(self.directory + "/*.txt")

        # Glob does not throw an error if the directory is invalid
        if fnames_paths == []:
            print("Invalid directory")
            return

        # Remove the path
        fnames = map(lambda tmp: tmp[-tmp[::-1].find('/'):], fnames_paths)

        print("Ordering filenames...")
        indexes = None 
        # Check if the user has defined a CSV file
        if type(self.csv) != type(None):

            if len(fnames_paths) != len(self.csv):
                print("Mismatch between CSV and loaded connectivity matrices")
                exit

            print("Extracting meaningful CSV column...")
            column = extract_column(self.csv.values, fnames[0])

            print("Column "+str(column))

            print("Matching CSV order...")
            # Get the csv column with the correct file order.
            real_order = self.csv.values[:, column]
            indexes = reorder_fn(real_order, fnames)

        else:
            # If no CSV sort the filenames in the same way as file explorers
            print("No CSV, Human sorting...")
            indexes = natsort.index_humansorted(fnames)

        # Apply the reordering
        fnames = np.array(fnames)
        fnames = fnames[indexes]
        fnames_paths = np.array(fnames_paths)
        fnames_paths = fnames_paths[indexes]

        print("Loading from the directory...")
        # Load the data from the files
        files = np.array([np.loadtxt(f) for f in fnames_paths])

        print("Assinging values...")
        # Assign the values to the class variables
        self.connectivity_mx = files
        m, n, n = self.connectivity_mx.shape
        self.num_subjects = m
        self.num_nodes = n
        # Init the pandas data frame
        self.data_frame = pd.DataFrame({"File Names" : fnames})
        # Add the index to a named column
        self.data_frame['Subject Number'] = self.data_frame.index
        # Initialise the user defined groups with zeros
        self.data_frame["Expert Labels"] = pd.Series(np.zeros(m, dtype=np.int64))

        print("Connectivity matrix loaded.")
        
    def build_distance_mx(self):
        """
        The function calls the external distance matrix function and stores 
        the result in a class variable.
        """
        # Extract the connectivity matrix
        connectivity_mx = self.connectivity_mx

        # Pass the connectivity matrix to the distance matrix function
        self.distance_mx = consensus.distance_matrix(connectivity_mx)
    
    def build_consensus_mx(self, ks):
        """
        The function calls the external consensus matrix function and stores 
        the result in a class variable. The distance matrix musst be built 
        first.

        Parameters
        ----------
        ks : int
            The value that the consensus algorithm iterates over.
        """
        # Complain if the distance matrix has not been built
        if type(self.distance_mx) == type(None):
            print("Invalid pipeline, build the distance matrix first.")
            return

        # Extract the distance matrix
        distance_mx = self.distance_mx

        # Pass the distance matrix to the consensus matrix function
        self.consensus_mx = consensus.consensus_matrix(distance_mx, ks)

    def max_modularity(self):
        """
        The function calls the external modularity maximisation function and 
        stores the result in a class variable. The consensus matrix must be 
        built first.
        """
        # Complain if the consensus matrix has not been built
        if type(self.consensus_mx) == type(None):
            print("Invalid pipeline, build the consensus matrix first.")
            return

        print("Maximizing modularity...")
        consensus_mx = self.consensus_mx

        partition = consensus.modularity_maximisation(consensus_mx)

        self.pseudo_labels = partition
        self.data_frame["Pseudo Labels"] = pd.Series(partition, 
            index=self.data_frame.index)

        print("Modularity maximised.")

    def save_model(self, compressed=True):
        """
        This function saves the model at the declared path. The file is 
        compressed by default.
        """
        print("Saving the model...")

        if compressed:
            # Theses data structures can be thrown away
            self.connectivity_mx = None
            self.distance_mx = None

        with open(self.f_name, 'wb') as f:
            pickle.dump(self, f)
            self.data_frame.to_csv(self.f_name+"_csv.csv")

    def return_relevant_subjects(self, index):
        """
        This function returns the similiar and dissimiliar subjects. it loads
        the consensus matrix and 

        Parameters
        ----------
        index : int
            The index of the selected subject.
        """
        similarity = self.consensus_mx[index]

        # Get the sorted index of the selected subjects features, ascending
        sorted_args = np.argsort(similarity)

        # The first element is the selected subject itself
        last_10 = sorted_args[1:11]

        # Reverse the order of the list
        sorted_args = sorted_args[::-1]

        # Store the 10 most similiar subjects
        top_10 = sorted_args[0:10]

        return top_10, last_10
    
    def default_pipeline(self, save=True, ks=20):
        """
        This function describes the default pipeline. This is so that external
        calls to the pipeline are consistent
        """
        self.load_connectivity_mx()
        self.build_distance_mx()
        self.build_consensus_mx(ks)
        self.max_modularity()
        if save:
            self.save_model()


# Module Specific Functions ---------------------------------------------------

def extract_column(csv, fname):
    """
    This function searches a CSV file for a column which matches thi given 
    filename.

    Parameters
    ----------
    fname : str
        The filename to search the CSV by.
    """
    score = 0
    column = 0
    for x in csv:
        i = 0
        for y in x:
            # Skip if the column is the wrong type
            if type(y) == type(fname):
                # Get a similarity score between the fname and CSV string
                curr_score = similar(fname, y)
                # If the current score is highest store the column index
                if curr_score > score:
                    score = curr_score
                    column = i
            i += 1
    
    return column

def reorder_fn(real_order, sbj_order):
    """
    This function iterativly searches a list for a similiar string and stores
    the index.

    Parameters
    ----------
    real_order : list
        The filename order in the CSV.
    sbj_order : list
        The filename order of the subjects.
    """
    count = len(sbj_order)
    sim_store = [[0, 0, "", ""]] * count

    for x in range(count):
        for y in range(count):
            real = real_order[x]
            subj = sbj_order[y]

            prev_score = sim_store[x][1]
            prev_index = sim_store[x][0]
            curr_score = similar(real, subj)
            curr_index = y

            # If the current score is best then store the index
            if curr_score > prev_score:
                sim_store[x] = [curr_index, curr_score, real, subj]

    # Convert to a numpy array to allow for slicing by lists.
    sim_store = np.array(sim_store)
    # Store the new index order in a list
    new_indexes = np.array(sim_store[:, 0], dtype=int)

    return new_indexes

def similar(a, b):
    """
    This function returns a similarity score between tow strings

    Parameters
    ----------
    a : str
        The string to be compare.
    b : str
        The string to compare to.
    """
    return SequenceMatcher(None, a, b).ratio()
