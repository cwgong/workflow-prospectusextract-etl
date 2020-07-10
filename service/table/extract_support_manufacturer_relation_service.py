# -*- coding: UTF-8 -*-
# 公司主要外协厂商业务及关联情况——招股说明书

import service.utils as service_util
import model.table.extract_support_manufacturer_relation as extract_support_manufacturer_relation


def extract(start_at, end_at, time_field):
    # print('extract')
    ann_group = '招股说明书'
    service_util.request_pdf_always(start_at, end_at, time_field, ann_group, extract_method)


def extract_method(detail, sec_name):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    # text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_support_manufacturer_relation.extract(detail)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
