# Load Balancer Project

This project implements a load balancer using Python and Docker, designed to distribute incoming network traffic across multiple servers. This ensures no single server bears too much demand. By spreading the requests across multiple servers, it increases reliability and availability within your application. The project is based on the principles outlined in the "DS_Assign_LB_2024.pdf" document, adapted to the specific implementation details found in the codebase.

## Overview

The load balancer utilizes consistent hashing to distribute the load evenly among a pool of servers. It's built on Flask, a lightweight WSGI web application framework in Python, to handle incoming requests and forward them to the appropriate backend server.

### Key Components

- **Consistent Hashing**: Implemented in `ConsistentHashing` within `hashing.py`, it ensures a distributed, scalable, and replicable distribution of requests.
- **Server Management**: Servers can be dynamically added or removed from the pool, with the `add_server` and `remove_server` methods. To add a server you may need to call the /add endpoint either with or without a payload. to remove you may call /rm without a payload.
- **Request Routing**: Incoming requests are routed to the appropriate server based on the consistent hashing algorithm. This is handled in the `assign` function within `loadbalancer.py`.
- **Docker Integration**: The application and its servers are containerized using Docker, allowing for easy deployment and scaling.

## Setup and Running

### Prerequisites

- Docker
- Python 3.8 or higher

### Installation

1. Clone the repository to your local machine.
2. Install the required Python packages:

```sh
pip install -r requirements.txt


```

3. to run the app run the following

```
make run
```
