# -*- coding: UTF-8 -*-
# 公司参与设立产业孵化基金情况——合作设立产业并购基金公告
# 基金名称
# 基金规模
# 投资期限
# 存续期限
# 投资方向
# 企业出资额
# 孵化/并购
import logging
import model.utils as utils

# {
#     "type" : "text",
#     "content" : "                                                                                                ",
#     "header" : "青岛蔚蓝生物股份有限公司                                          招股说明书",
#     "footer" : null,
#     "page_num" : 0
# },


def extract(detail, sec_name):
    fund_name = ''
    fund_name_page = None
    fund_scale = ''
    fund_scale_page = None
    invest_limit = ''
    invest_limit_page = None
    duration = ''
    duration_page = None
    invest_area = ''
    invest_area_page = None
    invest_money = ''
    invest_money_page = None
    incubate_or_merge = ''
    incubate_or_merge_page = None

    start_index = 0
    for i in range(len(detail)):
        item = detail[i]
        item_type = item.get('type')
        content = item.get('content')
        if item_type == 'text':
            if ('基金' in content or '拟成立合伙企业' in content) and ('主要情况' in content or '基本情况' in content):
                start_index = i
            if len(incubate_or_merge) > 0 or i > 10:
                continue
            if '孵化' in content:
                incubate_or_merge = '孵化'
            elif '并购' in content:
                incubate_or_merge = '并购'
            elif '股权投资基金' in content:
                incubate_or_merge = '股权投资基金'
            elif '产业投资基金' in content:
                incubate_or_merge = '产业投资基金'
            elif '转型发展基金' in content:
                incubate_or_merge = '转型发展基金'
            elif '产业基金' in content:
                incubate_or_merge = '产业基金'
            elif '投资基金' in content:
                incubate_or_merge = '投资基金'
            incubate_or_merge_page = 1

    for i in range(start_index, len(detail)):
        item = detail[i]
        item_type = item.get('type')
        content = item.get('content')
        page = item.get('page_num')
        if item_type == 'text':
            if '名称' in content and len(fund_name) == 0:
                if '：' in content:
                    fund_name = content.split('：')[1]
                else:
                    fund_name = content
                fund_name_page = page
            if '基金规模' in content or '基金募集规模' in content or '出资金额' in content or '基金目标规模' in content or '注册资本' in content or '基金总规模' in content or '出资额' in content:
                if '：' in content:
                    fund_scale = content.split('：')[1]
                else:
                    fund_scale = content
                fund_scale_page = page
            if '存续期' in content or '投资期' in content or '期限' in content:
                duration, invest_limit = extract_duration(content)

                invest_limit_page = page
                duration_page = page
            if '投资领域' in content or '投资方向' in content or '经营范围' in content:
                if '：' in content:
                    invest_area = content.split('：')[1]
                else:
                    invest_area = content
                invest_area_page = page
        # elif item_type == 'table':
        #     row1_string = utils.get_table_line(content[0])
        #     if '合伙人名称' in row1_string:

    logging.info('基金名称：' + fund_name)
    logging.info('基金规模：' + fund_scale)
    logging.info('存续期限：' + duration)
    logging.info('投资期限：' + invest_limit)
    logging.info('投资领域：' + invest_area)
    logging.info('孵化/并购：' + incubate_or_merge)

    knowledge = {"type": "公司参与设立产业孵化基金情况",
                 "table": [{"name": "基金名称",
                            "value": fund_name,
                            "evidence_page_number": [fund_name_page]},
                           {"name": "基金规模",
                            "value": fund_scale,
                            "evidence_page_number": [fund_scale_page]},
                           {"name": "投资期限",
                            "value": invest_limit,
                            "evidence_page_number": [invest_limit_page]},
                           {"name": "存续期限",
                            "value": duration,
                            "evidence_page_number": [duration_page]},
                           {"name": "投资方向",
                            "value": invest_area,
                            "evidence_page_number": [invest_area_page]},
                           {"name": "企业出资额",
                            "value": invest_money,
                            "evidence_page_number": [invest_money_page]},
                           {"name": "孵化/并购",
                            "value": incubate_or_merge,
                            "evidence_page_number": [incubate_or_merge_page]}
                           ]}
    return knowledge


def extract_duration(text):
    duration = text
    if '存续期：' in text or '基金存续期：' in text or '存续期限：' in text or '基金期限：' in text:
        duration = text.split('：')[1]

    invest_limit = ''
    sentence_list = text.split('。')
    for sentence in sentence_list:
        sub_sentence_list = sentence.split('，')
        for sub_sentence in sub_sentence_list:
            if '投资期' in sub_sentence and len(invest_limit) == 0:
                invest_limit = sub_sentence
    return duration, invest_limit
