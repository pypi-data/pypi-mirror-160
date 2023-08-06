class IOCShellUtils:

    def __init__(self, prefix: str, pv_list: list):
        self.pvdb = self.create_pvs_database(prefix, pv_list)
        self.tid = threading.Thread(target=self.interactive_ioc_shell,args=())
        self.tid.start()

    @staticmethod
    def create_pvs_database(prefix, pv_list):
        """Create the full PVs name from prefix and suffix"""
        pvdb = [prefix + suffix for suffix in pv_list]
        pvdb.sort()
        return pvdb

    def list_database(self):
        """List all PVs that driver contains"""
        for pv in self.pvdb:
            print(pv)

    def interactive_ioc_shell(self):
        """Shell to do some commands inisde a PCasPy IOC"""
        while True:
            if str(sys.stdin.readline()[:3]) == "dbl":
                self.list_database()
            time.sleep(0.25)
