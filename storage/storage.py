# work storage
from base.my_requests import get_tasks, get_notes, get_remainders

class Tasks:
    def __init__(self):
        self.tasks = {}
        self.remainders = {}
        self.notes = {}

    def load_remainders(data):
        pass

    def load_notes(data):
        pass

    def load_tasks(data):
        pass


class Remainders:
    def __init__(self):
        self.remainders = {}

    def load_remainders(data):
        pass


class Notes:
    def __init__(self):
        self.notes = {}

    def load_notes(data):
        pass


def get_tasks_today():
    pass


def get_tasks_week():
    pass


def get_tasks_all():
    pass


def get_tasks_completed():
    pass
