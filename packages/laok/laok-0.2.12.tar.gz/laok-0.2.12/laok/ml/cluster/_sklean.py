#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/11 21:54:21

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import numpy as np
#===============================================================================
'''  包装了 sklearn所支持的聚类算法
'''
#===============================================================================
__all__ = ['ClusterAffinityPropagation',
           'ClusterBirch',
           'ClusterDBScan',
           'ClusterGaussianMixture',
           'ClusterGaussianMixtureBayesian',
           'ClusterKMeans',
           'ClusterKMeansBisecting',
           'ClusterKMeansMiniBatch',
           'ClusterMeanShift',
           'ClusterOPTICS',
           'ClusterSpectral',
           'ClusterSpectralBiclustering',
           'ClusterSpectralCoclustering']

class ClusterAffinityPropagation:
    '''聚合聚类涉及合并示例，直到达到所需的群集数量为止。它是层次聚类方法的更广泛类的一部分
    '''
    def __init__(self,
                 damping=.5,
                 max_iter=200,
                 convergence_iter=15,
                 copy=True,
                 preference=None,
                 affinity='euclidean',
                 verbose=False,
                 random_state=None
                 ):
        from sklearn.cluster import AffinityPropagation as _Alg
        self._alg = _Alg(damping=damping,
                         max_iter=max_iter,
                         convergence_iter=convergence_iter,
                         copy=copy,
                         preference=preference,
                         affinity=affinity,
                         verbose=verbose,
                         random_state=random_state
                         )

    def getLabels(self):
        return self._alg.labels_

    def getClusterCentersIndices(self):
        return self._alg.cluster_centers_indices_

    def getClusterCenters(self):
        return self._alg.cluster_centers_

    def getAffinityMatrix(self):
        return self._alg.affinity_matrix_

    def getNIter(self):
        return self._alg.n_iter_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getLabels()


class Agglomerative:
    '''聚合聚类涉及合并示例，直到达到所需的群集数量为止。它是层次聚类方法的更广泛类的一部分
    '''
    def __init__(self,
                 n_clusters=2,
                 affinity="euclidean",
                 memory=None,
                 connectivity=None,
                 compute_full_tree='auto',
                 linkage='ward',
                 distance_threshold=None
                 ):
        from sklearn.cluster import AgglomerativeClustering as _Alg
        self._alg = _Alg(n_clusters=n_clusters,
                         affinity=affinity,
                         memory=memory,
                         connectivity=connectivity,
                         compute_full_tree=compute_full_tree,
                         linkage=linkage,
                         distance_threshold=distance_threshold,
                         compute_distances=True
                         )

    def getLabels(self):
        return self._alg.labels_

    def getNClusters(self):
        return self._alg.n_clusters_

    def getNLeaves(self):
        return self._alg.n_leaves_

    def getNConnectedComponents(self):
        return self._alg.n_connected_components_

    def getChildren(self):
        return self._alg.children_

    def getDistances(self):
        return self._alg.distances_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getLabels()


class ClusterBirch:
    '''BIRCH 聚类（ BIRCH 是平衡迭代减少的缩写，聚类使用层次结构)包括构造一个树状结构，从中提取聚类质心。'''
    def __init__(self,
                 threshold=0.5,
                 branching_factor=50,
                 n_clusters=3,
                 compute_labels=True,
                 copy=True
                 ):
        from sklearn.cluster import Birch as _Alg
        self._alg = _Alg(threshold=threshold,
                         branching_factor=branching_factor,
                         n_clusters=n_clusters,
                         compute_labels=compute_labels,
                         copy=copy
                         )

    def getLabels(self):
        return self._alg.labels_

    def getSubclusterCenters(self):
        return self._alg.subcluster_centers_

    def getSubclusterLabels(self):
        return self._alg.subcluster_labels_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getLabels()



