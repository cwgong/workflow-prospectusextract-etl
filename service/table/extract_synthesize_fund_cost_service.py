# -*- coding: UTF-8 -*-
# 公司综合融资成本——发行情况报告书

import service.utils as service_util
import model.table.extract_synthesize_fund_cost as extract_synthesize_fund_cost


def extract(start_at, end_at, time_field):
    # print('extract')
    ann_group = '发行情况报告书'
    service_util.request_pdf_always(start_at, end_at, time_field, ann_group, extract_method)


def extract_method(detail, sec_name):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_synthesize_fund_cost.extract(text_list, text_page_list)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
