import os
import sys
from typing import Callable, NamedTuple


class Mode(NamedTuple):
    arg: str
    description: str
    handle: Callable[[], None]


def exec(command: str):
    os.system(command)


def restart():
    arg_index = sys.argv.index("-r")
    if len(sys.argv) < arg_index + 2:
        print("Restarts need service name.")
        sys.exit(1)

    service_name = sys.argv[arg_index + 1]

    match service_name:
        case "assistant":
            restart_assitant()
        case "landing":
            restart_landing()
        case _:
            print(f"Service {service_name} not exist.")


def restart_assitant():
    exec("docker compose stop assistant")
    exec("docker compose stop server")
    exec("dcoker compoe rm -f")
    exec("docker compose build assistant")
    exec("docker compose up -d assistant")
    exec("docker compose up -d server")


def restart_landing():
    exec("docker compose rm -f")
    exec("docker image rm netku-landing")
    exec("docker compose build --no-cache landing")
    exec("docker compose up landing")


def help():
    print("Commands:")
    for mode in modes:
        print(f"{mode.arg}: {mode.description}")


def manage():
    for arg in sys.argv:
        mode = list(filter(lambda mode: mode.arg == arg, modes))
        if len(mode) == 1:
            mode[0].handle()
            return
    print("Bad usage, use -h to view list of commands.")
    sys.exit(1)


modes: list[Mode] = {
    Mode("-r", "Restarts service. Needed service_name after space.", restart),
    Mode("-h", "Shows available commands.", help),
}


if __name__ == "__main__":
    manage()
