
class InvalidUrlException(Exception):
    def __init__(self, url: str):
        super().__init__(f"invalid URL ({url})")

class UnexistingUrlException(Exception):
    def __init__(self, url: str):
        super().__init__(f"unexisting URL\n({url})")
