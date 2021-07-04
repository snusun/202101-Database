# 적절한 형식으로 공연장 정보를 출력
def print_all_buildings(db):
    print("--------------------------------------------------------------------------------")
    print_form = '%-10s%-34s%-14s%-14s%-s\n'
    column = print_form % ('id', 'name', 'location', 'capacity', 'assigned')
    print(column + "--------------------------------------------------------------------------------")

    buildings = db.select("select * from building")
    table_info = ''
    for i in buildings:
        building_id = i['ID']
        name = i['name']
        location = i['location']
        capacity = i['capacity']
        assigned_query = f'select count(performance_id) from assignment where assignment.building_id = {building_id}'
        assigned = db.select(assigned_query)[0]['count(performance_id)']
        table_info += print_form %(building_id, name, location, capacity, assigned)
    print(table_info + "--------------------------------------------------------------------------------\n")

# 적절한 형식으로 공연 정보를 출력
def print_all_performances(db):
    print("--------------------------------------------------------------------------------")
    print_form = '%-10s%-34s%-14s%-14s%-s\n'
    column = print_form % ('id', 'name', 'type', 'price', 'booked')
    print(column + "--------------------------------------------------------------------------------")

    performances = db.select("select * from performance")
    table_info = ''
    for i in performances:
        performance_id = i['ID']
        name = i['name']
        genre_type = i['type']
        price = i['price']
        booked_query = f'select count(audience_id) from reservation where reservation.performance_id = {performance_id}'
        booked = db.select(booked_query)[0]['count(audience_id)']
        table_info += print_form %(performance_id, name, genre_type, price, booked)
    print(table_info + "--------------------------------------------------------------------------------\n")

# 적절한 형식으로 관객 정보를 출력
def print_all_audiences(db):
    print("--------------------------------------------------------------------------------")
    print_form = '%-10s%-40s%-15s%-20s\n'
    column = print_form % ('id', 'name', 'gender', 'age')
    print(column + "--------------------------------------------------------------------------------")

    audiences = db.select("select * from audience")
    table_info = ''
    for i in audiences:
        audience_id = i['ID']
        name = i['name']
        gender = i['gender']
        age = i['age']
        table_info += print_form %(audience_id, name, gender, age)
    print(table_info + "--------------------------------------------------------------------------------\n")

# 새로운 공연장을 추가
def insert_a_new_building(db):
    name = input("Building name: ")[:200]
    location = input("Building location: ")[:200]
    capacity = int(input("Building capacity: "))
    
    if capacity>0:
        query = f'insert into building (name, location, capacity) values ("{name}", "{location}", {capacity});'
        db.insert_delete(query)
        print('A building is successfully inserted\n')
    else:
        print('Capacity should be more than 0\n')

# 공연장을 공연장 id를 가지고 삭제
def remove_a_building(db):
    building_id = int(input("Building ID: "))
    select_query = f'select * from building where id = {building_id}'
    if db.select(select_query) == []:
        print(f"Building {building_id} doesn't exist\n")
    else:
        query = f'delete from building where id = {building_id};'
        db.insert_delete(query)
        print("A building is successfully removed\n")

# 새로운 공연을 추가
def insert_a_new_performance(db):
    name = input("Performance name: ")[:200]
    genre_type = input("Performance type: ")[:200]
    price = int(input("Performance price: "))
    
    if price>=0:
        query = f'insert into performance (name, type, price) values ("{name}", "{genre_type}", {price});'
        db.insert_delete(query)
        print('A performance is successfully inserted\n')
    else:
        print('Price should be 0 or more\n')

# 공연을 공연 id를 가지고 삭제
def remove_a_performance(db):
    performance_id = int(input("Performance ID: "))
    select_query = f'select * from performance where id = {performance_id}'
    if db.select(select_query) == []:
        print(f"Performance {performance_id} doesn't exist\n")
    else:
        query = f'delete from performance where id = {performance_id};'
        db.insert_delete(query)
        print("A performance is successfully removed\n")

