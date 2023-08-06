from typing import List
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

from pyod.models.ecod import ECOD
from pyod.models.copod import COPOD
from pyod.models.abod import ABOD
from pyod.models.sos import SOS
from pyod.models.gmm import GMM
from pyod.models.sampling import Sampling
from pyod.models.kde import KDE

from pyod.models.ocsvm import OCSVM
from pyod.models.pca import PCA
from pyod.models.mcd import MCD

from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.knn import KNN
from pyod.models.lof import LOF

from pyod.models.loda import LODA
from pyod.models.inne import INNE
from pyod.models.rod import ROD
from pyod.models.iforest import IForest

from pyod.models.auto_encoder import AutoEncoder
from pyod.models.so_gaal import SO_GAAL
from pyod.models.mo_gaal import MO_GAAL
from pyod.models.deep_svdd import DeepSVDD
from pyod.models.anogan import AnoGAN


def build_classifiers(
    methods: str or List = "all",
    classifiers={},
    outliers_fraction=0.1,
    random_state=42,
    n_neighbors=25,
    n_estimators=250,
):
    all_methods = True if methods == "all" else False
    all_besides_nn_methods = True if methods == "all_besides_nn" else False

    # Probabilistic
    if all_methods or all_besides_nn_methods or "ECOD" in methods:
        classifiers["Empirical Cumulative Distribution Functions (ECOD)"] = ECOD(
            contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "COPOD" in methods:
        classifiers["Copula Based Outlier Detector (COPOD)"] = COPOD(
            contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "ABOD" in methods:
        classifiers["Angle-based Outlier Detector (ABOD)"] = ABOD(
            contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "ABOD" in methods:
        classifiers["Stochastic Outlier Selection (SOS)"] = SOS(
            contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "KDE" in methods:
        classifiers["Kernel Density Estimation (KDE)"] = KDE(
            contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "GMM" in methods:
        classifiers["Gaussian Mixture Models (GMM)"] = GMM(
            contamination=outliers_fraction, random_state=random_state
        )
    if all_methods or all_besides_nn_methods or "SP" in methods:
        classifiers["Outlier detection based on Sampling (SP)"] = Sampling(
            contamination=outliers_fraction
        )

    # Linear
    if all_methods or all_besides_nn_methods or "PCA" in methods:
        classifiers["Principal Component Analysis (PCA)"] = PCA(
            contamination=outliers_fraction, random_state=random_state
        )
    if all_methods or all_besides_nn_methods or "OCSVM" in methods:
        classifiers["One-class SVM (OCSVM)"] = OCSVM(contamination=outliers_fraction)
    if all_methods or all_besides_nn_methods or "MCD" in methods:
        classifiers["Minimum Covariance Determinant (MCD)"] = MCD(
            contamination=outliers_fraction, random_state=random_state
        )

    # Proximity-Based
    if all_methods or all_besides_nn_methods or "CBLOF" in methods:
        classifiers["Cluster-based Local Outlier Factor (CBLOF)"] = CBLOF(
            contamination=outliers_fraction,
            check_estimator=False,
            random_state=random_state,
        )
    if all_methods or all_besides_nn_methods or "LOF" in methods:
        classifiers["Local Outlier Factor (LOF)"] = LOF(
            n_neighbors=n_neighbors, contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "HBOS" in methods:
        classifiers["Histogram-base Outlier Detection (HBOS)"] = HBOS(
            contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "KNN" in methods:
        classifiers["K Nearest Neighbors (KNN)"] = KNN(
            method="largest", contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "mKNN" in methods:
        classifiers["Mean K Nearest Neighbors (mKNN)"] = KNN(
            method="mean", contamination=outliers_fraction
        )
    if all_methods or all_besides_nn_methods or "ROD" in methods:
        classifiers["Rotation-based Outlier Detector (ROD)"] = ROD(
            contamination=outliers_fraction
        )

    # Outlier Ensembles
    if all_methods or all_besides_nn_methods or "IF" in methods:
        classifiers["Isolation Forest (IF)"] = IForest(
            n_estimators=n_estimators,
            contamination=outliers_fraction,
            random_state=random_state,
        )
    if all_methods or all_besides_nn_methods or "INNE" in methods:
        classifiers[
            "Isolation-based anomaly detection using nearest-neighbor ensembles (INNE)"
        ] = INNE(
            contamination=outliers_fraction,
            n_estimators=n_estimators,
            random_state=random_state,
        )
    if all_methods or all_besides_nn_methods or "LODA" in methods:
        classifiers["Lightweight on-line detector of anomalies (LODA)"] = LODA(
            contamination=outliers_fraction
        )

    # Neural Networks

    if all_methods or "AutoEncoder" in methods:
        classifiers["AutoEncoder"] = AutoEncoder(
            contamination=outliers_fraction,
            random_state=random_state,
            hidden_neurons=[0],
            verbose=0,
        )
    if all_methods or "SOGAAL" in methods:
        classifiers[
            "Single-Objective Generative Adversarial Active Learning (SOGAAL)"
        ] = SO_GAAL(contamination=outliers_fraction)
    if all_methods or "MOGAAL" in methods:
        classifiers[
            "Multiple-Objective Generative Adversarial Active Learning (MOGAAL)"
        ] = MO_GAAL(contamination=outliers_fraction)
    if all_methods or "DeepSVDD" in methods:
        classifiers["Deep One-Class Classifier with AutoEncoder (DeepSVDD)"] = DeepSVDD(
            contamination=outliers_fraction, verbose=0, random_state=random_state
        )
    if all_methods or "AnoGAN" in methods:
        classifiers["Anomaly Detection with Generative Adversarial Networks"] = AnoGAN(
            contamination=outliers_fraction, verbose=0
        )
    return classifiers


def predict_outliers(clf, X, raw=False):
    clf.fit(X)
    if raw:
        return clf.decision_function(X)
    return clf.predict(X)


def get_number_of_methods(classifiers):
    return len(classifiers)


def detect_outliers(X, classifiers):
    results = {clf: predict_outliers(classifiers[clf], X) for clf in classifiers}
    return results


def aggregate_outliers(results):
    return np.array(list(results.values())).sum(axis=0) / len(results)


def run_ontlier_detection(X, classifiers, mode="per_class"):
    final_arr = np.array([])
    if mode == "per_class":
        detected_outliers_dict = {}
        for _class in np.unique(X[:, 2]):
            arr = X[X[:, 2] == _class]
            detected_outliers_dict[_class] = detect_outliers(arr[:, 0:2], classifiers)
            overall = aggregate_outliers(detected_outliers_dict[_class])
            if final_arr.size:
                final_arr = np.vstack(
                    (final_arr, np.hstack((arr, overall.reshape(-1, 1))))
                )
            else:
                final_arr = np.hstack((arr, overall.reshape(-1, 1)))
    else:
        detected_outliers_dict = detect_outliers(X[:, 0:2], classifiers)
        overall = aggregate_outliers(detected_outliers_dict)
        final_arr = np.hstack((X, overall.reshape(-1, 1)))
    return final_arr, detected_outliers_dict


def plot_classifiers(
    X, classifiers, detected_outliers=None, increase_coef=0.05, plot_per_row=3
):
    """
    X[:,:-2] - data columns
    X[:,-2]  - class column
    X[:,-1]  - proba column
    """
    min_x, max_x = X[:, 0].min() - abs(increase_coef * X[:, 0].min()), X[
        :, 0
    ].max() + abs(increase_coef * X[:, 0].max())
    min_y, max_y = X[:, 1].min() - abs(increase_coef * X[:, 1].min()), X[
        :, 1
    ].max() + abs(increase_coef * X[:, 1].max())
    xx, yy = np.meshgrid(np.linspace(min_x, max_x, 100), np.linspace(min_y, max_y, 100))

    figsize = (15, int(len(classifiers) / plot_per_row) * 3)
    plt.figure(figsize=figsize)

    for i, (clf_name, clf) in enumerate(classifiers.items()):
        y_pred = detected_outliers[clf_name]
        X_inline = X[np.where(y_pred == 0)][:, :-2]
        X_outline = X[np.where(y_pred == 1)][:, :-2]
        scores_pred = clf.decision_function(X[:, :-2]) * -1

        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
        Z = Z.reshape(xx.shape)
        scores_pred = np.maximum(scores_pred, Z)

        threshold = np.percentile(scores_pred, X_outline.shape[0] * 100 / X.shape[0])

        subplot = plt.subplot(
            int(len(classifiers) / plot_per_row) + 1, plot_per_row, i + 1
        )
        subplot.contourf(
            xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7), cmap=plt.cm.YlGnBu_r
        )
        a = subplot.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors="green")
        subplot.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors="orange")

        b = subplot.scatter(
            X_inline[:, 0], X_inline[:, 1], c="white", s=50, edgecolor="k"
        )
        c = subplot.scatter(
            X_outline[:, 0], X_outline[:, 1], c="red", s=50, edgecolor="k"
        )
        subplot.axis("tight")
        subplot.legend(
            [b, c],
            ["pred inliers", "pred outliers"],
            prop=matplotlib.font_manager.FontProperties(size=10),
            loc="lower right",
        )
        subplot.set_xlabel(f"{i}, {clf_name}")
        subplot.set_xlim((min_x, max_x))
        subplot.set_ylim((min_y, max_y))
    plt.subplots_adjust(0.1, 0.1, 1, 1, 0.1, 0.4)


def plot_overall(
    X,
    classifiers,
    calculated_class=None,
    show_heatmap=False,
    increase_coef=0.05,
    figsize=(12, 8),
):
    plt.figure(figsize=figsize)
    if not calculated_class:
        calculated_class = X[:, -1]
    min_x, max_x = (
        X[:, 0].min() - increase_coef * X[:, 0].min(),
        X[:, 0].max() + increase_coef * X[:, 0].max(),
    )
    min_y, max_y = (
        X[:, 1].min() - increase_coef * X[:, 1].min(),
        X[:, 1].max() + increase_coef * X[:, 1].max(),
    )

    if show_heatmap:
        k = gaussian_kde([X[:, 0], X[:, 1]])
        xi, yi = np.mgrid[
            min_x : max_x : X[:, 0].size * 1j * 3, min_y : max_y : X[:, 1].size * 1j * 3
        ]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))
        plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading="auto", cmap="YlGnBu_r")

    plt.scatter(X[:, 0], X[:, 1], s=75, c=calculated_class, cmap="Reds", edgecolor="k")
    cbar = plt.colorbar()
    cbar.set_label("Outlier probability", rotation=270, labelpad=15)
    plt.xlim((min_x, max_x))
    plt.ylim((min_y, max_y))
    plt.title(
        f"Overall outlier map based on {get_number_of_methods(classifiers)} methods"
    )


def detect_anomalies(
    dataset: np.array,
    methods: str = "all_besides_nn",
    mode: str = "per_class",
    outliers_fraction=0.05,
):
    classifiers = build_classifiers(
        methods=methods, outliers_fraction=outliers_fraction
    )
    result, detected_outliers = run_ontlier_detection(dataset, classifiers, mode=mode)
    return result, detected_outliers
