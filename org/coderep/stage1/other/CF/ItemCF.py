# --- coding:utf-8 ---
import numpy as np
import csv
import time
from pprint import pprint as p
import reader

def read_csv():
    #遍历csv，一个id是需要，
    #定位找到行和列加1.如何定位矩阵的行列'''
    read = csv.DictReader(open("data/score.csv"))
    print (read.fieldnames)

    np.mat(np.zeros(()))
    items_set = set()

    for row in read:
        items_set.add(row['Item'])
    items_list = list(items_set);
    items_list.sort()
    print (items_list)

    mat_size = items_list.__len__()
    mat = np.mat(np.zeros((mat_size, mat_size)))
    print mat
    '''遍历csv，一个id是需要，定位找到行和列加1.如何定位矩阵的行列'''
    # mat.

    # for i in mat.shape.


def log(func):
    def wrapper(*args, **kwargs):
        now_time = str(time.strftime('%Y-%m-%d %X', time.localtime()))
        print('------------------------------------------------')
        print('%s %s called' % (now_time, func.__name__))
        print('Document:%s' % func.__doc__)
        print('%s returns:' % func.__name__)
        re = func(*args, **kwargs)
        p(re)
        return re
    return wrapper


@log
def get_set_key(data):
    '''构建一个关键词集合，用于作为共现矩阵的首行和首列'''
    all_key = '/'.join(data)
    key_list = all_key.split('/')
    set_key_list = list(filter(lambda x: x != '', key_list))
    return list(set(set_key_list))


@log
def format_data(data):
    '''格式化需要计算的数据，将原始数据格式转换成二维数组'''
    formated_data = []
    for ech in data:
        ech_line = ech.split('/')
        formated_data.append(ech_line)
    return formated_data


@log
def build_matirx(set_key_list):
    '''建立矩阵，矩阵的高度和宽度为关键词集合的长度+1'''
    edge = len(set_key_list)+1
    # matrix = np.zeros((edge, edge), dtype=str)
    matrix = [['' for j in range(edge)] for i in range(edge)]
    return matrix


@log
def init_matrix(set_key_list, matrix):
    '''初始化矩阵，将关键词集合赋值给第一列和第二列'''
    matrix[0][1:] = np.array(set_key_list)
    matrix = list(map(list, zip(*matrix)))
    matrix[0][1:] = np.array(set_key_list)
    return matrix


@log
def count_matrix(matrix, formated_data):
    '''计算各个关键词共现次数'''
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
                # 遍历矩阵第一列，跳过下标为0的元素
                # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if matrix[0][row] == matrix[col][0]:
                # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                matrix[col][row] = str(0)
            else:
                counter = 0
                # 初始化计数器
                for ech in formated_data:
                        # 遍历格式化后的原始数据，让取出的行关键词和取出的列关键词进行组合，
                        # 再放到每条原始数据中查询
                    if matrix[0][row] in ech and matrix[col][0] in ech:
                        counter += 1
                    else:
                        continue
                matrix[col][row] = str(counter)
    return matrix


def main():
    keyword_path = r'data/test.xlsx'
    output_path = r'2.txt'
    data = reader.readxls_col(keyword_path)[0]
    set_key_list = get_set_key(data)
    formated_data = format_data(data)
    matrix = build_matirx(set_key_list)
    matrix = init_matrix(set_key_list, matrix)
    result_matrix = count_matrix(matrix, formated_data)
    np.savetxt(output_path, result_matrix, fmt=('%s,'*len(matrix))[:-1])


if __name__ == '__main__':
    # open_csv()
    # read_csv()
    main()