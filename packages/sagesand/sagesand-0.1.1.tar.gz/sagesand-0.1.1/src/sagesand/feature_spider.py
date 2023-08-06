"""FeatureSpider: A Spider for data/feature investigation and QA"""
# License: Apache 2.0 ©SuperCowPowers LLC
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# Feature Spider Class
class FeatureSpider:
    def __init__(self, df, features: list, target: str):

        # Check for expected columns (used later)
        for column in ['ID', 'SMILES', target]:
            if column not in df.columns:
                print(f'DataFrame does not have required {column} Column!')
                return

        # Set internal vars that are used later
        self.df = df
        self.features = features
        self.target = target
        self.source = df['Source'].values if 'Source' in df else None

        # Build our KNN model pipeline with StandardScalar
        knn = KNeighborsRegressor(n_neighbors=5, weights='distance')
        self.pipe = make_pipeline(StandardScaler(), knn)

        # Fit Model on features and target
        y = df[target]
        X = df[features]
        self.pipe.fit(X, y)

        # Grab the Standard Scalar and KNN from the pipeline model
        # Note: These handles need to be constructed after the fit
        self.scalar = self.pipe['standardscaler']
        self.knn = self.pipe['kneighborsregressor']

    def get_feature_matrix(self):
        """Return the KNN Model Internal Feature Matrix"""
        return self.knn._fit_X

    def predict(self, pred_df) -> list:
        """Provide a prediction from the KNN Pipeline model (knn_prediction)"""
        return self.pipe.predict(pred_df[self.features])

    def confidence_scores(self, pred_df, model_preds=None) -> list:
        """Compute Confidence Scores for each Prediction"""

        # Get all the KNN information relevant to this calculation
        neighbor_info = self.neighbor_info(pred_df)

        # Handles for all the relevant info
        knn_preds = neighbor_info['knn_prediction']
        target_values = neighbor_info['knn_target_values']
        distances = neighbor_info['knn_distances']

        # We can score confidence even if we don't have model predictions (less good)
        if model_preds is None:
            model_preds = knn_preds
            stddev_multiplier = 1.5
        else:
            stddev_multiplier = 1.0

        # Now a big loop over all these values to compute the confidence scores
        confidence_scores = []
        for pred, knn_pred, str_val_list, str_dist_list in zip(model_preds, knn_preds, target_values, distances):
            # Each of these is a string of a list (yes a bit cheesy)
            vals = [float(val) for val in str_val_list.split(', ')]
            _ = [float(dis) for dis in str_dist_list.split(', ')]  # dist current not used

            # Compute stddev of the target values
            knn_stddev = np.std(vals)

            # Confidence Score
            conf = 0.5 * (2.0 - abs(float(pred) - float(knn_pred)))
            conf -= knn_stddev * stddev_multiplier

            # Confidence score has min-max of 0-1
            conf = min(max(conf, 0), 1)

            confidence_scores.append(conf)

        # Return the confidence scores
        return confidence_scores

    def neighbor_info(self, pred_df) -> pd.DataFrame:
        """Provide information on the neighbors (prediction, knn_target_values, knn_distances)"""

        # Make sure we have all the features
        if not set(self.features) <= set(pred_df.columns):
            print(f'DataFrame does not have required features: {self.features}')
            return None

        # Run through scaler
        x_scaled = self.scalar.transform(pred_df[self.features])

        # Add the data to a copy of the dataframe
        results_df = pd.DataFrame()
        results_df['knn_prediction'] = self.knn.predict(x_scaled)

        # Get the Neighbors Information
        neigh_dist, neigh_ind = self.knn.kneighbors(x_scaled)
        target_values = self.knn._y[neigh_ind]

        # Note: We're assuming that the Neighbor Index is the same order/cardinality as the dataframe
        results_df['knn_target_values'] = [', '.join([str(val) for val in values]) for values in target_values]
        results_df['knn_distances'] = [', '.join([str(dis) for dis in distances]) for distances in neigh_dist]

        # Do we have Source data
        if self.source is not None:
            results_df['sources'] = [self.source[index] for index in neigh_ind]
        return results_df

    def neighbor_ids(self, pred_df) -> pd.DataFrame:
        """Provide id + smiles for the neighbors (knn_ids, knn_smiles)"""

        # Run through scaler
        x_scaled = self.scalar.transform(pred_df[self.features])

        # Add the data to a copy of the dataframe
        results_df = pred_df.copy()

        # Neighbor ID/SMILE lookups
        neigh_dist, neigh_ind = self.knn.kneighbors(x_scaled)
        results_df['knn_ids'] = [', '.join(self.df.iloc[index]['ID'] for index in indexes) for indexes in neigh_ind]
        results_df['knn_smiles'] = [', '.join(self.df.iloc[index]['SMILES'] for index in indexes) for indexes in neigh_ind]
        return results_df

    def coincident(self, target_diff, verbose=True):
        """Convenience method that calls high_gradients with a distance of 0"""
        return self.high_gradients(0.0, target_diff, verbose)

    def high_gradients(self, within_distance, target_diff, verbose=True) -> list:
        # This basically loops over all the X features in the KNN model
        # - Grab the neighbors distances and indices
        # - For neighbors `within_distance`* grab target values
        # - If target values have a difference > `target_diff` (in our case logS Mol(-1))
        #     - List out the details of the observations and the distance, target diff
        #
        # *standarized feature space
        high_gradient_indexes = set()
        for my_index, obs in enumerate(self.knn._fit_X):
            neigh_distances, neigh_indexes = self.knn.kneighbors([obs])
            neigh_distances = neigh_distances[0]  # Just ONE observation
            neigh_indexes = neigh_indexes[0]  # Just ONE observation
            target_values = self.knn._y[neigh_indexes]

            # Grab the info for this observation
            my_id = self.df.iloc[my_index]['ID']
            my_smile = self.df.iloc[my_index]['SMILES']
            my_target = self.knn._y[my_index]

            # Loop through the neighbors
            # Note: by definition this observation will be in the neighbors so account for that
            for n_index, dist, target in zip(neigh_indexes, neigh_distances, target_values):

                # Skip myself
                if n_index == my_index:
                    continue

                # Lower diagonal
                if n_index < my_index:
                    continue

                # Compute logS differences `within_distance` feature space
                logs_diff = abs(my_target - target)
                if dist <= within_distance and logs_diff > target_diff:

                    # Add these observations (rows) to high gradient index list
                    high_gradient_indexes.add(my_index)
                    high_gradient_indexes.add(n_index)

                    # Print out the info about both observations
                    if verbose:
                        print(f"\nFeature Dist: {dist}: logS Diff: {logs_diff:.2f}")
                        source = self.df.iloc[my_index]['Source'] if self.source else 'No Source'
                        print(f"{my_id}({my_target:.2f}): {my_smile} {source}")
                        neighbor_id = self.df.iloc[n_index]['ID']
                        neighbor_smile = self.df.iloc[n_index]['SMILES']
                        n_source = self.df.iloc[n_index]['Source'] if self.source else 'No Source'
                        print(f"{neighbor_id}({target:.2f}): {neighbor_smile} {n_source}")

        # Return the full list of indexes that are part of high gradient pairs
        return list(high_gradient_indexes)


