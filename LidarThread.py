import threading, queue
from lidar_lite import Lidar_Lite as lidar


class LidarThread(threading.Thread):
    def __init__(self, high_value_q: queue.Queue, name=None):
        super(LidarThread, self).__init__(name=name)
        self.stop_request = threading.Event()
        self.high_value_q = high_value_q
        self.lidar = lidar()
        connect = self.lidar.connect(1)
        if connect < -1:
            raise Exception("No LiDAR found")
        self.lidar.setThreshold(100)
        self.current_value = None

    def run(self):
        while not self.stop_request.isSet():
            value = self.lidar.getDistance()
            if value < self.lidar.thresh:
                self.high_value_q.put(value)
            if self.current_value is None:
                self.current_value = value

    def get_current(self):
        value = self.current_value
        self.current_value = None
        return value

    def join(self,timeout=None):
        self.stop_request.set()
        super(LidarThread, self).join(timeout)