import socket
import threading
import time
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font



class LoadyB:
    def __init__(self, servers):
        self.servers = servers
        self.num_servers = len(servers)
        self.last_server_used = -1
        self.server_request_count = [0] * self.num_servers

        self.root = tk.Tk()
        self.root.title("LoadyB")

        self.round = font.Font(family='Montserrat', size=24, weight='bold')

        self.label = tk.Label(self.root, text="LoadyB", font=self.round)
        self.label.config(fg="#D3D3D3", font=("Brush Script MT", 30, "italic"))
        self.label.pack()

        self.fig = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.bar_width = 0.35
        self.index = [1, 2, 3]

        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.request_count_entry = tk.Entry(self.root)
        self.request_count_entry.pack()

        self.method_choice = tk.StringVar(value="round_robin")

        self.method_radio_frame = tk.Frame(self.root)
        self.method_radio_frame.pack()

        self.round_robin_radio = tk.Radiobutton(self.method_radio_frame, text="Round Robin",
                                                variable=self.method_choice, value="round_robin")
        self.round_robin_radio.pack(side=tk.LEFT)

        self.least_connection_radio = tk.Radiobutton(self.method_radio_frame, text="Least Connection",
                                                     variable=self.method_choice, value="least_connection")
        self.least_connection_radio.pack(side=tk.LEFT)

        self.least_time_radio = tk.Radiobutton(self.method_radio_frame, text="Least Time", variable=self.method_choice,
                                               value="least_time")
        self.least_time_radio.pack(side=tk.LEFT)

        self.random_radio = tk.Radiobutton(self.method_radio_frame, text="Random", variable=self.method_choice,
                                           value="random")
        self.random_radio.pack(side=tk.LEFT)

        self.receive_button = tk.Button(self.root, text="Receive Request", command=self.receive_request)
        self.receive_button.pack()

        self.cancel_button = tk.Button(self.root, text="Cancel Requests", command=self.cancel_requests)
        self.cancel_button.pack(side=tk.LEFT)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack(side=tk.RIGHT)

        #
        # self.server1_button = tk.Button(self.root, text="Send Request to Server 1", command=lambda: self.send_request(0))
        # self.server1_button.pack(side=tk.LEFT)
        #
        # self.server2_button = tk.Button(self.root, text="Send Request to Server 2", command=lambda: self.send_request(1))
        # self.server2_button.pack(side=tk.LEFT)
        #
        # self.server3_button = tk.Button(self.root, text="Send Request to Server 3", command=lambda: self.send_request(2))
        # self.server3_button.pack(side=tk.LEFT)
        #



        self.root['bg'] = "#DDA0DD"

        self.update_bar_chart()

        self.server_listbox = tk.Listbox(self.root)
        self.server_listbox.pack()

        self.root.mainloop()

    def update_bar_chart(self):
        self.ax.clear()
        self.ax.bar(self.index, self.server_request_count, self.bar_width, color='#DDA0DD', edgecolor='black')
        self.ax.set_xlabel("Servers")
        self.ax.set_ylabel("Number of Requests")
        self.ax.set_xticks(self.index)
        self.ax.set_xticklabels(['Server 1', 'Server 2', 'Server 3'])
        self.ax.set_title(self.method_choice.get().capitalize() + " Requests")
        self.ax.set_facecolor("#D3D3D3")

        self.canvas.draw()

        total_requests = sum(self.server_request_count)
        if total_requests == 100:
            messagebox.showinfo(title="Thank You", message="Thank you so much ❤️")

    def update_server_listbox(self):
        self.server_listbox.delete(0, 'end')
        for i in range(self.num_servers):
            self.server_listbox.insert('end', f"Server {i + 1}: {self.server_request_count[i]} requests")

    def restart(self):
        self.last_server_used = -1
        self.server_request_count = [0] * self.num_servers
        self.update_bar_chart()
        self.update_server_listbox()


    def cancel_requests(self):
        # Prompt user for server index
        server_index = simpledialog.askinteger("Cancel Requests",
                                               "Enter server index (1-{}): ".format(self.num_servers))

        # If user canceled the dialog box or entered invalid input, return
        if not server_index or server_index <= 0 or server_index > self.num_servers:
            messagebox.showerror("Cancel Requests", "Error: Invalid server index.")
            return

        # Prompt user for number of requests to cancel
        num_cancel_requests = simpledialog.askinteger("Cancel Requests", "Enter number of requests to cancel: ")

        # If user canceled the dialog box or entered invalid input, return
        if not num_cancel_requests or num_cancel_requests <= 0:
            messagebox.showerror("Cancel Requests", "Error: Invalid number of requests.")
            return

        # Update the server request count
        server_index -= 1  # Adjust index to zero-based
        if self.server_request_count[server_index] >= num_cancel_requests:
            self.server_request_count[server_index] -= num_cancel_requests
            self.update_bar_chart()
            self.update_server_listbox()
            messagebox.showinfo("Cancel Requests",
                                "Cancelled {} requests from server {}.".format(num_cancel_requests, server_index + 1))
        else:
            messagebox.showerror("Cancel Requests", "Error: Not enough requests to cancel.")

    def receive_request(self):
        if self.request_count_entry.get():
            request_count = int(self.request_count_entry.get())
        else:
            request_count = 1

        for i in range(request_count):
            while True:
                try:
                    if self.method_choice.get() == "round_robin":
                        self.last_server_used = (self.last_server_used + 1) % self.num_servers
                    elif self.method_choice.get() == "least_connection":
                        self.last_server_used = self.server_request_count.index(min(self.server_request_count))
                    elif self.method_choice.get() == "least_time":
                        processing_times = []
                        for j in range(self.num_servers):
                            if self.server_request_count[j] < 2000000000:
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.connect((socket.gethostname(), self.servers[j]))
                                start_time = time.time()
                                s.send(b"Hello, server!")
                                response = s.recv(1024)
                                end_time = time.time()
                                time_taken = end_time - start_time
                                processing_times.append(time_taken)
                                s.close()
                            else:
                                processing_times.append(float("inf"))
                            self.last_server_used = processing_times.index(min(processing_times))
                    else:   
                        self.last_server_used = random.randint(0, self.num_servers - 1)

                    if self.server_request_count[self.last_server_used] < 20000000000:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((socket.gethostname(), self.servers[self.last_server_used]))
                        start_time = time.time()
                        s.send(b"Hello, server!")
                        response = s.recv(1024)
                        end_time = time.time()
                        time_taken = end_time - start_time
                        print(f"Request processed in {time_taken} seconds.")
                        self.server_request_count[self.last_server_used] += 1
                        break  # Exit the while loop and proceed to the next request

                except (ConnectionRefusedError, TimeoutError):
                    # The server did not respond, try the next one
                    self.last_server_used = (self.last_server_used + 1) % self.num_servers

            self.update_bar_chart()
            self.update_server_listbox()

import threading
import socket
import time

class Server(threading.Thread):
    def __init__(self, port, max_connections=None):
        threading.Thread.__init__(self)
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostname(), port))
        self.server_socket.listen(5)
        self.running = False
        self.connections = 0
        self.max_connections = max_connections

    def run(self):
        self.running = True
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.connections += 1
                print(f"Connection from {address} has been established! (total connections: {self.connections})")
                client_socket.send(bytes("Welcome to the Server!", "utf-8"))
                client_socket.close()
                if self.max_connections is not None and self.connections >= self.max_connections:
                    raise socket.timeout
            except socket.timeout:
                print(f"Maximum number of connections ({self.max_connections}) reached!")
                self.server_socket.close()
                break

    def stop(self):
        self.running = False
        self.server_socket.close()

my_server = Server(port=8080, max_connections=5)
my_server.start()
server = Server(8787)
server.start()
server = Server(7676)
server.start()

serversss = [8080, 8787, 7676]


LoadyB(serversss)

