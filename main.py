import json
import hashlib

FILE_DATA = 'db.json'

def load_data(name_file):
    try:
        with open(name_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}, "transactions": {}}

def save_data(name_file, data):
    with open(name_file, 'w') as file:
        json.dump(data, file, indent=4)

db = load_data(FILE_DATA)
current_user = None
 
def login_required(func):
    def wrapper(*args, **kwargs):
        if current_user == None:
            print('Вам треба увійти у систему, щоб зробити цю дію')
            return
        else:
            result = func(*args, **kwargs)
        return result

    return wrapper

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    print("---Створення нового користувача---")
    login = input('Введіть логін: ')

    if login in db['users']:
        print('Користувач з таким логіном вже існує')
        return

    password = input('Введіть пароль: ')

    db['users'][login] = {
        "password": hash_password(password),
        "budget": 0
    }

    db['transactions'][login] = []
    save_data(FILE_DATA, db)
    print('Реєстрація пройшла успішно!')

def login():
    print("---Вхід в аккаунт---")
    login = input('Введіть логін: ')
    password = input('Введіть пароль: ')

    global current_user

    if login in db['users']:
        password = hash_password(password)
        if password in db['users'][login][password]:
            current_user = login
            print('Ласкаво просимо!')
            return

    print('Невірний логін або пароль')

def get_valid_amount():
    try:
        amount = int(input('Введіть суму, яку хочете витратити: '))
        amount = float(amount)

        if amount <= 0:
            print('Сума повинна бути додатньою')
            return get_valid_amount()

        return amount
    except ValueError:
        print('Некоректна сума коштів')
        return get_valid_amount()



@login_required
def create_transaction():
    print("---Створення нової транзакції---")
    amount = get_valid_amount()
    category = input('Введіть категорію, на яку хочете витратити суму: ')

    t = {
        "amount": amount,
        "category": category
    }

    db["transactions"][current_user].append(t)
    save_data(FILE_DATA, db)
    print('Транзакція пройшла успішно')
