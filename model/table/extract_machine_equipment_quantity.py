# -*- coding: UTF-8 -*-
# 公司核心机器设备的自有情况
# [{"name":"公司核心机器设备的自有情况",
#
# "value":[{"主要设备":"string",
#
# "账面价值（万元）":"float",
#
# "成新率（%）":"float"}],
#
# "evidence_page_number":[int]}]

import logging
import model.utils as utils
import re


def extract(table_list, table_page_list,sec_name):
    # text_list = []
    # table_list = []
    # text_page_list = []
    # table_page_list = []
    new_table = [['主要设备', '账面价值（万元）', '成新率（%）']]
    new_table_page_list = []

    for i in range(len(table_list)):
        table = table_list[i]
        page = table_page_list[i]

        line_1 = table[0]
        line_1_string = utils.get_table_line(line_1)

        main_machine_index = -1
        now_price_index = -1
        new_rate_index = -1

        if len(table) == 1:
            continue
        if ('账面价值' in line_1_string or '净值' in line_1_string) and '设备名称' in line_1_string and '成新率' in line_1_string:
            for j in range(len(line_1)):
                if line_1[j] is None:
                    continue
                line_1[j] = line_1[j].replace('\n', '').replace(' ', '').replace('（', '').replace('）', '')
                if '设备名称' in line_1[j]:
                    main_machine_index = j
                if '成新率' in line_1[j]:
                    new_rate_index = j
                if '账面价值' in line_1[j] or '净值' in line_1[j]:
                    now_price_index = j

            for k in range(1,len(table)):
                row = table[k]
                main_machine = row[main_machine_index]
                if main_machine is None:
                    main_machine = ''
                main_machine = main_machine.replace('\n', '').replace(',', '')

                new_rate = row[new_rate_index]
                if new_rate is None:
                    new_rate = ''
                new_rate = new_rate.replace('\n', '').replace(',', '')

                now_price = row[now_price_index]
                if now_price is None:
                    now_price = ''
                now_price = now_price.replace('\n', '').replace(',', '')

                new_row = [main_machine, now_price, new_rate]
                new_table.append(new_row)
            new_table_page_list.append(page)

    if len(new_table) == 1:
        return None
    else:
        knowledge_list = []
        for item in new_table:
            if item == ['主要设备', '账面价值（万元）', '成新率（%）']:
                continue
            if '%' in item[2]:
                item[2] = item[2].replace('%','')

            if item[0] != '':
                item_1 = str(item[0])
            else:
                item_1 = None

            if item[1] != '':
                item_2 = float(item[1])
            else:
                item_2 = None

            if item[2] != '':
                item_3 = float(item[2])
            else:
                item_3 = None
            item_dict = {"主要设备": item_1,
                         "账面价值（万元）": item_2,
                         "成新率（%）": item_3}
            knowledge_list.append(item_dict)

        for value_item in knowledge_list:
            if value_item['主要设备'] != None:
                break
            if value_item['账面价值（万元）'] != None:
                break
            if value_item['成新率（%）'] != None:
                break
            return None

        knowledge = {"type": "公司核心机器设备的自有情况",
                     "table": [{"name": "公司核心机器设备的自有情况",
                                "value": knowledge_list,
                                "evidence_page_number": new_table_page_list}]
                     }
    return knowledge



def delete_word_in_brackets(text):
    s = '3.88'
    print(s.isdigit())

if __name__ == "__main__":
    t = None
    if t != '':
        t = str(t)
    else:
        t = None
    print(t)
