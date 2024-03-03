import os
import time

project_root = os.getcwd()
services_path = os.path.join(project_root, "services")
service_bot_path = os.path.join(services_path, 'bot')


def start_project() -> str:
    commands = ''

    # if not venv in bot service exists
    if not os.path.isdir(f'{service_bot_path}/venv'):
        # create and initialize venv
        commands += f'python3.10 -m venv {service_bot_path}/venv && '
        commands += f'. {service_bot_path}/venv/bin/activate && '
        commands += f'pip3.10 install -r {service_bot_path}/requirements.txt && '
    else:
        # update requirements.txt file (based on venv)
        commands += f'. {service_bot_path}/venv/bin/activate && '
        commands += f'pip3.10 freeze > {service_bot_path}/requirements.txt && '

    # start project
    commands += f'cd {services_path} && '
    commands += f'docker-compose --env-file {project_root}/.env up --build -d'

    return commands


def stop_project() -> str:
    commands = ''

    #stop project
    commands += f'cd {services_path} && '
    commands += f'docker-compose down'

    return commands


def run_ut(html_cov: bool) -> str:
    commands = ''

    commands += f'cd {service_bot_path}/src && '
    if html_cov:
        commands += f'python3.10 -m pytest -s --cov=./ --cov-report=html'
    else:
        commands += f'python3.10 -m pytest -s --cov=./'

    return commands


def docker_compose_logs() -> str:
    commands = ''

    commands += f'cd {services_path} && '
    commands += f'docker-compose logs'

    return commands


def cleanup() -> str:
    commands = ""

    commands += f"sudo rm -rf {project_root}/out/"

    return commands
