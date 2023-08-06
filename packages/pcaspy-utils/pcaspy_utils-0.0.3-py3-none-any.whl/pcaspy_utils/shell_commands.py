import os
import sys
import threading
import time


class IOCShellUtils:
    def __init__(self, prefix: str, pv_list: list):
        self.pvdb = self.create_pvs_database(prefix, pv_list)
        self.tid = threading.Thread(target=self.interactive_ioc_shell, args=())
        self.tid.start()

    @staticmethod
    def create_pvs_database(prefix, pv_list):
        """Create the full PVs name from prefix and suffix"""
        pvdb = [prefix + suffix for suffix in pv_list]
        pvdb.sort()
        return pvdb

    def list_database(self, user_input):
        """List all PVs that driver contains"""
        if ">" in user_input:
            file = user_input.replace(" ", "").replace(os.linesep, "").split(">")[-1]
            self.export_database_to_file(file)
        else:
            for pv in self.pvdb:
                print(pv)

    def export_database_to_file(self, file):
        """Export the output of dbl to a file"""
        with open(file, "w") as current_file:
            for pv in self.pvdb:
                line = pv + os.linesep
                current_file.write(line)

    def interactive_ioc_shell(self):
        """Shell to do some commands inisde a PCasPy IOC"""
        while True:
            user_input = str(sys.stdin.readline())
            if user_input.startswith("dbl"):
                self.list_database(user_input)
            time.sleep(0.25)


if __name__ == "__main__":
    obj = IOCShellUtils("foo:", ["bar", "foo"])