class ClusterDBScan:
    '''聚类（其中 DBSCAN 是基于密度的空间聚类的噪声应用程序）涉及在域中寻找高密度区域，并将其周围的特征空间区域扩展为群集。'''
    def __init__(self,
                eps=0.5,  # float, default=0.5, The maximum distance between two samples for one to be considered as in the neighborhood of the other
                min_samples=5,
                metric='euclidean',
                metric_params=None, # dict, default=None
                algorithm='auto',   # 'auto', 'ball_tree', 'kd_tree', 'brute'
                leaf_size=30,
                p=None,            # float, default=None, The power of the Minkowski metric to be used to calculate distance between points.
                n_jobs=None,        # int, default=None,  The number of parallel jobs to run. -1表示所有
                use_daal4py=True
                ):

        if use_daal4py:
            try:
                from daal4py.sklearn.cluster import DBSCAN as _Alg
            except Exception as e:
                pass
        else:
            from sklearn.cluster import DBSCAN as _Alg

        self._alg = _Alg(eps=eps,
                    min_samples=min_samples,
                    metric=metric,
                    metric_params= metric_params,
                    algorithm= algorithm,
                    leaf_size= leaf_size,
                    p = p,
                    n_jobs= n_jobs
                    )

    def getLabels(self):
        return self._alg.labels_

    def getComponents(self):
        return self._alg.components_

    def getCoreSampleIndices(self):
        return self._alg.core_sample_indices_

    def __call__(self, X, sample_weight=None):
        self._alg.fit(X=X, sample_weight=sample_weight)
        return self.getLabels()



class ClusterGaussianMixture:
    '''高斯混合模型总结了一个多变量概率密度函数，顾名思义就是混合了高斯概率分布。'''
    def __init__(self,
                 n_components=1,
                 covariance_type='full',
                 tol=1e-3,
                 reg_covar=1e-6,
                 max_iter=100,
                 n_init=1,
                 init_params='kmeans',
                 weights_init=None,
                 means_init=None,
                 precisions_init=None,
                 random_state=None,
                 warm_start=False,
                 verbose=0,
                 verbose_interval=10
                 ):
        from sklearn.mixture import GaussianMixture as _Alg
        self._alg = _Alg(n_components=n_components, covariance_type=covariance_type,
                         tol=tol, reg_covar=reg_covar, max_iter=max_iter, n_init=n_init,
                         init_params=init_params, weights_init=weights_init, means_init=means_init,
                         precisions_init=precisions_init, random_state=random_state,
                         warm_start=warm_start, verbose=verbose, verbose_interval=verbose_interval)

    def getLabels(self):
        return self.labels_

    def getWeights(self):
        return self._alg.weights_

    def getMeans(self):
        return self._alg.means_

    def getCovariances(self):
        return self._alg.covariances_

    def getPrecisions(self):
        return self._alg.precisions_

    def getPrecisionsCholesky(self):
        return self._alg.precisions_cholesky_

    def getConverged(self):
        return self._alg.converged_

    def getNIter(self):
        return self._alg.n_iter_

    def getLowerBound(self):
        return self._alg.lower_bound_

    def __call__(self, X):
        self.labels_ = self._alg.fit_predict(X=X)
        return self.getLabels()



