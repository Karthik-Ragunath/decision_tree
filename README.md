# DECISION TREE FROM SCRATCH

```
Information-Gain and Gini-Index are used as criteria for computing the best splits in decision tree.

For building decision tree with Information-Gain as split criteria refer the file:
decision_tree_information_gain.py

For building decision tree with Gini-Index as split criteria refer the file:
decision_tree_gini_index.py

This code is designed to work with dataset which has discrete values in its features.
This repository supports Multi-Class classifications too.
```

## REQUIREMENTS

```
python >= 3.6
```

## CONFIGS

The code is designed to be config driven.
Configs associated with a particular dataset is to be stored in the `configs` directory

### TRAIN CONFIG
Keys in train_config:

```
cols - columns associated with the train portion of the dataset (Optional).
output_column - column which is to be used as output column (Required).
max_depth - max_depth upto which decision tree is created (Optional). Default value is 1000.
filename - file path which contains training data (Required).
```

### TEST CONFIG
Keys in test_config:

```
cols - columns associated with the train portion of the dataset (Optional).
output_column - column which is to be used as output column (Optional). Default - Output column name specified in train config.
filename - file path which contains test data (Required).
output_filename - filepath where decision tree classified file is to be stored (Optional).
```

### SAMPLE TRAIN AND TEST CONFIG
1. Configs for subset of UCI Mushroom dataset\
https://archive.ics.uci.edu/ml/datasets/mushroom
```
refer configs/mush_dataset_config.py file
```

2. Configs for subset of UCI Heart Dataset\
https://archive.ics.uci.edu/ml/datasets/spect+heart
```
refer configs/heart_dataset_config.py file
```

## STEPS TO RUN
```
- STEP 1: Specify the config to be used for training and testing in the decision_tree_information_gain.py (for building decision trees which uses information gain calculated from entropy as splitting criteria) and decision_tree_gini_index.py (for building decision trees which uses gini index as splitting criteria) files.
    - STEP 1 WILL BE MADE CONFIG DRIVEN IN THE NEXT COMMITS
    - EXAMPLE CODE CHANGES IN CODE:
        - from configs.mush_dataset_config import train_config, test_config
        - from configs.heart_dataset_config import train_config, test_config
- STEP 2__:  
    Run decision_tree_information_gain.py python script for building decision trees which uses information gain as splitting criteria.
    Run decision_tree_gini_index.py python script for building decision trees which uses gini index as splitting criteria. 
    - EXAMPLE COMMANDS:
        - For building decision tree which uses Information-Gain as splitting criteria:
          python decison_tree_information_gain.py
        
        - For building decision tree which uses Gini-Index as splitting criteria:
          python decision_tree_gini_index.py
```

## SAMPLE CONFIGS

1. Config for subset of UCI Mushroom dataset\
https://archive.ics.uci.edu/ml/datasets/mushroom

dataset is added in `data` directory\
train_data - data/mush_train.data\
test_data - data/mush_test.data

```
train_config = {
    'cols': [
        "Y",
        "cap-shape",
        "cap-surface",
        "cap-color",
        "bruises",
        "odor",
        "gill-attachment",
        "gill-spacing",
        "gill-size",
        "gill-color",
        "stalk-shape",
        "stalk-root",
        "stalk-surface-above-ring",
        "stalk-surface-below-ring",
        "stalk-color-above-ring",
        "stalk-color-below-ring",
        "veil-type",
        "veil-color",
        "ring-number",
        "ring-type",
        "spore-print-color",
        "population",
        "habitat"
    ],
    "output_column": "Y",
    "max_depth": 3,
    "filename": "data/mush_train.data",
}

test_config = {
    'cols': [
        "Y",
        "cap-shape",
        "cap-surface",
        "cap-color",
        "bruises",
        "odor",
        "gill-attachment",
        "gill-spacing",
        "gill-size",
        "gill-color",
        "stalk-shape",
        "stalk-root",
        "stalk-surface-above-ring",
        "stalk-surface-below-ring",
        "stalk-color-above-ring",
        "stalk-color-below-ring",
        "veil-type",
        "veil-color",
        "ring-number",
        "ring-type",
        "spore-print-color",
        "population",
        "habitat"
    ],
    "output_column": "Y",
    "filename": "data/mush_test.data",
    "output_filename": "mushroom_output.csv"
}
```

2. Config for subset of UCI Heart Dataset\
https://archive.ics.uci.edu/ml/datasets/spect+heart

dataset is added in `data` directory\
train_data - data/heart_train.data\
test_data - data/heart_test.data

