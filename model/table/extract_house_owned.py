# -*- coding: UTF-8 -*-
# 公司房屋建筑物的自有情况——招股说明书
# [{"name":"自有房屋建筑物数量",
# "value":int
# "evidence_page_number":[int]},
# {"name":"自有房屋建筑物面积",
# "value":float
# "evidence_page_number":[int]},
# {"name":"自有房屋建筑物用途",
# "value":string
# "evidence_page_number":[int]},
# {"name":"自有房屋建筑物抵押数量",
# "value":int
# "evidence_page_number":[int]},
# {"name":"自有房屋建筑物抵押面积",
# "value":float
# "evidence_page_number":[int]},
# {"name":"自有房屋建筑物抵押账面价值",
# "value":float
# "evidence_page_number":[int]}]

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
        if ('房产证号' in row1_string or '房权证号' in row1_string or '权证编号' in row1_string) and '面积' in row1_string\
                and '租' not in row1_string and '土地' not in row1_string:
            logging.info(row1_string)
            selected_table.append(merged_table_list[i])
            selected_table_page.append(merged_table_page_list[i])

    logging.info('table count %d' % len(selected_table))
    if len(selected_table) == 0:
        return None

    house_count = None
    house_total_size = None
    house_use_set = set()
    house_mortgage_count = None
    house_mortgage_size = None
    house_mortgage_value = None

    house_size_index = None
    house_use_index = None
    house_mortgage_index = None
    house_number_index = None

    table = selected_table[0]
    for i in range(len(table[0])):
        item = table[0][i]
        if item is None:
            continue
        item = item.replace('\n', '').replace(' ', '')
        if '面积' in item:
            house_size_index = i
        if '用途' in item:
            house_use_index = i
        if '抵押' in item:
            house_mortgage_index = i
        if '房产证号' in item or '房权证号' in item or '权证编号' in item:
            house_number_index = i

    if house_number_index is not None:
        number_list = utils.extract_column(table, house_number_index)
        house_count = len(number_list) - 1
        logging.info('自有房屋建筑物数量：%d' % house_count)

    if house_size_index is not None:
        house_total_size = extract_column_add_on(table, house_size_index)
        house_total_size = round(house_total_size, 4)
        logging.info('自有房屋建筑物面积：%f' % house_total_size)

    for i in range(1, len(table)):
        if house_use_index is not None:
            use_item = table[i][house_use_index]
            if use_item is None:
                continue
            use_item = use_item.replace('\n', '').replace(' ', '')
            if len(use_item) == 0 or '-' == use_item:
                continue
            use_sub_list = None
            if '、' in use_item:
                use_sub_list = use_item.split('、')
            if '/' in use_item:
                use_sub_list = use_item.split('/')
            if use_sub_list is not None:
                for sub_item in use_sub_list:
                    house_use_set.add(sub_item)
            else:
                house_use_set.add(use_item)

        if house_mortgage_index is not None:
            mortgage_item = table[i][house_mortgage_index]
            size_item = table[i][house_size_index]
            if mortgage_item is None:
                continue
            if house_mortgage_count is None:
                house_mortgage_count = 0
                house_mortgage_size = 0
            if '是' == mortgage_item or '抵押' == mortgage_item:
                house_mortgage_count += 1

                if size_item is None:
                    continue
                if '建筑' in size_item:
                    size_item = size_item[size_item.index('建筑'):]
                house_mortgage_size += utils.get_item_number(size_item)

    if len(house_use_set) > 0:
        logging.info('自有房屋建筑物用途：' + ','.join(house_use_set))

    if house_mortgage_count is not None:
        house_mortgage_size = round(house_mortgage_size, 4)
        logging.info('自有房屋建筑物抵押数量：%d' % house_mortgage_count)
        logging.info('自有房屋建筑物抵押面积：%f' % house_mortgage_size)

    # logging.info('自有房屋建筑物抵押账面价值：' + house_mortgage_value)

    knowledge = {"type": "公司房屋建筑物的自有情况",
                 "table": [{"name": "自有房屋建筑物数量",
                            "value": house_count,
                            "evidence_page_number": selected_table_page},
                           {"name": "自有房屋建筑物面积",
                            "value": house_total_size,
                            "evidence_page_number": selected_table_page},
                           {"name": "自有房屋建筑物用途",
                            "value": ','.join(house_use_set),
                            "evidence_page_number": selected_table_page},
                           {"name": "自有房屋建筑物抵押数量",
                            "value": house_mortgage_count,
                            "evidence_page_number": selected_table_page},
                           {"name": "自有房屋建筑物抵押面积",
                            "value": house_mortgage_size,
                            "evidence_page_number": selected_table_page},
                           {"name": "自有房屋建筑物抵押账面价值",
                            "value": house_mortgage_value,
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
        item = column[i].replace(' ', '')
        if '建筑' in item:
            item = item[item.index('建筑'):]
        add_on += utils.get_item_number(item)
    return add_on


# if __name__ == "__main__":
#     item = '建筑：7,106.32'
#     if '建筑' in item:
#         item = item[item.index('建筑'):]
#     item = utils.get_item_number(item)
#     print(item)
