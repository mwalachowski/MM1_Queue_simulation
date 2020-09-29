import math
import random


class SimulationM:

    def __init__(self, influx, time_end, server_type):
        self.queue = []  # dynamic list of events
        self.timer = 0  # timer of actual event
        self.index = 0
        self.influx = influx
        self.time_end = time_end
        self.counter = 0
        self.customer_service_time = 0.125
        self.server_type = server_type  # False - server without exlusions, True - server with exlusions
        self.server_state = True  # server ON
        self.server_off_time = 35
        self.server_on_time = 40
        self.specific_time = 0

        self.avg_index = 0
        self.avg_index2 = 0
        self.average_time_in_system = []

        self.average_wait = []
        self.average_wait2 = []
        self.wait_index = 0
        self.wait_index2 = 0

    def start(self):

        self.queue.append({"type": "START",
                           "time": 0,
                           "used": False,
                           "count": 0,
                           "server_state": self.server_state
                           })
        self.queue.append({"type": "END",
                           "time": self.time_end,
                           "used": False,
                           "count": 0,
                           "server_state": self.server_state
                           })

        j = 0
        while self.queue[j]["type"] != "END":
            self.event_action(self.get(), j)
            # self.queue[j]["count"] = self.counter
            # self.queue[j]["server_state"] = self.server_state
            j += 1

    def event_action(self, event_type, j):

        if True:
            if event_type == "START":
                self.put("Customer come", self.timer + self.gen_time("Customer come"))
                if self.server_type:
                    self.put("Server OFF", self.timer + self.gen_time("Server ON"))

            elif event_type == "Customer come":

                # do zbierania danych zwiazanych ze srednim czasem obslugi
                self.average_time_in_system.append({"index": self.avg_index,
                                                    "time_start": self.timer,
                                                    "time_end": 0,
                                                    "use": False})  # set time to calculate average time in system
                self.avg_index += 1

                # do zbierania danych zwiazanych ze srednim czasem oczekiwania
                if self.counter == 0:
                    self.average_wait2.append({"time_start": self.timer,
                                              "time_end": 0,
                                               "use": True})
                if self.counter > 0:
                    self.average_wait.append({"index": self.wait_index,
                                              "time_start": self.timer,
                                              "time_end": 0,
                                              "use": False})
                    self.wait_index += 1

                self.counter += 1
                self.put("Customer come", self.timer + self.gen_time(event_type))
                if self.counter == 1:
                    self.put("Customer leave", self.timer + self.gen_time("Customer leave"))

            elif event_type == "Customer leave":
                if self.server_state:

                    self.average_time_in_system[self.avg_index2]["time_end"] = self.timer
                    self.average_time_in_system[self.avg_index2]["use"] = True
                    self.avg_index2 += 1

                    if self.counter > 1:
                        self.average_wait[self.wait_index2]["time_end"] = self.timer
                        self.average_wait[self.wait_index2]["use"] = True
                        self.wait_index2 += 1

                    self.counter -= 1

                    if self.counter > 0:
                        self.put("Customer leave", self.timer + self.gen_time(event_type))
                else:
                    self.put("Customer leave", self.timer + self.specific_time)

            elif event_type == "Server OFF":
                self.specific_time = self.gen_time(event_type)
                self.server_state = False
                self.put("Server ON", self.timer + self.specific_time)

            elif event_type == "Server ON":
                self.server_state = True
                self.put("Server OFF", self.timer + self.gen_time(event_type))

        self.queue[j]["count"] = self.counter
        self.queue[j]["server_state"] = self.server_state
        self.index = j

    def gen_time(self, event_type):
        """Function calculate time before next event"""
        if event_type == "Customer come":
            return -math.log(1 - random.uniform(0, 1)) / self.influx
        elif event_type == "Customer leave":
            return -math.log(1 - random.uniform(0, 1)) * self.customer_service_time
        elif event_type == "Server OFF":
            return -math.log(1 - random.uniform(0, 1)) * self.server_off_time
        elif event_type == "Server ON":
            return -math.log(1 - random.uniform(0, 1)) * self.server_on_time

    def check_time(self, time):
        """Checking time of actual event to return proper index"""
        i = self.index
        while self.queue[i]["type"] != "END":
            if self.queue[i]["time"] < time < self.queue[i + 1]["time"]:
                return i + 1
            i += 1

    def put(self, event_type, time):
        """Putting event in exact place in dynamic list"""
        if time < self.time_end:
            self.queue.insert(self.check_time(time), {"type": event_type,
                                                      "time": time,
                                                      "used": False,
                                                      "count": 0,
                                                      "server_state": True
                                                      })

    def get(self):
        """Function that return first event that haven't been used"""
        for i in range(self.index, len(self.queue)):
            if self.queue[i]["used"] is False:
                self.queue[i]["used"] = True
                # self.index = i
                self.timer = self.queue[i]["time"]
                return self.queue[i]["type"]
            i += 1
