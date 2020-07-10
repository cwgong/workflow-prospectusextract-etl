# -*- coding: UTF-8 -*-
# 公司综合融资成本——发行情况报告书
import logging
import model.utils as utils


def extract(text_list, text_page_list):
    cost_list = []
    cost_page_list = []
    for i in range(len(text_list)):
        temp_text = text_list[i]
        if is_cost(temp_text):
            cost_list.append(temp_text)
            cost_page_list.append(text_page_list[i])

    if len(cost_list) == 0:
        logging.info('none')
        return None
    # logging.info(str(cost_list))

    text = cost_list[0]
    if len(cost_list) > 1:
        logging.info('cost list length > 1' + str(cost_list))
    if '。' in text:
        sentence_list = text.split('。')
        for i in range(len(sentence_list)):
            if is_cost(sentence_list[i]):
                text = sentence_list[i]
    if '。' in text:
        logging.info('none。')
        return None

    if '，' in text:
        sub_sentence_list = text.split('，')
        for i in range(len(sub_sentence_list)):
            if is_cost(sub_sentence_list[i]):
                text = sub_sentence_list[i]
    if '，' in text:
        logging.info('none，')
        return None

    logging.info("费用:" + text)
    text = text.replace(',', '')
    numbers = utils.extract_number(text)
    if len(numbers) == 0:
        logging.info('none number:' + text)
        return None

    knowledge = {"type": "公司综合融资成本",
                 "table": [{"name": "公司综合融资成本",
                            "value": numbers[0],
                            "evidence_page_number": cost_page_list}
                           ]
                 }

    return knowledge


def is_cost(text):
    if ('发行费用' in text or '与发行有关的费用' in text) and utils.contain_number(text) and '元' in text:
        return True
    else:
        return False


if __name__ == "__main__":
    print(utils.extract_number('333.12'))
    print(utils.extract_number('333'))
