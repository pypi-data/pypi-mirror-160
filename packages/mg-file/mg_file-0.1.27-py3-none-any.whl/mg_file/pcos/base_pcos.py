import typing
from asyncio import create_subprocess_shell, run, subprocess, gather
from subprocess import check_output, CalledProcessError, STDOUT
from threading import Lock, Thread

from logsmal import loglevel, logger
# poetry add tqdm
from tqdm import tqdm


class type_os_res(typing.NamedTuple):
    stdout: str
    stderr: str
    cod: str
    cmd: str

    def __str__(self, logger_info: logger, logger_error: logger, flag:str):
        # Если есть ошибка выполнения
        if self.stderr:
            logger_error(f"CMD:{self.cmd}\nTEXT:{self.stderr}\nCODE:{self.cod}", flag)
        else:
            logger_info(f"CMD:{self.cmd}\nTEXT:{self.stdout}", flag)


def os_exe_async(command_list: list[str]) -> list[type_os_res]:
    """
    Выполнить асинхронно команды OS

    :param command_list: Список команд
    :return:


    :Пример:

    .. code-bloc:: python

        pprint(os_exe_async(['ls', 'ls /home/']))
    """

    async def __self(_command: str):
        # Выполняем команду
        proc = await create_subprocess_shell(
            cmd=_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()
        # Обновляем текст в плейсхолжере
        pbar.set_description(f"{_command}")
        pbar.update()

        return type_os_res(
            stdout=stdout.decode(),
            stderr=stderr.decode(),
            cod=proc.returncode,
            cmd=_command,
        )

    async def __loop():
        task = [__self(_cmd) for _cmd in command_list]
        return await gather(*task)

    with tqdm(total=len(command_list)) as pbar:
        return run(__loop())


def os_exe_thread(
        label_command: str,
        command_list: list[str],
        call_log_info: loglevel = lambda _x, flag: ...,
        call_log_error: loglevel = lambda _x, flag: ...,
):
    """
    Выполнить команды системы в нескольких потоках.


    :param label_command: Общее название команд
    :param command_list: Список команд
    :param call_log_info: Функция для логов информации
    :param call_log_error: Функция для логов ошибок

    :Пример вызова:

    ..code-bloc:: python

        indir = os.path.dirname(__file__)
        command_list: list[str] = []
        command = "pull"

        for _path in listdir():
            command_list.append(f"cd {path.join(indir, _path)} && git {command}")

        os_exe_thread(
            "GIT PULL",
            command_list,
            call_log_info=logger.info,
            call_log_error=logger.error
        )
    """

    lock = Lock()

    def self_(_command: str):
        """

        :param _command:
        """

        try:
            res = check_output(_command, shell=True, stderr=STDOUT)
            with lock:
                call_log_info(f"{_command}:{res.decode('utf-8')}", flag=label_command)
        except CalledProcessError as e:
            with lock:
                call_log_error(f"{_command}:{e.output.decode('utf-8')}", flag=str(e.returncode))
        finally:
            with lock:
                pbar.set_description(f"{_command}")
                pbar.update()

    list_thread: list[Thread] = []
    with tqdm(total=len(command_list)) as pbar:
        for _command in command_list:
            th = Thread(
                target=self_, args=(_command,),
                name=f"th_{_command}", daemon=True,
            )
            list_thread.append(th)
            th.start()

        for th in list_thread:
            th.join()
