# -*- coding: UTF-8 -*-

# service通用配置，调用extract_service.py，使用TornadoScheduler调度任务

import sys

sys.path.append('./service')

# 自定义版本
from _version import __version__

# python
import io
import json

# tornado
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

import apscheduler.events
from apscheduler.schedulers.background import BackgroundScheduler

# 进程间共享一个job store会出错，需要存在不同的表里，即每次都在db中新建一个table
# sql_alchemy_job_store = SQLAlchemyJobStore(url='mysql://analyse:GemanticYes!@10.0.0.20:3306/apscheduler',
#                                            tablename='annual_report_extract_jobs')
# job_stores = {'mysql': sql_alchemy_job_store}
# sched = TornadoScheduler(jobstores=job_stores)
# sched = TornadoScheduler()
back_sched = BackgroundScheduler()

import service.table.extract_set_up_fund_service as extract_set_up_fund_service
import service.table.extract_synthesize_fund_cost_service as extract_synthesize_fund_cost_service
import service.table.extract_support_manufacturer_relation_service as extract_support_manufacturer_relation_service
import service.table.extract_house_owned_service as extract_house_owned_service
import service.table.extract_house_rent_service as extract_house_rent_service
import service.table.extract_land_use_rights_service as extract_land_use_rights_service
import service.table.extract_machine_equipment_quantity_service as extract_machine_equipment_quantity_service


# const
# version
VERSION = "0.1"
START_AT = ''  # 默认跑最近一天
END_AT = ''  # 默认跑最近一天
TIME_FIELD_UPDATE = 'updateAt'  # 定时任务使用
TIME_FIELD_PUB = 'pubDateAt'  # debug使用
DEBUG_START_AT = '1483200000000'  # 2017-01-01
DEBUG_END_AT = '1586966400000'  # 2020-04-16


@back_sched.scheduled_job('cron', id='1', name='set_up_fund',
                          second='0', minute='1', hour='4', day='*', month='*', day_of_week='*')
def extract_set_up_fund():
    # print("start")
    extract_set_up_fund_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='2', name='synthesize_fund_cost',
                          second='0', minute='2', hour='4', day='*', month='*', day_of_week='*')
def extract_synthesize_fund_cost():
    # print("start")
    extract_synthesize_fund_cost_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='3', name='support_manufacturer_relation',
                          second='0', minute='3', hour='4', day='*', month='*', day_of_week='*')
def extract_support_manufacturer_relation():
    # print("start")
    extract_support_manufacturer_relation_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='4', name='house_owned',
                          second='0', minute='4', hour='4', day='*', month='*', day_of_week='*')
def extract_house_owned():
    # print("start")
    extract_house_owned_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='5', name='house_rent',
                          second='0', minute='5', hour='5', day='*', month='*', day_of_week='*')
def extract_house_rent():
    # print("start")
    extract_house_rent_service.extract(start_at=DEBUG_START_AT, end_at=DEBUG_END_AT, time_field=TIME_FIELD_PUB)


@back_sched.scheduled_job('cron', id='6', name='land_use_rights',
                          second='0', minute='6', hour='4', day='*', month='*', day_of_week='*')
def extract_land_use_rights():
    # print("start")
    extract_land_use_rights_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='7', name='machine_equipment_quantity',
                          second='10', minute='7', hour='4', day='*', month='*', day_of_week='*')
def extract_machine_equipment_quantity():
    # print("start")
    extract_machine_equipment_quantity_service.extract(start_at=DEBUG_START_AT, end_at=DEBUG_END_AT, time_field=TIME_FIELD_PUB)


class RunExtractHandler(tornado.web.RequestHandler):
    # input: {'startAt':1521648000000,'endAt':1521648000000,'timeField':updateAt,'knowledgeType':'公司税收优惠'}
    def get(self):
        logging.info("run extract by get")
        try:
            start_at = self.get_query_argument('startAt')
        except Exception as e:
            logging.exception(e)
            start_at = ''
        try:
            end_at = self.get_query_argument('endAt')
        except Exception as e:
            logging.exception(e)
            end_at = ''
        try:
            time_field = self.get_query_argument('timeField')
        except Exception as e:
            logging.exception(e)
            time_field = ''
        try:
            knowledge_type = self.get_query_argument('knowledgeType')
        except Exception as e:
            logging.exception(e)
            knowledge_type = ''
        if knowledge_type == '公司参与设立产业孵化基金情况':
            extract_set_up_fund_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司综合融资成本':
            extract_synthesize_fund_cost_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司主要外协厂商业务及关联情况':
            extract_support_manufacturer_relation_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司土地使用权情况':
            extract_land_use_rights_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司房屋建筑物的租赁情况':
            extract_house_rent_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司房屋建筑物的自有情况':
            extract_house_owned_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司核心机器设备的自有情况':
            extract_machine_equipment_quantity_service.extract(start_at=start_at, end_at=end_at, time_field=time_field)
        else:
            logging.info('knowledge type not recognized: ' + knowledge_type)
            self.write('knowledge type not recognized: ' + knowledge_type)
            return
        logging.info(
            "finish to run extract: " + knowledge_type + " start at: " + start_at + " end at: " + end_at + " time field: " + time_field)
        self.write(
            "finish to run extract: " + knowledge_type + " start at: " + start_at + " end at: " + end_at + " time field: " + time_field)


