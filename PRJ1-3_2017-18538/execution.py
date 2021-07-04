from os import read
from core import SimpleBDB
from exceptions import *

FILENAME = 'myBDB.db'


def init_db():
    with SimpleBDB(FILENAME, flags=SimpleBDB.CREATE) as db:
        try:
            assert isinstance(db['.meta.tables'], set)
        except (KeyError, AssertionError):
            db['.meta.tables'] = set()


def execute(msg):
    if msg[0] == 'create':
        create_table(msg[1], msg[2])
        print(f"DB_2017-18538> '{msg[1]}' table is created")
    if msg[0] == 'drop':
        drop_table(msg[1])
        print(f"DB_2017-18538> '{msg[1]}' table is dropped")
    if msg[0] == 'desc':
        desc_table(msg[1])
    if msg[0] == 'show':
        show_tables()
    # DML implementation
    if msg[0] == 'insert':
        insert(msg[1], msg[2])
        print(f"DB_2017-18538> The row is inserted")
    if msg[0] == 'delete':
        rows = delete(msg[1], msg[2])
        print(f"DB_2017-18538> {rows} row(s) is deleted")
    if msg[0] == 'select':
        select(msg[1], msg[2], msg[3])

def check_fk(db, ad, fk):
    atts, ref_table, ref_atts = fk

    try:
        ref_ad = db[ref_table + '.ad']
        ref_pk = db[ref_table + '.pk']
    except KeyError as e:
        raise ReferenceTableExistenceError() from e

    for a in ref_atts:
        if a not in ref_ad:
            raise ReferenceColumnExistenceError()

    if set(ref_atts) != set(ref_pk):
        raise ReferenceNonPrimaryKeyError()

    if len(atts) != len(ref_atts):
        raise ReferenceTypeError()

    for a1, a2 in zip(atts, ref_atts):
        d1 = ad[a1]
        d2 = ref_ad[a2]
        if d1[0] != d2[0] or d1[1] != d2[1]:
            raise ReferenceTypeError()


def create_table(name, schema):
    with SimpleBDB(FILENAME) as db:
        ad, pk, fk_list = schema
        for fk in fk_list:
            check_fk(db, ad, fk)

        tables = db['.meta.tables']
        if name in tables:
            raise TableExistenceError()
        tables.add(name)
        db['.meta.tables'] = tables

        db[name + '.ad'] = ad
        db[name + '.pk'] = pk
        db[name + '.fk'] = fk_list
        db[name + '.ref'] = 0
        ###
        db[name + '.record'] = []

        for _, ref_table, _ in fk_list:
            key = ref_table + '.ref'
            db[key] = db[key] + 1


def drop_table(name):
    with SimpleBDB(FILENAME) as db:
        try:
            ref = db[name + '.ref']
        except KeyError as e:
            raise NoSuchTable() from e

        if ref > 0:
            raise DropReferencedTableError(name)

        for _, ref_table, _ in db[name + '.fk']:
            key = ref_table + '.ref'
            db[key] = db[key] - 1

        del db[name + '.ad']
        del db[name + '.pk']
        del db[name + '.fk']
        del db[name + '.ref']
        ###
        del db[name + '.record']

        tables = db['.meta.tables']
        tables.remove(name)
        db['.meta.tables'] = tables


def desc_table(name):
    with SimpleBDB(FILENAME) as db:
        try:
            ad = db[name + '.ad']
            pk = db[name + '.pk']
            fk = db[name + '.fk']
            fk = {a for atts, _, _ in fk for a in atts}
        except KeyError as e:
            raise NoSuchTable() from e

        print_form = "{:22s}{:14}{:14}{:14}"

        print("-------------------------------------------------")
        print(f"table_name [{name}]")
        print(print_form.format("column_name", "type", "null", "key"))
        for a, d in ad.items():
            type = d[0] if d[0] != 'char' else f'char({d[1]})'
            null = 'Y' if d[2] else 'N'
            p, f = (a in pk), (a in fk)
            key = ("PRI/FOR" if f else "PRI") if p else ("FOR" if f else "")
            print(print_form.format(a, type, null, key))
        print("-------------------------------------------------")


