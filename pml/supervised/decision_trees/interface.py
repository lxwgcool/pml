# Copyright (C) 2012 David Rusk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
"""
Decision trees classification algorithm.

@author: drusk
"""

from pml.supervised.classifiers import AbstractClassifier
from pml.supervised.decision_trees import id3
from pml.supervised.decision_trees.tree_plotting import MatplotlibAnnotationTreePlotter
from pml.utils import collection_utils

class DecisionTree(AbstractClassifier):
    """
    Decision tree classifier.
    
    Builds a tree which is like a flow chart.  It allows a decision to be 
    reached by checking the values for various features and following the 
    appropriate branches until a destination is reached.
        
    In addition to being useful as a classifier, the structure of the 
    decision tree can lend insight into the data. 
    """
    
    def __init__(self, training_set):
        """
        Constructs a new decision tree.
        
        Args:
          training_set: model.DataSet
            The training data to use when building the decision tree.
        """
        self.training_set = training_set
        self._tree = id3.build_tree(training_set)
        self._plotter = MatplotlibAnnotationTreePlotter(self._tree)
    
    def _classify(self, sample):
        """
        Predicts a sample's classification based on the decision tree that 
        was built from the training data.
        
        Args:
          sample: 
            The sample or observation to be classified.
          
        Returns:
          The sample's classification.
        """
        node = self._tree.get_root_node()
        while not node.is_leaf():
            feature = node.get_value()
            branch = sample[feature]
            try:
                node = node.get_child(branch)
            except KeyError:
                return self._handle_value_not_trained_for()
        
        return node.get_value()

    def _handle_value_not_trained_for(self):
        """
        Handles the case where a sample has a value for a feature which was 
        not seen in the training set and therefore is not accounted for in 
        the tree.
        
        Current strategy is to just return the most common label in the 
        training data set.  It might be better to narrow this down to the 
        most common among samples that would reach the node at which the 
        unrecognized value was found.
        
        Returns:
          label:
            The best guess at the label.
        """
        return collection_utils.get_most_common(
                                    self.training_set.get_labels())

    def plot(self):
        """
        Generates a plot of the decision tree to visualize its structure.
        
        Returns:
          void
        """
        self._plotter.plot()

