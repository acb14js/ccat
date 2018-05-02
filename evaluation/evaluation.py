import subjects as subjects
import consensus as consensus
import matplotlib.pyplot as plt
import numpy as np
import toymodel
import sys

"""
There is no penalisation for incorrect number of groupings.
    Could divide by the number of found clusters as well
Need to now plot the results
The code to run the evaluation functions will be external to the software. 
because its specific to my file system.
"""

show = True
export = False

def groupify(thing):

    Lc = [[], []]

    count = 1
    for x in set(thing):
        tmp = []
        for i, y in enumerate(thing):
            if x == y:
                tmp.append(i)
                Lc[1].append(count)
        Lc[0].append(tmp)
        count += 1
    
    Lc = np.array(Lc)
    return Lc

def accuracy_fn(m, M, a):

    m = float(m)

    err = 0 

    for x in M:

        tmp = [] 
        for y in a:

            x = set(x)

            y = set(y)

            intersect = y.intersection(x)

            cardinality = len(intersect)

            tmp += [cardinality]
        
        err += max(tmp)

    return err/m

def evaluation_pipe(sbj, Lc, k):

    # Calculate method error --------------------------------------------------
    sbj.build_consensus_mx(k)
    sbj.max_modularity()

    M = sbj.pseudo_labels

    Mc = groupify(M)[0]

    m = sbj.num_subjects

    error = accuracy_fn(m, Mc, Lc[0])

    # Calculate kmedoid error -------------------------------------------------
    dis_mx = sbj.distance_mx
    data = np.mean(dis_mx, axis=0)

    _, clust = consensus.km.kMedoids(data, k)

    clust = np.array(clust.values())

    km_error = accuracy_fn(m, clust, Lc[0])

    # Calculate relevance function error --------------------------------------

    rel_error = np.zeros((2, m))

    for x in range(m):
        a, b = sbj.return_relevant_subjects(x)
        real_class = Lc[1][x]

        sim = 0
        disim = 0
        for aa in a:
            if Lc[1][aa] == real_class:
                sim += 1

        for bb in b:
            if Lc[1][bb] != real_class:
                disim += 1

        sim = sim/10.0
        disim = disim/10.0

        rel_error[0, x] = sim
        rel_error[1, x] = disim

    final_rel_error = np.mean(rel_error, axis=1)

    return error, km_error, final_rel_error

def total_pipe(fname, sbj, labels, kk=20):

    main_error = np.zeros((kk,2))
    medoid_error = np.zeros((kk,2))
    similiar_error = np.zeros((kk, 2))
    disimiliar_error = np.zeros((kk, 2))
    for k in range(2, kk):
        error, km_error, rel_error = evaluation_pipe(sbj, labels, k)
        sim, disim = rel_error
        main_error[k] = [k,error]
        medoid_error[k] = [k,km_error]
        similiar_error[k] = [k,sim]
        disimiliar_error[k] = [k,disim]

    print(main_error)
    print(medoid_error)
    print(similiar_error)
    print(disimiliar_error)

    # Now plot the results ----------------------------------------------------

    plt.figure(1)
    plt.xlabel('K')
    plt.ylabel('Accuracy')
    plt.title(
        r'$ \frac{1}{m}\sum^{M}_{i=1}max_{\alpha}| G_{\alpha} \cap C_i | $')
    plt.plot(main_error[:, 0][3:], main_error[:, 1]
             [3:], "rs-", label="Consensus")
    plt.plot(medoid_error[:, 0][3:], medoid_error[:, 1]
             [3:], "bo-", label="K-medoids")
    plt.legend(loc=4)

    global export
    if export:
        plt.savefig(fname+".pdf", bbox_inches='tight')

    global show
    if show:
        plt.show()

    plt.close('all')

    plt.figure(1)
    plt.xlabel('K')
    plt.ylabel('Accuracy')
    plt.title('Relevance Function Evaluation')
    plt.plot(similiar_error[:, 0][3:],
             similiar_error[:, 1][3:], "rs-", label="Similiar")
    plt.plot(disimiliar_error[:, 0][3:],
             disimiliar_error[:, 1][3:], "bo-", label="Disimiliar")
    plt.legend(loc=4)

    if export:
        plt.savefig(fname+"_relevance.pdf", bbox_inches='tight')

    if show:
        plt.show()

    plt.close('all')

