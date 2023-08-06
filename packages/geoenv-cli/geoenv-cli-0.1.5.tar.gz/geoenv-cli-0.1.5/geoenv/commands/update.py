from .core import GEOENV_DOCKER_IMAGE, process, sub_parsers


def handler(*args, **kwargs):
    process(f"docker pull {GEOENV_DOCKER_IMAGE}:latest")


update_parser = sub_parsers.add_parser("update", help="Update geoenv docker image")
update_parser.set_defaults(handler=handler)
