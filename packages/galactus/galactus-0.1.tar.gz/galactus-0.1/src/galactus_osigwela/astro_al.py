#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Much of this code is a modified version of the Astronomaly system presented by M. Lochner and B.A Bassett

# from astronomaly.base.base_pipeline import PipelineStage
# from astronomaly.base import logging_tools
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


class ScoreConverter:
    def __init__(self, lower_is_weirder=True, new_min=0, new_max=5, 
                 convert_integer=False, column_name='score',
                 **kwargs):
        """
        Convenience function to convert anomaly scores onto a standardised 
        scale, for use with the human-in-the-loop labelling frontend.
        Parameters
        ----------
        lower_is_weirder : bool
            If true, it means the anomaly scores in input_column correspond to 
            a lower is more anomalous system, such as output by isolation 
            forest.
        new_min : int or float
            The new minimum score (now corresponding to the most boring 
            objects)
        new_max : int or float
            The new maximum score (now corresponding to the most interesting 
            objects)
        convert_integer : bool
            If true will force the resulting scores to be integer.
        column_name : str
            The name of the column to convert to the new scoring method. 
            Default is 'score'. If 'all' is used, will convert all columns 
            the DataFrame.
        """
#         super().__init__(lower_is_weirder=lower_is_weirder, new_min=new_min, 
#                          new_max=new_max, **kwargs)
        self.lower_is_weirder = lower_is_weirder
        self.new_min = new_min
        self.new_max = new_max
        self.convert_integer = convert_integer
        self.column_name = column_name

    def _execute_function(self, df):
        """
        Does the work in actually running the scaler.
        Parameters
        ----------
        df : pd.DataFrame or similar
            The input anomaly scores to rescale.
        Returns
        -------
        pd.DataFrame
        Contains the same original index and columns of the features input 
        with the anomaly score scaled according to the input arguments in 
        __init__.
        """
        print('Running anomaly score rescaler...')

        if self.column_name == 'all':
            cols = df.columns
        else:
            cols = [self.column_name]
        try:
            scores = df[cols]
        except KeyError:
            msg = 'Requested column ' + self.column_name + ' not available in                     input dataframe. No rescaling has been performed'
#             logging_tools.log(msg, 'WARNING')
            print(msg, 'WARNING')
            return df

        if self.lower_is_weirder:
            scores = -scores

        scores = (self.new_max - self.new_min) * (scores - scores.min()) /             (scores.max() - scores.min()) + self.new_min

        if self.convert_integer:
            scores = round(scores)

        return scores


class NeighbourScore:
    def __init__(self, min_score=0.1, max_score=5, alpha=1, **kwargs):
        """
        Computes a new anomaly score based on what the user has labelled,
        allowing anomalous but boring objects to be rejected. This function
        takes training data (in the form of human given labels) and then
        performs regression to be able to predict user scores as a function of
        feature space. In regions of feature space where the algorithm is
        uncertain (i.e. there was little training data), it simply returns
        close to the original anomaly score. In regions where there was more
        training data, the anomaly score is modulated by the predicted user
        score resulting in the user seeing less "boring" objects.
        Parameters
        ----------
        min_score : float
            The lowest user score possible (must be greater than zero)
        max_score : float
            The highest user score possible
        alpha : float
            A scaling factor of how much to "trust" the predicted user scores.
            Should be close to one but is a tuning parameter.
        """
#         super().__init__(min_score=min_score, max_score=max_score, alpha=alpha, 
#                          **kwargs)
        self.min_score = min_score
        self.max_score = max_score
        self.alpha = alpha

    def anom_func(self, nearest_neighbour_distance, user_score, anomaly_score):
        """
        Simple function that is dominated by the (predicted) user score in 
        regions where we are reasonably sure about our ability to predict that 
        score, and is dominated by the anomaly score from an algorithms in 
        regions we have little data.
        Parameters
        ----------
        nearest_neighbour_distance : array
            The distance of each instance to its nearest labelled neighbour.
        user_score : array
            The predicted user score for each instance
        anomaly_score : array
            The actual anomaly score from a machine learning algorithm
        Returns
        -------
        array
            The final anomaly score for each instance, penalised by the
            predicted user score as required.
        """

        f_u = self.min_score + 0.85 * (user_score / self.max_score)
        d0 = nearest_neighbour_distance / np.mean(nearest_neighbour_distance)
        dist_penalty = np.exp(d0 * self.alpha)
        
        
        return anomaly_score * np.tanh(dist_penalty - 1 + np.arctanh(f_u)) #relevance score, as described in the Astronomaly paper

    def compute_nearest_neighbour(self, features_with_labels):
        """
        Calculates the distance of each instance to its nearest labelled
        neighbour. 
        Parameters
        ----------
        features_with_labels : pd.DataFrame
            A dataframe where the first columns are the features  and the last
            two columns are 'human_label' and 'score' (the anomaly score from
            the ML algorithm).
        Returns
        -------
        array
            Distance of each instance to its nearest labelled neighbour.
        """
        features = features_with_labels.drop(columns=['human_label', 'score'])
        # print(features)
        label_mask = features_with_labels['human_label'] != -1
        labelled = features.loc[features_with_labels.index[label_mask]].values
        features = features.values

        mytree = cKDTree(labelled)
        distances = np.zeros(len(features))
        for i in range(len(features)):
            dist = mytree.query(features[i])[0]
            distances[i] = dist
        # print(labelled)
        return distances

    def train_regression(self, features_with_labels):
        """
        Uses machine learning to predict the user score for all the data. The
        labels are provided in the column 'human_label' which must be -1 if no
        label exists.
        Parameters
        ----------
        features_with_labels : pd.DataFrame
            A dataframe where the first columns are the features  and the last
            two columns are 'human_label' and 'score' (the anomaly score from
            the ML algorithm).
        Returns
        -------
        array
            The predicted user score for each instance.
        """
        label_mask = features_with_labels['human_label'] != -1
        inds = features_with_labels.index[label_mask]
        features = features_with_labels.drop(columns=['human_label', 'score'])
        reg = RandomForestRegressor(n_estimators=100)
        print(inds)
        reg.fit(features.loc[inds], 
                features_with_labels.loc[inds, 'human_label'])

        fitted_scores = reg.predict(features)
        return fitted_scores

    def combine_data_frames(self, features, ml_df):
        """
        Convenience function to correctly combine dataframes.
        """
        return pd.concat((features, ml_df), axis=1, join='inner')

    def _execute_function(self, features_with_labels):
        """
        Does the work in actually running the NeighbourScore.
        Parameters
        ----------
        features_with_labels : pd.DataFrame
            A dataframe where the first columns are the features  and the last
            two columns are 'human_label' and 'score' (the anomaly score from
            the ML algorithm).
        Returns
        -------
        pd.DataFrame
            Contains the final scores using the same index as the input.
        """
        
