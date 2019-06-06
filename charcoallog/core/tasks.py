import json

from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

# from charcoallog.core.scrap_line3_service import Scrap
from charcoallog.core.service import SUMMARY, collect_summary

LOGGER = get_task_logger(__name__)


# @periodic_task(run_every=(crontab(day_of_week='sat', hour='6', minute='0')), name='ibov')
# def ibov():
#     LOGGER.info('inicio de core/ibov.json')
#
#     ibov_stuff = Scrap()
#     json_data = {"ibov": ibov_stuff.ibov_webscrapping()}
#
#     with open('./charcoallog/core/ibov.json', 'w') as ibov_info:
#         json.dump(json_data, ibov_info)
#
#     LOGGER.info('fim de core/ibov.json')
#
#
# @periodic_task(run_every=(crontab(day_of_month='14-16', hour='6', minute='10')), name='selic')
# def selic():
#     LOGGER.info('inicio de core/selic.json')
#
#     selic_stuff = Scrap()
#     json_data = {"selic": selic_stuff.selic_webscrapping()}
#
#     with open('./charcoallog/core/selic.json', 'w') as selic_info:
#         json.dump(json_data, selic_info)
#
#     LOGGER.info('fim de core/selic.json')
#
#
# @periodic_task(run_every=(crontab(day_of_month='14-16', hour='6', minute='20')), name='ipca')
# def ipca():
#     LOGGER.info('inicio de core/ipca.json')
#
#     ipca_stuff = Scrap()
#     json_data = {"ipca": ipca_stuff.ipca_webscrapping()}
#
#     with open('./charcoallog/core/ipca.json', 'w') as ipca_info:
#         json.dump(json_data, ipca_info)
#
#     LOGGER.info('fim de core/ipca.json')


@periodic_task(run_every=(crontab(day_of_month='1', hour='4', minute='20')), name='summary')
def summary():
    LOGGER.info('inicio de summary')

    to_json = collect_summary()

    with open(SUMMARY, 'w') as fd:
        json.dump(to_json, fd)

    LOGGER.info('fim de summary')
