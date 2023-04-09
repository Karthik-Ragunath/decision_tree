import argparse
import pandas as pd
from collections import defaultdict
import math

# Global Variables
information_gain_dict = defaultdict(lambda: defaultdict(list))
dt_dict = dict()
decision_tree = dict()
MAX_DEPTH = 10


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
        print("C-Dict:", counter_dict)
        max_key = max(counter_dict.items(), key = lambda k: k[1])[0]
        print("max_key:", max_key)
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

def iterate(key=None, parent=None, dt=None):
    """Iterate through decision tree."""
    if dt.end_val:
        print("Leaf Node:", "Key:", key, "Parent:", parent, "Label:", dt.end_val)
    else:
        print("Parent:", parent, "Key:", key, "Split Column:", dt.node_val, "Info Gain:", dt.info_gain)
        for key, obj in dt.children.items():
            iterate(key, dt.node_val, obj)

def make_decisions(node, sample=None):
    """Make decisions during inference."""
    if node.end_val:
        return node.end_val
    decision_tree_split_col = node.node_val
    next_node = node.children[sample[decision_tree_split_col]]
    return make_decisions(next_node, sample)

if __name__ == '__main__':
    """Main functions."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--cols", default=None, help="column names in order for the data.")
    parser.add_argument("--input_data_location", required=True, help="location of the input data.")
    parser.add_argument("--output_column", required=False, default=None, help="specify the output column name.")
    parser.add_argument("--max_depth", required=False, default=None, help="specify max depth of the decision tree.")

    cols = ["Y", "cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment", "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type", "spore-print-color", "population", "habitat"]
    mushroom_df = pd.read_csv('data/mush_train.data', names = cols, header=None, index_col=False)

    root = DecisionTreeNode(X=mushroom_df, depth=1, output_column='Y', max_depth=MAX_DEPTH)
    root.split_node()
    print(information_gain_dict)

    decision_tree = DT(root)
    decision_tree.create_dt_from_trained_data()

    node = decision_tree
    iterate(dt=node)

    test_cols = ["Y", "cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment", "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type", "spore-print-color", "population", "habitat"]
    mushroom_test_df = pd.read_csv('data/mush_test.data', names = test_cols, header=None, index_col=False)

    decisions = []
    for i in range(len(mushroom_test_df)):
        decision = make_decisions(decision_tree, mushroom_test_df.iloc[i])
        decisions.append(decision)

    count = 0
    for index, decision in enumerate(decisions):
        if decision == mushroom_test_df.iloc[index]["Y"]:
            count += 1

    accuracy = count/ len(mushroom_test_df)
    print("Test Accuracy:", accuracy)
