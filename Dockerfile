# Use an Ubuntu base image
FROM docker:dind


# Set the timezone (Avoid interactive prompts)
ENV TZ=Africa/Nairobi   
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update package list and install dependencies
RUN apk add --no-cache python3 py3-pip \
    gcc g++ \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    make \
    cmake \
    pkgconfig \
    freetype-dev \
    libpng-dev

# Verify Docker installation
RUN docker --version

# Verify Python installation
RUN python3 --version && pip3 --version



# Set up a working directory
WORKDIR /app

# Copy your application files (if any) into the container
COPY . .

EXPOSE 7432

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment and install dependencies
RUN . /app/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/run.sh
RUN rm Dockerfile


# Set the entry point to bash (you can change this to your application's entry point)
CMD /app/run.sh
