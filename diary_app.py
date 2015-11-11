import sys
import os
import datetime
from collections import OrderedDict

from peewee import *


# CREATE DATABASE
# create a new database file "students.db"
db = SqliteDatabase('diary.db')


# CREATE TABLE
# inherit from peewee's Model class
class Entry(Model):
    # content
    content = TextField()

    # timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)

    # set Meta.database to our SqliteDatabse
    class Meta:
        database = db


def initialize():
    """Create the database and table if they don't exist"""

    # connect to the database
    db.connect()

    # create tables by passing in a list, "safe=True" wont err if db and tables exist
    db.create_tables([Entry], safe=True)


def clear():
    # clears all output in the system terminal
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")

        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an entry."""
    print('Enter your entry. Press "ctrl+d" when finished.')

    # collect the users entry and strip the whitespace
    # this method allows for multiple lines
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [Yn]: ').lower() != 'n':
            Entry.create(content=data)
            print('Saved successfully!')


def view_entries(search_query=None):
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('=' * len(timestamp))
        print(entry.content)
        print('\n\n' + '=' * len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entries for a string."""
    view_entries(input('Search query: '))


def delete_entry(entry):
    """Delete an entry."""
    if input('Are you sure? [yN] ').lower() == 'y':
        entry.delete_instance()
        print('Entry deleted!')

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('d', delete_entry),
    ('s', search_entries)
])

# RUN PROGRAM
# if this is the main file running and not
if __name__ == '__main__':

    initialize()
    menu_loop()

