from threading import Thread


class OnStopThread(object):
    """
    Creates a decorator to run something in new thread
    """

    def __init__(self, st, nd, stop):
        """
        :param firST: callback to run current thread function
        :param secoND: callback to run in other thread
        :param stop: callback function for thread
        """
        self.st = st
        self.nd = nd
        self.stop = stop

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def run(self, *args, **kwds):
        thread = self._start_nd_in_thread(*args, **kwds)
        thread.start()
        try:
            self.st(*args, **kwds)
        except:
            pass
        try:
            self.stop(*args, **kwds)
        finally:
            thread.join(1)

    def _start_nd_in_thread(self, *args, **kwds):
        def in_thread(*args, **kwds):
            self.nd(*args, **kwds)
            self.stop(*args, **kwds)
        return Thread(target=in_thread, args=args, kwargs=kwds)