# 새로운 관객을 추가
def insert_a_new_audience(db):
    name = input("Audience name: ")[:200]
    gender = input("Audience gender: ")[:200]
    if not (gender=='F' or gender=='M'):
        print("Gender should be 'M' or 'F'\n")
        return

    age = int(input("Audience age: "))
    if age<=0:
        print("Age should be more than 0\n")
    else:
        query = f'insert into audience (name, gender, age) values ("{name}", "{gender}", {age});'
        db.insert_delete(query)
        print('An audience is successfully inserted\n')

# 관객을 관객 id를 가지고 삭제
def remove_an_audience(db):
    audience_id = int(input("Audience ID: "))
    select_query = f'select * from audience where id = {audience_id}'
    if db.select(select_query) == []:
        print(f"Audience {audience_id} doesn't exist\n")
    else:
        query = f'delete from audience where id = {audience_id};'
        db.insert_delete(query)
        print("An audience is successfully removed\n")

# 공연장에 공연을 배정
def assign_a_performance_to_a_building(db):
    building_id = int(input("Building ID: "))
    # building이 있는지 확인
    building_exist = f'select * from building where ID = {building_id}'
    if db.select(building_exist) == []:
        print(f"Building {building_id} doesn't exist\n")
        return

    performance_id = int(input("Performance ID: "))
    performance_exist = f'select * from performance where ID = {performance_id}'
    # performance가 있는지 확인
    if db.select(performance_exist) == []:
        print(f"Performance {performance_id} doesn't exist\n")
        return

    assigned = f'select * from assignment where performance_id = {performance_id}'
    # performance가 이미 배정되었는지 확인
    if db.select(assigned) == []:
        query = f'insert into assignment (building_id, performance_id) values ("{building_id}", "{performance_id}");'
        db.insert_delete(query)
        print("Successfully assign a performance\n")
    else: 
        print(f"Performance {performance_id} is already assigned\n")
    
# 관객이 공연을 예약
def book_a_performance(db):
    performance_id = int(input("Performance ID: "))
    # 공연이 존재하는지 확인
    if db.select(f'select * from performance where ID = {performance_id}') == []:
        print(f"Performance {performance_id} doesn't exist\n")
        return 
    # 공연이 공연장에 배정되어 있지 않으면 실패
    if db.select(f'select * from assignment where performance_id = {performance_id}') == []:
        print(f"Performance {performance_id} isn't assigned\n")
        return 

    audience_id = int(input("Audience ID: "))
    # 관객이 존재하는지 확인
    if db.select(f'select * from audience where ID = {audience_id}') == []:
        print(f"Audience {audience_id} doesn't exist\n")
        return 

    seat_number = input("Seat number: ").split(",")
    #print(seat_number)
    int_seat = []
    for i in seat_number:
        i = i.replace(" ","")
        int_seat.append(int(i))
    #print(int_seat)

    capacity_query = f'''select capacity from building, assignment 
        where assignment.performance_id = {performance_id} 
        and building.ID = assignment.building_id'''
    capacity = db.select(capacity_query)
    
    # 좌석 번호 하나라도 범위를 벗어나면 실패
    for i in int_seat:
        if capacity[0]['capacity'] < i:
            print("Seat number out of range\n")
            return
    # 좌석 번호 하나라도 예매되어 있으면 실패
    for i in int_seat:
        if db.select(f'select * from reservation where performance_id = {performance_id} and seat_number = {i}') != []:
            print("The seat is already taken\n")
            return
    for i in int_seat:
        query = f'insert into reservation (performance_id, audience_id, seat_number) values ("{performance_id}", "{audience_id}", "{i}");'
        db.insert_delete(query)
    # price 계산
    price_query = f''' select price from performance
        where ID = {performance_id}'''
    price = db.select(price_query)[0]['price']
    age_query = f''' select age from audience
        where ID = {audience_id}'''
    age = db.select(age_query)[0]['age']

    if age <= 7:
        price = 0
    elif age >= 8 and age <=12:
        price = rounding(price*(0.5)*len(int_seat))
    elif age >= 13 and age <= 18:
        price = rounding(price*(0.8)*len(int_seat))
    else:
        price = price*len(int_seat)
    price = format(price, ',')    
    print(f"Successfully book a performance\nTotal ticket price is {price}\n")    

