# -*- coding: utf-8 -*-

__author__ = 'Doohoon Kim'

"""
    직접 구현한 간단한 Indexer 및 Searcher
"""

from operator import itemgetter

class indexer:
    def __init__(self):
        self.__dic_name = dict()
        self.__valuelist_of_name_ = [[] for _ in range(255)]

    def __delete_dup(self, v):
        # 중복을 제거한다.
        arrayx = list(set(v))

        # data를 sort 시킨다(desc).
        return sorted(arrayx, reverse=True)

    def __chg_list_to_intl(self, v):
        # list를 int형으로 변환한다.
        return [int(i) for i in v]

    def __sort_dic(self):
        return sorted(self.__dic_name.iteritems(), key=itemgetter(1), reverse=True)

    def insertData(self, v, name):
        # 인덱서 Data 삽입 파트.

        # 중복 제거 및 sort
        dd = self.__delete_dup(v)
        # 부동소숫점형(float)을 int형으로 변환
        ci = self.__chg_list_to_intl(dd)

        # 문서 번호와 함께 딕셔너리를 만든다.
        # 단, 생성될때와 아닐때를 구분한다.
        if name in self.__dic_name:
            pass
        else:
            self.__dic_name[name] = 0

        # 이름 인덱스를 삽입한다.
        for i in range(len(ci)):
            # 이름들을 인덱스(0부터 180 미만 까지)에 맞게 이름을 삽입
            self.__valuelist_of_name_[ci[i]].append(name)

    def findData(self, v):
        dd = self.__delete_dup(v)
        ci = self.__chg_list_to_intl(dd)
        # 오는 리스트의 값을 하나씩 확인하여 vote함.
        for i in enumerate(ci):
            for j in self.__valuelist_of_name_[i[1]]:
                self.__dic_name[j] += 1

        # 마지막으로, 값으로 정렬하여 가장 높은 것 중 10개 미만을 가져온다.
        res = self.__sort_dic()

        retRes = []
        for i in range(9):
            retRes.append(res[i])
        return  retRes # [i for i in res(range(0, 9))]

    def innerDic(self):
        return self.__dic_name