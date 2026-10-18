FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-pandas \
    python3-numpy \
    python3-psycopg2 \
    gcc \
    g++ \
    gdb \
    valgrind \
    make \
    cmake \
    git \
    openssh-server \
    sudo \
    vim \
    curl \
    wget \
    ca-certificates \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


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



WORKDIR /workspace

RUN useradd -m -s /bin/bash student \
    && echo 'student:course' | chpasswd \
    && mkdir -p /run/sshd

CMD ["/usr/sbin/sshd", "-D"]