def init_variables(sdir, fname, label_path, csv=None):

    sbj = subjects.Subject(sdir, fname, csv=csv)
    sbj.load_connectivity_mx()
    sbj.build_distance_mx()

    L = []
    with open(label_path) as f:
        L = f.read().splitlines()
    Lc = groupify(L)

    return sbj, Lc

def main():

    def toy():
        # Toymodel ------------------------------------------------------------
        print("Evaluation upon the Toymodel dataset")
        sbj, labels = toymodel.toymodel()

        # Start the evaluation pipeline.
        total_pipe('report/pictures/Toymodel_accuracy.pdf', sbj, labels)

    def ucs():
        print("Evaluation upon the UCS_MAC_PSP dataset")
        # UCS_MAC_PSP ---------------------------------------------------------

        # Init the variables for the evaluation
        fname = "evaluation_data/ucs_mac_psp/UCS_MAC_PSP_subject_model"
        sdir = "evaluation_data/ucs_mac_psp/connectivity"
        csv_path = "evaluation_data/ucs_mac_psp/UCSF_MAC_PSP_CSV"
        label_path = "evaluation_data/ucs_mac_psp/subject_labels_list.txt"
        sbj, labels = init_variables(sdir, fname, label_path, csv=csv_path)

        # Start the evaluation pipeline.
        total_pipe('evaluation_data/ucs_mac_psp/UCS_MAC_PSP', sbj, labels)

    def adhd():
        # ADHD200_CC200 -------------------------------------------------------
        print("Evaluation upon the ADHD200_CC200 dataset")

        # Init the variables for the evaluation
        fname = "evaluation_data/adhd_cc200/UCLA_AUTISM_subject_model"
        sdir = "evaluation_data/adhd_cc200/connectivity"
        csv_path = "evaluation_data/adhd_cc200/ADHD_EXTRACTED.csv"
        label_path = "evaluation_data/adhd_cc200/subject_labels_list.txt"
        sbj, labels = init_variables(sdir, fname, label_path, csv=csv_path)

        # Start the evaluation pipeline.
        total_pipe('evaluation_data/adhd_cc200/ADHD200_CC200', sbj, labels)

    def autism():
        # UCLA_AUTISM ---------------------------------------------------------
        print("Evaluation upon the UCLA_AUTISM dataset")

        # Init the variables for the evaluation
        fname = "evaluation_data/ucla_autism/UCLA_AUTISM_subject_model"
        sdir = "evaluation_data/ucla_autism/connectivity"
        csv_path = "evaluation_data/ucla_autism/UCLA_Autism.csv"
        label_path = "evaluation_data/ucla_autism/subject_labels_list.txt"
        sbj, labels = init_variables(sdir, fname, label_path, csv=csv_path)

        # Start the evaluation pipeline.
        total_pipe('evaluation_data/adhd_cc200/UCLA_AUTISM', sbj, labels)

    if len(sys.argv) > 1:

        if sys.argv[1] == "--toy":
            toy()
            sys.exit()

        if sys.argv[1] == "--ucs":
            ucs()
            sys.exit()

        if sys.argv[1] == "--adhd":
            adhd()
            sys.exit()
        
        if sys.argv[1] == "--autism":
            autism()
            sys.exit()

        if sys.argv[1] == "--all":
            toy()
            ucs()
            adhd()
            autism()
            sys.exit()

        print("Command Line arguement not recognised.")

if __name__ == '__main__':
    main()
