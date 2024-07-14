import time

import mp_queue


def example_function(duration: int, message: str) -> None:
    """Пример фунции."""
    start_time = time.time()
    print(f'Запуск задачи - {message}.')
    time.sleep(duration)
    ex_time = time.time() - start_time
    print(f'Задача {message} завершила работу за {ex_time:.0f}.')


if __name__ == '__main__':
    controller = mp_queue.ProcessController()

    # Ограничение на максимальное число одновременно выполняемых процессов
    controller.set_max_proc(2)

    # Список заданий
    tasks = [
        (example_function, (2, 'Task 1')),
        (example_function, (3, 'Task 2')),
        (example_function, (4, 'Task 3')),
        (example_function, (5, 'Task 4')),
        (example_function, (6, 'Task 5')),
        (example_function, (7, 'Task 6')),
        (example_function, (8, 'Task 7')),
    ]

    # Максимальное время выполнения 5 секунд
    controller.start(tasks, max_exec_time=5)

    # Ожидание завершения всех задач
    controller.wait()

    print(f'Осталось задач: {controller.wait_count()}')
    print(f'Запущенные задачи: {controller.alive_count()}')
