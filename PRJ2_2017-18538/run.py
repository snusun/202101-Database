from DB import Database
import actions

def menu(): # action들을 출력
    act = {
        1: 'print all buildings',
        2: 'print all performances',
        3: 'print all audiences',
        4: 'insert a new building',
        5: 'remove a buildling',
        6: 'insert a new performance',
        7: 'remove a performance',
        8: 'insert a new audience',
        9: 'remove an audience',
        10: 'assign a performance to a building',
        11: 'book a performance',
        12: 'print all performances which assgned at a building',
        13: 'print all audiences who booked for a performance',
        14: 'print ticket booking status of a performance',
        15: 'exit',
        16: 'reset database'
    }
    menu = '============================================================\n'
    for i in range(1, 17):
        menu += f'{i}. {act[i]}\n'
    menu += '============================================================'
    print(menu)

def select_action(action, db): # 사용자가 입력한 action 번호에 따라 함수 호출
    if action==1:
        actions.print_all_buildings(db)
    elif action==2:
        actions.print_all_performances(db)
    elif action==3:
        actions.print_all_audiences(db)
    elif action==4:
        actions.insert_a_new_building(db)
    elif action==5:
        actions.remove_a_building(db)
    elif action==6:
        actions.insert_a_new_performance(db)
    elif action==7:
        actions.remove_a_performance(db)
    elif action==8:
        actions.insert_a_new_audience(db)
    elif action==9:
        actions.remove_an_audience(db)
    elif action==10:
        actions.assign_a_performance_to_a_building(db)
    elif action==11:
        actions.book_a_performance(db)
    elif action==12:
        actions.print_all_performances_which_assigned_at_a_building(db)
    elif action==13:
        actions.print_all_audiences_who_booked_for_a_performance(db)
    elif action==14:
        actions.print_ticket_booking_status_of_a_performance(db)
    #elif action==15:
    #    actions.exit(db)
    elif action==16:
        actions.reset_database(db)


if __name__ == "__main__":
    db = Database()
    menu()
    while True: # 프로그램이 끝날 때 까지 계속해서 action 입력을 받음
        a = input('Select your action: ')
        if not a.isdigit(): # 숫자 입력이 아닐 경우
            print('Invalid action\n')
            continue
        a = int(a)
        if a==15: # 프로그램 종료
            del db
            print("Bye!")
            break
        if a>=1 and a<=16: # 적절한 입력인 경우
            select_action(a, db)
        else: # 범위를 벗어나는 경우
            print('Invalid action\n')
