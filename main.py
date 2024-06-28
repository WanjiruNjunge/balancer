import subprocess

# Build the Docker image
build_command = "docker build -t loadbalancer ."
subprocess.run(build_command, shell=True, check=True)

build_server_command = "docker build -t server -f server/Dockerfile server"
subprocess.run(build_server_command, shell=True, check=True)

check_network_command = "docker network inspect my-network"
network_exists = subprocess.run(check_network_command, shell=True, capture_output=True)
if network_exists.returncode != 0:
  build_network_command = "docker network create my-network"
  subprocess.run(build_network_command, shell=True, check=True)

# Run the Docker container in privileged mode
run_command = "docker run --privileged --name loadbalancer_container -v /var/run/docker.sock:/var/run/docker.sock -p 7432:7432 -p 2375:2375 -d loadbalancer"
subprocess.run(run_command, shell=True, check=True)