class ClusterGaussianMixtureBayesian:
    def __init__(self,
                 n_components=1,
                 covariance_type='full',
                 tol=1e-3,
                 reg_covar=1e-6,
                 max_iter=100,
                 n_init=1,
                 init_params='kmeans',
                 weight_concentration_prior_type='dirichlet_process',
                 weight_concentration_prior=None,
                 mean_precision_prior=None, mean_prior=None,
                 degrees_of_freedom_prior=None,
                 covariance_prior=None,
                 random_state=None,
                 warm_start=False,
                 verbose=0,
                 verbose_interval=10
                 ):
        from sklearn.mixture import BayesianGaussianMixture as _Alg
        self._alg = _Alg(n_components=n_components, covariance_type=covariance_type,
                         tol=tol, reg_covar=reg_covar, max_iter=max_iter, n_init=n_init,
                         init_params=init_params,
                         weight_concentration_prior_type = weight_concentration_prior_type,
                         weight_concentration_prior = weight_concentration_prior,
                         mean_precision_prior = mean_precision_prior,
                         mean_prior = mean_prior,
                         degrees_of_freedom_prior = degrees_of_freedom_prior,
                         covariance_prior = covariance_prior,
                         random_state=random_state,
                         warm_start=warm_start, verbose=verbose, verbose_interval=verbose_interval)

    def getLabels(self):
        return self.labels_

    def getWeights(self):
        return self._alg.weights_

    def getMeans(self):
        return self._alg.means_

    def getCovariances(self):
        return self._alg.covariances_

    def getPrecisions(self):
        return self._alg.precisions_

    def getPrecisionsCholesky(self):
        return self._alg.precisions_cholesky_

    def getConverged(self):
        return self._alg.converged_

    def getNIter(self):
        return self._alg.n_iter_

    def getLowerBound(self):
        return self._alg.lower_bound_

    def getWeightConcentrationPrior(self):
        return self._alg.weight_concentration_prior_

    def getWeightConcentration(self):
        return self._alg.weight_concentration_

    def getMeanPrecisionPrior(self):
        return self._alg.mean_precision_prior_

    def getMeanPrecision(self):
        return self._alg.mean_precision_

    def getMeanPrior(self):
        return self._alg.mean_prior_

    def getDegreesOfFreedomPrior(self):
        return self._alg.degrees_of_freedom_prior_

    def getDegreesOfFreedom(self):
        return self._alg.degrees_of_freedom_

    def getCovariancePrior(self):
        return self._alg.covariance_prior_

    def __call__(self, X):
        self.labels_ = self._alg.fit_predict(X=X)
        return self.getLabels()



class ClusterKMeans:
    def __init__(self,
                 n_clusters=8,
                 init='k-means++', # 'k-means++', 'random'
                 n_init=10,
                 max_iter=300,
                 tol=1e-4,
                 precompute_distances='deprecated', #'auto', True, False
                 verbose=0,
                 random_state=None,
                 copy_x=True,
                 n_jobs='deprecated',
                 algorithm='auto',  # "auto", "full", "elkan"
                 use_daal4py = True
                ):

        if use_daal4py:
            try:
                from daal4py.sklearn.cluster import KMeans as _Alg
            except Exception as e:
                pass
        else:
            from sklearn.cluster import KMeans as _Alg

        self._alg = _Alg(n_clusters=n_clusters,
                         init=init,
                         n_init=n_init,
                         max_iter=max_iter,
                         tol=tol,
                         precompute_distances=precompute_distances,
                         verbose=verbose,
                         random_state=random_state,
                         copy_x = copy_x,
                         n_jobs=n_jobs,
                         algorithm=algorithm)

    def getLabels(self):
        return self._alg.labels_

    def getClusterCenters(self):
        return self._alg.cluster_centers_

    def getInertia(self):
        return self._alg.inertia_

    def getNIter(self):
        return self._alg.n_iter_

    def __call__(self, X, sample_weight=None):
        ''' labels中 -1表示离群点
        :param X:
        :param sample_weight:
        :return:
        '''
        self._alg.fit(X=X, sample_weight=sample_weight)
        return self.getLabels()



