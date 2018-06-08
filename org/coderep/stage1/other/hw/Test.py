# -- encoding:utf-8 --

import operator
import InfoGain
import Data

def majority_cnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1

        sort_class_count=sorted(classCount.iteritems(),key=operator.itemgetter(1), reverse=True )

    print("sort_class_count  ",sort_class_count)
    return sort_class_count[0][0]

'''
边界判断：label完全一样，不必分类

'''
def create_tree(dataSet, feature_name):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majority_cnt(classList)

    best_feature = InfoGain.chooseBestFeatureToSplit(dataSet)
    best_feature_name = feature_name[best_feature]

    myTree={best_feature_name:{}}
    del (feature_name[best_feature])

    feature_value= [example[best_feature] for example in dataSet]
    unique = set(feature_value)

    # 一个根的每个子节点（不同的value是一棵树），都是一棵 子树
    #每个子树，都不再有 根节点的信息。
    for value in unique:
        sub_feature_name = feature_name[:] ##防止修改原值的复制
        myTree[best_feature_name][value] = create_tree(Data.splitDataSet(dataSet,best_feature,value),sub_feature_name)

    return myTree

if __name__ == '__main__':
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']
               ]
    feature_name = ['no surfacing', 'flippers']

    myTree = create_tree(dataSet, feature_name)
    print "myTree ",myTree










