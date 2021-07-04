from lark import Lark
from lark import Transformer

class MyTransformer(Transformer): #function for printing according to each query
    def create_table_query(self, items):
        print(items[0]) #create
        print(items[1]) #table
        print(items[2].children[0]) #table name
        print(items[3])
        #print(items[4])
        #print(items[5])
        
        print("DB_2017-18538> 'CREATE TABLE' requested")
    def drop_table_query(self, items):
        print("DB_2017-18538> 'DROP TABLE' requested")
    def desc_query(self, items):
        print("DB_2017-18538> 'DESC' requested")
    def insert_query(self, items):
        print("DB_2017-18538> 'INSERT' requested")
    def delete_query(self, items):
        print("DB_2017-18538> 'DELETE' requested")
    def select_query(self, items):
        print("DB_2017-18538> 'SELECT' requested")
    def show_tables_query(self, items):
        print("DB_2017-18538> 'SHOW TABLES' requested")

with open('grammar.lark') as file: #create parser using Lark function and transformer parameter
    sql_parser = Lark(file.read(), start="command", parser="lalr",transformer=MyTransformer(), lexer="standard")

while True: #while loop for continued input query
    try:
        print("DB_2017-18538> ", end='')
        input_str = ""
        query = ""
        exit = "exit;"
        while True: #append input query until ';' is come
            temp = input().rstrip()
            if temp.endswith(";"):
                input_str += " " + temp
                break
            else:
                input_str += " " + temp

        if input_str.find(exit) != -1: #split input query for middle of 'exit' query
            query = input_str.split(exit)[0] + exit
        else:
            query = input_str

        result = sql_parser.parse(query) #parse input query using parser
        if query.find(exit) != -1: #break if 'exit' query exist
            break
        
    except Exception as e: #except for catching exception
        print("DB_2017-18538> Syntax error")
