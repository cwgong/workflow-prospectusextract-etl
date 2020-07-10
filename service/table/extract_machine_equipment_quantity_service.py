# -*- coding: UTF-8 -*-
# 公司核心机器设备的自有情况

import service.utils as service_util
import model.table.extract_machine_equipment_quantity as extract_machine_equipment_quantity


def extract(start_at, end_at, time_field):
    # print('extract')
    ann_group = '债券募集说明书'
    service_util.request_pdf_always(start_at, end_at, time_field, ann_group, extract_method)


def extract_method(detail, sec_name):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_machine_equipment_quantity.extract(table_list, table_page_list, sec_name)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
