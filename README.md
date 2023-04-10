# DECISION TREE FROM SCRATCH

## REQUIREMENTS
```
python >= 3.6
```

## CONFIGS
This code is designed to be config driven.
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
output_filename - filepath where decision tree classified file is to be stored.
```

### STEPS TO RUN
```
- STEP 1: Specify the config to be used for training and testing in the decision_tree.py file.
    - STEP 1 WILL BE MADE CONFIG DRIVEN IN THE NEXT COMMITS
    - EXAMPLE CODE CHANGES IN CODE:
        - from configs.mush_dataset_config import train_config, test_config
        - from configs.heart_dataset_config import train_config, test_config
- STEP 2__:  Run the decision_tree.py python script.
    - EXAMPLE COMMAND:
        - python decison_tree.py
```

### SAMPLE CONFIGS

1. Subset of UCI Mushroom dataset\
https://archive.ics.uci.edu/ml/datasets/mushroom\
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

2. Subset of UCI Heart Dataset\
https://archive.ics.uci.edu/ml/datasets/spect+heart\
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

### OUTPUT GENERATED FOR THE CONFIGS ADDED ABOVE

1. Subset of UCI Mushroom dataset\
https://archive.ics.uci.edu/ml/datasets/mushroom\
dataset is added in `data` directory\
train_data - data/mush_train.data\
test_data - data/mush_test.data

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

2. Subset of UCI Heart Dataset\
https://archive.ics.uci.edu/ml/datasets/spect+heart\
dataset is added in `data` directory\
train_data - data/heart_train.data\
test_data - data/heart_test.data

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
