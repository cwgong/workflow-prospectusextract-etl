# -*- coding: UTF-8 -*-
# 公司参与设立产业孵化基金情况——合作设立产业并购基金公告

import service.utils as service_util
import model.table.extract_set_up_fund as extract_set_up_fund


def extract(start_at, end_at, time_field):
    # print('extract')
    ann_group = '合作设立产业并购基金公告'
    service_util.request_pdf_always(start_at, end_at, time_field, ann_group, extract_method)


def extract_method(detail, sec_name):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    # text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_set_up_fund.extract(detail, sec_name)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
