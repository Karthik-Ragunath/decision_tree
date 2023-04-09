import argparse
import pandas as pd
from collections import defaultdict
import math
from config import train_config, test_config
import queue

# Global Variables
information_gain_dict = defaultdict(lambda: defaultdict(list))
dt_dict = dict()
decision_tree = dict()
MAX_DEPTH = 1000


class DecisionTreeNode:
    """DecisionTreeNode."""
    def __init__(self, X=None, depth=None, output_column=None, max_depth=None):
        """Init function."""
        self.X = X
        self.depth = depth
        self.children = dict()
        self.end_value = None
        self.split_column = None
        self.information_gain_val = None
        self.output_column = output_column
        self.unique_class_outputs = list(X[output_column].unique())
        self.max_depth = max_depth
  
    def information_gain(self, col_considered=None):
        """Information gain."""
        unique_col_values = self.X[col_considered].unique()
        count_dictionary = defaultdict(int)
        for uniq_val in unique_col_values:
            count_dictionary[uniq_val] = len(self.X[self.X[col_considered] == uniq_val])
        total_len = len(self.X)
        conditional_entropy = 0
        col_split = defaultdict(lambda: defaultdict(int))
        for uniq_val in unique_col_values:
            for unique_class_output in self.unique_class_outputs:
                col_split[uniq_val][unique_class_output] = len(self.X[(self.X[col_considered] == uniq_val) & (self.X[self.output_column] == unique_class_output)])
            multiplication_term = count_dictionary[uniq_val] / len(self.X)
            feature_split_entropy = 0
            for unique_class_output in self.unique_class_outputs:
                if col_split[uniq_val][unique_class_output] != 0:
                    feature_split_entropy += (-1 * (col_split[uniq_val][unique_class_output] / count_dictionary[uniq_val]) * math.log((col_split[uniq_val][unique_class_output] / count_dictionary[uniq_val]), 2))
            total_prob = multiplication_term * feature_split_entropy
            conditional_entropy += total_prob
        return conditional_entropy
  
    def find_max_info_gain_ele(self):
        """Find max information gain column/feature."""
        min_entropy_col_name = None
        min_entropy = None
        for col in list(self.X.columns):
            if col != self.output_column:
                entropy = self.information_gain(col_considered=col)
                if not min_entropy or entropy <= min_entropy:
                    min_entropy = entropy
                    min_entropy_col_name = col
        return min_entropy_col_name, min_entropy

    def compute_children(self, col_considered=None, df=None):
        """Compute children."""
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

    def compute_entropy(self):
        """Compute entropy."""
        total_counts = len(self.X)
        total_entropy = 0
        for unique_class in self.unique_class_outputs:
            count_class_samples = len(self.X[self.X[self.output_column] == unique_class])
            if count_class_samples != 0 or count_class_samples != total_counts:
                total_entropy += (-1 * (count_class_samples / total_counts) * math.log((count_class_samples / total_counts), 2))
        return total_entropy

    def compute_majority_voting(self):
        """Compute majority voting."""
        counter_dict = dict(self.X[self.output_column].value_counts())
        max_key = max(counter_dict.items(), key = lambda k: k[1])[0]
        return max_key

    def split_node(self):
        """Split node."""
        if len(list(self.X[self.output_column].unique())) != 1 and len(self.X.columns) != 1:
            if self.depth == self.max_depth:
                max_voted_class = self.compute_majority_voting()
                self.end_value = max_voted_class
            else:
                total_entropy = self.compute_entropy()
                min_entropy_col_name, min_entropy = self.find_max_info_gain_ele()
                self.split_column = min_entropy_col_name
                information_gain_dict[self.depth][min_entropy_col_name].append(self.compute_entropy() - min_entropy)
                self.information_gain_val = self.compute_entropy() - min_entropy
                col_index = self.X.columns.get_loc(min_entropy_col_name)
                children_list, attributes_split_on = self.compute_children(col_considered=min_entropy_col_name, df=self.X)
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
        """Init function."""
        self.children = dict()
        self.node_val = None
        self.children = dict()
        self.end_val = None
        self.root = root
        self.info_gain = None
  
    def create_dt_from_trained_data(self):
        """Create decision tree from trained data."""
        if not self.root.end_value:
            self.node_val = self.root.split_column
            self.info_gain = self.root.information_gain_val
            for key, obj in self.root.children.items():
                self.children[key] = DT(obj)
                self.children[key].create_dt_from_trained_data()
        else:
            self.end_val = self.root.end_value
        return

def print_tree(node, key=None, tab_spaces=0):
    if node.end_val:
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
                f"- info gain: {node.info_gain}"
            )
        else:
            print(
                tab_spaces * '\t' + f"split_key: {key}",
                f"split_col: {node.node_val}",
                f"- info gain: {node.info_gain}"
            )
        for key, node_obj in node.children.items():
            print_tree(node=node_obj, key=key, tab_spaces=tab_spaces + 1)

def make_decisions(node, sample=None):
    """Make decisions during inference."""
    if node.end_val:
        return node.end_val
    decision_tree_split_col = node.node_val
    next_node = node.children[sample[decision_tree_split_col]]
    return make_decisions(next_node, sample)

if __name__ == '__main__':
    """Main functions."""
    
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
    
    print("-" * 20)
    print("Information Gain On Splits:")
    print(information_gain_dict)
    print("-" * 20)

    decision_tree = DT(root)
    decision_tree.create_dt_from_trained_data()

    print()
    print('-' * 10, 'DECISION TREE CREATED', '-'*10)
    node = decision_tree
    print_tree(node=node)
    print('-' * 20)

    if test_config.get('filename', None) is not None:
        test_filename = test_config['filename']
    else:
        raise 'test filename is not specified'

    if 'cols' in test_config:
        test_data_cols = test_config['cols']
    if not isinstance(test_data_cols, list):
        raise 'Please check the data type of cols data in test_config. List data type is expected'

    if test_data_cols:
        test_df = pd.read_csv('data/mush_test.data', names = test_data_cols, header=None, index_col=False)
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
