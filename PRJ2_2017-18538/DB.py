from mysql.connector import connect
from mysql.connector.locales.eng import client_error

class Database:
# connect to database
    def __init__(self):
        self.connection = None
        self.connection = connect(
                host='astronaut.snu.ac.kr', 
                port=7000,
                user='DB2017_18538',
                password='DB2017_18538',
                database='DB2017_18538',
                charset='utf8'
        )

# input select query and return records
    def select(self, query):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

# do insert or delete query
    def insert_delete(self, query):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            self.connection.commit()

# reset database
    def reset(self):
        with self.connection.cursor(dictionary=True) as cursor: 
            cursor.execute("drop table reservation;")
            cursor.execute("drop table assignment;")
            cursor.execute("drop table building;")
            cursor.execute("drop table performance;")
            cursor.execute("drop table audience;")
            cursor.execute(
                '''
                CREATE TABLE `DB2017_18538`.`building` (
                    `ID` INT NOT NULL AUTO_INCREMENT,
                    `name` VARCHAR(200) NULL,
                    `location` VARCHAR(200) NULL,
                    `capacity` INT NULL,
                    PRIMARY KEY (`ID`)
                );
                '''
            )
            cursor.execute(
                '''
                CREATE TABLE `DB2017_18538`.`performance` (
                    `ID` INT NOT NULL AUTO_INCREMENT,
                    `name` VARCHAR(200) NULL,
                    `type` VARCHAR(200) NULL,
                    `price` INT NULL,
                    PRIMARY KEY (`ID`)
                );
                '''
            )
            cursor.execute(
                '''
                CREATE TABLE `DB2017_18538`.`audience` (
                `ID` INT NOT NULL AUTO_INCREMENT,
                `name` VARCHAR(200) NULL,
                `gender` VARCHAR(200) NULL,
                `age` INT NULL,
                PRIMARY KEY (`ID`));
                '''
            )
            cursor.execute(
                '''
                CREATE TABLE `assignment` (
                `performance_id` int NOT NULL,
                `building_id` int NOT NULL,
                PRIMARY KEY (`performance_id`),
                KEY `ID_idx` (`building_id`),
                CONSTRAINT `building_id` FOREIGN KEY (`building_id`) REFERENCES `building` (`ID`) ON DELETE CASCADE,
                CONSTRAINT `performance_id` FOREIGN KEY (`performance_id`) REFERENCES `performance` (`ID`) ON DELETE CASCADE);
                '''
            )
            cursor.execute(
                '''
                CREATE TABLE `reservation` (
                `performance_id` int NOT NULL,
                `audience_id` int NOT NULL,
                `seat_number` int NOT NULL,
                PRIMARY KEY (`performance_id`,`seat_number`),
                KEY `audience_id_idx` (`audience_id`),
                CONSTRAINT `audience_id` FOREIGN KEY (`audience_id`) REFERENCES `audience` (`ID`) ON DELETE CASCADE,
                CONSTRAINT `reservation_performance` FOREIGN KEY (`performance_id`) REFERENCES `assignment` (`performance_id`) ON DELETE CASCADE);
                '''
            )
            self.connection.commit()

# deconnect to database
    def __del__(self):
        if self.connection != None:
            self.connection.close()
