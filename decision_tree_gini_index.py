"""
Author - Karthik Ragunath Ananda Kumar
"""

import pandas as pd
from collections import defaultdict
import math
from configs.mush_dataset_config import train_config, test_config
# from configs.heart_dataset_config import train_config, test_config

# Global Variables
gini_index_dict = defaultdict(lambda: defaultdict(list))
dt_dict = dict()
decision_tree = dict()
MAX_DEPTH = 1000


class DecisionTreeNode:
    """DecisionTreeNode."""
    def __init__(self, X=None, depth=None, output_column=None, max_depth=None):
        """Init function.
        
        Input Args
        ==========
        X - dataframe for the node
        depth - current depth of the decision tree
        output column - name of the output column in the dataframe
        max_depth - max_depth allowed in the decision tree
        
        Output
        ======
        None
        """
        self.X = X
        self.depth = depth
        self.children = dict()
        self.end_value = None
        self.split_column = None
        self.gini_index_val = None
        self.output_column = output_column
        self.unique_class_outputs = list(X[output_column].unique())
        self.max_depth = max_depth
    
    def compute_gini_index(self, col_considered=None):
        """Compute Gini Index

        Input Args
        ==========
        col_considered - feature considered for computing gini index upon split.

        Output
        ======
        Gini index associated with splitting on 'col_considered' feature in dataframe.
        """
        unique_col_values = self.X[col_considered].unique()
        count_dictionary = defaultdict(int)
        for uniq_val in unique_col_values:
            count_dictionary[uniq_val] = len(self.X[self.X[col_considered] == uniq_val])
        gini_impurity_measure = 0
        col_split = defaultdict(lambda: defaultdict(int))
        for uniq_val in unique_col_values:
            for unique_class_output in self.unique_class_outputs:
                col_split[uniq_val][unique_class_output] = len(self.X[(self.X[col_considered] == uniq_val) & (self.X[self.output_column] == unique_class_output)])
            multiplication_term = count_dictionary[uniq_val] / len(self.X)
            feature_gini_index = 0
            for unique_class_output in self.unique_class_outputs:
                if col_split[uniq_val][unique_class_output] != 0:
                    feature_gini_index += (1 * (col_split[uniq_val][unique_class_output] / count_dictionary[uniq_val]) ** 2)
            gini_index = multiplication_term * (1 - feature_gini_index)
            gini_impurity_measure += gini_index
        return gini_impurity_measure, len(unique_col_values)
  
    def find_min_gini_index_col(self):
        """Find max information gain column/feature.
        
        Input Args
        ==========
        None
        # instance variables are accessed for computation in this method

        Output
        ======
        min_entropy_col_name - name of the feature which gives minimum entropy when used for split.
        min_entropy - entropy associated with "min_entropy_col_name" feature when used for split the dataframe.
        """
        min_gini_col_name = None
        min_gini_index = None
        min_gini_col_num_uniq_values = None
        for col in list(self.X.columns):
            if col != self.output_column:
                gini_index, num_unique_values = self.compute_gini_index(col_considered=col)
                if min_gini_index is None or gini_index < min_gini_index:
                    min_gini_index = gini_index
                    min_gini_col_name = col
                    min_gini_col_num_uniq_values = num_unique_values
                elif gini_index == min_gini_index:
                    if num_unique_values > min_gini_col_num_uniq_values:
                        min_gini_index = gini_index
                        min_gini_col_name = col
                        min_gini_col_num_uniq_values = num_unique_values
        return min_gini_col_name, min_gini_index, min_gini_col_num_uniq_values

    def compute_children(self, col_considered=None, df=None):
        """Compute children.
        
        Input Args
        ==========
        col_considered - feature upon which dataframe 'df' is split

        Output
        ======
        df_list - dataframe associated with child nodes when split on the column passed in the argument.
        attributes_split_on - unique value associated with each child node when split with column passed in the argument.
        """
        unique_vals = df[col_considered].unique()
        df_list = []
        attributes_split_on = []
        for unique_val in unique_vals:
            temp_df = df[df[col_considered] == unique_val]
            temp_df = temp_df.drop(columns=[col_considered])
            temp_df = temp_df.reset_index(drop=True)
            df_list.append(temp_df)
            attributes_split_on.append(unique_val)
        return df_list, attributes_split_on

    def compute_majority_voting(self):
        """Compute majority voting.
        
        Input Args
        ==========
        None
        # instance variables are used in this method.

        Output
        ======
        max_key - output class label which is present with highest frequency in the dataframe.
        """
        counter_dict = dict(self.X[self.output_column].value_counts())
        max_key = max(counter_dict.items(), key = lambda k: k[1])[0]
        return max_key

    def split_node(self):
        """Split node.
        
        Input Args
        ==========
        None
        # instance variables are used in this method.

        Output
        ======
        Instance variables are updated in this method.
        # Acts as the master method in the class which calls other instance methods.
        """
        if len(list(self.X[self.output_column].unique())) != 1 and len(self.X.columns) != 1:
            if self.depth == self.max_depth:
                max_voted_class = self.compute_majority_voting()
                self.end_value = max_voted_class
            else:
                min_gini_index_col_name, min_gini_index, min_gini_col_num_uniq_values = self.find_min_gini_index_col()
                if min_gini_index == 0.5 or min_gini_col_num_uniq_values == 1:
                    max_voted_class = self.compute_majority_voting()
                    self.end_value = max_voted_class
                    return
                self.split_column = min_gini_index_col_name
                gini_index_dict[self.depth][min_gini_index_col_name].append(min_gini_index)
                self.gini_index_val = min_gini_index
                col_index = self.X.columns.get_loc(min_gini_index_col_name)
                children_list, attributes_split_on = self.compute_children(col_considered=min_gini_index_col_name, df=self.X)
                total_len = 0
                len_list = []
                for children_df in children_list:
                    total_len += len(children_df)
                    len_list.append(len(children_df))
                for children_df, attribute_val in zip(children_list, attributes_split_on):
                    self.children[attribute_val] = DecisionTreeNode(X=children_df, depth=self.depth + 1, output_column=self.output_column, max_depth=self.max_depth)
                for child_key, child_obj in self.children.items():
                    child_obj.split_node()
        else:
            self.end_value =  list(self.X[self.output_column].unique())[0]

