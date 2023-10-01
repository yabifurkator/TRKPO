from doit.tools import Interactive

from tools.doit import impl


def task_start_project():
    return {
        'basename': 'start-project',
        'doc': 'Start all project containers',
        'actions': [
            Interactive(impl.start_project)
        ]
    }


def task_stop_project():
    return {
        'basename': 'stop-project',
        'doc': 'Stop all project containers',
        'actions': [
            Interactive(impl.stop_project)
        ]
    }


def task_restart_project():
    return {
        'basename': 'restart-project',
        'doc': 'Stop all project containers and then start all project containers',
        'actions': [
            Interactive(impl.stop_project),
            Interactive(impl.start_project),
        ]
    }


def task_docker_compose_logs():
    return {
        'basename': 'docker-compose-logs',
        'doc': 'Show docker-compose logs in terminal',
        'actions': [
            Interactive(impl.docker_compose_logs)
        ]
    }


def task_cleanup():
    return {
        'basename': 'cleanup',
        'doc': 'Remove all temporary files',
        'actions': [
            Interactive(impl.cleanup)
        ]
    }
