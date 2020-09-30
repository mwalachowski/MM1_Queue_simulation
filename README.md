# M/M/1 queue simulation

### How to use simulator

There is simple GUI where you can set desirable influx of clients, duration of the simulation and choose if you want simulation with or without exclusions. "Simulation" button runs simulation with provided parameters. "Diagram" button shows number of clients in queue in time. "Statistics" button shows several statistics collected during last simulation compared with values calculated from theoretical equations.

![Image](GUI.png)

### Short description of methods used in simulation.

* gen_time() - a method responsible for generating time between successive events depending on the type of event.
* check_time() - a method that returns the corresponding index in the event table according to the specified time of occurrence.
* put() - method of adding an event to the list. It uses the check_time() method to put the event in the right place
* get() - a method that retrieves an event with the least time of occurrence among events not yet downloaded.
* event_action() - a method that, depending on the current event, changes the parameters of the simulation and using the put() method to add the appropriate events to the list. In case of a client's arrival event, it generates the next client's arrival event and checks if the simulation conditions (if the server can handle the next client) allow adding the client's output event. In the case of the client output event, it checks if the server is active, if not, it adds the output event after the server's switch on event. It also checks if there is another client to handle and, depending on that, adds or not the handle event. In case of a server switch off event, the server generates switching on event. 
* start() - a method that adds the simulation start and end events, and then executes the event_action() method with the get() parameter until it encounters the end event.