# 반올림 함수 구현
def rounding(n):
    if n - int(n) >= 0.5:
        return int(n)+1
    return int(n)

# 공연장에 배정된 공연을 출력
def print_all_performances_which_assigned_at_a_building(db):
    building_id = int(input("Building ID: "))

    if db.select(f'select * from building where ID = {building_id}') == []:
        print(f"Building {building_id} doesn't exist\n")
    else:
        print("--------------------------------------------------------------------------------")
        print_form = '%-10s%-34s%-14s%-14s%-s\n'
        column = print_form % ('id', 'name', 'type', 'price', 'booked')
        print(column + "--------------------------------------------------------------------------------")
        performance_sql = f'''
            select * from performance, assignment
            where assignment.building_id = {building_id} and
            performance.id = assignment.performance_id;
        '''
        performances = db.select(performance_sql)
        table_info = ''
        for i in performances:
            performance_id = i['ID']
            name = i['name']
            genre_type = i['type']
            price = i['price']
            table_info += print_form %(performance_id, name, genre_type, price, '0')
        print(table_info + "--------------------------------------------------------------------------------\n")

# 공연을 예매한 관객을 출력
def print_all_audiences_who_booked_for_a_performance(db):
    #print("13")
    performance_id = int(input("Performance ID: "))
    if db.select(f'select * from performance where ID = {performance_id}') == []:
        print(f"Performance {performance_id} doesn't exist\n")
        return

    query = f'''
        select distinct ID, name, gender, age from reservation, audience
        where reservation.performance_id = {performance_id} and
        reservation.audience_id = audience.ID
    '''
    print("--------------------------------------------------------------------------------")
    print_form = '%-10s%-40s%-15s%-20s\n'
    column = print_form % ('id', 'name', 'gender', 'age')
    print(column + "--------------------------------------------------------------------------------")
    audiences = db.select(query)
    table_info = ''
    for i in audiences:
        audience_id = i['ID']
        name = i['name']
        gender = i['gender']
        age = i['age']
        table_info += print_form %(audience_id, name, gender, age)
    print(table_info + "--------------------------------------------------------------------------------\n")

# 좌석 예매 현황을 확인
def print_ticket_booking_status_of_a_performance(db):
    #print("14")
    performance_id = int(input("Performance ID: "))
    if db.select(f'select * from performance where ID = {performance_id}') == []:
        print(f"Performance {performance_id} doesn't exist\n")
        return
    elif db.select(f'select * from assignment where performance_id = {performance_id}') == []:
        print(f"Performance {performance_id} isn't assigned\n")
        return     
    capacity_query = f'''select capacity from building, assignment 
        where assignment.performance_id = {performance_id} 
        and building.ID = assignment.building_id'''
    capacity = db.select(capacity_query)[0]['capacity']
    
    print("--------------------------------------------------------------------------------")
    print_form = '%-50s%-50s\n'
    column = print_form % ('seat_number', 'audience_id')
    print(column + "--------------------------------------------------------------------------------")
    #seats = db.select(query)
    table_info = ''
    for i in range(1, capacity + 1):
        seat_number = i
        #audience_id = i['audience_id']
        audience_query = f''' select audience_id from reservation
            where performance_id = {performance_id} and seat_number = {seat_number}'''
        audience_id = db.select(audience_query)
        #print(audience_id)
        if audience_id == []:
            table_info += print_form %(seat_number, '')
        else:
            table_info += print_form %(seat_number, audience_id[0]['audience_id'])
    print(table_info + "--------------------------------------------------------------------------------\n")

# database를 reset
def reset_database(db):
    #print("16")
    while True:
        delete = input("Delete? (y/n) ")
        if delete == 'y':
            db.reset()
            break
        elif delete == 'n':
            break
    print("")