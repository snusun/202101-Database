class SyntaxError(Exception):
    def __str__(self):
        return "Syntax error"

class CreateTableSuccess(Exception):
    def __init__(self, tableName):
        self.tableName = tableName
    def __str__(self):
        return "'{}' table is created".format(self.tableName)

class DuplicateColumnDefError(Exception):
    def __str__(self):
        return "Create table has failed: column definition is duplicated"

class DuplicatePrimaryKeyDefError(Exception):
    def __str__(self):
        return "Create table has failed: primary key definition is duplicated"

class ReferenceTypeError(Exception):
    def __str__(self):
        return "Create table has failed: foreign key references wrong type"

class ReferenceNonPrimaryKeyError(Exception):
    def __str__(self):
        return "Create table has failed: foreign key references non primary key column"

class ReferenceColumnExistenceError(Exception):
    def __str__(self):
        return "Create table has failed: foreign key references non existing column"

class ReferenceTableExistenceError(Exception):
    def __str__(self):
        return "Create table has failed: foreign key references non existing table"

class NonExistingColumnDefError(Exception):
    def __init__(self, colName):
        self.colName = colName
    def __str__(self):
        return "Create table has failed: '{}' does not exists in column definition".format(self.colName)

class TableExistenceError(Exception):
    def __str__(self):
        return "Create table has failed: table with the same name already exists"

class DropSuccess(Exception):
    def __init__(self, tableName):
        self.tableName = tableName
    def __str__(self):
        return "'{}' table is dropped".format(self.tableName)

class DropReferencedTableError(Exception):
    def __init__(self, tableName):
        self.tableName = tableName
    def __str__(self):
        return "Drop table has failed: '{}' is referenced by other table".format(self.tableName)

class NoSuchTable(Exception):
    def __str__(self):
        return "No such table"

class CharLengthError(Exception):
    def __str__(self):
        return "Char length should be over 0"