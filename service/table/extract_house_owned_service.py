# -*- coding: UTF-8 -*-
# 公司房屋建筑物的自有情况——招股说明书

import service.utils as service_util
import model.table.extract_house_owned as extract_house_owned


def extract(start_at, end_at, time_field):
    # print('extract')
    ann_group = '招股说明书'
    service_util.request_pdf_always(start_at, end_at, time_field, ann_group, extract_method)


def extract_method(detail, sec_name):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_house_owned.extract(table_list, table_page_list)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
