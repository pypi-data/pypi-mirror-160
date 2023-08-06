"""多进程处理任务"""
import time
from multiprocessing import Manager, Process
from typing import List

from tqdm import tqdm


def multi_tasks(func, data_list: List, pbar_name: str = "waiting", workers: int = 10, refresh_time: float = 0.1) -> None:
    """_summary_

    Args:
        func (_type_): 处理函数
        data_list (List): 需要处理的数据列表
        pbar_name (str, optional): 进度条显示名称. Defaults to "waiting".
        workers (int, optional): 进程数量. Defaults to 10.
        refresh_time (float, optional): 进度条更新时间(秒). Defaults to 0.1.
    """
    results = Manager().list()
    process_list: List[Process] = []

    step = len(data_list) // workers + 1
    all_idx = list(range(len(data_list)))
    for i in range(0, len(data_list), step):
        part_idxs = all_idx[i : i + step]
        process_list.append(Process(target=_batch_func, args=(func, data_list, part_idxs, results)))
    process_list.append(Process(target=_show_processon, args=(len(data_list), pbar_name, refresh_time, results)))
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()

    real_results = [None] * len(data_list)
    for i, result in results:
        real_results[i] = result
    return real_results


def _show_processon(nums: int, pbar_name: str, refresh_time: float, results):
    """显示进度条"""
    cnt = 0
    step = 0
    pbar = tqdm(range(nums), desc=pbar_name)
    while cnt < nums:
        cnt = len(results)
        pbar.update(cnt - step)
        step = cnt
        time.sleep(refresh_time)


def _batch_func(func, data_list: List, part_idxs: List[int], results):
    n = func.__code__.co_argcount
    for idx in part_idxs:
        data = data_list[idx]
        if n == 1:
            result = func(data)
        else:
            result = func(*data)
        results.append([idx, result])


def test_tasks():
    """测试"""
    multi_tasks(lambda x: print(x), [1, 2, 3, 4, 5], pbar_name="print")
