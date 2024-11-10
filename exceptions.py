class DatabaseError(Exception):
    pass

class DbnotFoundException(DatabaseError):
    pass

class SectionInUseError(DatabaseError):
    pass
