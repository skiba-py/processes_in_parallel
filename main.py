from mp_queue import ProcessController, example_function


if __name__ == '__main__':
    controller = ProcessController()

    # Ограничение на максимальное число одновременно выполняемых процессов
    controller.set_max_proc(2)

    # Список заданий
    tasks = [
        (example_function, (3, 'Task 1')),
        (example_function, (4, 'Task 2')),
        (example_function, (5, 'Task 3')),
        (example_function, (6, 'Task 4')),
        (example_function, (7, 'Task 5')),
    ]

    # Второй список заданий
    second_tasks = [
        (example_function, (1, 'Task 6')),
        (example_function, (2, 'Task 7')),
        (example_function, (3, 'Task 8')),
        (example_function, (4, 'Task 9')),
    ]

    # Максимальное время выполнения 5 секунд
    controller.start(tasks, max_exec_time=5)

    print(f'Осталось задач: {controller.wait_count()}')
    print(f'Запущенные задачи: {controller.alive_count()}')

    print('Запускается второй вызов')

    # Максимальное время выполнения 5 секунд
    controller.start(second_tasks, max_exec_time=3)

    print(f'Осталось задач: {controller.wait_count()}')
    print(f'Запущенные задачи: {controller.alive_count()}')

    # Ожидание завершения всех задач
    controller.wait()

    print(f'Осталось задач: {controller.wait_count()}')
    print(f'Запущенные задачи: {controller.alive_count()}')
