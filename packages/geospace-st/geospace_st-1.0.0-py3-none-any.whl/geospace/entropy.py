# TODO: put this file somewhere else

import scipy.stats

import numpy as np

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import adjusted_rand_score

from geospace.hotspot.hotspot import _compute_cutoff


def entropy(adata, labels, pca=True, dim=16, depth=10, output_label="entropy", use_raw=False):
    X, y = get_data_and_labels(adata, labels, pca, dim, use_raw=use_raw)
    clf = RandomForestClassifier(max_depth=depth)
    clf.fit(X, y)

    class_probs = clf.predict_proba(X)
    entropy = scipy.stats.entropy(class_probs, axis=1)

    adata.obs[output_label] = entropy
    entropy_binary = np.zeros(entropy.shape)
    cutoff = _compute_cutoff(entropy)
    entropy_binary[entropy > cutoff] = 1
    # TODO: figure out all these labels
    adata.obs["entropy_binary"] = entropy_binary

    # TODO: also compute the scaled entropy or whatever
    scaled_entropy = np.empty(entropy.shape)
    for c in y:
        scaled_entropy[y == c] = scipy.stats.zscore(entropy[y == c])
    adata.obs["scaled_entropy"] = scaled_entropy


def forest_depth_analysis(adata, labels, depths=None, pca=True, dim=16, verbose=True):
    # TODO: rewrite this with proper cross validation and stuff
    if depths is None:
        depths = list(range(2, 15))
    X, y = get_data_and_labels(adata, labels, pca, dim)
    # TODO: shuffle properly
    train_cutoff = round(0.8 * len(adata))
    X_train = X[:train_cutoff, :]
    y_train = y[:train_cutoff]

    X_test = X[train_cutoff:, :]
    y_test = y[train_cutoff:]

    train_scores = []
    test_scores = []
    test_aris = []
    for depth in depths:
        clf = RandomForestClassifier(max_depth=depth)
        clf.fit(X_train, y_train)
        train_score = clf.score(X_train, y_train)
        test_score = clf.score(X_test, y_test)
        ari = adjusted_rand_score(clf.predict(X_test), y_test)
        train_scores.append(train_score)
        test_scores.append(test_score)
        test_aris.append(ari)
        if verbose:
            print("Depth %d: Train %f - Test %f - ari %f" % (depth, train_score, test_score, ari))

    return depths, test_aris


def get_data_and_labels(adata, labels, pca, dim, use_raw=False):
    if use_raw:
        adata_to_use = adata.raw
    else:
        adata_to_use = adata
    try:
        data = adata_to_use.X.toarray()
    except AttributeError:
        data = adata_to_use.X
    if pca:
        # Reduce dimensions using PCA
        pca_transform = PCA(n_components=dim)
        X = pca_transform.fit_transform(data)
    else:
        X = data

    # labels provided either as list or key in adata.obs
    try:
        y = adata.obs[labels]
    except IndexError:
        y = labels

    return X, y