class ClusterKMeansBisecting:
    def __init__(self,
                 n_clusters=8,
                 init="random",
                 n_init=1,
                 random_state=None,
                 max_iter=300,
                 verbose=0,
                 tol=1e-4,
                 copy_x=True,
                 algorithm="lloyd",
                 bisecting_strategy="biggest_inertia",
                ):
        from sklearn.cluster import BisectingKMeans as _Alg
        self._alg = _Alg(n_clusters=n_clusters,
                         init=init,
                         n_init=n_init,
                         random_state=random_state,
                         max_iter=max_iter,
                         verbose=verbose,
                         tol=tol,
                         copy_x = copy_x,
                         algorithm=algorithm,
                         bisecting_strategy=bisecting_strategy
                         )

    def getLabels(self):
        return self._alg.labels_

    def getClusterCenters(self):
        return self._alg.cluster_centers_

    def getInertia(self):
        return self._alg.inertia_

    def getNFeaturesIn(self):
        return self._alg.n_features_in_

    # def getFeatureNamesIn(self):
    #     return self._alg.feature_names_in_

    def __call__(self, X, sample_weight=None):
        ''' labels中 -1表示离群点
        :param X:
        :param sample_weight:
        :return:
        '''
        self._alg.fit(X=X, sample_weight=sample_weight)
        return self.getLabels()



class ClusterKMeansMiniBatch:
    '''K-均值是 K-均值的修改版本，它使用小批量的样本而不是整个数据集对群集质心进行更新，
    这可以使大数据集的更新速度更快，并且可能对统计噪声更健壮，我们建议使用 k-均值聚类的迷你批量优化。
    与经典批处理算法相比，这降低了计算成本的数量级，同时提供了比在线随机梯度下降更好的解决方案。
    '''
    def __init__(self,
                 n_clusters=8,
                 init='k-means++',
                 max_iter=100,
                 batch_size=100,
                 verbose=0,
                 compute_labels=True,
                 random_state=None,
                 tol=0.0,
                 max_no_improvement=10,
                 init_size=None,
                 n_init=3,
                 reassignment_ratio=0.01):

        from sklearn.cluster import MiniBatchKMeans as _Alg
        self._alg = _Alg(n_clusters=n_clusters, init=init, max_iter=max_iter,
                         batch_size=batch_size, verbose=verbose, compute_labels=compute_labels,
                         random_state=random_state, tol=tol, max_no_improvement=max_no_improvement,
                         init_size=init_size, n_init=n_init, reassignment_ratio=reassignment_ratio)

    def getLabels(self):
        return self._alg.labels_

    def getNIter(self):
        return self._alg.n_iter_

    def getInertia(self):
        return self._alg.inertia_

    def __call__(self, X, sample_weight=None):
        self._alg.fit(X=X, sample_weight=sample_weight)
        return self.getLabels()


class ClusterMeanShift:
    '''
    均值漂移聚类涉及到根据特征空间中的实例密度来寻找和调整质心。
    '''
    def __init__(self,
                 bandwidth=None,
                 seeds=None,
                 bin_seeding=False,
                 min_bin_freq=1,
                 cluster_all=True,
                 n_jobs=None,
                 max_iter=300
                 ):
        from sklearn.cluster import MeanShift as _Alg
        self._alg = _Alg(bandwidth=bandwidth, seeds=seeds, bin_seeding=bin_seeding,
                         min_bin_freq=min_bin_freq, cluster_all=cluster_all, n_jobs=n_jobs,
                         max_iter=max_iter)

    def getLabels(self):
        return self._alg.labels_

    def getClusterCenters(self):
        return self._alg.cluster_centers_

    def getNIter(self):
        return self._alg.n_iter_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getLabels()


