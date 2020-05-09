"""Database class for operations on alarm data."""

import pickledb

class AlarmDatabaseError(Exception):
    """Error performing operation database."""


class AlarmDatabase:
    """ Class to provide access and operations to the alarm database
    """

    def __init__(self, path):
        """ Constructor class. Loads provided database file."""
        self.database = pickledb.load(path, True)

    def list(self):
        """ Lists all objects in the database
        """
        return self.database.getall()

    def get(self, key):
        """ Gets a record as specified by key
        """
        return self.database.get(key)

    def delete(self, key):
        """ Deletes a record as specified by key
        """
        return self.database.rem(key)

    def create(self, key, value):
        """ Creates a new record
        """
        return self.database.set(key, value)

    def update(self, key, value):
        """ Updates an entry
        """
        return self.database.set(key, value)
