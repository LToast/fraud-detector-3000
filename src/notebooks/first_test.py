# mypy: ignore-errors
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# VALIDATION
VALID_SIZE = 0.20  # simple validation using train_test_split
TEST_SIZE = 0.20  # test size using_train_test_split
RFC_METRIC = "gini"  # metric used for RandomForrestClassifier
NUM_ESTIMATORS = 100  # number of estimators used for RandomForrestClassifier
NO_JOBS = 4  # number of parallel jobs used for RandomForrestClassifier


RANDOM_STATE = 2018

data_df = pd.read_csv("../../data/raw/creditcard.csv")

target = "Class"
predictors = [
    "Time",
    "V1",
    "V2",
    "V3",
    "V4",
    "V5",
    "V6",
    "V7",
    "V8",
    "V9",
    "V10",
    "V11",
    "V12",
    "V13",
    "V14",
    "V15",
    "V16",
    "V17",
    "V18",
    "V19",
    "V20",
    "V21",
    "V22",
    "V23",
    "V24",
    "V25",
    "V26",
    "V27",
    "V28",
    "Amount",
]

train_df, test_df = train_test_split(
    data_df, test_size=TEST_SIZE, random_state=RANDOM_STATE, shuffle=True
)
train_df, valid_df = train_test_split(
    train_df, test_size=VALID_SIZE, random_state=RANDOM_STATE, shuffle=True
)

clf = RandomForestClassifier(
    n_jobs=NO_JOBS,
    random_state=RANDOM_STATE,
    criterion=RFC_METRIC,
    n_estimators=NUM_ESTIMATORS,
    verbose=False,
)

clf.fit(train_df[predictors], train_df[target].values)

preds = clf.predict(valid_df[predictors])

# %%
cm = pd.crosstab(
    valid_df[target].values, preds, rownames=["Actual"], colnames=["Predicted"]
)
fig, (ax1) = plt.subplots(ncols=1, figsize=(5, 5))
sns.heatmap(
    cm,
    xticklabels=["Not Fraud", "Fraud"],
    yticklabels=["Not Fraud", "Fraud"],
    annot=True,
    ax=ax1,
    linewidths=0.2,
    linecolor="Darkblue",
    cmap="Blues",
)
plt.title("Confusion Matrix", fontsize=14)
plt.show()
roc_auc_score(valid_df[target].values, preds)

# %%
