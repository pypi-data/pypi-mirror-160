"""
Takes care of data splitting into training / testing / evaluation
"""
import sklearn.model_selection as skm


def train_test_split(centroids, labels, test_size=0.2):
    """
    Splits data into train and test.
    centroids : N x 3 ( zyx ) array of centroids
    labels : 2D boolean array of labels
    :return:

    """
    X_train, X_test, y_train, y_test = skm.train_test_split(centroids, labels, test_size=test_size,
                                                            stratify=labels, random_state=42, shuffle=True)
    return X_train, X_test, y_train, y_test


def train_test_val_split(centroids, labels, test_fraction=0.2, val_fraction=0.2, verbose = False):
    """
    Splits data into train and test.
    centroids : N x 3 ( zyx ) array of centroids
    labels : 2D boolean array of labels
    :return:

    """

    withheld_fraction = test_fraction + val_fraction
    X_train, X_test_val, y_train, y_test_val = skm.train_test_split(centroids, labels,
                                                                    test_size=withheld_fraction,
                                                                    stratify=labels, random_state=42, shuffle=True)
    X_val, X_test, y_val, y_test = skm.train_test_split(X_test_val, y_test_val,
                                                        test_size=test_fraction / withheld_fraction,
                                                        stratify=y_test_val, random_state=22, shuffle=True)
    if verbose:
        print(f"X_train shape: {X_train.shape}")
        print(f"X_test shape: {X_test.shape}")
        print(f"X_val shape: {X_val.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"y_test shape: {y_test.shape}")
        print(f"y_val shape: {y_val.shape}")

    return X_train, X_test, X_val, y_train, y_test, y_val

# TODO :
# undersampling
# oversampling
