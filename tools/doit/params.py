
def param_html_cov() -> dict:
    return {
        "name": "html_cov",
        "long": "html-cov",
        "type": bool,
        "default": False,
        "help": "Make UT result in HTML-report",
    }

def param_show_output() -> dict:
    return {
        "name": "show_output",
        "long": "show-output",
        "type": bool,
        "default": False,
        "help": "Show IT output in console",
    }
