# -*- coding: utf-8 -*-
import logging
import sys

import pymongo

# 开发环境
dev_uri = 'mongodb://test:test@10.0.0.173:27017/test_yyh'
dev_db_name = 'test_yyh'

# 测试环境
sta_uri = 'mongodb://dc_report:dcRep0rt2get@10.0.0.173:27017/dc_report'
sta_db_name = 'dc_report'

# 生产环境
prod_uri = 'mongodb://dc_report:dcRep0rt2get@192.168.10.172:27017,192.168.10.174:27017/dc_report'
prod_db_name = 'dc_report'

# 开发连生产
prod_dev_uri = 'mongodb://dc_report:dcRep0rt2get@10.0.0.95:27017/dc_report'
prod_dev_db_name = 'dc_report'

# 表名
# table = 'annDetailTW'


class DataBase(object):

    def __init__(self, uri, db_name, table):
        self.client = pymongo.MongoClient(uri)  # timeout时间serverSelectionTimeoutMS=300000, socketTimeoutMS=300000
        self.db = self.client[db_name]
        self.collection = self.db.get_collection(table)

    # start end 时间区间，前闭后开
    def get_data(self, start, end, time_filed, ann_group):
        start = int(start)
        end = int(end)
        data = self.collection.find({time_filed: {"$gte": start, "$lt": end}, 'parseStatus': '1',
                                     'annGroup': ann_group}).batch_size(10)
        return data


def get_pdf(start, end, time_field, ann_group):
    env = sys.argv[2]
    uri = dev_uri
    db_name = dev_db_name
    if env == 'staging':
        uri = sta_uri
        db_name = sta_db_name
    elif env == 'prod':
        uri = prod_uri
        db_name = prod_db_name
    elif env == 'prod_dev':
        uri = prod_dev_uri
        db_name = prod_dev_db_name
    logging.info(env)
    logging.info(uri)
    logging.info(db_name)

    if ann_group == '合作设立产业并购基金公告' or ann_group == '发行情况报告书':
        table_name = 'annDetailTW'
    else:
        table_name = 'annDetail'

    # 连接数据库
    db = DataBase(uri, db_name, table_name)
    # 迭代器中元素只能被获取一次
    data = db.get_data(start, end, time_field, ann_group)
    return data

