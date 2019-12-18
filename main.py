import logging
import time
import schedule
from burgeramt_bot import check_termin_and_send_email


logging.basicConfig(
    filename="burgeramt.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def job():
    logging.info("Job starts...")
    check_termin_and_send_email()


schedule.every().hour.do(job)

time.sleep(30)

job()

while 1:
    schedule.run_pending()
    time.sleep(1)
