import subprocess
import threading
from typing import List

class ZipController:
    def compress(self, file_list: List[str], output: str, threads: int, level: int = 5):
        call = ["7za", "a", "-r", "-t7z", "-m0=lzma2", f"-mx={level}", f"-mmt={threads}", output]

        for file in file_list:
            call.append(file)

        self.start_thread(call)

    def do_subprocess(self, call):
        subprocess.check_call(call)

    def start_thread(self, call):
        t = threading.Thread(target=self.do_subprocess, kwargs={'call': call})
        t.start()
