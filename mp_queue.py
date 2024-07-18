import multiprocessing
import threading
import queue
import time


class ProcessController:
    def __init__(self):
        """Инициализация атрибутов."""
        self.max_procs = 1  # кол-во запущенных одновременно процессов
        self.running_processes = {}
        self.queue = queue.Queue()
        self.count_of_tasks = 0  # атрибут для подсчета количества задач
        runner = threading.Thread(target=self._run_processes)
        runner.start()

    def set_max_proc(self, n: int) -> None:
        """Устанавливает ограничение: максимальное число
        одновременно выполняемых заданий не должно превышать n.
        """
        self.max_procs = n

    def start(self, tasks: list, max_exec_time: int) -> None:
        """Помещает в очередь все задания из tasks."""
        for task in tasks:
            self.queue.put((task, max_exec_time))
            self.count_of_tasks += 1

    def _run_processes(self):
        """Запускает задания из очереди."""
        while True:
            proc_to_remove = []
            for p, end_time in self.running_processes.items():
                if not p.is_alive():
                    proc_to_remove.append(p)
                elif end_time <= time.time():
                    p.terminate()
                    print(f'Процесс {p} завершился из-за ограничения.')
                    proc_to_remove.append(p)

            for p in proc_to_remove:
                self.running_processes.pop(p)
                self.queue.task_done()

            # Запуск новых процессов, если есть доступные слоты
            while (len(self.running_processes) < self.max_procs
                   and not self.queue.empty()):
                (func, args), max_exec_time = self.queue.get()
                self.count_of_tasks -= 1
                p = multiprocessing.Process(target=func, args=args)
                p.start()
                self.running_processes[p] = time.time() + max_exec_time

            time.sleep(0.1)

    def wait(self) -> None:
        """Ждет завершения выполнения всех заданий из очереди."""
        self.queue.join()

        print('Все процессы завершили работу.')

    def wait_count(self) -> int:
        """Возвращает число заданий, которые осталось запустить."""
        return self.count_of_tasks

    def alive_count(self) -> int:
        """Возвращает число выполняемых в данный момент заданий."""
        return len(self.running_processes)


def example_function(duration: int, message: str) -> None:
    """Пример фунции."""
    start_time = time.time()
    print(f'Запуск задачи - {message}.')
    time.sleep(duration)
    ex_time = time.time() - start_time
    print(f'Задача {message} завершила работу за {ex_time:.0f} секунды.')