class DT:
    def __init__(self, root):
        """Init function.
        
        Input Args
        ==========
        root - decision tree node object.

        Output
        ======
        None
        # instance variables are initialized.
        """
        self.children = dict()
        self.node_val = None
        self.children = dict()
        self.end_val = None
        self.root = root
        self.gini_index_val = None
  
    def create_dt_from_trained_data(self):
        """Create decision tree from trained data.

        Input Args
        ==========
        None
        # instance variables are used for computations.

        Output
        ======
        instance variables are updated in this method.
        """
        if self.root.end_value is None:
            self.node_val = self.root.split_column
            self.gini_index_val = self.root.gini_index_val
            for key, obj in self.root.children.items():
                self.children[key] = DT(obj)
                self.children[key].create_dt_from_trained_data()
        else:
            self.end_val = self.root.end_value
        return

def print_tree(node, key=None, tab_spaces=0):
    """Print tree.
    
    Input Args
    ==========
    key - attribute associated with parent node which result in creation of current (self) subset of data in decision tree node.

    Output
    ======
    None
    # Tree is printed. 
    """
    if node.end_val is not None:
        if key is None:
            print(
                tab_spaces * '\t' + f"predicted: {node.end_val}"
            )
        else:
            print(
                tab_spaces * '\t' + f"split_key: {key}", 
                f"predicted: {node.end_val}"
            )
    else:
        if key is None:
            print(
                tab_spaces * '\t' + "Root:",
                f"split_col: {node.node_val}",
                f"- gini index: {node.gini_index_val}"
            )
        else:
            print(
                tab_spaces * '\t' + f"split_key: {key}",
                f"split_col: {node.node_val}",
                f"- gini index: {node.gini_index_val}"
            )
        for key, node_obj in node.children.items():
            print_tree(node=node_obj, key=key, tab_spaces=tab_spaces + 1)

def make_decisions(node, sample=None):
    """Make decisions during inference.
    
    Input Args
    ==========
    sample - row to be classified

    Output
    ======
    output label determined as the result of decision tree splits.
    """
    if node.end_val is not None:
        return node.end_val
    decision_tree_split_col = node.node_val
    next_node = node.children[sample[decision_tree_split_col]]
    return make_decisions(next_node, sample)

if __name__ == '__main__':
    """Main functions."""
    # ------------------------------------------------------
    # TRAINING (CREATING DECISION TREE)
    train_data_cols = None
    train_filename = None

    if train_config.get('filename', None) is not None:
        train_filename = train_config['filename']
    else:
        raise 'train filename is not specified'

    if 'cols' in train_config:
        train_data_cols = train_config['cols']
    if not isinstance(train_data_cols, list):
        raise 'Please check the data type of cols data in train_config. List data type is expected'

    if train_data_cols:
        train_df = pd.read_csv(train_filename, names = train_data_cols, header=None, index_col=False)
    else:
        train_df = pd.read_csv(train_filename)
        train_data_cols = train_df.head()

    output_column = train_config.get('output_column', None)
    if output_column is None:
        raise 'output_column name is not specified'

    max_depth = train_config.get('max_depth', MAX_DEPTH)

    root = DecisionTreeNode(
        X=train_df,
        depth=1,
        output_column=output_column,
        max_depth=max_depth
    )
    root.split_node()
    
    # print("-" * 20)
    # print("Information Gain On Splits:")
    # print(information_gain_dict)
    # print("-" * 20)

    decision_tree = DT(root)
    decision_tree.create_dt_from_trained_data()

    print()
    print('-' * 10, 'DECISION TREE CREATED', '-'*10)
    node = decision_tree
    print_tree(node=node)
    print('-' * 20)

    # ------------------------------------------------------

    # ------------------------------------------------------
    # INFERENCE BASED ON DECISION TREE CREATED

    if test_config.get('filename', None) is not None:
        test_filename = test_config['filename']
    else:
        raise 'test filename is not specified'

    if 'cols' in test_config:
        test_data_cols = test_config['cols']
    if not isinstance(test_data_cols, list):
        raise 'Please check the data type of cols data in test_config. List data type is expected'

    if test_data_cols:
        test_df = pd.read_csv(test_filename, names = test_data_cols, header=None, index_col=False)
    else:
        test_df = pd.read_csv(test_filename)
        test_data_cols = test_df.head()

    decisions = []
    for i in range(len(test_df)):
        decision = make_decisions(decision_tree, test_df.iloc[i])
        decisions.append(decision)

    # NO ELSE PART: IF OUTPUT COLUMN IS NOT PRESENT SAME OUTPUT COLUMN 
    # AS TRAIN CONFIG IS CONSIDERED
    if test_config.get('output_column', None):
        output_column = test_config['output_column']

    count = 0
    for index, decision in enumerate(decisions):
        if decision == test_df.iloc[index][output_column]:
            count += 1

    accuracy = count/ len(test_df)

    print()
    print('-' * 20)
    print("Test Accuracy:", accuracy)
    print('-' * 20)

    output_file_name = test_config.get('output_filename', 'output.csv')
    test_df['output_predicted'] = decisions
    test_df.to_csv(f"{output_file_name}", index=False)
    # ------------------------------------------------------