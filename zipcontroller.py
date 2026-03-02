import re
import subprocess
import threading
from typing import Callable, List, Optional

class ZipController:
    def compress(self, file_list: List[str], output: str, threads: int, level: int = 5,
                 progress_callback: Optional[Callable[[float], None]] = None):
        call = ["7za", "a", "-r", "-t7z", "-m0=lzma2", f"-mx={level}", f"-mmt={threads}", output]

        for file in file_list:
            call.append(file)

        self.start_thread(call, progress_callback)

    def do_subprocess(self, call, progress_callback=None):
        process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        buf = b''
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            for byte in chunk:
                c = bytes([byte])
                if c in (b'\r', b'\n'):
                    if progress_callback and buf:
                        match = re.search(rb'(\d+)%', buf)
                        if match:
                            progress_callback(int(match.group(1)) / 100.0)
                    buf = b''
                else:
                    buf += c
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, call)

    def start_thread(self, call, progress_callback=None):
        t = threading.Thread(target=self.do_subprocess, kwargs={'call': call, 'progress_callback': progress_callback})
        t.start()
