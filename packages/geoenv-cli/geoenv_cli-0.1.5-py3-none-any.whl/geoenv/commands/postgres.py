import json
import os
from argparse import RawDescriptionHelpFormatter

from .core import GEOENV_NETWORK, is_container_running, run, sub_parsers

PG_CONTAINER_NAME = "geoenv-postgres-container"
PG_USER = "postgres"
PG_PASSWORD = "postgres"
PG_PORT = 5432

PGADMIN_CONTAINER_NAME = "geoenv-pgadmin-container"
PGADMIN_USER = "postgres@sparkgeo.com"
PGADMIN_PASSWORD = PG_PASSWORD
PGADMIN_PORT = 5433

HOST = "host.docker.internal"


def register_server_config():
    config = {
        "Servers": {
            "1": {
                "Name": "Localhost",
                "Group": "Servers",
                "Host": HOST,
                "Port": 5432,
                "MaintenanceDB": "postgres",
                "Username": "postgres",
                "SSLMode": "prefer",
                "SSLCert": "<STORAGE_DIR>/.postgresql/postgresql.crt",
                "SSLKey": "<STORAGE_DIR>/.postgresql/postgresql.key",
                "SSLCompression": 0,
                "Timeout": 10,
                "UseSSHTunnel": 0,
                "TunnelPort": "22",
                "TunnelAuthentication": 0,
            }
        }
    }
    name = os.path.join(os.getcwd(), "pg_admin_servers.json")
    with open(name, "w") as f:
        f.write(json.dumps(config))
    return name


@run
def pg_admin(parser_args, *args, **kwargs):

    if is_container_running(PGADMIN_CONTAINER_NAME):
        if parser_args.stop:
            return f"docker kill {PGADMIN_CONTAINER_NAME}"
        return
    elif parser_args.stop:
        return

    config_path = register_server_config()
    return (
        f"docker run --rm -d -v {config_path}:/pgadmin4/servers.json "
        f"-e PGADMIN_SERVER_JSON_FILE=/pgadmin4/servers.json --add-host={HOST}:host-gateway "
        f"-p {PGADMIN_PORT}:80 --network {GEOENV_NETWORK} --name '{PGADMIN_CONTAINER_NAME}' "
        f"-e PGADMIN_DEFAULT_EMAIL={PGADMIN_USER} -e PGADMIN_DEFAULT_PASSWORD={PGADMIN_PASSWORD} "
        "-e PGADMIN_LISTEN_ADDRESS=0.0.0.0 dpage/pgadmin4"
    )


@run
def postgres(parser_args, *args, **kwargs):
    if is_container_running(PG_CONTAINER_NAME):
        if parser_args.stop:
            return f"docker kill {PG_CONTAINER_NAME}"
        return
    return (
        f"docker run --rm -d -p {PG_PORT}:{PG_PORT} --add-host={HOST}:host-gateway"
        f" --network {GEOENV_NETWORK} --name '{PG_CONTAINER_NAME}' "
        f"-e POSTGRES_USER={PG_USER} -e POSTGRES_PASSWORD={PG_PASSWORD} kartoza/postgis"
    )


def handler(parser_args, *args, **kwargs):
    if parser_args.skip_pgadmin is False or parser_args.stop:
        pg_admin(parser_args, *args, **kwargs)

    postgres(parser_args, *args, **kwargs)


postgres_parser = sub_parsers.add_parser(
    "postgres",
    description=f"""Start postgres docker container.

    Details:

    Postgres Username: {PG_USER}
    Postgres Password: {PG_PASSWORD}
    Postgres Port: {PG_PORT}
    Postgres Host: localhost

    PGAdmin URL: http://localhost:{PGADMIN_PORT}
    PGAdmin Username: {PGADMIN_USER}
    PGAdmin Password: {PGADMIN_PASSWORD}
    """,
    formatter_class=RawDescriptionHelpFormatter,
)
postgres_parser.add_argument(
    "--stop", action="store_true", help="Stop postgres docker container."
)
postgres_parser.add_argument(
    "--skip-pgadmin", action="store_true", help="Don't start PGAdmin container."
)

postgres_parser.set_defaults(handler=handler)
