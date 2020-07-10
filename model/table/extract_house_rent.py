# -*- coding: UTF-8 -*-
# 公司房屋建筑物的租赁情况——招股说明书
# [{"name":"租赁房屋建筑物数量",
# "value":int
# "evidence_page_number":[int]},
# {"name":"平均每月租金",
# "value":float
# "evidence_page_number":[int]},
# {"name":"租赁房屋用途表",
# "value":[{"用途":string,
# "数量（处）":int,
# "面积（平方米）":float}],
# "evidence_page_number":[int]},

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
        if '租方' in row1_string and '面积' in row1_string and '用途' in row1_string:
            logging.info(row1_string)
            selected_table.append(merged_table_list[i])
            selected_table_page.append(merged_table_page_list[i])

    logging.info('table count %d' % len(selected_table))
    if len(selected_table) == 0:
        return None

    house_count = None
    average_rent = None
    house_use_list = []
    house_size_list = []

    house_size_index = None
    house_use_index = None
    house_rent_index = None

    table = selected_table[0]
    for i in range(len(table[0])):
        house_count = len(table) - 1

        item = table[0][i]
        if item is None:
            continue
        item = item.replace('\n', '').replace(' ', '')

        if item is None:
            continue
        if '面积' in item:
            house_size_index = i
        if '用途' in item:
            house_use_index = i
        if '租金' in item:
            house_rent_index = i

    if house_count is not None:
        logging.info('租赁房屋建筑物数量：%d' % house_count)

    if house_rent_index is not None:
        total_rent = extract_column_add_on(table, house_rent_index)
        average_rent = total_rent / house_count
        logging.info('平均每月租金：%f' % average_rent)

    for i in range(1, len(table)):
        if house_use_index is not None:
            use_item = table[i][house_use_index]
            house_use_list.append(use_item)
        if house_size_index is not None:
            size_item = table[i][house_size_index]
            house_size_list.append(size_item)

    if len(house_use_list) > 0 and len(house_size_list) > 0:
        logging.info('use list: ' + str(house_use_list))
        logging.info('size list: ' + str(house_size_list))

    total_use = set()
    for i in range(len(house_use_list)):
        item = house_use_list[i]
        if item is None:
            continue
        item = item.replace('\n', '').replace(' ', '')
        if len(item) == 0 or '-' == item:
            continue

        use_sub_list = None
        if '、' in item:
            use_sub_list = item.split('、')
        if '/' in item:
            use_sub_list = item.split('/')
        if use_sub_list is not None:
            for sub_item in use_sub_list:
                total_use.add(sub_item)
        else:
            total_use.add(item)

    value_list = []
    total_use = list(total_use)
    for i in range(len(total_use)):
        use = total_use[i]
        use_count = 0
        use_size = 0
        for j in range(len(house_use_list)):
            use_item = house_use_list[j]
            if use_item is None:
                continue
            use_item = use_item.replace('\n', '').replace(' ', '')
            if len(use_item) == 0 or '-' == use_item:
                continue

            size_item = house_size_list[j]
            if size_item is None:
                continue
            # logging.info('use:' + use + ' use item: ' + use_item)
            if use not in use_item:
                continue
            use_count += 1
            use_size += utils.get_item_number(size_item)
        value_list.append({"用途": use,
                           "数量（处）": use_count,
                           "面积（平方米）": use_size})

    logging.info('租赁房屋用途表：' + str(value_list))

    knowledge = {"type": "公司房屋建筑物的租赁情况",
                 "table": [{"name": "租赁房屋建筑物数量",
                            "value": house_count,
                            "evidence_page_number": selected_table_page},
                           {"name": "平均每月租金",
                            "value": average_rent,
                            "evidence_page_number": selected_table_page},
                           {"name": "租赁房屋用途表",
                            "value": value_list,
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
        item = column[i].replace(' ', '').replace(',', '').replace('．', '.')

        factor = 1
        if '/日' in item or '/天' in item or '每日' in item or '每天' in item:
            factor = 30
        if '/年' in item or '每年' in item:
            factor = 1/float(12)

        number_list = utils.extract_number(item)
        if len(number_list) == 1:
            item = float(number_list[0])
        else:
            if '元' in item:
                money_list = item.split('元')
                money = money_list[0]
                number_list = utils.extract_number(money)
                # logging.info('租金' + item + 'list:' + str(number_list))
                if len(number_list) > 1:
                    item = float(number_list[-1])
                elif len(number_list) == 0:
                    item = 0
                else:
                    item = float(number_list[0])
            elif '/' in item:  # 3.03/3.10
                item = float(number_list[0])

        add_on += item * factor
    return add_on


# if __name__ == "__main__":
#     item = '4元/平方米/天'
#     money_list = item.split('元')
#     print(money_list)
#     money = money_list[0]
#     print(money)
#     number_list = utils.extract_number(money)
#     print(number_list)
#     print(utils.extract_number('2'))
