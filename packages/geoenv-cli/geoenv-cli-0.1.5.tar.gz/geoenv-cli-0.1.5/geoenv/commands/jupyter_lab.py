import uuid

from .core import interactive, ping, register_port, run, sub_parsers, threaded

register_port(8001)


@threaded
@run
def open_in_browser(url: str):
    if ping(
        url,
        timeout_message=f"Not able to automatically open url in browser [{url}]"
    ):
        return f"python -m webbrowser {url}"
    return None


def handler(parser_args, *args, **kwargs):
    jl_key = ""
    if parser_args.no_browser is False:
        key = uuid.uuid4()
        jl_key = f"--NotebookApp.token='{key}'"
        url = f"http://localhost:8001/lab?token={key}"
        open_in_browser(url)

    interactive(
        lambda: f"python -m 'jupyterlab' {jl_key} --port=8001 --ip=0.0.0.0"
    )()


jl_parser = sub_parsers.add_parser("jl", help="Start jupyter lab server")
jl_parser.add_argument(
    "--no-browser", action="store_true", help="Don't open Jupyter in browser"
)

jl_parser.set_defaults(handler=handler)
