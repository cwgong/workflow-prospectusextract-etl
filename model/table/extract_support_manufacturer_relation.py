# -*- coding: UTF-8 -*-
# 公司主要外协厂商业务及关联情况——招股说明书
# [{"name":"",
# "value":[{"名称":"",
# ""
# "是否关联方":""}],
# "evidence_page_number":[int]}]
import logging
import model.utils as utils


def extract(detail):
    page_list = []

    relation_text = ''
    for i in range(len(detail)):
        item = detail[i]
        item_type = item.get('type')
        content = item.get('content')
        if item_type == 'text':
            if is_relation(content):
                sentence_list = content.split('。')
                for sentence in sentence_list:
                    if is_relation(sentence):
                        relation_text = sentence
                        page_list.append(item.get('page_num'))
                        break

    table_list = []
    for i in range(len(detail)):
        item = detail[i]
        item_type = item.get('type')
        content = item.get('content')
        if item_type == 'table':
            if len(content) <= 1:
                continue
            row1_string = utils.get_table_line(content[0])
            if not has_support_name(row1_string):
                continue

            table_list.append(content)
            page_list.append(item.get('page_num'))

    if len(table_list) == 0:
        return None

    page_list = utils.remove_duplicate_item(page_list)
    relation = get_relation_from_text(relation_text)
    name_relation_dict = {}
    for i in range(len(table_list)):
        table = table_list[i]

        name_index = -1
        relation_index = -1
        for j in range(len(table[0])):
            title = table[0][j]
            if title is None:
                continue
            title = title.replace('\n', '').replace(' ', '')
            if is_support_name(title):
                name_index = j
            if '是否关联' in title:
                relation_index = j

        if name_index == -1:
            logging.info('error 无法找到厂商名称列 continue' + str(table[0]))
            continue

        for j in range(1, len(table)):
            name = table[j][name_index]
            if name is None:
                continue
            name = name.replace('\n', '').replace(' ', '')
            if relation_index != -1:
                relation = table[j][relation_index]

            if relation is None:
                logging.info('error 无法找到关联关系 return none')
                return None
            name_relation_dict[name] = relation

    if len(name_relation_dict) == 0:
        return None

    value_list = []
    for key in name_relation_dict.keys():
        value_list.append({"名称": key,
                           "是否关联方": name_relation_dict.get(key)})

    if len(value_list) == 0:
        return None

    knowledge = {"type": "公司主要外协厂商业务及关联情况",
                 "table": [{"name": "公司主要外协厂商业务及关联情况",
                            "value": value_list,
                            "evidence_page_number": page_list}],
                 "text": relation_text
                 }

    return knowledge


def get_relation_from_text(text):
    if len(text) == 0:
        return None
    if '不存在任何关联关系' in text or '不存在关联关系' in text or '无关联关系' in text:
        return '否'
    # 均未在上述外协厂商中持有权益或存在关联关系
    if '，' in text:
        sub_sentence_list = text.split('，')
        for sub_sentence in sub_sentence_list:
            if '未' in sub_sentence and '存在关联关系' in sub_sentence:
                return '否'
    logging.info('关联关系：' + text)
    return '是'


def is_relation(text):
    if ('外协' in text or '委外' in text or '委托加工' in text) and '关联关系' in text:
        return True
    else:
        return False


def has_support_name(text):
    # if ('外协' in row1_string or '委外' in row1_string) and ('比例' in row1_string or '占比' in row1_string or '关联关系' in row1_string):
    if ('外协' in text or '委外' in text) and ('名称' in text or '厂商' in text):
        return True
    else:
        return False


def is_support_name(text):
    if ('外协' in text or '委外' in text or '供应商' in text) and ('名称' in text or '厂商' in text):
        return True
    elif '名称' in text and '产品名称' not in text:
        return True
    else:
        return False
