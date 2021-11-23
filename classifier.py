'''
By: Jonah Stegman
Classifier for ENGG*6500 project
This file will use a random forest to classify the data set
'''
import pandas as pd
import os
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve, accuracy_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.metrics import RocCurveDisplay
import numpy as np
from datetime import datetime

def depth_of_forest(clf):
    nodes = []
    depth = []
    for tree in clf.estimators_:
        nodes.append(tree.tree_.node_count)
        depth.append(tree.tree_.max_depth)
    print(f'Average number of nodes {int(np.mean(nodes))}')
    print(f'Average maximum depth {int(np.mean(depth))}')


def feature_importance(clf, x):
    '''
    graphs each feature and its importance score
    :param clf:
    :param x:
    :return:
    '''
    importance = pd.Series(clf.feature_importances_, index=x.columns).sort_values(ascending=False)
    sns.barplot(x=importance, y=importance.index)
    # Add labels to your graph
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.title("Important Features")
    plt.show()


def visualize_tree(clf, x):
    '''
    visualizes the random forest tree
    :param clf:
    :param x:
    :return:
    '''
    fn=x.columns
    cn='Label'
    fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (40,30), dpi=100)
    tree.plot_tree(clf.estimators_[0],
                   feature_names = fn,
                   class_names=cn,
                   filled = True)
    fig.savefig('rf_individualtree.png')



def evaluate_model(clf, test_values, test_labels):
    '''
    Generates the ROC curve of the random forest
    :param probs:
    :param test_labels:
    :return:
    '''

    probs = clf.predict_proba(test_values)[:, 1]
    auc = roc_auc_score(test_labels, clf.predict_proba(test_values)[:, 1])
    # Calculate false positive rates and true positive rates
    base_fpr, base_tpr, _ = roc_curve(test_labels, [1 for _ in range(len(test_labels))])
    model_fpr, model_tpr, _ = roc_curve(test_labels, probs)
    plt.figure(figsize=(8, 6))
    plt.rcParams['font.size'] = 16
    # Plot both curves
    plt.plot(base_fpr, base_tpr, 'b', label=f'baseline: 0.5')
    plt.plot(model_fpr, model_tpr, 'r', label=f'AUC: {auc:.3f}')
    plt.legend()
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves')
    plt.show()

def speed_test(clf,path):
    '''
    This function tests the speed of the classifier
    :param clf:
    :param path:
    :return:
    '''
    input_file = "data/extracted_features2.csv"
    df = pd.read_csv(os.path.join(path, input_file))
    x = df.drop(['Label', 'URL', 'Num_Digits', 'Num_Alpha'], 1)
    for i in range(10):
        start = datetime.now()
        clf.predict(x[i:i+1])
        stop = datetime.now()
        diff = stop - start
        print(diff.total_seconds())

if __name__ == "__main__":
    path = os.path.dirname(__file__)
    input_file = "data/extracted_features2.csv"
    #read in file
    df = pd.read_csv(os.path.join(path, input_file))
    #drop unused columns
    x = df.drop(['Label', 'URL', 'Num_Digits', 'Num_Alpha'], 1)
    y = df['Label']

    #split data set into train and test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4)
    start = datetime.now()
    #classifier
    clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                                 max_depth=None, max_features='auto', max_leaf_nodes=None,
                                 min_impurity_decrease=0.0,
                                 min_samples_leaf=1, min_samples_split=2,
                                 min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
                                 oob_score=False, random_state=None, verbose=0,
                                 warm_start=False)
    clf.fit(x_train, y_train)
    stop = datetime.now()
    diff = stop - start
    print(diff.total_seconds())
    #speed_test(clf, path)
    y_pred = clf.predict(x_test)

    #get f1 score
    f1 = f1_score(y_test, y_pred)
    print(f1)
    #looking at fp and fn's
    # y_test = y_test.reset_index()
    # x_test = x_test.reset_index()
    # df2 = pd.DataFrame()
    # data = []
    # for j in range(0, len(y_pred)):
    #     if y_test['Label'][j] != y_pred[j] and y_pred[j] == 0:
    #         data.append(x_test[j:j+1])
    # df2 = df2.append(data, ignore_index=True)
    # print(df2)
    #get accuracy
    print("Accuracy:", accuracy_score(y_test, y_pred))
    #depth_of_forest(clf)
    #feature_importance(clf, x)
    #visualize_tree(clf, x)
    #evaluate_model(clf, x_test, y_test)


