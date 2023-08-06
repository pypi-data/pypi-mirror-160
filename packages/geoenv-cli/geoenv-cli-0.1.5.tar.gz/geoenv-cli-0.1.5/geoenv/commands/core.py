import argparse
import contextlib
import logging
import os
import subprocess
import threading
import time
import urllib.request
from datetime import datetime

GEOENV_DOCKER_IMAGE = "gridcell/geoenv"
GEOENV_NETWORK = "geoenv-network"
GEOENV_CONTAINER_NAME = "geoenv-container"
GEOENV_DOCKER_EXEC = f"docker exec -w /app -it {GEOENV_CONTAINER_NAME}"
GEOENV_DOCKER_RUN = (
    f"docker run --network {GEOENV_NETWORK} --name='{GEOENV_CONTAINER_NAME}' "
    f"{{ports}} -w /app --rm -v `pwd`:/app -it gridcell/geoenv "
)

_exposed_ports = []

main_parser = argparse.ArgumentParser(prog="geoenv")
sub_parsers = main_parser.add_subparsers(dest="command", required=True)


def threaded(fn):
    def _run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()

    return _run


def register_port(port: int):
    if port in _exposed_ports:
        raise ValueError(f"Port {port} already used")

    _exposed_ports.append(port)


def process(cmd, *args):
    try:
        args = args or []
        _cmd = [cmd, *args]
        result = subprocess.check_output(
            " ".join(_cmd), stderr=subprocess.STDOUT, shell=True
        )
        return 0, result.decode("utf-8")
    except subprocess.CalledProcessError as err:
        return err.returncode, err.stdout


def interactive(func):
    def inner(*args, **kwargs):
        command = func(*args, **kwargs)
        base_cmd = get_docker_base_cmd()
        os.system(f"{base_cmd} {command}")

    return inner


def run(func):
    def inner(*arg, **kwargs):
        cmd_args = func(*arg, **kwargs)
        if cmd_args is None:
            return True
        elif not isinstance(cmd_args, list):
            cmd_args = [cmd_args]

        code, msg = process(*cmd_args)
        if code != 0:
            print(msg.decode("utf-8"))
            return False
        return True

    return inner


def ping(url: str, timeout: int = 30, timeout_message: str = ""):
    start_ts = datetime.now().timestamp()
    while True:
        with contextlib.suppress(Exception):
            with urllib.request.urlopen(url) as r:
                if r.status < 400:
                    return True

        if start_ts + timeout < datetime.now().timestamp():
            logging.error(f"{timeout_message}\n")
            return False

        time.sleep(1)


def is_container_running(container_name):
    cmd = "docker ps"
    args = [
        "--format 'table {{.Names}}'",
        "|",
        f"grep {container_name}",
    ]
    return_code, _ = process(cmd, *args)
    return return_code == 0


def network_exists(name):
    cmd = "docker network ls"
    args = [
        "--format 'table {{.Name}}'",
        "|",
        f"grep {name}",
    ]
    return_code, _ = process(cmd, *args)
    return return_code == 0


def get_docker_base_cmd():
    if is_container_running(GEOENV_CONTAINER_NAME):
        return GEOENV_DOCKER_EXEC

    ports = " ".join([f"-p {port}:{port}" for port in _exposed_ports])
    return GEOENV_DOCKER_RUN.format(ports=ports)


@run
def create_network():
    if network_exists(GEOENV_NETWORK):
        return
    return f"docker network create -d bridge {GEOENV_NETWORK}"


@run
def remove_network():
    if not network_exists(GEOENV_NETWORK):
        return

    return f"docker network rm {GEOENV_NETWORK}"


def setup():
    create_network()


def tear_down():
    remove_network()
