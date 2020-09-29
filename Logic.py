import Simulation as Sim
import matplotlib.pyplot as plt
import math


def sim_var(influx, time, server_state):
    """Function to calculate simulation"""
    global s
    s = Sim.SimulationM(influx, time, server_state)
    s.start()
    global time_sim
    time_sim = time
    global influx_sim
    influx_sim = influx
    global server_state_sim
    server_state_sim = server_state


def show_diagram(server_state):
    """Function to show step-diagram with birth and death process"""
    time_s = []
    state_s = [0]  # because of plt.step we need to set first value
    customers_s = [0]
    for i in range(0, len(s.queue)):
        # print(s.queue[i])
        time_s.append(s.queue[i]["time"])
        state_s.append(s.queue[i]["server_state"])
        customers_s.append(s.queue[i]["count"])
    for i in range(0, len(s.queue)):
        if state_s[i]:
            state_s[i] = max(customers_s) / 2
    state_s.pop()
    customers_s.pop()

    plt.title("Wykres zdarzeń w systemie M/M/1")
    plt.xlabel("Czas [s]")
    plt.ylabel("Liczba klientów")
    plt.step(time_s, customers_s, label="Napływ: "+str(influx_sim)+" [1/s]")
    if server_state:
        plt.step(time_s, state_s, linewidth=3, color='red', label="Stan serwera")
    plt.legend()
    plt.show()


def avg_customers_in_system():
    customers_in_queue = 0

    # for i in range(math.floor(len(s.queue)/10), len(s.queue) - 1):
    #     customers_in_queue += (s.queue[i]["count"] * (s.queue[i + 1]["time"] - s.queue[i]["time"])) / (time_sim - s.queue[math.floor(len(s.queue)/10)]["time"])

    for i in range(0, len(s.queue) - 1):
        customers_in_queue += (s.queue[i]["count"] * (s.queue[i + 1]["time"] - s.queue[i]["time"])) /time_sim
    return customers_in_queue


def avg_time_in_system():
    avg_time = 0.0
    avg_index = 0
    for i in range(math.floor(len(s.average_time_in_system)/10), len(s.average_time_in_system), 1):
        if s.average_time_in_system[i]["use"]:
            avg_time += s.average_time_in_system[i]["time_end"] - s.average_time_in_system[i][
                "time_start"]
            avg_index += 1
    avg_time = avg_time / avg_index
    return avg_time


def avg_wait_in_system():
    avg_time = 0.0
    avg_index = 0
    for i in range(0, len(s.average_wait), 1):
        if s.average_wait[i]["time_start"] > time_sim/10:
            if s.average_wait[i]["use"]:
                avg_time += s.average_wait[i]["time_end"] - s.average_wait[i][
                    "time_start"]
                avg_index += 1
    for i in range(0, len(s.average_wait2), 1):
        if s.average_wait2[i]["time_start"] > time_sim / 10:
            avg_index += 1
    avg_time = avg_time / avg_index
    return avg_time


def avg_buffer():
    buffer_state = 0
    for i in range(math.floor(len(s.queue) / 10), len(s.queue) - 1):
        if s.queue[i]["count"] == 0:
            buffer = 0
        else:
            buffer = s.queue[i]["count"]-1
        buffer_state += (buffer * (s.queue[i + 1]["time"] - s.queue[i]["time"])) / (time_sim - s.queue[math.floor(len(s.queue)/10)]["time"])
    return buffer_state


def estimated_buffer():
    return estimated_wait()*influx_sim


def estimated_wait():
    return estimated_time_in_system()-0.125


def estimated_customers_in_system():
    return estimated_time_in_system()*influx_sim


def estimated_time_in_system():
    if server_state_sim:
        p_on = s.server_on_time / (s.server_on_time + s.server_off_time)
        p_off = 1 - p_on
        p_prim = influx_sim / (8 * p_on)
        e_t = (p_prim + influx_sim * s.server_off_time * p_off) / ((1 - p_prim) * influx_sim)
        return e_t
    else:
        return 1 / (8 - influx_sim)


def confidence_interval(values):
    values_mean = sum(values)/len(values)
    deviation = []
    dev = 0
    for i in range(0, len(values)):
        deviation.append((values_mean-values[i])**2)
    dev = math.sqrt(sum(deviation)/len(deviation))
    conf_up = values_mean + dev*1.96/math.sqrt(50)
    conf_down = values_mean - dev * 1.96 / math.sqrt(50)
    nr_rep = 0
    # for i in range(0, len(values)):
    #     if conf_down < values[i] < conf_up:
    #         nr_rep += 1
    # print("testy na pass: " + str(nr_rep) + "   srednia: " + str(values_mean) + "   min: " + str(min(values)) + "   max: " + str(max(values)))
    print("Przedział od " + str(round(conf_down, 4)) + " do " + str(round(conf_up, 4)) + "    srednia: " + str(round(values_mean, 4)))


