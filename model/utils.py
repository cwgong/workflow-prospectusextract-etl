# -*- coding: UTF-8 -*-

import re
import json
import requests


# 删除序号
def delete_index(text):
    text = re.sub(r'^（[0-9]{1,2}）', '', text)  # 替换（1）
    text = re.sub(r'^[0-9]{1,2}）', '', text)  # 替换1）
    text = re.sub(r'^[0-9]{1,2}、', '', text)  # 替换1、
    text = re.sub(r'^[0-9]{1,2}\.', '', text)  # 替换1.
    text = re.sub(r'^[0-9]{1,2}．', '', text)  # 替换1．
    text = re.sub(r'^\([0-9]{1,2}\)', '', text)  # 替换(1)
    text = re.sub(r'^（[一二三四五六七八九十]+）', '', text)  # 替换（一）
    text = re.sub(r'^[一二三四五六七八九十]+、', '', text)  # 替换一、
    text = re.sub(r'^\([一二三四五六七八九十]+\)', '', text)  # 替换(一)
    text = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩⑪]+', '', text)  # 替换①
    return text


# 判断是否为标题
def is_title(text):
    if '。' in text:
        return -1
    if text.endswith('；'):
        return -1

    rule_list = [r'^（[0-9]{1,2}）',  # （1）
                 r'^[0-9]{1,2}）',  # 1）
                 r'^[0-9]{1,2}、',  # 1、
                 r'^[0-9]{1,2}\.',  # 1.
                 r'^[0-9]{1,2}．',  # 1．
                 r'^\([0-9]{1,2}\)',  # (1)
                 r'^（[一二三四五六七八九十]+）',  # （一）
                 r'^[一二三四五六七八九十]+、',  # 一、
                 r'^\([一二三四五六七八九十]+\)',  # (一)
                 r'^[①②③④⑤⑥⑦⑧⑨⑩⑪]+']  # ①

    text = text.strip('\t').strip()
    for i in range(len(rule_list)):
        pattern = re.compile(rule_list[i])
        result = pattern.findall(text)
        if len(result) != 0:
            return i
    return -1


# 标题等级
def title_level(text):
    text = text.strip()
    if '。' in text:
        return -1
    if text.endswith('；'):
        return -1

    level1_list = [
        r'^[一二三四五六七八九十]+、',  # 一、
    ]

    level2_list = [
        r'^（[一二三四五六七八九十]+）',  # （一）
        r'^\([一二三四五六七八九十]+\)',  # (一)
    ]

    level3_list = [
        r'^[0-9]{1,2}、',  # 1、
        r'^[0-9]{1,2}\.',  # 1.
        r'^[0-9]{1,2}．',  # 1．
    ]

    level4_list = [
        r'^（[0-9]{1,2}）',  # （1）
        r'^[0-9]{1,2}）',  # 1）
    ]

    level5_list = [
        r'^[①②③④⑤⑥⑦⑧⑨⑩⑪]+']  # ①

    levels = [level5_list, level4_list, level3_list, level2_list, level1_list]

    text = text.strip('\t').strip()
    for i in range(len(levels)):
        rule_list = levels[i]
        for j in range(len(rule_list)):
            pattern = re.compile(rule_list[j])
            result = pattern.findall(text)
            if len(result) != 0:
                return i
    return -1


def text_valid(para):
    para = para.strip()
    if not para:
        return False
    if "√适用" in para:
        return False
    if '具体内容详见' in para:
        return False
    if para.startswith('详见本报告'):
        return False
    return True


def extract_number(text):
    if len(text) == 1 and text.isdigit():
        return [float(text)]
    pattern = re.compile(r'[0-9]+\.?[0-9]+')  # 查找数字
    result = pattern.findall(text)
    return result


def contain_number(text):
    pattern = re.compile(r'\d+')  # 查找数字
    result = pattern.findall(text)
    return len(result) != 0


def contain_all_number(text):
    pattern = re.compile(r'\d+')  # 查找数字
    result1 = pattern.findall(text)
    pattern = re.compile(r'[一二三四五六七八九十]+')
    result2 = pattern.findall(text)
    pattern = re.compile(r'[①②③④⑤⑥⑦⑧⑨⑩⑪]+')
    result3 = pattern.findall(text)
    return len(result1) != 0 or len(result2) != 0 or len(result3) != 0


