from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import threading
from multiprocessing import Process

DEFAULT_MAX_WORKERS = 5


def run_thread(target, args=()) -> None:
    t = threading.Thread(target, args=args)
    t.start()


def run_process(target, args=()) -> None:
    p = Process(target=target, args=args)
    p.start()


def execute_threads(runnable, tasks: list, max_workers: int = DEFAULT_MAX_WORKERS) -> list:
    thread_pool = ThreadPoolExecutor(max_workers=max_workers)
    futures = []
    for t in tasks:
        futures.append(thread_pool.submit(runnable, t))

    result = join_futures(futures)
    thread_pool.shutdown()
    return result


def execute_process(runnable, tasks: list, max_workers: int = DEFAULT_MAX_WORKERS) -> list:
    process_pool = ProcessPoolExecutor(max_workers=max_workers)
    futures = []
    for t in tasks:
        futures.append(process_pool.submit(runnable, t))

    result = join_futures(futures)
    process_pool.shutdown()
    return result


def join_futures(futures: list):
    result = []
    for f in futures:
        result.append(f.result())
    return result