def save_simulation(server_state):

    nr_of_simulations = 5
    time_of_each_simulation = 1000
    s1_avg_l = []
    s1_avg_time = []
    s1_avg_time_2 = []
    s1_avg_axis = []
    s1_avg_box_chart = []
    s1_avg_2 = []

    s1_avg_wait = []
    s1_est_wait = []

    s1_avg_buff = []
    s1_est_buff = []

    if server_state:
        sim_end = 17
        server_state_sim = True
    else:
        sim_end = 25
        server_state_sim = False
    for lambda_sim in range(2, sim_end, 1):
        s1_avg = []
        s1_avg_t = []
        s1_avg_w = []
        s1_avg_b = []
        for i in range(0, nr_of_simulations):
            sim_var(lambda_sim/4, time_of_each_simulation, server_state_sim)
            s1_avg.append(avg_customers_in_system())
            s1_avg_t.append(avg_time_in_system())
            s1_avg_w.append(avg_wait_in_system())
            s1_avg_b.append(avg_buffer())

        print(lambda_sim/4)
        print("Customers")
        confidence_interval(s1_avg)
        print(round(estimated_customers_in_system(), 4))
        print("time")
        confidence_interval(s1_avg_t)
        print(round(estimated_time_in_system(), 4))
        print("wait")
        confidence_interval(s1_avg_w)
        print(round(estimated_wait(), 4))
        print("buffer")
        confidence_interval(s1_avg_b)
        print(round(estimated_buffer(), 4))

        s1_avg_buff.append(sum(s1_avg_b) / len(s1_avg_b))
        s1_est_buff.append(estimated_buffer())

        s1_avg_wait.append(sum(s1_avg_w) / len(s1_avg_w))
        s1_est_wait.append(estimated_wait())

        s1_avg_axis.append(lambda_sim / 4)
        s1_avg_box_chart.append(s1_avg)
        s1_avg_l.append(sum(s1_avg)/len(s1_avg))
        s1_avg_time.append(sum(s1_avg_t) / len(s1_avg_t))
        s1_avg_2.append(estimated_customers_in_system())
        s1_avg_time_2.append(estimated_time_in_system())

    plot1 = plt.figure(1)
    plt.rc('axes', axisbelow=True)
    plt.grid()
    plt.plot(s1_avg_axis, s1_avg_l, zorder=33, linewidth=1.5, label="Wynik symulacji", marker="*", linestyle='--')
    plt.plot(s1_avg_axis, s1_avg_2, zorder=2, linewidth=4.5, color="#5beb89", label="Wynik uzyskany z modelu analitycznego")
    if server_state:
        plt.title("System M/M/1 z wyłączeniami")
    else:
        plt.title("System M/M/1 bez wyłączeń")
    plt.title("System M/M/1 bez wyłączeń")
    plt.xlabel("Średnia intensywność napływu [1/s]")
    plt.ylabel("Średnia liczba klientów w systemie")
    plt.legend()
    plot1.show()

    plot2 = plt.figure(2)
    plt.boxplot(s1_avg_box_chart, positions=s1_avg_axis, widths=0.2)
    if server_state:
        plt.title("System M/M/1 z wyłączeniami")
    else:
        plt.title("System M/M/1 bez wyłączeń")
    plt.xlabel("Średnia intensywność napływu [1/s]")
    plt.ylabel("Średnia liczba klientów w systemie")
    plot2.show()

    plot3 = plt.figure(3)
    plt.grid()
    plt.plot(s1_avg_axis, s1_avg_time, zorder=2, linewidth=1.5, label="Wynik symulacji", marker="d", linestyle='--', color="#e36424")
    plt.plot(s1_avg_axis, s1_avg_time_2, zorder=1, linewidth=4.5, color="#5beb89", label="Wynik uzyskany z modelu analitycznego")
    if server_state:
        plt.title("System M/M/1 z wyłączeniami")
    else:
        plt.title("System M/M/1 bez wyłączeń")
    plt.xlabel("Średnia intensywność napływu [1/s]")
    plt.ylabel("Średni czas przejścia przez system [s]")
    plt.legend()
    plot3.show()

    plot4 = plt.figure(4)
    plt.grid()
    plt.plot(s1_avg_axis, s1_avg_wait, zorder=2, linewidth=1.5, label="Wynik symulacji", marker="P", linestyle='--', color="#95229c")
    plt.plot(s1_avg_axis, s1_est_wait, zorder=1, linewidth=4.5, color="#5beb89", label="Wynik uzyskany z modelu analitycznego")
    if server_state:
        plt.title("System M/M/1 z wyłączeniami")
    else:
        plt.title("System M/M/1 bez wyłączeń")
    plt.xlabel("Średnia intensywność napływu [1/s]")
    plt.ylabel("Średni czas oczekiwania [s]")
    plt.legend()
    plot4.show()

    plot5 = plt.figure(5)
    plt.grid()
    plt.plot(s1_avg_axis, s1_avg_buff, zorder=2, linewidth=1.5, label="Wynik symulacji", marker="h",
             linestyle='--', color="#db2e54")
    plt.plot(s1_avg_axis, s1_est_buff, zorder=1, linewidth=4.5, color="#5beb89", label="Wynik uzyskany z modelu analitycznego")
    if server_state:
        plt.title("System M/M/1 z wyłączeniami")
    else:
        plt.title("System M/M/1 bez wyłączeń")
    plt.xlabel("Średnia intensywność napływu [1/s]")
    plt.ylabel("Średni stan bufora")
    plt.legend()
    plot5.show()
