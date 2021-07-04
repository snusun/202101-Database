class SimpleDatabaseError(Exception):
    pass


class CreateTableError(SimpleDatabaseError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Create table has failed: {self.msg}"


class DropTableError(SimpleDatabaseError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Drop table has failed: {self.msg}"


class DuplicateColumnDefError(CreateTableError):
    def __init__(self):
        super().__init__("column definition is duplicated")


class DuplicatePrimaryKeyDefError(CreateTableError):
    def __init__(self):
        super().__init__("primary key definition is duplicated")


class ReferenceTypeError(CreateTableError):
    def __init__(self):
        super().__init__("foreign key references wrong type")


class ReferenceNonPrimaryKeyError(CreateTableError):
    def __init__(self):
        super().__init__("foreign key references non primary key column")


class ReferenceColumnExistenceError(CreateTableError):
    def __init__(self):
        super().__init__("foreign key references non existing column")


class ReferenceTableExistenceError(CreateTableError):
    def __init__(self):
        super().__init__("foreign key references non existing table")


class NonExistingColumnDefError(CreateTableError):
    def __init__(self, column):
        super().__init__(f"'{column}' does not exists in column definition")


class TableExistenceError(CreateTableError):
    def __init__(self):
        super().__init__("table with the same name already exists")


class DropReferencedTableError(DropTableError):
    def __init__(self, table):
        super().__init__(f"'{table}' is referenced by other table")


class NoSuchTable(SimpleDatabaseError):
    def __str__(self):
        return "No such table"


class CharLengthError(SimpleDatabaseError):
    def __str__(self):
        return "Char length should be over 0"

# DML exceptions

class InsertResult(SimpleDatabaseError):
    def __str__(self):
        return "The row is inserted"

class InsertError(SimpleDatabaseError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Insertion has failed: {self.msg}"

class InsertDuplicatePrimaryKeyError(InsertError):
    def __init__(self):
        super().__init__("Primary key duplication")

class InsertReferentialIntegrityError(InsertError):
    def __init__(self):
        super().__init__("Feferential integrity violation")

class InsertTypeMismatchError(InsertError):
    def __init__(self):
        super().__init__("Types are not matched")

class InsertColumnExistenceError(InsertError):
    def __init__(self, column):
        super().__init__(f"'{column}' does not exist")

class InsertColumnNonNullableError(InsertError):
    def __init__(self, column):
        super().__init__(f"'{column}' is not nullable")

class DeleteResult(SimpleDatabaseError):
    def __init__(self, count):
        self.count = count

    def __str__(self):
        return f"{self.count} row(s) are deleted"

class DeleteReferentialIntegrityPassed(SimpleDatabaseError):
    def __init__(self, count):
        self.count = count

    def __str__(self):
        return f"{self.count} row(s) are not deleted due to referential integrity"

class SelectTableExistenceError(SimpleDatabaseError):
    def __init__(self, table):
        self.table = table

    def __str__(self):
        return f"Selection has failed: '{self.table}' does not exist"

class SelectColumnResolveError(SimpleDatabaseError):
    def __init__(self, column):
        self.column = column

    def __str__(self):
        return f"Selection has failed: fail to resolve '{self.column}'"

class WhereIncomparableError(SimpleDatabaseError):
    def __str__(self):
        return "Where clause try to compare incomparable values"

class WhereTableNotSpecified(SimpleDatabaseError):
    def __str__(self):
        return "Where clause try to reference tables which are not specified"

class WhereColumnNotExist(SimpleDatabaseError):
    def __str__(self):
        return "Where clause try to reference non existing column"

class WhereAmbiguousReference(SimpleDatabaseError):
    def __str__(self):
        return "Where clause contains ambiguous references"