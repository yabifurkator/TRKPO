
class AlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("already exists")


class NotFoundException(Exception):
    def __init__(self):
        super().__init__("not found")