```
# https://archive.ics.uci.edu/ml/datasets/spect+heart
train_config = {
    "cols": [
        "Y", 
        "F1", 
        "F2", 
        "F3", 
        "F4", 
        "F5", 
        "F6", 
        "F7", 
        "F8", 
        "F9", 
        "F10", 
        "F11", 
        "F12", 
        "F13", 
        "F14", 
        "F15", 
        "F16", 
        "F17", 
        "F18", 
        "F19", 
        "F20", 
        "F21", 
        "F22"
    ],
    "output_column": "Y",
    "max_depth": 10,
    "filename": "data/heart_train.data",
}

test_config = {
    "cols": [
        "Y", 
        "F1", 
        "F2", 
        "F3", 
        "F4", 
        "F5", 
        "F6", 
        "F7", 
        "F8", 
        "F9", 
        "F10", 
        "F11", 
        "F12", 
        "F13", 
        "F14", 
        "F15", 
        "F16", 
        "F17", 
        "F18", 
        "F19", 
        "F20", 
        "F21", 
        "F22"
    ],
    "output_column": "Y",
    "filename": "data/heart_test.data",
    'output_filename': 'heart_diagnosis.csv'
}
```

## OUTPUT GENERATED FOR THE CONFIGS ADDED ABOVE

1. Output generated for subset of UCI Mushroom dataset\
https://archive.ics.uci.edu/ml/datasets/mushroom

dataset is added in `data` directory\
train_data - data/mush_train.data\
test_data - data/mush_test.data

`1.1. OUTPUT GENERATED BY decision_tree_information_gain.py`

```
---------- DECISION TREE CREATED ----------
Root: split_col: odor - info gain: 0.9078035498174333
        split_key: n split_col: spore-print-color - info gain: 0.1397150073622939
                split_key: n predicted: e
                split_key: k predicted: e
                split_key: w predicted: e
                split_key: o predicted: e
                split_key: r predicted: p
                split_key: h predicted: e
                split_key: b predicted: e
                split_key: y predicted: e
        split_key: a predicted: e
        split_key: p predicted: p
        split_key: y predicted: p
        split_key: l predicted: e
        split_key: f predicted: p
        split_key: c predicted: p
        split_key: s predicted: p
        split_key: m predicted: p
--------------------

--------------------
Test Accuracy: 0.9944314185228605
--------------------
```

`1.2. OUTPUT GENERATED BY decision_tree_gini_index.py`

```
---------- DECISION TREE CREATED ----------
Root: split_col: odor - gini index: 0.027906022365856188
        split_key: n split_col: spore-print-color - gini index: 0.025909681611436017
                split_key: n predicted: e
                split_key: k predicted: e
                split_key: w predicted: e
                split_key: o predicted: e
                split_key: r predicted: p
                split_key: h predicted: e
                split_key: b predicted: e
                split_key: y predicted: e
        split_key: a predicted: e
        split_key: p predicted: p
        split_key: y predicted: p
        split_key: l predicted: e
        split_key: f predicted: p
        split_key: c predicted: p
        split_key: s predicted: p
        split_key: m predicted: p
--------------------

--------------------
Test Accuracy: 0.9944314185228605
--------------------
```

2. Output generated for subset of UCI Heart Dataset\
https://archive.ics.uci.edu/ml/datasets/spect+heart

dataset is added in `data` directory\
train_data - data/heart_train.data\
test_data - data/heart_test.data

`2.1. OUTPUT GENERATED BY decision_tree_information_gain.py`

