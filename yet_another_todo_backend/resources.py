from typing import List
from yet_another_todo_backend.utils import print_with_indent
import json
import os


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry: Entry
            entry.save(self.data_path)

    def load(self):
        for entry in os.listdir(self.data_path):

            path = os.path.join(self.data_path, entry)

            if '.json' in path:
                self.entries.append(Entry.load(path))

    def add_entry(self, title: str):
        self.entries.append(Entry(title))


class Entry:
    def __init__(self, title: str, entries: list = None, parent=None):
        self.title = title

        if entries is None:
            entries = []

        self.entries = entries
        self.parent = parent

    def add(self, entry):
        self.entries.append(entry)
        entry.parent = self

        '''
        entry = Entry('products')
        while entry:
            print(entry)
            entry = entry.parent
        '''

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):  # return JSON?

        result = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries],
        }

        return result

    @classmethod
    def from_json(cls, value: dict):  # value - str?
        new_entry = cls(value['title'])

        for sub_entry in value.get('entries', []):
            new_entry.add(cls.from_json(sub_entry))

        return new_entry

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as f:
            f.write(json.dumps(self.json()))

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            return cls.from_json(json.loads(f.read()))  # or load(f)?

    def __str__(self):
        return self.title
