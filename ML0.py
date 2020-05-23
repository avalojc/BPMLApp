from flask import Flask
import sklearn.linear_model
import joblib
import random
import pandas as pd
import gcsfs

# url = 'https://storage.cloud.google.com/javalo-nhanes-bucket-cen/NHANESbpLabeled.csv'
url = pd.read_csv('gs://javalo-nhanes-bucket-cen/NHANESbpLabeled.csv')
# df = pd.read_csv(url)
# include = ['BPACSZ1', 'BPACSZ2', 'BPACSZ3', 'BPACSZ4', 'BPACSZ5', 'BPXPLS', 'BPXPULS','BPXPTY', 'BPXSY1', 'BPXDI1', 'SysRiskLevels']
# df_ = df[include]

# this is the url without headings

#
# def minkoskiDistribution(v1, v2, p):
#     dist = 0.0
#     for i in range(len(v1)):
#         dist += abs(v1[i] - v2[i]) ** p
#     return dist ** (1 / p)
#
#
# class NHANESSeqn(object):
#     featureNames = ('c2', 'c3', 'c4', 'c5', 'pulse', 'pulseRegularity')
#
#     #  BPACSZ1	BPACSZ2	BPACSZ3	BPACSZ4	BPACSZ5	BPXPLS	BPXPULS	BPXPTY	BPXSY1	BPXDI1	SysRiskLevels
#     def __init__(self, seqNumber, c2, c3, c4, c5, pulse, pulseRegularity, risk):
#         self.seqNumber = seqNumber
#         self.featureVec = [c2, c3, c4, c5, pulse, pulseRegularity]
#         self.label = risk
#
#     def distance(self, other):
#         return minkoskiDistribution(self.featureVec, other.featureVec, 2)
#
#     def getCSize2(self):
#         return self.featureVec[0]
#
#     def getCSize3(self):
#         return self.featureVec[1]
#
#     def getCSize4(self):
#         return self.featureVec[2]
#
#     def getCSize5(self):
#         return self.featureVec[3]
#
#     def getPulse(self):
#         return self.featureVec[4]
#
#     def getPulseRegularity(self):
#         return self.featureVec[5]
#
#     def getSeqNumber(self):
#         return self.seqNumber
#
#     def getFeatures(self):
#         return self.featureVec[:]
#
#     def getLabel(self):
#         return self.label
#
#
# def getNHANESData(fname):
#     data = {'SeqNumber': [], 'CSize2': [], 'CSize3': [], 'CSize4': [], 'CSize5': [], 'pulse': [], 'pulseRegularity': [],
#             'risk': [], }
#     f = open(fname)
#     line = f.readline()
#     while line != '':
#         split = line.split(',')
#         data['SeqNumber'].append(int(split[0]))
#         data['CSize2'].append(int(split[1]))
#         data['CSize3'].append(int(split[2]))
#         data['CSize4'].append(int(split[3]))
#         data['CSize5'].append(int(split[4]))
#         data['pulse'].append(int(split[5]))
#         data['pulseRegularity'].append(int(split[6]))
#         data['risk'].append(int(split[11]))
#
#         line = f.readline()
#     return data
#
#
# def buildNHANESExamples(fileName):
#     data = getNHANESData(fileName)
#     examples = []
#     for i in range(len(data['SeqNumber'])):
#         d = NHANESSeqn(data['SeqNumber'][i], data['CSize2'][i], data['CSize3'][i], data['CSize4'][i], data['CSize5'][i],
#                        data['pulse'][i], data['pulseRegularity'][i], data['risk'][i])
#         examples.append(d)
#     print('Finished processing', len(examples), 'NHANES individuals\n')
#     print(examples[2].getFeatures())
#     print(examples[2].getLabel())
#     print(examples[3].getLabel())
#     print(examples[2].getSeqNumber())
#     return examples
#
#
# examples = buildNHANESExamples(url)
#
#
# def buildModel(examples, toPrint=True):
#     featureVecs, labels = [], []
#     for e in examples:
#         featureVecs.append(e.getFeatures())
#         labels.append(e.getLabel())
#     LogisticRegression = sklearn.linear_model.LogisticRegression
#     model = LogisticRegression().fit(featureVecs, labels)
#     if toPrint:
#         print('model.classes_ =', model.classes_)
#         for i in range(len(model.coef_)):
#             print('For label', model.classes_[1])
#             for j in range(len(model.coef_[0])):
#                 print('   ', NHANESSeqn.featureNames[j], '=',
#                       model.coef_[0][j])
#     return model
#
#
# def applyModel(model, testSet, label, prob=0.95):
#     testFeatureVecs = [e.getFeatures() for e in testSet]
#     probs = model.predict_proba(testFeatureVecs)
#     truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
#     for i in range(len(probs)):
#         if probs[i][1] > prob:
#             if testSet[i].getLabel() == label:
#                 truePos += 1
#             else:
#                 falsePos += 1
#         else:
#             if testSet[i].getLabel() != label:
#                 trueNeg += 1
#             else:
#                 falseNeg += 1
#     return truePos, falsePos, trueNeg, falseNeg
#
#
# def findNearest(name, exampleSet, metric):
#     for e in exampleSet:
#         if e.getName() == name:
#             example = e
#             break
#     curDist = None
#     for e in exampleSet:
#         if e.getName() != name:
#             if curDist == None or \
#                     metric(example, e) < curDist:
#                 nearest = e
#                 curDist = metric(example, nearest)
#     return nearest
#
#
# def accuracy(truePos, falsePos, trueNeg, falseNeg):
#     numerator = truePos + trueNeg
#     denominator = truePos + trueNeg + falsePos + falseNeg
#     return numerator / denominator
#
#
# def sensitivity(truePos, falseNeg):
#     try:
#         return truePos / (truePos + falseNeg)
#     except ZeroDivisionError:
#         return float('nan')
#
#
# def specificity(trueNeg, falsePos):
#     try:
#         return trueNeg / (trueNeg + falsePos)
#     except ZeroDivisionError:
#         return float('nan')
#
#
# def posPredVal(truePos, falsePos):
#     try:
#         return truePos / (truePos + falsePos)
#     except ZeroDivisionError:
#         return float('nan')
#
#
# def getStats(truePos, falsePos, trueNeg, falseNeg, toPrint=True):
#     accur = accuracy(truePos, falsePos, trueNeg, falseNeg)
#     sens = sensitivity(truePos, falseNeg)
#     spec = specificity(trueNeg, falsePos)
#     ppv = posPredVal(truePos, falsePos)
#     if toPrint:
#         print(' Accuracy =', round(accur, 5))
#         print(' Sensitivity =', round(sens, 5))
#         print(' Specificity =', round(spec, 5))
#         print(' Pos. Pred. Val. =', round(ppv, 5))
#     return (accur, sens, spec, ppv)
#
#
# def findKNearest(example, exampleSet, k):
#     kNearest, distances = [], []
#     # Build lists containing first k examples and their distances
#     for i in range(k):
#         kNearest.append(exampleSet[i])
#         distances.append(example.distance(exampleSet[i]))
#     maxDist = max(distances)  # Get maximum distance
#     # Look at examples not yet considered
#     for e in exampleSet[k:]:
#         dist = example.distance(e)
#         if dist < maxDist:
#             # replace farther neighbor by this one
#             maxIndex = distances.index(maxDist)
#             kNearest[maxIndex] = e
#             distances[maxIndex] = dist
#             maxDist = max(distances)
#     return kNearest, distances
#
#
# def KNearestClassify(training, testSet, label, k):
#     """Assumes training & testSet lists of examples, k an int
#        Predicts whether each example in testSet has label
#        Returns number of true positives, false positives,
#           true negatives, and false negatives"""
#     truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
#     for testCase in testSet:
#         nearest, distances = findKNearest(testCase, training, k)
#         # conduct vote
#         numMatch = 0
#         for i in range(len(nearest)):
#             if nearest[i].getLabel() == label:
#                 numMatch += 1
#         if numMatch > k // 2:  # guess label
#             if testCase.getLabel() == label:
#                 truePos += 1
#             else:
#                 falsePos += 1
#         else:  # guess not label
#             if testCase.getLabel() != label:
#                 trueNeg += 1
#             else:
#                 falseNeg += 1
#     return truePos, falsePos, trueNeg, falseNeg
#
#
# def leaveOneOut(examples, method, toPrint=True):
#     truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
#     for i in range(len(examples)):
#         testCase = examples[i]
#         trainingData = examples[0:i] + examples[i + 1:]
#         results = method(trainingData, [testCase])
#         truePos += results[0]
#         falsePos += results[1]
#         trueNeg += results[2]
#         falseNeg += results[3]
#     if toPrint:
#         getStats(truePos, falsePos, trueNeg, falseNeg)
#     return truePos, falsePos, trueNeg, falseNeg
#
#
# def split80_20(examples):
#     sampleIndices = random.sample(range(len(examples)),
#                                   len(examples) // 5)
#     trainingSet, testSet = [], []
#     for i in range(len(examples)):
#         if i in sampleIndices:
#             testSet.append(examples[i])
#         else:
#             trainingSet.append(examples[i])
#     return trainingSet, testSet
#
#
# def randomSplits(examples, method, numSplits, toPrint=True):
#     truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
#     random.seed(0)
#     for t in range(numSplits):
#         trainingSet, testSet = split80_20(examples)
#         results = method(trainingSet, testSet)
#         truePos += results[0]
#         falsePos += results[1]
#         trueNeg += results[2]
#         falseNeg += results[3]
#     getStats(truePos / numSplits, falsePos / numSplits,
#              trueNeg / numSplits, falseNeg / numSplits, toPrint)
#     return truePos / numSplits, falsePos / numSplits, \
#            trueNeg / numSplits, falseNeg / numSplits


