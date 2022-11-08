import service.user_serv as user_serv
from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        hint = '''1. create user;
2. get user info by username;
3. update password by username;
q. quit
        '''
        print(hint)
        select = input('input number or "q"\n')
        while not select == 'q':
            if select == '1':
                input_line = input('input username and password:\n')
                username, password = input_line.split(' ')
                user_serv.add_user_with_username_password(username, password)
            if select == '2':
                input_line = input("input username.")
                user = user_serv.get_by_username(input_line)
                print(f'user info:\nusername:\t{user.username}\
                    \npassword:\t{user.password}\npassword salt:\t{user.salt}')
            if select == '3':
                password = ''
                while len(password) < 6:
                    print('length of password should greater than 6.')
                    print('press "Q" for quiting...')
                    if password.upper == 'Q':
                        break
                    input_line = input('input username and password:\n')
                    username, password = input_line.split(' ')
                    user = user_serv.update_password_by_username(username, password)
            if select == 'q':
                break
            select = input(hint)
