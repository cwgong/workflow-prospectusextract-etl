# -*- coding: UTF-8 -*-
# 公司土地使用权情况——招股说明书
# [{"name":"土地使用权数量",
# "value":int
# "evidence_page_number":[int]},
# {"name":"土地使用权总面积",
# "value":float
# "evidence_page_number":[int]}

import model.utils as utils
import logging


def extract(table_list, table_page_list):
    merged_table_list, merged_table_page_list = utils.merge_table(table_list, table_page_list)
    selected_table = []
    selected_table_page = []
    for i in range(len(merged_table_list)):
        if len(merged_table_list[i]) <= 1:
            continue
        row1_string = utils.get_table_line(merged_table_list[i][0])
        if '土地' in row1_string and '面积' in row1_string:
            logging.info(row1_string)
            selected_table.append(merged_table_list[i])
            selected_table_page.append(merged_table_page_list[i])

    logging.info('table count %d' % len(selected_table))
    if len(selected_table) == 0:
        return None

    count = None
    total_size = None

    size_index = None

    table = selected_table[0]
    for i in range(len(table[0])):
        count = len(table) - 1

        item = table[0][i]
        if item is None:
            continue
        item = item.replace('\n', '').replace(' ', '')

        if '面积' in item:
            size_index = i

    for i in range(1, len(table)):
        if size_index is not None:
            total_size = extract_column_add_on(table, size_index)

    logging.info('土地使用权数量：%d' % count)
    if total_size is not None:
        logging.info('土地使用权总面积：%f' % total_size)

    knowledge = {"type": "公司土地使用权情况",
                 "table": [{"name": "土地使用权数量",
                            "value": count,
                            "evidence_page_number": selected_table_page},
                           {"name": "土地使用权总面积",
                            "value": total_size,
                            "evidence_page_number": selected_table_page}
                           ]}
    return knowledge


def extract_column_add_on(table, index):
    column = utils.extract_column(table, index)
    if len(column) == 0:
        print('error')
        return 0

    add_on = 0.0
    for i in range(len(column)):
        if i == 0:
            continue
        item = column[i].replace(' ', '').replace('²', '')
        if '分摊面积' in item:
            item_list = item.split('分摊面积')
            item = item_list[-1]
        add_on += utils.get_item_number(item)
    return add_on
