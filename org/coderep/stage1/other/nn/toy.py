# -- encoding:utf-8 --
import numpy as np

def lookup(w,i):
    return w[i]

def d_lookup(djdy,w,i):
    djdw = np.zeros_like(w)
    djdw[i] = djdy
    return djdw

def linear(w,b,x):
    return np.dot(x,w) + b
'''
??? db=y
'''
def d_linear(djdy,w,b,x):
    djdb = djdy
    djdw = np.dot(x.reshape(-1,1),djdy.reshape(1,-1)).T
    djdx = np.dot(djdy,w.T)
    return djdx,djdw,djdb

def tanh(x):
    return np.tanh(x)

def d_tanh(djdy,y):
    djdx = djdy * (1 - y)*y
    return djdx

def softmax(x):
    ex = np.exp(x)
    ex = ex / np.sum(ex)
    return ex

def cross_entropy(x,i):
    return -np.log(x[i])
'''
有softmax和cross_entropy结合的求导公式，最终操作的就是x “推所有拉一个”
'''
def d_cross_entropy_softmax(softmax_y,i):
    djdx = softmax_y
    djdx[i] -= 1
    return djdx

'''
h1 = lookup
h2= wx+b
h3=tanh(h2)
h4=wx+b
h5=softmax(h4)
ce=cross_entropy(h5,current_word)


input_embed [[0.4,1],[0.2,0.4],[-0.3,2]] 
pre_word 0 ,
分析下 词典是0，1，2 共3个维度，one-hot，[1 0 0][0 1 0][1 0 0]
比如第一个词是0， one-hot 就是[1 0 0] shape=1,3 ; embeding=3*2。
输入= 1行vocab_size列 ，embedding=vocab_size行 降维列
将维度从 vocab_size 降到 低维度，2列的内容是什么呢， 应该是0或者随机数。因为内容最后是学到的。
所以embed一定得是 3行，因为就3个词，这个例子只能2列，降维，还得学东西。

经过 input 0和embed[[0.4,1],[0.2,0.4],[-0.3,2]]得lookup 
得到h1 = [0.4,1]  
h1=[0.4,1] w=[[1.2,0.2],[-0.4,0.4]] [0,0.5]
得到h2=[0.08,0.98] 得到h3=[ 0.07982977  0.7530659 ]

h3=[ 0.07982977  0.7530659 ] embed[[-1,1],[0.4,0.5],[-0.3,0.2]]的转置，b[0, 0.5, 0] 得到h4[ 0.67323614  0.90846486  0.12666425]

h4[ 0.67323614  0.90846486  0.12666425] softmax h5[ 0.35160147  0.44484552  0.20355301]，现在是字典中每个词是label的概率
ce = 负对数， 0.810028205586 

对交叉熵有些懵，看看解释。这里的计算只是去了信息量，没有用真实概率。

'''
def forward(input_embed,linear_w,linear_b,output_embed, output_embed_b, pre_word, current_word):

    print("Forward")
    print()
    print(input_embed)
    print(pre_word)
    # forward
    h1 = lookup(input_embed, pre_word)
    print("h1")
    print(h1)

    h2 = linear(linear_w,linear_b,h1)
    print("h2")
    print(h2)

    h3 = tanh(h2)
    print("h3")
    print(h3)

    h4 = linear(output_embed.T,output_embed_b,h3)
    print("h4")
    print(h4)

    h5 = softmax(h4)
    print("h5")
    print(h5)

    ce = cross_entropy(h5,current_word)
    print("ce")
    print(ce)
    
    return h1,h2,h3,h4,h5,ce
'''

'''
def backward(input_embed,linear_w,linear_b,output_embed, output_embed_b, pre_word, current_word,h1,h2,h3,h4,h5):

    print("Backward")
    print()

    # backward
    # dj/d_softmax_y
    djdh4 = d_cross_entropy_softmax(h4,current_word)
    
    print("djdh4")
    print(djdh4)

    djdh3, djd_output_embed, djd_output_embed_b = d_linear(djdh4,output_embed.T, output_embed_b, h3)
    print("djdh3, djd_output_embed, djd_output_embed_b")
    print(djdh3) 
    print(djd_output_embed) 
    print(djd_output_embed_b)

    
    djdh2 = d_tanh(djdh3,h2)
    print("djdh2")
    print(djdh2)


    djdh1, djd_linear_w, djd_linear_b = d_linear(djdh2, linear_w, linear_b, h1)
    print("djdh1, djd_linear_w, djd_linear_b")
    print(djdh1)
    print(djd_linear_w)
    print(djd_linear_b)


    djd_input_embed = d_lookup(djdh1,input_embed,pre_word)
    print("djd_input_embed")
    print(djd_input_embed)


    return djdh4,djdh3,djdh2,djdh1,djd_input_embed,djd_linear_w,djd_linear_b,djd_output_embed, djd_output_embed_b

def update_weight(input_embed,linear_w,linear_b,output_embed, output_embed_b,djd_input_embed,djd_linear_w,djd_linear_b,djd_output_embed, djd_output_embed_b,eta):
    input_embed += - eta * djd_input_embed
    linear_w += -eta * djd_linear_w
    output_embed += eta * djd_output_embed
    output_embed_b +=-eta * djd_output_embed_b
    return input_embed,linear_w,linear_b,output_embed, output_embed_b




def main():
    # Define the matrix
    input_embed = np.array([[0.4,1],[0.2,0.4],[-0.3,2]])
    linear_w = np.array([[1.2,0.2],[-0.4,0.4]])
    linear_b = np.array([0,0.5])
    output_embed = np.array([[-1,1],[0.4,0.5],[-0.3,0.2]])
    output_embed_b = np.array([0,0.5,0])
    pre_word = 0 # a
    current_word = 1 # b
    eta = 0.1

    #forward
    for i in range(10):

        print("======================")
        print("Iteration ", i)
        
        h1,h2,h3,h4,h5,ce = forward(input_embed,linear_w,linear_b,output_embed, output_embed_b, pre_word, current_word)
        print()

        # backward
        djdh4,djdh3,djdh2,djdh1,djd_input_embed,djd_linear_w,djd_linear_b,djd_output_embed, djd_output_embed_b = backward(input_embed,linear_w,linear_b,output_embed, output_embed_b, pre_word, current_word,h1,h2,h3,h4,h5)
        print() 

        # update the parameters
        input_embed,linear_w,linear_b,output_embed, output_embed_b = update_weight(input_embed,linear_w,linear_b,output_embed, output_embed_b,djd_input_embed,djd_linear_w,djd_linear_b,djd_output_embed, djd_output_embed_b,eta)

if __name__ == "__main__":
    main()