def show_tables():
    with SimpleBDB(FILENAME) as db:
        print("----------------")
        for x in db['.meta.tables']:
            print(x)
        print("----------------")

# DML implementation
def insert(name, row):
    with SimpleBDB(FILENAME) as db:
        tables = db['.meta.tables']
        if name not in tables:
            raise NoSuchTable()
        
        ad = db[name + '.ad']
        record = db[name + '.record']

        if isinstance(row[0][0], list) == False: # col name이 명시된 경우
            for col in row[0]:
                if col not in ad:
                    raise InsertColumnExistenceError(col)
            if len(row[0]) != len(ad):
                raise InsertTypeMismatchError()
            for i in (0, len(ad)-1):
                if row[1][i][0] == 'INT':
                    if ad[row[0][i]][0] != 'int':
                        raise InsertTypeMismatchError()
                if row[1][i][0] == 'STR':
                    if ad[row[0][i]][0] != 'char':
                        raise InsertTypeMismatchError()
                    if len(row[1][i][1])-2 > ad[row[0][i]][1]: #truncated char
                        row[1][i][1] = "'" + row[1][i][1][1:ad[row[0][i]][1]+1] + "'"
                if row[1][i][0] == 'DATE':
                    if ad[row[0][i]][0] != 'date':
                        raise InsertTypeMismatchError()  
                if ad[row[0][i]][2] == False: # False가 not null / True가 null 가능
                    if row[1][i][0] == 'NULL':
                        raise InsertColumnNonNullableError(row[0][i])
            # insert into db
            r = []
            for rec in row[1]:
                r.append(rec[1])
            record.append(r)
            
        else: # col name이 명시되지 않은 경우
            if len(row[0]) != len(ad):
                raise InsertTypeMismatchError()
            
            for index, (key, elem) in enumerate(ad.items()):
                if elem[2] == False:
                    if row[0][index][1] == 'null':
                        raise InsertColumnNonNullableError(key)
                if elem[0] == 'char': #truncated char
                    if elem[1] < len(row[0][index][1]):
                        row[0][index][1] = "'" + row[0][index][1][1:elem[1]+1] + "'"

            # insert into db
            r = []
            for rec in row[0]:
                r.append(rec[1])
            record.append(r)
            
        db[name + '.record'] = record

def delete(name, cond):
    with SimpleBDB(FILENAME) as db:
        tables = db['.meta.tables']
        if name not in tables:
            raise NoSuchTable()
        ad = db[name + '.ad']
        record = db[name + '.record']
        #print(record)

        length = len(record) # where 절이 없는 경우
        if cond == []:
            db[name + '.record'] = []
            return length

        for i in cond: # check WhereColumnNotExist
            if isinstance(i, list):
                if i[0] not in ad:
                    raise WhereColumnNotExist()

        for i in cond: # check WhereIncomparableError
            if ad[i[0]][0] == 'int':
                if i[2][0] != 'INT' and i[2][0] != 'NULL':
                    raise WhereIncomparableError()
            if ad[i[0]][0] == 'char':
                if i[2][0] != 'STR' and i[2][0] != 'NULL':
                    raise WhereIncomparableError()
            if ad[i[0]][0] == 'date':
                if i[2][0] != 'DATE' and i[2][0] != 'NULL':
                    raise WhereIncomparableError()

        idx = 0
        deleted = 0
        len_record = len(record)
        new_record = []
        if len(cond) == 1: # check where clause
            for index, (key, elem) in enumerate(ad.items()):
                if key == cond[0][0]:
                    idx = index
            n=0
            for r in record:
                #print(r)
                #print(r[idx], cond[0][2][1])
                if r[idx] != cond[0][2][1]:
                    new_record.append(record[n])
                    deleted += 1
                n+=1

        db[name + '.record'] = new_record
        #print(db[name + '.record'])
        return len_record - deleted

def select(cols, froms, cond):
    with SimpleBDB(FILENAME) as db:
        tables = db['.meta.tables']
        for i in froms: # check No such table
            if i[0] not in tables and len(i) == 1:
                raise NoSuchTable()
            if len(i) != 1 and i[2] not in tables:
                raise NoSuchTable()
