from typing import Sequence
from abc import ABC, abstractmethod
import logging
import time
import os
import sys
from psutil import virtual_memory

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.join(os.getcwd(), 'logfile.log'),
                    filemode='w', format=LOG_FORMAT)
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
        logger.debug(f'prep')
        seconds_since_epoch = int(time.time())
        return True if seconds_since_epoch % 2 != 0 else False


    def run(self) -> Sequence:
        logger.debug(f'run')
        home_user_dir = os.path.expanduser("~")
        list_of_files = [file for file in os.listdir(home_user_dir) if
                         os.path.isfile(os.path.join(home_user_dir, file))]
        return list_of_files

    def clean_up(self):
        logger.debug(f'clean_up')
        sys.exit()

    def execute(self):
        logger.debug(f'execute')
        if self.prep():
            print(self.run())
        else:
            self.clean_up()


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
        logger.debug(f'prep')
        memory = virtual_memory()
        gigabytes = memory.total // 1024 ** 2
        return True if gigabytes < 1024 else False

    def run(self):
        logger.debug(f'run')
        with open('test', 'wb') as test_file:
            test_file.write(os.urandom(1024 ** 2))

    def clean_up(self):
        logger.debug(f'clean_up')
        path_to_test_file = os.path.join(os.getcwd(), 'test')
        if os.path.exists(path_to_test_file):
            os.remove(path_to_test_file)
        else:
            raise FileNotFoundError

    def execute(self):
        logger.debug(f'execute')
        if not self.prep():
            self.run()
            self.clean_up()


if __name__ == '__main__':
    # test_case_1 = TestCase1(name='test1', tc_id=1)
    # test_case_1.execute()
    test_case_2 = TestCase2(name='test2', tc_id=2)
    test_case_2.execute()
