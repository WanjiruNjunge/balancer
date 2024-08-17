# Load Balancer Project

This project implements a load balancer using Python and Docker, designed to distribute incoming network traffic across multiple servers. This ensures no single server bears too much demand. By spreading the requests across multiple servers, it increases reliability and availability within your application. 
The project is based on the principles outlined in a Load Balancer Assignment, adapted to the specific implementation details found in the codebase.

## Overview

The load balancer implemented utilizes consistent hashing to distribute the load evenly among a pool of servers. It's built on Flask, a lightweight WSGI web application framework in Python, to handle incoming requests and forward them to the appropriate backend server.

## Key Components

- *Consistent Hashing*: Implemented in ConsistentHashing within hashing.py, it ensures a distributed, scalable, and replicable distribution of requests.
- *Server Management*: Servers can be dynamically added or removed from the pool, with the add_server and remove_server methods. To add a server you may need to call the /add endpoint either with or without a payload. to remove you may call /rm without a payload.
- *Request Routing*: Incoming requests are routed to the appropriate server based on the consistent hashing algorithm. This is handled in the assign function within loadbalancer.py.
- *Docker Integration*: The application and its servers are containerized using Docker, allowing for easy deployment and scaling.

## Setup and Running

### Pre-requisites

- Docker
- Python 3.8 or higher

### Installation

1. *Start Docker Engine*: Ensure that Docker is running on your machine. You can start Docker from the command line or by using your desktop client.
2. *Clone the repository*: Clone the repository to your local machine using:
   ```sh
   git clone git@github.com:WanjiruNjunge/balancer.git
   ```

3. *Install Python Dependencies:*
Navigate to the project directory and install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
4. *Run the Main Script:*
   Execute your main.py script using the command:
    ```sh
    python main.py
    ```
This will start the load balancer and all associated services.

5. Ensure the server is running
   - Open your web browser and navigate to `localhost:7432/home` to confirm the server is up and running.
![Screenshot 2024-08-17 211137](https://github.com/user-attachments/assets/f7e91e7c-1944-4bce-8fe8-32e2f1316783)


## Visual Performance Monitoring

1. *Load Balancer Performance:* Monitor the performance of your load balancer through the graphical analysis provided. 
2. *Request Handling Success Rate:* Check the success rate of handled requests.

### Testing the Project

To test if the load balancer is working correctly, you can send multiple requests to the load balancer and verify that the requests are being distributed across  Flask servers:

#### 1. Send Requests:

You could use a tool like curl or Postman to send requests to `http://localhost:7432`

#### 2. Verify Load Balancing:

Check the logs of the Flask server containers to see if the requests are being distributed among them. You can view the logs using the following command:

```bash
docker logs [container_id]
```

#### 3. Analyze Performance Metrics:
After running tests, analyze the generated charts and logs to understand:

- Distribution of requests across servers
- Success rates of requests
- Resource utilization during high load
- Ability of the system to handle concurrent requests


### Analyzing Performance
#### Sample Results
For these tests, carry out an analysis of the balancer to get the relevant metrics by running:
```sh
python analysis.py
```
#### Test 1: Load Distribution
Launch 10,000 asynchronous requests on 3 server containers.
Record the number of requests handled by each server and plot a bar chart.
*Opening* `localhost:7432/performancegraph` *should display the graph*

*Ideally:* the load would be evenly distributed among server instances.

![graph](https://github.com/user-attachments/assets/fb456d75-680c-41e6-ba21-3b4159e1ebcc)


#### Test 2: Scalability
Increament the number of server containers from 2 to 6 (launching 10,000 requests each time).
*Ideally:* The load would be evenly distributed and efficiently scaled as server instances increase. 


#### Test 3: Failure Recovery
Test load balancer endpoints until server failure is achieved.
Ensure the load balancer spawns new instances to handle the load and maintain the specified number of replicas.

![short_requests](https://github.com/user-attachments/assets/c7195478-511c-4251-ae02-c583f1b4e7ba)


## Additional Info
### Docker Setup Process
To deploy the project,assuming Docker Desktop is already installed: 

- *Open Docker Desktop:* Launch Docker Desktop from your start menu or applications folder.
- *Navigate to Project Directory:* Use the Docker Desktop interface or the built-in terminal to navigate to your project directory.
- *Run Docker Compose:* 
Build and run the containers. 
   ```sh
   docker-compose up --build
   ```  
     
- *Check Docker Status:* 
Ensure Docker is running by checking the status in the Docker Desktop dashboard or by running ```docker info``` in your terminal.

Or within your IDE terminal, if that's what you're using.

![running_engine](https://github.com/user-attachments/assets/0d034263-9e17-4bf0-b6ce-ae59740d6baa)


## Contribution
Contributions to the load balancer implementation project are welcome! Feel free to fork, raise issues, and submit pull requests to the repo while ensuring that your code follows the project's coding guidelines and standards.

## Acknowledgments
Special thanks to the course instructor for providing the assignment specifications and guidance and to the contributors of the project.
<!-- Containers with the prefix 'emergency_' are spawned on failure of a replica.
On failure of a server during a test run with 40000 requests, 'emergency_52' and 'emergency_11' were spawned to handle requests -->
