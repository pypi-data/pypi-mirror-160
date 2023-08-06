#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/23 01:32:08

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''

#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['RegressorDecisionTree']

class RegressorDecisionTree:
    def __init__(self,
                 criterion="mse",
                 splitter="best",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features=None,
                 random_state=None,
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 min_impurity_split=None,
                 ccp_alpha=0.0
                 ):

        from sklearn.tree import DecisionTreeRegressor as _Alg
        self._alg = _Alg(criterion=criterion, splitter=splitter, max_depth=max_depth,
                         min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                         min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features,
                         random_state=random_state, max_leaf_nodes=max_leaf_nodes,
                         min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split,
                         ccp_alpha=ccp_alpha
                         )

    def getFeatureImportances(self):
        return self._alg.feature_importances_

    def getMaxFeatures(self):
        return self._alg.max_features

    def getNFeatures(self):
        return self._alg.n_features_

    def getNOutputs(self):
        return self._alg.n_outputs_

    def getTree(self):
        return self._alg.tree_

    def train(self, X, y, sample_weight=None, check_input=True):
        self._alg.fit(X=X, y=y, sample_weight=sample_weight, check_input=check_input)
        return self

    def __call__(self, X, check_input=True):
        return self._alg.predict(X=X, check_input=check_input)
