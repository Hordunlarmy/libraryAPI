#!/usr/bin/env python3
from decouple import config as ENV
from fabric import Connection

# Configuration
REMOTE_DIR = "/home/ubuntu/"
GIT_URL = ENV("GIT_URL")
ACCESS_TOKEN = ENV("ACCESS_TOKEN")  # GitHub Access Token
GIT_DIR = REMOTE_DIR + GIT_URL.split("/")[-1].split(".")[0]
REMOTE_USER = ENV("REMOTE_USER")
REMOTE_HOST = ENV("REMOTE_HOST")


def install_docker(conn):
    """Install Docker on the remote host."""

    result = conn.run("which docker", warn=True, hide=True)
    if result.stdout.strip():
        print("------------Docker already installed--------------")
        return

    INSTALL = "sudo apt-get install -y"
    UPDATE = "sudo apt-get update"

    conn.run(f"{UPDATE}")
    conn.run(
        f"{INSTALL} apt-transport-https ca-certificates curl "
        f"software-properties-common"
    )

    conn.run(
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | "
        "sudo apt-key add -"
    )
    conn.run(
        'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"'
    )
    conn.run(f"{UPDATE}")
    conn.run(f"{INSTALL} docker-ce")

    conn.run(
        'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
    )
    conn.run("sudo chmod +x /usr/local/bin/docker-compose")
    conn.run("sudo usermod -aG docker ${USER}")
    conn.run("sudo systemctl enable docker")
    conn.run("sudo systemctl start docker")
    print("--------------Docker installed---------------")


def clone_repo(conn):
    """
    Clone the repository using GitHub Access Token and start the application
    """

    result = conn.run(
        f'test -d {GIT_DIR} && echo "exists" || echo "not exists"', hide=True
    )

    if "not exists" in result.stdout:
        print("--------------Cloning the repository---------------")
        # Clone using access token in the URL
        token_url = GIT_URL.replace("https://", f"https://{ACCESS_TOKEN}@")
        conn.run(f"git clone {token_url}")

    conn.run(f"git config --global --add safe.directory ${GIT_DIR}")
    conn.run(f"sudo chown -R $(whoami) {GIT_DIR}")
    with conn.cd(GIT_DIR):
        conn.run("git fetch origin && git reset --hard origin/main")
    print("--------------Repository cloned & Up-To-Date---------------")


def deploy(conn):
    """Deploy the application"""

    with conn.cd(GIT_DIR):
        conn.run("sudo docker compose up --build -d")
        conn.run("sudo docker image prune -af")
    print("--------------Application deployed---------------")


def handle_connection(host, user):
    """Handle connection and execute all tasks"""

    conn = Connection(host=host, user=user)
    result = conn.run("hostname", hide=True)
    print(
        f"== == == == == == == == == == == == == == == == == == == ==\n"
        f"Connected to {host}, hostname: {result.stdout.strip()}\n"
        f"== == == == == == == == == == == == == == == == == == == =="
    )

    install_docker(conn)
    clone_repo(conn)
    deploy(conn)


if __name__ == "__main__":
    try:
        handle_connection(REMOTE_HOST, REMOTE_USER)
    except Exception as e:
        print(f"Deployment failed: {e}")
        exit(1)
