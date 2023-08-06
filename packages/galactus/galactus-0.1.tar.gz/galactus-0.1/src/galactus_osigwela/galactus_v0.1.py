#!/usr/bin/env python
# coding: utf-8

"""This is a basic prototype of the outlier detection system for RATT's transient and variable source detection project
    Designed and implemented by: Olwethu Sigwela
"""


PLOT = False
VERBOSE = False

def component_search(reducer, X_train, X_test, component_range = (1, 300), verbose = 0):
    
    """
    Experiment used to heuristically select the number of components for Principal Component Analysis (PCA)
    
    """
    
    pulsar_detected = []
    
    for c in range(component_range[0], component_range[1]):
        if verbose == 1:
            print(f"===# components: {c}===")
        dim_reducer = reducer(n_components = c)
        dim_reducer.fit(X_train)
        train_components = dim_reducer.transform(X_train)
        test_components = dim_reducer.transform(X_test)
#         clf = IsolationForest(random_state = 0, n_jobs = -1)
        clf = LocalOutlierFactor(novelty = True)
        clf.fit(train_components)
        
        test_predictions = clf.predict(test_components)
        if test_predictions[0] == -1:
            pulsar_detected.append(1)
            if verbose == 1:
                print("Pulsar detected")
        else:
            pulsar_detected.append(0)
            if verbose == 1:
                print("Pulsar not detected")
        if PLOT:
            sns.lineplot(x = [i for i in range(len(pulsar_detected))], y = pulsar_detected)
            plt.show()
        


from radiopadre import ls, settings
import pickle as pkl
import numpy as np

from astro_al import *

import seaborn as sns

from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM


n_strangest = 10 #how many of the strangest anomalies the AL system will display to the user
N_CLASSES = 5 #arbitrarily choose to divide the anomalies into five classes of increasing strangeness (as done in Astronomaly paper)


dd = ls()
data_dir = dd("obs3uhf")[0]("lightcurves")[0]
fits_dir = dd("obs3uhf")[0]





def get_data(directory, idx, data_type = "lc"): #small function for obtaining data from the file system
    
    """
    obtains data from the data directory
    
    """
    curves = []
    light_curves = directory
    for item in range(len(light_curves[idx])):
        candidate = light_curves[idx][item]
        if data_type in candidate.name:
            curves.append(candidate)
    return curves





def get_lightcurves(directory, start_idx = 0, end_idx = 340, switch = 0):
    #switch = 0 for light curves
    #switch = 1 for noise estimations
    #switch = 2 for source coordinates
    #switch = 3 for FITS files?
    
    curves = []
    for i in range(start_idx, end_idx):
        pickled_data = directory[i]("*.p")
        for pickled_datum in pickled_data:
            curves.append(pkl.load(open(pickled_datum.fullpath, "rb"))[switch])
    return curves

#test_frac = 0.01
test_frac = max(0, min(eval(input("Enter a test set fraction: ")), 1)) #ensures that fraction is between 0 and 1
num_dirs = data_dir.ndirs
train_end_idx = int(np.floor((1 - test_frac)*num_dirs))
test_start_idx = train_end_idx
test_end_idx = num_dirs

lightcurves = get_lightcurves(data_dir, end_idx = train_end_idx)
coords = get_lightcurves(data_dir, end_idx = train_end_idx, switch = 3)
test_curves = get_lightcurves(data_dir, start_idx = test_start_idx, end_idx = test_end_idx)
test_coords = get_lightcurves(data_dir, start_idx = test_start_idx, end_idx = test_end_idx, switch = 3)



lightcurve_idx = [i for i in range(len(lightcurves))]
test_curve_idx = [len(lightcurves) + i for i in range(len(test_curves))]


pulsar = lightcurves[0][:]
pulsar_coords = coords[0]
pulsar_idx = lightcurve_idx[0]

lightcurves = lightcurves[1:]
coords = coords[1:]
lightcurve_idx = lightcurve_idx[1:]

test_curves = [pulsar] + test_curves
test_coords = [pulsar_coords] + test_coords
test_curve_idx = [pulsar_idx] + test_curve_idx

X_train = lightcurves
X_test = test_curves




def get_pos(skymodel):
    ra = skymodel.pos.ra
    dec = skymodel.pos.dec
    dec_err = skymodel.pos.dec_err
    
    return (ra, dec, dec_err)




import math
def write_region(pos, radius = 20, coord_system = "FK5"):
    return f'{coord_system};circle({math.degrees(pos[0])},{math.degrees(pos[1])},{radius}")'

def write_crtf(pos, idx, outlier_score = 0, radius = 20, coord_system = "FK5"):

    colour_map = {0: "white", -0.6: "green", -0.9: "yellow", -1.2: "orange"}
    colour_thresholds = list(colour_map)
    colour = "red" #the final colour will only have the value "red" if it is an extreme outlier that exceeds all listed thresholds
    
    for threshold in colour_thresholds:
        if outlier_score >= threshold:
            colour = colour_map[threshold]
            break

    return f'circle[[{math.degrees(pos[0])}deg,{math.degrees(pos[1])}deg],{radius}pix], color={colour}, label="{idx} [{colour}]"'


pulsar_pos = get_pos(pulsar_coords)











from sklearn.decomposition import PCA
import pandas as pd
dim_reducer = PCA(n_components = 35)
dim_reducer.fit(lightcurves)
components = dim_reducer.transform(lightcurves)
test_components = dim_reducer.transform(test_curves)




components_df = pd.DataFrame(components)
test_components_df = pd.DataFrame(test_components)




import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt





from sklearn.ensemble import IsolationForest

print("Training model...")
clf = LocalOutlierFactor(novelty = True) 
clf.fit(components)

print("Generating test predictions...")
test_predictions = clf.decision_function(test_components) #continuous outlier score

binary_test_predictions = [-1 if i < 0 else 1 for i in test_predictions ]
binary_test_predictions_df = pd.DataFrame(binary_test_predictions)
binary_test_predictions_df.columns = ["score"]
N_COMPONENTS_TO_SHOW = 3

binary_test_df = pd.concat((test_components_df.iloc[:, :N_COMPONENTS_TO_SHOW], binary_test_predictions_df), axis = 1)

print("Writing predictions to region file...")

CRTF = True
region_radius = 20
region_file = None
index_file = None

if not CRTF:
    region_file = open("transient_regions.reg", "w")
    index_file = open("source_indices.txt", "w")
else:
    region_file = open("transient_regions.crtf", "w")
    region_file.write("#CRTF\n")
    index_file = open("source_indices.txt", "w")
    

for i in range(len(test_predictions)):
  
    if test_predictions[i] < 0: #if the continuous score is less than zero
         
        if PLOT:
            sns.lineplot(x = [j for  j in range(len(test_curves[i]))], y = test_curves[i])
            plt.show()

        skymodel = test_coords[i]
        position = get_pos(skymodel)
        if CRTF:
            if VERBOSE:
                print(write_crtf(position, test_curve_idx[i], test_predictions[i], radius = region_radius))
            region_file.write(write_crtf(position, test_curve_idx[i], test_predictions[i], radius = region_radius) + "\n")
        else:
            if VERBOSE:
                print(write_region(position, radius = region_radius))
            region_file.write(write_region(position, radius = region_radius) + "\n")
        
        index_file.write(str(test_curve_idx[i]) + "\n")
            
        
region_file.close()
index_file.close()

print("Done!")