class ClusterOPTICS:
    '''聚类（ OPTICS 短于订购点数以标识聚类结构）是上述 DBSCAN 的修改版本'''
    def __init__(self,
                 min_samples=5,
                 max_eps=np.inf,
                 metric='minkowski',
                 p=2,
                 metric_params=None,
                 cluster_method='xi',
                 eps=None,
                 xi=0.05,
                 predecessor_correction=True,
                 min_cluster_size=None,
                 algorithm='auto',
                 leaf_size=30,
                 n_jobs=None
                 ):
        from sklearn.cluster import OPTICS as _Alg
        self._alg = _Alg(min_samples=min_samples,
                         max_eps=max_eps,
                         metric = metric,
                         p = p,
                         metric_params=metric_params,
                         cluster_method=cluster_method,
                         eps=eps,
                         xi=xi,
                         predecessor_correction=predecessor_correction,
                         min_cluster_size=min_cluster_size,
                         algorithm=algorithm,
                         leaf_size=leaf_size,
                         n_jobs=n_jobs)

    def getLabels(self):
        return self._alg.labels_

    def getReachability(self):
        return self._alg.reachability_

    def getOrdering(self):
        return self._alg.ordering_

    def getCoreDistances(self):
        return self._alg.core_distances_

    def getPredecessor(self):
        return self._alg.predecessor_

    def getClusterHierarchy(self):
        return self._alg.cluster_hierarchy_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getLabels()



class ClusterSpectral:
    def __init__(self,
                 n_clusters=8,
                 eigen_solver=None,
                 n_components=None,
                 random_state=None,
                 n_init=10,
                 gamma=1.,
                 affinity='rbf',
                 n_neighbors=10,
                 eigen_tol=0.0,
                 assign_labels='kmeans',
                 degree=3,
                 coef0=1,
                 kernel_params=None,
                 n_jobs=None,
                 verbose=False
                 ):
        from sklearn.cluster import SpectralClustering as _Alg
        self._alg = _Alg(n_clusters=n_clusters, eigen_solver=eigen_solver, n_components=n_components,
                         random_state=random_state, n_init=n_init, gamma=gamma, affinity=affinity,
                         n_neighbors=n_neighbors, eigen_tol=eigen_tol, assign_labels=assign_labels,
                         degree=degree, coef0=coef0, kernel_params=kernel_params,
                         n_jobs=n_jobs, verbose=verbose)

    def getLabels(self):
        return self._alg.labels_

    def getAffinityMatrix(self):
        return self._alg.affinity_matrix_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getLabels()



class ClusterSpectralBiclustering:
    def __init__(self,
                 n_clusters=3,
                 method='bistochastic',
                 n_components=6,
                 n_best=3,
                 svd_method='randomized',
                 n_svd_vecs=None,
                 mini_batch=False,
                 init='k-means++',
                 n_init=10,
                 n_jobs='deprecated',
                 random_state=None
                 ):
        from sklearn.cluster import SpectralBiclustering as _Alg
        self._alg = _Alg(n_clusters=n_clusters, method=method,
                         n_components=n_components, n_best=n_best,
                         svd_method=svd_method, n_svd_vecs=n_svd_vecs,
                         mini_batch=mini_batch, init=init, n_init=n_init,
                         n_jobs=n_jobs, random_state=random_state)

    def getRowsLabels(self):
        return self._alg.row_labels_

    def getColumnLabels(self):
        return self._alg.column_labels_

    def getColumns(self):
        return self._alg.columns_

    def getRows(self):
        return self._alg.rows_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getRowsLabels(), self.getColumnLabels()



class ClusterSpectralCoclustering:
    def __init__(self,
                 n_clusters=3,
                 svd_method='randomized',
                 n_svd_vecs=None,
                 mini_batch=False,
                 init='k-means++',
                 n_init=10,
                 n_jobs='deprecated',
                 random_state=None
                 ):
        from sklearn.cluster import SpectralCoclustering as _Alg
        self._alg = _Alg(n_clusters=n_clusters, svd_method=svd_method, n_svd_vecs=n_svd_vecs,
                         mini_batch=mini_batch, init=init, n_init=n_init,
                         n_jobs=n_jobs, random_state=random_state)

    def getRowsLabels(self):
        return self._alg.row_labels_

    def getColumnLabels(self):
        return self._alg.column_labels_

    def getColumns(self):
        return self._alg.columns_

    def getRows(self):
        return self._alg.rows_

    def __call__(self, X):
        self._alg.fit(X=X)
        return self.getRowsLabels(), self.getColumnLabels()