```
---------- DECISION TREE CREATED ----------
Root: split_col: F13 - info gain: 0.1704317024641
        split_key: 1 split_col: F16 - info gain: 0.1463105191321331
                split_key: 0 split_col: F8 - info gain: 0.19241911353132402
                        split_key: 1 split_col: F21 - info gain: 0.10803154614560007
                                split_key: 0 predicted: 1
                                split_key: 1 split_col: F22 - info gain: 0.17095059445466865
                                        split_key: 1 predicted: 1
                                        split_key: 0 split_col: F5 - info gain: 0.9182958340544896
                                                split_key: 1 predicted: 1
                                                split_key: 0 predicted: 0
                        split_key: 0 split_col: F10 - info gain: 0.46956521111470706
                                split_key: 1 predicted: 1
                                split_key: 0 split_col: F11 - info gain: 0.7219280948873623
                                        split_key: 1 predicted: 1
                                        split_key: 0 predicted: 0
                split_key: 1 predicted: 1
        split_key: 0 split_col: F11 - info gain: 0.1342677686499959
                split_key: 1 split_col: F16 - info gain: 0.18905266854301628
                        split_key: 0 split_col: F19 - info gain: 0.23645279766002802
                                split_key: 0 split_col: F6 - info gain: 0.3219280948873623
                                        split_key: 0 split_col: F5 - info gain: 0.8112781244591328
                                                split_key: 0 predicted: 1
                                                split_key: 1 predicted: 0
                                        split_key: 1 predicted: 0
                                split_key: 1 predicted: 1
                        split_key: 1 predicted: 0
                split_key: 0 split_col: F16 - info gain: 0.11344158768624768
                        split_key: 1 predicted: 1
                        split_key: 0 split_col: F7 - info gain: 0.02927697024553788
                                split_key: 1 split_col: F10 - info gain: 0.4199730940219749
                                        split_key: 0 split_col: F2 - info gain: 0.9182958340544896
                                                split_key: 0 predicted: 1
                                                split_key: 1 predicted: 0
                                        split_key: 1 predicted: 0
                                split_key: 0 split_col: F9 - info gain: 0.02128337627903576
                                        split_key: 0 split_col: F8 - info gain: 0.016977551901060983
                                                split_key: 0 split_col: F20 - info gain: 0.012892544935989791
                                                        split_key: 1 split_col: F19 - info gain: 0.2516291673878229
                                                                split_key: 0 predicted: 1
                                                                split_key: 1 predicted: 0
                                                        split_key: 0 split_col: F19 - info gain: 0.040707324032982384
                                                                split_key: 0 split_col: F5 - info gain: 0.03536418926926277
                                                                        split_key: 0 predicted: 0
                                                                        split_key: 1 predicted: 0
                                                                split_key: 1 predicted: 1
                                                split_key: 1 predicted: 0
                                        split_key: 1 predicted: 0
--------------------

--------------------
Test Accuracy: 0.732620320855615
--------------------
```

`2.2. OUTPUT GENERATED BY decision_tree_gini_index.py`

```
---------- DECISION TREE CREATED ----------
Root: split_col: F13 - gini index: 0.3887362637362637
        split_key: 1 split_col: F8 - gini index: 0.24904507257448427
                split_key: 1 split_col: F10 - gini index: 0.1008403361344538
                        split_key: 0 predicted: 1
                        split_key: 1 split_col: F5 - gini index: 0.19047619047619047
                                split_key: 1 predicted: 1
                                split_key: 0 split_col: F4 - gini index: 0.0
                                        split_key: 1 predicted: 1
                                        split_key: 0 predicted: 0
                split_key: 0 split_col: F1 - gini index: 0.2424242424242424
                        split_key: 0 split_col: F22 - gini index: 0.2222222222222222
                                split_key: 1 split_col: F3 - gini index: 0.0
                                        split_key: 0 predicted: 1
                                        split_key: 1 predicted: 0
                                split_key: 0 predicted: 0
                        split_key: 1 predicted: 1
        split_key: 0 split_col: F11 - gini index: 0.3540849394507931
                split_key: 1 split_col: F3 - gini index: 0.29090909090909073
                        split_key: 0 split_col: F19 - gini index: 0.24
                                split_key: 0 split_col: F5 - gini index: 0.30000000000000004
                                        split_key: 0 split_col: F6 - gini index: 0.0
                                                split_key: 0 predicted: 1
                                                split_key: 1 predicted: 0
                                        split_key: 1 predicted: 0
                                split_key: 1 predicted: 1
                        split_key: 1 predicted: 0
                split_key: 0 split_col: F16 - gini index: 0.2801751094434022
                        split_key: 1 predicted: 1
                        split_key: 0 split_col: F7 - gini index: 0.2802413273001508
                                split_key: 1 split_col: F1 - gini index: 0.26666666666666666
                                        split_key: 0 split_col: F2 - gini index: 0.0
                                                split_key: 0 predicted: 1
                                                split_key: 1 predicted: 0
                                        split_key: 1 predicted: 0
                                split_key: 0 split_col: F4 - gini index: 0.24667931688804542
                                        split_key: 0 split_col: F6 - gini index: 0.26696329254727474
                                                split_key: 0 split_col: F19 - gini index: 0.27939876215738285
                                                        split_key: 0 split_col: F20 - gini index: 0.2403846153846154
                                                                split_key: 1 predicted: 1
                                                                split_key: 0 split_col: F1 - gini index: 0.2125000000000001
                                                                        split_key: 0 predicted: 0
                                                                        split_key: 1 predicted: 0
                                                        split_key: 1 split_col: F1 - gini index: 0.3333333333333333
                                                                split_key: 1 predicted: 1
                                                                split_key: 0 predicted: 0
                                                split_key: 1 predicted: 0
                                        split_key: 1 predicted: 0
--------------------

--------------------
Test Accuracy: 0.7272727272727273
--------------------
```

## OUTPUT FIlES

The output files are written to:

1. Output generated for subset of UCI Mushroom dataset
```
mushroom_output.csv
```

2. Output generated for subset of UCI Heart dataset
```
heart_diagnosis.csv
```