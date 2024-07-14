import multiprocessing
import time

# TODO: прописать README.md
# TODO: залить на гитхаб


class ProcessController:
    def __init__(self):
        """Инициализация атрибутов."""
        self.max_procs = 1  # кол-во запущенных одновременно процессов
        self.running_processes = []
        self.queue = multiprocessing.Queue()
        self.count_of_tasks = 0  # атрибут для подсчета количества задач

    def set_max_proc(self, n: int) -> None:
        """Устанавливает ограничение: максимальное число
        одновременно выполняемых заданий не должно превышать n.
        """
        self.max_procs = n

    def start(self, tasks: list, max_exec_time: int) -> None:
        """Помещает в очередь все задания из tasks
        и запускает их параллельно.
        """
        for task in tasks:
            self.queue.put(task)
            self.count_of_tasks += 1

        while not self.queue.empty() or self.running_processes:
            for p, start_time in self.running_processes.copy():
                if not p.is_alive():
                    self.running_processes.remove((p, start_time))
                elif time.time() - start_time > max_exec_time:
                    p.terminate()
                    print(f'Процесс {p} завершился из-за ограничения.')
                    self.running_processes.remove((p, start_time))

            # Запуск новых процессов, если есть доступные слоты
            while (len(self.running_processes) < self.max_procs
                   and not self.queue.empty()):
                func, args = self.queue.get()
                self.count_of_tasks -= 1
                p = multiprocessing.Process(target=func, args=args)
                p.start()
                self.running_processes.append((p, time.time()))

            time.sleep(0.1)

    def wait(self) -> None:
        """Ждет завершения выполнения всех заданий из очереди."""
        for p in self.running_processes:
            p.join()

        print('Все процессы завершили работу.')

    def wait_count(self) -> int:
        """Возвращает число заданий, которые осталось запустить."""
        return self.count_of_tasks

    def alive_count(self) -> int:
        """Возвращает число выполняемых в данный момент заданий."""
        return len(self.running_processes)
