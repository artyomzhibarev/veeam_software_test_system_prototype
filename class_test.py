from typing import Sequence
from abc import ABC, abstractmethod
import logging
import time
import os
from psutil import virtual_memory

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.join(os.getcwd(), 'logfile.log'),
                    filemode='a', format=LOG_FORMAT)
logger = logging.getLogger()


class Test(ABC):

    @abstractmethod
    def prep(self):
        """Метод для выполнения теста"""
        ...

    @abstractmethod
    def run(self):
        """ Метод для подготовки теста"""
        ...

    @abstractmethod
    def clean_up(self):
        """Метод для завершения (clean_up) тестов"""
        ...

    @abstractmethod
    def execute(self):
        """
        Метод execute, который задаёт общий порядок выполнения тест-кейса
        и обрабатывает исключительные ситуации.
        :return:
        """
        ...


class TestCase1(Test):
    """
    [prep] Если текущее системное время, заданное как целое количество секунд от начала эпохи Unix,
    не кратно двум, то необходимо прервать выполнение тест-кейса.
    [run] Вывести список файлов из домашней директории текущего
    пользователя.
    [clean_up] Действий не требуется.
    """

    def __init__(self, tc_id: int, name: str):
        self.tc_id = tc_id
        self.name = name

    def prep(self) -> bool:
        seconds_since_epoch = int(time.time())
        return False if seconds_since_epoch % 2 != 0 else True

    def run(self) -> Sequence:
        home_user_dir = os.path.expanduser("~")
        list_of_files = [file for file in os.listdir(home_user_dir) if
                         os.path.isfile(os.path.join(home_user_dir, file))]
        return list_of_files

    def clean_up(self):
        ...

    def execute(self):
        if self.prep():
            logger.info(f'The test {self.tc_id}, {self.name} will run')
            print(self.run())
            logger.info(f'The list of files from home directory was printed to the console')
            logger.info(f'Test id {self.tc_id}, {self.name} completed successfully!')
            self.clean_up()
        else:
            self.clean_up()
            logger.error(f'Test id {self.tc_id}, {self.name} execution terminated')


class TestCase2(Test):
    """
    [prep] Если объем оперативной памяти машины, на которой исполняется тест, меньше одного гигабайта,
    то необходимо прервать выполнение тест-кейса.
    [run] Создать файл test размером 1024 КБ со случайным содержимым.
    [clean_up] Удалить файл test.

    """

    def __init__(self, tc_id: int, name: str):
        self.tc_id = tc_id
        self.name = name

    def prep(self) -> bool:
        memory = virtual_memory()
        return False if memory.total // 1024 ** 2 < 1024 else True

    def run(self):
        with open('test', 'wb') as test_file:
            test_file.write(os.urandom(1024 ** 2))

    def clean_up(self):
        path_to_test_file = os.path.join(os.getcwd(), 'test')
        if os.path.exists(path_to_test_file):
            os.remove(path_to_test_file)
        else:
            raise FileNotFoundError

    def execute(self):
        if self.prep():
            logger.info(f'The test id {self.tc_id}, {self.name} will run')
            self.run()
            logger.info(f'File <test> with random content created')
            self.clean_up()
            logger.info(f'Test id {self.tc_id}, {self.name} completed successfully!')
        else:
            logger.error(
                f'Test id {self.tc_id}, {self.name} execution terminated {virtual_memory().total / 1024 ** 3} GB < 1 GB')


if __name__ == '__main__':
    test_case_1 = TestCase1(name='test1', tc_id=1)
    test_case_1.execute()
    test_case_2 = TestCase2(name='test2', tc_id=2)
    test_case_2.execute()