def remove_duplicate_item(item_list):
    new_list = []
    for i in range(len(item_list)):
        item = item_list[i]
        if item in new_list:
            continue
        else:
            new_list.append(item)
    return new_list


# 删除key_word所在句，逗号分隔
def delete_half_sentence(text, key_word):
    sentence_list = text.split('，')
    new_sentence_list = []
    for sentence in sentence_list:
        if key_word in sentence:
            continue
        new_sentence_list.append(sentence)
    return_text = '，'.join(new_sentence_list)
    return return_text


# 删除key_word后所有，逗号分隔
def delete_suffix(text, key_word):
    sentence_list = text.split('，')
    new_sentence_list = []
    for sentence in sentence_list:
        if key_word in sentence:
            break
        new_sentence_list.append(sentence)
    return_text = '，'.join(new_sentence_list)
    return return_text


def get_table_line(row):
    row_string = ''
    for item in row:
        if item is not None:
            row_string += item + ' '
    row_string = row_string.replace('\n', '')
    return row_string


def split_sentence(sen):
    nlp_url = 'http://hanlp-nlp-service:31001/hanlp/segment/segment'
    try:
        cut_sen = dict()
        cut_sen['content'] = sen
        cut_sen['customDicEnable'] = True
        data = json.dumps(cut_sen).encode("UTF-8")
        cut_response = requests.post(nlp_url, data=data, headers={'Connection': 'close'})
        cut_response_json = cut_response.json()
        return cut_response_json['data']
    except Exception as e:
        print("Exception: {}".format(e))
        print("hanlp-nlp-service error")
        print("sentence: {}".format(sen))
        return []


def get_striped(string):
    return ''.join([x for x in string if len(x.strip()) > 0])


def get_item_number(item):
    if item is None:
        return 0
    if item == '/' or item == '-' or len(item) == 0 or item == "—":
        return 0

    item = item.replace(',', '')
    item = item.strip()
    if not item.isnumeric():
        item = get_number_sequence(item)
        if len(item) == 0:
            return 0
    return float(item)


def get_number_sequence(text):
    number_string = ''
    for item in text:
        if item.isdigit():
            number_string += item
        if item == '.':
            number_string += item
        if item == '．':
            number_string += '.'
    return number_string


def extract_column_add_on(table, index):
    column = extract_column(table, index)
    if len(column) == 0:
        print('error')
        return 0

    add_on = 0.0
    for i in range(len(column)):
        if i == 0:
            continue
        item = column[i]
        add_on += get_item_number(item)
    return add_on


def extract_column(table, index):
    column_list = []
    for line in table:
        item = line[index]
        if item is None:
            continue
        item = item.replace('\n', '')
        column_list.append(item)
    return column_list


def merge_table(table_list, table_page_list):
    merged_table_list = []
    merged_table_page_list = []

    last_table_line1 = ''
    last_line_item_count = 0
    for i in range(len(table_list)):
        table = table_list[i]
        page = table_page_list[i]

        table_line1 = get_table_line(table[0])
        if len(merged_table_list) == 0:
            merged_table_list.append(table)
            merged_table_page_list.append(page)
            last_table_line1 = table_line1
            last_line_item_count = len(table[0])
            continue

        if last_line_item_count != len(table[0]):
            merged_table_list.append(table)
            merged_table_page_list.append(page)
            last_table_line1 = table_line1
            last_line_item_count = len(table[0])
            continue

        not_title = contain_number(table_line1) and '年' not in table_line1 and 'm2' not in table_line1
        if not_title:
            last_table = merged_table_list[-1]
            last_table.extend(table)
        elif table_line1 == last_table_line1:
            last_table = merged_table_list[-1]
            last_table.extend(table[1:])
        else:
            merged_table_list.append(table)
            merged_table_page_list.append(page)
            last_table_line1 = table_line1
            last_line_item_count = len(table[0])

    return merged_table_list, merged_table_page_list
