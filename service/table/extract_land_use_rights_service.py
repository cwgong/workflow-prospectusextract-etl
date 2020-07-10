# -*- coding: UTF-8 -*-
# 公司土地使用权情况——招股说明书

import service.utils as service_util
import model.table.extract_land_use_rights as extract_land_use_rights


def extract(start_at, end_at, time_field):
    # print('extract')
    ann_group = '招股说明书'
    service_util.request_pdf_always(start_at, end_at, time_field, ann_group, extract_method)


def extract_method(detail, sec_name):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_land_use_rights.extract(table_list, table_page_list)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
