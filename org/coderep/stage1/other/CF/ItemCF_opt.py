@log
def get_set_key(dic,threshold):
    '''选取频数大于等于Threshold的关键词构建一个集合，用于作为共现矩阵的首行和首列'''
    wf = {k: v for k, v in dic.items() if v >= threshold}
    set_key_list=[]
    for a in sorted(wf.items(), key=lambda item: item[1], reverse=True):
        set_key_list.append(a[0])
    return set_key_list

@log
def format_data(data,set_key_list):
    '''格式化需要计算的数据，将原始数据格式转换成二维数组'''
    formated_data = []
    for ech in data:
        ech_line = ech.split('/')

        temp=[]            # 筛选出format_data中属于关键词集合的词
        for e in ech_line:
            if e in set_key_list:
                temp.append(e)
        ech_line=temp

        ech_line = list(set(filter(lambda x: x != '', ech_line))) #set去掉重复数据
        formated_data.append(ech_line)
    return formated_data

@log
def count_matrix(matrix, formated_data):
    '''计算各个关键词共现次数'''
    keywordlist=matrix[0][1:]  #列出所有关键词
    appeardict={}  #每个关键词与 [出现在的行(formated_data)的list] 组成的dictionary
    for w in keywordlist:
        appearlist=[]
        i=0
        for each_line in format_data:
            if w in each_line:
                appearlist.append(i)
            i +=1
        appeardict[w]=appearlist
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
                # 遍历矩阵第一列，跳过下标为0的元素
                # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if col >= row:
                #仅计算上半个矩阵
                if matrix[0][row] == matrix[col][0]:
                    # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                    matrix[col][row] = str(0)
                else:
                    counter = len(set(appeardict[matrix[0][row]])&set(appeardict[matrix[col][0]]))

                    matrix[col][row] = str(counter)
            else:
                matrix[col][row]=matrix[row][col]
    return matrix