import math
import numpy as np
import subjects
import consensus
import pandas as pd
import evaluation

"""
I should call the toymodel code from the eval code. 
The toymodel will replace the distance matrix with the synthetic one. 
It will also return the real label list.
There is no need to extend the subjects class.
will be easier to make a subject model and then rename the distance matrix manually. 
"""

def split_for_a_range(total, groups):
        division = total/groups*1.0
        return [int(math.ceil(x/division)) for x in range(1,total+1)]

class SyntheticSubjects(subjects.Subject):
    def __init__(self, total, nodes, groups, rel, relrange, etcrange):
        print("Initializing subjects")
        self.num_subjects = total
        self.num_nodes = nodes
        fake_data = np.arange(total)
        self.data_frame = pd.DataFrame({"File Names": fake_data})

        print("Producing synthetic distance matrix")
        np.random.seed(0)  # Seed for reproducibility
        un_rel = nodes - rel

        print("Assigning subject groups")
        subjects = split_for_a_range(total, groups)
        self.groups = subjects

        # Matrix of subjects, data sets to compare.
        self.distance_mx = np.zeros((nodes, total, total))

        for node in range(rel):
            # select a subject from the x dimension of the matrix.
            for xsub in range(total):
                # select a subject from the y dimension of the matrix.
                for ysub in range(total):
                    if xsub == ysub:
                        self.distance_mx[node, xsub, ysub] = 0.0
                        continue  # skip the computation
                    if subjects[xsub] == subjects[ysub]:
                        self.distance_mx[node, xsub, ysub] = np.random.uniform(
                            relrange[0], relrange[1])
                    else:
                        self.distance_mx[node, xsub, ysub] = np.random.uniform(
                            etcrange[0], etcrange[1])

        self.distance_mx[rel:, :, :] = np.random.uniform(
            etcrange[0], etcrange[1], (un_rel, total, total))
        for node in range(un_rel):
            np.fill_diagonal(self.distance_mx[rel+node], 0.0)

        print("produced!")

def toymodel(k=20):
    num_subjects = 100 # Simulate a set of 100 subjects.
    num_nodes = 30 # With 30 nodes each.
    meta_groups = 4 # Split into 4 groups.
    rel_range = (0.1, 0.4) # Range for the relevant node random distance.
    rest_range = (0.2, 0.4) # Range for the other node random distance.
    relevant_nodes = 10 # The number of nodes considered relevant.
    subject_model = SyntheticSubjects(num_subjects,
                                    num_nodes,
                                    meta_groups,
                                    relevant_nodes,
                                    rel_range,
                                    rest_range)

    subject_model.build_consensus_mx(k)
    subject_model.max_modularity()

    labels = subject_model.groups

    labels = evaluation.groupify(labels)

    return subject_model, labels

if __name__ == '__main__':
    toymodel()
