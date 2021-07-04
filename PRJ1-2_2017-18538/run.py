from bsddb3 import db
from lark import Tree, Token
import lark
import json
from exception_handling import *

myDB = db.DB()
myDB.open('myDB.db', dbtype=db.DB_HASH, flags=db.DB_CREATE)

def put_table(key, value): # put table in DB
    k = key.encode('utf-8')
    v = json.dumps(value).encode('utf-8')
    return myDB.put(k, v)

def get_table(key): # get table in DB
    k = key.encode('utf-8')
    v = myDB.get(k)
    if v is None:
        return None
    value = json.loads(v.decode('utf-8'))
    return value if value else None

def delete_table(key): # delete table in DB
    myDB.delete(key.encode('utf-8'))

class Transformer(lark.Transformer):
    def command(self, items):
        if not isinstance(items[0], list):
            exit()
        return items[0]

    # manipulating tree in table structure(dictionary)
    def query_list(self, items):
        return items
    def table_name(self, items):
        return items[0]
    def table_element_list(self, items):
        elements = []
        for i in items:
            if isinstance(i, Tree) and i.data == 'table_element':
                elements.append(i.children[0])
        return elements
    def column_name(self, items):
        return items[0]
    def data_type(self, items):
        if items[0].value == 'char':
            return {'type': 'char', 'length': items[2].value}
        return {'type': items[0].value}
    def IDENTIFIER(self, items):
        return str(items)
    def column_definition(self, items):
        attri = {'attri': items[0].lower(), **items[1]}
        if isinstance(items[-1], Token) and items[-1].value == "null":
            attri['null'] = 'N'
        else:
            attri['null'] = 'Y'
        return attri
    def table_constraint_definition(self, items):
        return items[0]
    def primary_key_constraint(self, items):
        return {"primary_key": items[2]}
    def referential_constraint(self, items):
        return {"ref_table": items[4], "ref_attri": items[5], "foreign_key": items[2]}
    def column_name_list(self, items):
        col_name = []
        for i in items:
            if not isinstance(i, Token):
                col_name.append(i)
        return col_name
    
    def create_table_query(self, items): # handling create table query
        try:
            table = {}
            table_name = items[2].lower()
            if get_table(table_name) is not None: # if table is not exist
                raise TableExistenceError() 
            for line in items[3]:
                if 'attri' in line: # examine attributes
                    if line['attri'] in table:
                        raise DuplicateColumnDefError()
                    if 'length' in line:
                        if int(line['length']) < 1:
                            raise CharLengthError()
                    table[line['attri']] = line
                if 'primary_key' in line: # examine primary key
                    temp = []
                    for p in line['primary_key']: # check each primary key
                        t = p
                        p = p.lower()
                        if p not in table:
                            raise NonExistingColumnDefError(t)
                        if p in temp:
                            raise DuplicatePrimaryKeyDefError()
                        temp.append(p)
                        table[p]['null'] = 'N' 
                    table['primary_key'] = line
                if 'foreign_key' in line: # examine foreign key
                    for p in line['foreign_key']: # check foreign key is in table
                        t = p
                        p = p.lower()
                        if p not in table:
                            raise NonExistingColumnDefError(t)
                    if get_table(line['ref_table']) is None: # check reference table is exist
                        raise ReferenceTableExistenceError()
                    ref_table = get_table(line['ref_table'])
                    temp = []
                    for p in line['ref_attri']:
                        try: # check referenced attribute is exist
                            f = ref_table[p]
                        except Exception:
                            raise ReferenceColumnExistenceError()
                        if f['attri'] not in ref_table['primary_key']['primary_key']: # check whether referenced attribute is primary key
                            raise ReferenceNonPrimaryKeyError()
                        if len(line['ref_attri']) != len(line['foreign_key']): # check number of foreign key 
                            raise ReferenceTypeError()
                        refed = line['foreign_key'][line['ref_attri'].index(p)] 
                        if table[refed]['type'] != f['type']: # check type of foreign key
                            raise ReferenceTypeError()
                        if table[refed]['type'] == 'char' and f['type'] == 'char':
                            if table[refed]['length'] != f['length']:
                                raise ReferenceTypeError()
                    table['foreign_key'] = line
            put_table(table_name, table) # put table in DB
            #print(get_table(table_name))
            raise CreateTableSuccess(table_name)
        except Exception as e:
            print("DB_2017-18538>", e)

    def drop_table_query(self, items):
        try:
            table_name = items[2].lower()
            table = get_table(table_name)
            if table is None:
                raise NoSuchTable()
            cursor = myDB.cursor()
            while x := cursor.next(): # check the table is referenced from different table
                ref_table = get_table(x[0].decode('utf-8'))
                if 'foreign_key' in ref_table:
                    if table_name == ref_table['foreign_key']['ref_table'].lower():
                        raise DropReferencedTableError(items[2])
            delete_table(table_name)
            print(f"DB_2017-18538> '{items[2]}' table is dropped")
        except Exception as e:
            print("DB_2017-18538>", e)

    def desc_query(self, items):
        try:
            table_name = items[1].lower()
            table = get_table(table_name)
            if table is None:
                raise NoSuchTable()
            print("-------------------------------------------------")
            print("table_name [" + items[1] + "]")
            print_form = '%-20s%-20s%-20s%-20s\n'
            table_info = print_form % ('column_name', 'type', 'null', 'key')
            attr = []
            keys = []
            for line in table:
                if line != 'primary_key' and line != 'foreign_key': # split attributes and keys
                    attr.append(line)
                else:
                    keys.append(line)
            for a in attr:
                key = ''
                if table[a]['type'] == 'int':  # determine type of attribute
                    data_type = 'int'
                else:
                    data_type = table[a]['type'] + "(" + table[a]["length"] + ")"
                for k in keys: # determine whether each attribute is key or not
                    a = a.lower()
                    for t in table[k][k]:
                        if a.lower() == t.lower():
                            if k == 'primary_key':
                                key += 'PRI'
                            else:
                                key += 'FOR'
                        if key == 'PRIFOR':
                            key = 'PRI/FOR'
                table_info += print_form %(a, data_type, table[a]['null'], key)
            print(table_info + "-------------------------------------------------")
        except Exception as e:
            print("DB_2017-18538>", e)

    def show_tables_query(self, items):
        cursor = myDB.cursor()
        print("-------------------------------------------------")
        while x := cursor.next(): # using iteration, print table name
            print(x[0].decode("utf-8"))
        print("-------------------------------------------------")

    def select_query(self, items):
        print("DB_2017-18538> 'SELECT' requested")
    def insert_query(self, items):
        print("DB_2017-18538> 'INSERT' requested")
    def delete_query(self, items):
        print("DB_2017-18538> 'DELETE' requested")

def input_queries(prompt):
    s = input(prompt)
    if not s.strip():
        return []
    while not s.rstrip().endswith(';'):
        s += '\n' + input()
    return [x + ';' for x in s.split(';')[:-1]]


if __name__ == "__main__":
    prompt = "DB_2017-18538> "

    with open('grammar.lark') as file:
        parser = lark.Lark(file.read(), start="command", lexer='standard')
    transformer = Transformer()

    while True:
        for query in input_queries(prompt):
            try:
                tree = parser.parse(query)
                msg = transformer.transform(tree)[0].children[0]
                #print(prompt + f" '{msg}' requested")
            except lark.exceptions.UnexpectedInput:
                print(prompt + "Syntax error")
