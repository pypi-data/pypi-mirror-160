from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import threading

DEFAULT_MAX_WORKERS = 5


def run_thread(target, args=()) -> None:
    t = threading.Thread(target=target, args=args)
    t.start()


def execute_tasks_in_thread_pool(runnable, tasks: list, max_workers: int = DEFAULT_MAX_WORKERS) -> list:
    thread_pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='flyers_default')
    futures = []
    for t in tasks:
        futures.append(thread_pool.submit(runnable, t))

    result = join_futures(futures)
    thread_pool.shutdown()
    return result


def execute_tasks_in_process_pool(runnable, tasks: list, max_workers: int = DEFAULT_MAX_WORKERS) -> list:
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
