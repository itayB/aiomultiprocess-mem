import logging
import os
import sys

from multiprocessing import Pool

logger = logging.getLogger(__name__)


def init_logger():
    logging.basicConfig(
        format="%(asctime)-15s %(process)d %(levelname)-18.18s %(message)s [%(filename)s:%(lineno)d]",
        stream=sys.stdout
    )
    logging.root.setLevel(logging.INFO)


def my_mem_task(task_id):
    logger.info(f"T{task_id:03} started!")
    data = []
    for i in range(100_000):
        data.append([i] * 1_000)
    logger.info(f"T{task_id:03} {len(data)}")


def main():
    init_logger()
    number_of_processes = int(os.getenv("NUMBER_OF_PROCESSES", "4"))
    logger.info("creating pool")
    with Pool(
            processes=number_of_processes,
            initializer=init_logger,
    ) as pool:
        task_ids = [task_id for task_id in range(150)]
        pool.map(my_mem_task, task_ids)
        pool.close()
        logger.info("processes pool closed")
        pool.join()
        logger.info("all processes are done")