def test():
    """Test for the Feature Spider Class"""
    # Make some fake data
    data = {'ID': ['IVC-123-1', 'IVC-124-1', 'IVC-125-1', 'IVC-125-2', 'IVC-126-1'],
            'SMILES': ['CC1(C)[C@@H]2C[C@H]1C2(C)C',
                       'CC1(C)[C@H]2C[C@@H]1C2(C)C',
                       'C[C@]12O[C@H]1C[C@H]1C[C@@H]2C1(C)C',
                       'C[C@]12O[C@H]1C[C@H]1C[C@@H]2C1(C)C',
                       'CC(C)[C@@H]1CC[C@@H](C)C[C@H]1OC(=O)[C@H](C)O'],
            'feat1': [1.0, 1.0, 1.1, 3.0, 4.0],
            'feat2': [1.0, 1.0, 1.1, 3.0, 4.0],
            'feat3': [0.1, 0.1, 0.2, 1.6, 2.5],
            'logS': [-3.1, -6.0, -6.0, -4.0, -2.0]}
    data_df = pd.DataFrame(data)

    # Create the class and run the taggers
    f_spider = FeatureSpider(data_df, ['feat1', 'feat2', 'feat3'], 'logS')
    preds = f_spider.predict(data_df)
    print(preds)
    coincident = f_spider.coincident(2)
    print('COINCIDENT')
    print(coincident)
    high_gradients = f_spider.high_gradients(2, 2)
    print('\nHIGH GRADIENTS')
    print(high_gradients)


if __name__ == '__main__':
    test()
