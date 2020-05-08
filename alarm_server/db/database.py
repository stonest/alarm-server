import pickledb

class AlarmDatabaseError:
    pass

class AlarmDatabase:
    """ Class to provide access and operations to the alarm database
    """

    def __init__(self, path):
        self.db = pickledb.load(path, True)
        
    def list(self):
        """ Lists all objects in the database
        """
        return self.db.getall()

    def get(self, key):
        """ Gets a record as specified by key
        """
        return self.db.get(key)

    def delete(self, key):
        """ Deletes a record as specified by key
        """
        return self.db.rem(key)

    def create(self, key, value):
        """ Creates a new record
        """
        return self.db.set(key, value)

    def update(self, key, value):
        """ Updates an entry
        """
        return self.db.set(key, value)