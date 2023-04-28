
# Load Balancer

This is a simple load balancer implementation that distributes incoming requests to multiple backend servers using different balancing algorithms. It is written in Python and uses sockets for communication between the load balancer and backend servers.

## Features

- Round-robin load balancing algorithm
- Least connection load balancing algorithm
- Least processing time load balancing algorithm
- Random load balancing algorithm

## Requirements

- Python 3.6+
- Socket module
- Threading module
- Tkinter module
- matpotlib module
- time module

## Usage

1. Clone this repository
2. Start the load balancer by running `python load_balancer.py`
3. Configure your backend servers by editing the `servers` variable in `load_balancer.py`
4. Choose your balancing algorithm by setting the `method_choice` variable in `load_balancer.py`
5. Send requests to the load balancer by running `python client.py`

## Configuration

### Backend Servers

To configure the backend servers, edit the `servers` variable in `load_balancer.py`. The `servers` variable is a list of tuples where each tuple represents a server and its port number. For example, to add a server at IP address 192.168.1.100 on port 8000, add the following tuple to the `servers` list:

```
my_server = Server(port=8080, max_connections=5)
```

### Balancing Algorithms

To choose a balancing algorithm, set the `method_choice` variable in `load_balancer.py`. The available options are:

- `round_robin` - distributes requests in a round-robin fashion to all servers
- `least_connection` - distributes requests to the server with the least number of connections
- `least_time` - distributes requests to the server with the least processing time
- `random` - distributes requests randomly to all servers

## License

This project is licensed under the ESIB License .
