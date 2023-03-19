import asyncio
import logging
import os
import sys

from aiomultiprocess import Pool

logger = logging.getLogger(__name__)


def init_logger():
    logging.basicConfig(
        format="%(asctime)-15s %(process)d %(levelname)-18.18s %(message)s [%(filename)s:%(lineno)d]",
        stream=sys.stdout
    )
    logging.root.setLevel(logging.INFO)


async def is_alive(pool):
    while True:
        if pool is not None:
            logger.info(f"heartbeat alive {len(pool.processes.keys())} processes")
        await asyncio.sleep(1)


async def my_mem_task(task_id):
    logger.info(f"T{task_id:03} started!")
    data = []
    for i in range(100_000):
        data.append([i] * 1_000)
    logger.info(f"T{task_id:03} {len(data)}")


async def main():
    init_logger()
    number_of_processes = int(os.getenv("NUMBER_OF_PROCESSES", "4"))
    number_of_async_tasks = int(os.getenv("NUMBER_OF_ASYNC_TASKS", "3"))
    logger.info("creating pool")
    async with Pool(
            processes=number_of_processes,
            childconcurrency=number_of_async_tasks,
            initializer=init_logger,
    ) as pool:
        asyncio.create_task(is_alive(pool))
        task_ids = [task_id for task_id in range(150)]
        await pool.map(my_mem_task, task_ids)
        pool.close()
        logger.info("processes pool closed")
        await pool.join()
        logger.info("all processes are done")
