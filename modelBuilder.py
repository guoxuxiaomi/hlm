#!/usr/bin/python
# -*- coding:gbk -*-

import sys
# import sys
# import imp

import numpy as np

# imp.reload(sys)
# sys.setdefaultencoding("utf-8")


class modelBuilder(object):
    def __init__(self):
        pass

    def get_wordnum_of_chapter(self, DocID):
        path_str = 'text/chapter-' + str(DocID)
        file_in = open(path_str,encoding='UTF-8')

        text = ""
        for line in file_in:
            text += "".join(line.split('\n'))  # ȥ���س�
        file_in.close

        num = len(text)
        return num

    # ÿ���ĵ���ȡ��������
    def build_feature_vector(self, DocID, label):
        path_str = 'text/chapter-wordcount-' + str(DocID)

        # function_word_list = ['֮', '��', '��', '��', '��', '��', '��', '��', '��', '��',
        # 					  '��', '��', '��', '��', '��', '��', '��', '��', 'ѽ',
        # 					  '��', '��', '��', '��', '��', '��', '��', '��', '��', 'Խ',
        # 					  '��', '��', '��', '��', 'ƫ', '��', '��', '��', '��', '��',
        # 					  '��', '��', # 42 ���������
        # 					  '��', 'Ҳ', # ��Ƶ����
        # 					  '��', '��', '��', '��', '��' #��Ƶ����
        # 					  '��', 'ȥ', '��', 'Ц'] #��Ƶ����

        function_word_list = ['֮', '��', '��', '��', '��', '��', '��', '��', '��', '��',
                              '��', '��', '��', '��', '��', '��', 'һ', '��', '��', 'ѽ',
                              '��', '��', '��', '��', '��', '��', '��', '��', '��', 'Խ',
                              '��', '��', '��', '��', 'ƫ', '��', '��', '��', '��', '��',
                              '��', '��',  # 42 ���������
                              '��', 'Ҳ', '��', 'Ҫ',  # ��Ƶ����
                              '��', '��', '��', '��', '��'  # ��Ƶ����
                                                  '��', 'ȥ', '��', 'Ц', '˵'  # ��Ƶ����
                              ]
        feature_vector_list = []

        for function_word in function_word_list:

            find_flag = 0
            file_in = open(path_str, 'r', encoding='UTF-8')  # ÿ�δ��ƶ� cursor ��ͷ��
            line = file_in.readline()
            while line:
                words = line[:-1].split('\t')
                if words[0] == function_word:
                    total_words = self.get_wordnum_of_chapter(DocID)
                    rate = float(words[1]) / total_words * 1000
                    rate = float("%.6f" % rate)  # ָ��λ��
                    feature_vector_list.append(rate)
                    # print words[0] + ' : ' + line

                    file_in.close()
                    find_flag = 1
                    break
                line = file_in.readline()

            # δ�ҵ���ʱ����Ϊ 0
            if not find_flag:
                feature_vector_list.append(0)

        feature_vector_list.append(label)
        return feature_vector_list

    def make_positive_trainset(self):
        positive_trainset_list = []
        for loop in range(20, 30):
            feature = self.build_feature_vector(loop, 1)  # label Ϊ 1 ��ʾ����
            positive_trainset_list.append(feature)
        # print positive_trainset_list
        np.save('pos_trainset.npy', positive_trainset_list)

    def make_negative_trainset(self):
        negative_trainset_list = []
        for loop in range(110, 120):
            feature = self.build_feature_vector(loop, 2)  # label Ϊ 2 ��ʾ����
            negative_trainset_list.append(feature)
        # print negative_trainset_list
        np.save('neg_trainset.npy', negative_trainset_list)

    def make_trainset(self):
        feature_pos = np.load('pos_trainset.npy')
        feature_neg = np.load('neg_trainset.npy')
        trainset = np.vstack((feature_pos, feature_neg))
        np.save('trainset.npy', trainset)

    def make_testset(self):
        testset_list = []
        for loop in range(1, 121):
            feature = self.build_feature_vector(loop, 0)  # ���� label������Ϊ 0
            testset_list.append(feature)
        # print testset_list
        np.save('testset.npy', testset_list)


if __name__ == '__main__':
    builder = modelBuilder()
    # print builder.build_feature_vector(1)

    builder.make_positive_trainset()
    builder.make_negative_trainset()

    builder.make_trainset()
    builder.make_testset()
