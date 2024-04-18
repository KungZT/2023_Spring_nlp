"""中文分词
步骤一:
数据准备
    1.准备训练数据
    2.准备标签数据
    3.生成词表
"""

import pickle as pkl


# 准备训练数据，从文件中读取文本，删除不必要的字符，如空格和换行符，然后将处理过的文本转储到 pickle 文件中。
def build_train_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tmp = f.readlines()

    t = []
    for i in tmp:
        t1 = i.replace('“  ', '')#将“替换为空字符串
        t2 = t1.replace('\n', '')#换行符替换为空字符串
        t.append(t2)

    sum_list = []
    for i in t:
        sum_ = i.replace('  ', '')#两个空格替换为一个空格
        sum_list.append(sum_)

    with open('./train_data.pkl', 'wb') as f:
        pkl.dump(sum_list, f)#以二进制保存


# 准备标签数据(B:begin,M:median,E:end,S:single)，遵循中文分词的 BEMS（Begin、End、Middle、Single）标注方案。它为输入文本中的每个字符分配标签，然后将结果标签转储到 pickle 文件中。
def build_target(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tmp = f.readlines()

    t = []
    for i in tmp:
        t1 = i.replace('“  ', '')
        t2 = t1.replace('\n', '')
        t.append(t2)

    sum_list = []
    for i in t:
        sum_ = ''
        for j in i.split():
            if len(j) == 1:
                sum_ += 'S'
                continue
            else:
                sum_ += 'B'
                for k in range(1, len(j)):
                    if k == len(j) - 1:
                        sum_ += 'E'
                    else:
                        sum_ += 'M'#对于单个字符的单词，直接将其标记为单个字符 S；对于多个字符的单词，将首字母标记为 B，中间字符标记为 M，末尾字符标记为 E。最后将每一行的标记序列添加到列表 sum_list 中。
        sum_list.append(sum_)

    with open('./target.pkl', 'wb') as f:
        pkl.dump(sum_list, f)


# 生成词表，此函数基于训练数据生成词汇表字典。它计算训练数据中每个字符的出现次数，按频率排序，并为每个字符分配一个索引。最后，它将词汇表字典转储到 pickle 文件中。
def build_vocab_dict(file_path):
    vocab_dic = {}
    with open(file_path, 'rb') as f:
        z = pkl.load(f)
        for line in z:
            for hang in line:
                vocab_dic[hang] = vocab_dic.get(hang, 0) + 1#遍历每个字符 hang，并将其作为键加入到 vocab_dic 字典中，同时统计该字符在训练数据中出现的次数
        vocab_dic_sorted = sorted(vocab_dic.items(), key=lambda x: x[1], reverse=True)#排序

    vocab_dic2 = {word_count[0]: idx for idx, word_count in enumerate(vocab_dic_sorted)}#创建一个新的字典 vocab_dic2，其中键为字符，值为该字符在排序后的列表中的索引。
    with open('./vocab.pkl', 'wb') as f:
        pkl.dump(vocab_dic2, f)


if __name__ == '__main__':
    build_train_data('F:/课程/nlp/nlp_class-main/tokenizer/train.txt')  # 准备训练数据
    build_target('./train.txt')  # 准备标签数据(B:begin,M:median,E:end,S:single)
    build_vocab_dict('./train_data.pkl')  # 生成词表
