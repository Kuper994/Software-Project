FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system tools and development dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    postgresql-client \
    gcc \
    g++ \
    gdb \
    valgrind \
    make \
    cmake \
    python3-dev \
    openssh-server \
    sudo \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Make /usr/bin/python3 use the Python 3.12 interpreter from the official image.
RUN ln -sf /usr/local/bin/python3 /usr/bin/python3 \
    && ln -sf /usr/local/bin/python3 /usr/bin/python

# Install the Docker CLI and Compose v2 plugin (amd64 / arm64).
RUN set -eux; \
    ARCH="$(dpkg --print-architecture)"; \
    case "$ARCH" in \
        amd64) DOCKER_ARCH=x86_64; COMPOSE_ARCH=x86_64 ;; \
        arm64) DOCKER_ARCH=aarch64; COMPOSE_ARCH=aarch64 ;; \
        *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;; \
    esac; \
    curl -fsSL \
        "https://download.docker.com/linux/static/stable/${DOCKER_ARCH}/docker-27.3.1.tgz" \
        | tar -xz --strip-components=1 -C /usr/local/bin docker/docker; \
    mkdir -p /usr/local/lib/docker/cli-plugins; \
    curl -fsSL \
        "https://github.com/docker/compose/releases/download/v2.30.3/docker-compose-linux-${COMPOSE_ARCH}" \
        -o /usr/local/lib/docker/cli-plugins/docker-compose; \
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Install all Python dependencies globally from requirements.txt.
WORKDIR /home/student
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && python3 -m pip check \
    && python3 -c "import pandas; print('pandas:', pandas.__version__)"

# Create the student account and configure SSH.
RUN useradd -m -s /bin/bash student \
    && echo 'student:course' | chpasswd \
    && mkdir -p /run/sshd \
    && sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' \
        /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
