# CCAT - Connectome Clustering Analysis Tool
Version 0.1

![alt text](https://github.com/acb14js/ccat/blob/master/gui/icon.gif "CCAT icon")

## Table of Contents
1. [About](#about)
2. [Requirements](#requirements)
3. [Running](#running)
4. [Running Evaluation Code](#running-evaluation-code)
5. [Acknowledgements](#acknowledgements)

## About

CCAT was produced as a part of my 3rd year computer science dissertation at the University of Sheffield.

### Abstract

A software tool to improve the workflow of experts analysing Brain scans by 
  making use of unsupervised machine learning techniques.
Human analysis of MRI data is time consuming and requires experts to look 
  through many obtained scans with no order to their search.
The project aims to produce a software tool to sort the relevance of brain
  scans by using a consensus clustering technique and the connectome brain 
  network data structure.
The tool will offer a easy to use GUI frontend to enable experts to make use of 
  machine learning techniques without the need for technical skill.
A novel relevance function will be suggested to interperate the most relevant scans in comparison to the
  currently observed scan.
The GUI will update the list of relevant scans to help the expert 
  in the task of classification.

## Requirements

Python 2.7, numpy, matplotlib, scipy, pandas, bctpy and natsort

If pip is installed the requirements can be downloaded by executing the 
  following in a terminal:

```
pip install -r requirements.txt
```

## Running
The code can be run with this command

```
python2 gui/gui.py
```
 
## Running Evaluation Code

The algorithm can be tested upon sample datasets.
First download the evaluation code from https://goo.gl/CaUMWb.
The extract this into the evaluation folder.
From the application root directory run.

```
python2 evaluation/evaluation.py --ucs
```

The command line flag arguement defines which dataset the evaluation code will be run on.
The options are summarised in the table.

| Flag          | Dataset             | No. Subjects  | No. Nodes |
| ------------- |:-------------------:|:-------------:|:---------:|
| --toy         |The toy model dataset|100            |25 	      |	
| --adhd        |The dataset          |520            |190 	      |	
| --ucs         |the dataset          |64             |27 	      |	
| --autism      |the dataset          |79             |264        |

## Acknowledgments

I would like to thank Haiping Lu for supervising this project.

Also acknowledgments to Nigel Hoggard, for meeting and discussing the MRI pipeline with me.

