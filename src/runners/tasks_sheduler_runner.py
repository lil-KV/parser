import schedule
import time
import threading
from constants import USED_PARSERS


def parse_all():
    for parser in USED_PARSERS:
        thread = threading.Thread(target=parser.update_with_last_flats())  # запуск потоков
        thread.start()


# планировщик
schedule.every(3).seconds.do(parse_all)

# нужно иметь свой цикл для запуска планировщика с периодом в 1 сек:
while True:
    schedule.run_pending()
    time.sleep(1)