# ############################################################# Linear Regression
# def lr(trainingData, testData, prob=0.5):
#     model = buildModel(trainingData, False)
#     results = applyModel(model, testData, 1, prob)
#     return results
#
#
# random.seed(0)
# numSplits = 10
# print('Average of', numSplits, '80/20 splits LR')
# truePos, falsePos, trueNeg, falseNeg = \
#     randomSplits(examples, lr, numSplits)
#
# # Look at weights
# trainingSet, testSet = split80_20(examples)
# model = buildModel(trainingSet, True)

# Look at changing prob

# random.seed(0)
# trainingSet, testSet = split80_20(examples)
# model = buildModel(trainingSet, False)
# print('Try p = 0.1')
# truePos, falsePos, trueNeg, falseNeg = \
#     applyModel(model, testSet, 0, 0.1)
# getStats(truePos, falsePos, trueNeg, falseNeg)
# print('Try p = 0.8')
# truePos, falsePos, trueNeg, falseNeg = \
#     applyModel(model, testSet, 0, 0.8)
# getStats(truePos, falsePos, trueNeg, falseNeg)


# Save your model


# joblib.dump(lr, 'model.pkl')
# print("Model dumped!")
#
# # Load the model that you just saved
# lr = joblib.load('model.pkl')
# print("model loaded")
# # # Saving the data columns from training
# # model_columns = list(x.columns)
# # joblib.dump(model_columns, 'model_columns.pkl')
# # print("Models columns dumped!")
df = pd.read_csv(url)
include = ['BPACSZ2',	'BPACSZ3',	'BPACSZ4',	'BPACSZ5',	'BPXPLS',	'BPXPULS', 'SysRiskLevels']  # Only four features
df_ = df[include]

# Data Preprocessing
categoricals = []
for col, col_type in df_.dtypes.iteritems():
     if col_type == 'O':
          categoricals.append(col)
     else:
          df_[col].fillna(0, inplace=True)

df_ohe = pd.get_dummies(df_, columns=categoricals, dummy_na=True)

# Logistic Regression classifier
from sklearn.linear_model import LogisticRegression
dependent_variable = 'SysRiskLevels'
x = df_ohe[df_ohe.columns.difference([dependent_variable])]
y = df_ohe[dependent_variable]
lr = LogisticRegression()
lr.fit(x, y)

# Save your model
import joblib
joblib.dump(lr, 'model.pkl')
print("Model dumped!")

# Load the model that you just saved
lr = joblib.load('model.pkl')

# Saving the data columns from training
model_columns = list(x.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print("Models columns dumped!")