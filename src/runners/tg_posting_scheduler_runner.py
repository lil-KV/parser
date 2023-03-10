# import schedule
# import time
# import threading
# from constants import USED_PARSERS
# from src import db_client
#
# PARSE_EVERY_MINUTES = 5
#
# def make_post():
#     for parser in USED_PARSERS:
#         parser.get_not_posted_flats()
#         thread = threading.Thread(target=parser.send_tg_post())  # запуск потоков
#         thread.start()
#
#
# # планировщик
# schedule.every(PARSE_EVERY_MINUTES).minutes.do(make_post)
#
# # нужно иметь свой цикл для запуска планировщика с периодом в 1 сек:
# while True:
#     schedule.run_pending()
#     time.sleep(1)