class PauseJobHandler(tornado.web.RequestHandler):
    # 接口输入 {'jobId':'dayTask'}
    def get(self):
        try:
            logging.info("pause job by get")
            job_id = self.get_query_argument('jobId')

            back_sched.pause_job(job_id)
            self.write("pause job: %s" % job_id)
        except Exception as e:
            logging.exception(e)


class ResumeJobHandler(tornado.web.RequestHandler):
    # 接口输入 {'jobId':'dayTask'}
    def get(self):
        try:
            logging.info("resume job by get")
            job_id = self.get_query_argument('jobId')

            back_sched.resume_job(job_id)
            self.write("resume job: %s" % job_id)
        except Exception as e:
            logging.exception(e)


class RemoveJobHandler(tornado.web.RequestHandler):
    # 接口输入 {'jobName':'dayTask'}
    def get(self):
        try:
            logging.info("remove job by get")
            job_id = self.get_query_argument('jobId')

            back_sched.remove_job(job_id)
            self.write("remove job: %s" % 2)
        except Exception as e:
            logging.exception(e)


class RemoveAllJobsHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("remove all jobs by get")
        back_sched.remove_all_jobs()
        self.write("remove all jobs")


class QueryJobsHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("query jobs by get")
        jobs = back_sched.get_jobs()
        job_info_list = []
        for job in jobs:
            time = job.next_run_time
            time_string = time.strftime("%Y-%m-%d %H:%M:%S")
            job_info = {"job_id": job.id,
                        "job_name": job.name,
                        "next_run_time": time_string}
            job_info_list.append(job_info)
        result_json = json.dumps(job_info_list, ensure_ascii=False)
        self.write(result_json)
        logging.info('query jobs by get finished!')


class ModifyJobHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("modify job by get")
        job_id = self.get_query_argument('jobId')
        job_name = self.get_query_argument('jobName')
        max_instances = self.get_query_argument('maxInstances')
        back_sched.modify_job(job_id, name=job_name, max_instances=max_instances)
        self.write('modify job: ' + job_id + ', new name: ' + job_name + ', new max instances: ' + max_instances)
        logging.info('modify job by get finished!')


class RescheduleJobHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("reschedule job by get")
        job_id = self.get_query_argument('jobId')
        seconds = self.get_query_argument('seconds')
        back_sched.reschedule_job(job_id=job_id, trigger='interval', seconds=seconds)
        logging.info("reschedule job by get finished!")


class StartHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.start()
        result = back_sched.running
        self.write("start scheduler: %s" % result)


class ShutdownSchedHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.shutdown()
        self.write("shutdown scheduler")


class PauseSchedHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.pause()
        self.write("pause scheduler")


class ResumeSchedHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.resume()
        self.write("resume scheduler")


class Application(tornado.web.Application):

    def __init__(self, config):
        handlers = [
            # run
            (r"/run", RunExtractHandler),
            # scheduler
            (r"/scheduler/start", StartHandler),
            (r"/scheduler/shutdown", ShutdownSchedHandler),
            (r"/scheduler/pause", PauseSchedHandler),
            (r"/scheduler/resume", ResumeSchedHandler),
            # job
            (r"/job/pause", PauseJobHandler),
            (r"/job/resume", ResumeJobHandler),
            (r"/job/remove_one", RemoveJobHandler),
            (r"/job/remove_all", RemoveAllJobsHandler),
            (r"/job/query", QueryJobsHandler),
            (r"/job/modify", ModifyJobHandler),
            (r"/job/rechedule", RescheduleJobHandler),
        ]
        settings = dict(
            debug=bool(config['debug']),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def job_exception_listener(event):
    if event.exception:
        logging.critical("crashed job id: " + event.job_id)
    else:
        logging.info('The job worked :' + event.job_id)


def job_missed_listener(event):
    logging.critical("The job missed: " + event.job_id)


def job_max_instances_listener(event):
    logging.info("The job reached max executing instances : " + event.job_id)


def init_apscheduler():
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    back_sched.add_listener(job_exception_listener,
                            apscheduler.events.EVENT_JOB_ERROR | apscheduler.events.EVENT_JOB_EXECUTED)
    back_sched.add_listener(job_missed_listener, apscheduler.events.EVENT_JOB_MISSED)
    back_sched.add_listener(job_max_instances_listener, apscheduler.events.EVENT_JOB_MAX_INSTANCES)


# config
def parse_conf_file(config_file):
    config = {}
    with io.open(config_file, 'r', encoding='utf8') as f:
        config = json.load(f)
    return config


def main(argv):
    if sys.version_info < (3,):
        reload(sys)
        sys.setdefaultencoding("utf-8")

    if VERSION != __version__:
        print("version error!")
        logging.info("version error!")
        exit(-1)

    if len(argv) < 3:
        print('arg error.')
        exit(-2)

    config = parse_conf_file(argv[1])
    tornado.options.parse_config_file(config['log_config_file'])

    logging.info("Server Inititial ... ")

    app = Application(config)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(config['port'])
    server.start(config['process_num'])

    init_apscheduler()
    back_sched.start()

    logging.info("Server Inititial Success! ")
    print("Server Inititial Success! ")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(sys.argv)