#         print(f"run (1) features_with_labels shape = {features_with_labels.shape}")
        distances = self.compute_nearest_neighbour(features_with_labels)
#         print(f"run (2) distances shape = {distances.shape}")
        regressed_score = self.train_regression(features_with_labels)
#         print(f"run (3) regressed score = {regressed_score}")
        trained_score = self.anom_func(distances, 
                                       regressed_score, 
                                       features_with_labels.score.values)
#         print(f"run (4) trained_score = {trained_score}")
        dat = np.column_stack(([regressed_score, trained_score]))
#         print(f"run (5) dat = {dat}")
        
        output_df = pd.DataFrame(data=dat, 
                            index=features_with_labels.index, 
                            columns=['predicted_user_score', 'trained_score'])
        
#         print(f"output_df = {output_df}")
        
        return output_df
    
    def run(self, features_with_labels): #my own addition
#         print(f"run (0) features_with_labels shape = {features_with_labels.shape}")
        return self._execute_function(features_with_labels)


# In[ ]:


def run_active_learning(active_learning, features, anomaly_scores):
        """
        Runs the selected active learning algorithm.
        """
        
        anomaly_scores_output_copy = anomaly_scores.copy(deep = True)

        has_no_labels = 'human_label' not in anomaly_scores.columns
        labels_unset = np.sum(anomaly_scores['human_label'] != -1) == 0
        if has_no_labels or labels_unset:
            print("Active learning requested but no training labels "
                  "have been applied.")
            return "failed"
        else:
            pipeline_active_learning = active_learning
            features_with_labels =                 pipeline_active_learning.combine_data_frames(
                    features, anomaly_scores)
#             print(f"run_active_learning (0) features_with_labels shape = {features_with_labels.shape}")
            active_output = pipeline_active_learning.run(features_with_labels)
#             print(f"run_active_learning (1) active_output = {active_output}")
            
#             print(active_output.head(100))
#             print(f"active_output.columns = {active_output.columns}")

            # This is safer than pd.combine which always makes new columns
            
            
            
            for col in active_output.columns:
                anomaly_scores_output_copy[col] =                     active_output.loc[anomaly_scores.index, col]
            return anomaly_scores_output_copy


# In[ ]:

def scale_values(values, min_target, max_target, debug_mode = False):

    output = []
#     print("---------values-----------------------")
#     print(values)
#     print("--------------------------------------")
#     print(f"r_max = {r_max}")
#     print(f"max_target = {max_target}")
#     print(f"min_target = {min_target}")
    
    #step1: convert all positive values to zero:
    step1_list = list(values)
    
    if debug_mode:
        print(f"initial step1_list = {step1_list}")
    
    for i in range(len(step1_list)):
        if step1_list[i] > 0:
            step1_list[i] = 0
    
    
    if debug_mode:
        print("--------------step1_list-----------------------------------")
        print(step1_list)
        print("------------------------------------------------------------")

    
    #step2: make the remaining negative values positive
    inverted_values = -np.ravel(np.array(step1_list))
    step2_array = inverted_values
    
    if debug_mode:
        print("--------------step2_array-----------------------------------")
        print(step2_array)
        print("------------------------------------------------------------")
#     print("-----------------------inverted values-----------------")
#     print(inverted_values)
#     print(inverted_values.shape)
#     print("-------------------------------------------------------")
    
    non_zero_indices = [i for i in range(len(step2_array)) if step2_array[i] != 0]
    non_zero_elements = [step2_array[j] for j in non_zero_indices]
    
    step3_array = np.array(non_zero_elements)
    
    
    #step4: perform range scaling
    r_min = min(step3_array)
    r_max = max(step3_array)
    
    scaled_values = (((step3_array - r_min)/(r_max - r_min))*(max_target - min_target)) + min_target
    
    if debug_mode:
        print("--------------step4_array-----------------------------------")
        
    step4_list = list(np.copy(step2_array))
    
    for k in range(len(scaled_values)):
        step4_list[non_zero_indices[k]] = scaled_values[k]
    
    step4_array = np.array(step4_list)
    
    if debug_mode:
        print(step4_array)
        print("------------------------------------------------------------")
    
    #step4: turn any residual negative values to zero
    list_output = list(step4_array)
    
    for i in range(len(list_output)):
        if list_output[i] != 0:
            list_output[i] = max(1, round(abs(max(list_output[i], 0))))
        elif list_output[i] < 0:
            list_output[i] = 0
    
    step5_array = np.array(list_output)
    
    output = step5_array
    
    if debug_mode:
        print("--------------step5_array-----------------------------------")
        print(step5_array)
        print("------------------------------------------------------------")
    
    
    return output



