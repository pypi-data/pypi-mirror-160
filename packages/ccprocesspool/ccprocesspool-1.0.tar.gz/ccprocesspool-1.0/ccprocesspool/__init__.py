from multiprocessing import Process


class CCProcessPool(object):

    def __init__(self, name: str, loop_duration: float = 3, max_running_time: float = 3600):
        self.name: str = name
        self.__loop_duration = loop_duration
        self.__max_running_time = max_running_time
        self.__process_list = list()
        print('Process pool named "' + name + '" inited: ' + str(self))

    def __del__(self):
        self.stop_all()

    def add_job(self, target, args):
        if args is None:
            args = ()
        elif not isinstance(args, tuple):
            args = (args, )
        process = Process(target=target, args=args)
        process.start()
        self.__process_list.append(process)
        return

    def living_process_count(self):
        return len(self.__process_list)

    def check_job(self):
        process_list = self.__process_list
        for i in range(len(process_list) - 1, -1, -1):
            process = process_list[i]
            if not process.is_alive():
                print('Process pool ' + self.name + ' ended process: ' + str(process))
                del process_list[i]
        print('living process count', self.living_process_count())

    def stop_all(self):
        print('stop all for process pool', self.name)
        process_list = self.__process_list
        for i in range(len(process_list) - 1, -1, -1):
            process = process_list[i]
            if process.is_alive():
                process.terminate()
                process.join()
            del process_list[i]
