import psycopg
import shelve

def create_db():
    print("Вот это уже серьёзное намерение. Я вижу, что решение принято" \
    " осознанно с полным пониманием дела. Поэтому, надеюсь, дальше не пойдёт " \
    "детских исследований типа 'а что, если нажать сюда'. Иными словами, данные" \
    " принимаются как есть, без проверок и валидаций. Будьте внимательны, " \
    "смотрите, что вводите.")
    dbname = input("Введите название базы данных для вашего каталога игр: ")
    user = input("Имя пользователя: ")
    password = input("Пароль (от СУБД, не от банковского аккаунта," \
    " было бы глупо, если бы они совпадали, правда?): ")
    host = input("Адрес хоста (оставь пустым, если БД на локальном устройстве):")
    if not host:
        host = 'localhost'
    
    connection_string = "user="+user+" password="+password+" host="+host
    print("Вот, что вы указали.")
    print("dbname="+ dbname, connection_string)
    print("Это будет иметь последствия.")

    try:
        conn = psycopg.connect(connection_string)
        cursor = conn.cursor()
        conn.autocommit = True
        query = 'CREATE DATABASE '+dbname
        if 'drop' in query.lower():
            print("НУ ТЫ И ХИТРЕЦ! Я покажу всем твою историю браузера за это!" \
            " (Придётся всё настаривать с начала.)")
        cursor.execute(query)
    except Exception as e:
        print('Ну я же просил...')
        print(e)
        return
    finally:
        cursor.close()
        conn.close()
    print("База данных создана, живите теперь с этим.")

    connection_string = "dbname="+dbname+" "+connection_string
    print(connection_string)
    
    try:
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                conn.autocommit = False
                cursor.execute('''
                    CREATE TYPE status_state as enum ('wishlist', 'backlog', 'playing', 'paused', 'completed', 'dropped');
''')
                cursor.execute('''
                    CREATE TABLE game_catalog (
                        game_id VARCHAR(30) PRIMARY KEY,
                        title VARCHAR(30),
                        platform VARCHAR(15),
                        release_date VARCHAR(10),
                        genres VARCHAR(15)[],
                        status status_state,
                        notes text);
''')
                conn.commit()
            #TODO: переписать функцию создания дб
            m1_execute_sql(conn)
    except Exception as e:
        print(e)
        print("Что-то мне нехорошо...")
        return

    with shelve.open('settings') as file:
        file['dbname'] = dbname
        file['user'] = user
        file['password'] = password
        file['host'] = host
    

def update_settings():
    with shelve.open('settings') as settings:
        while True:
            print("\nУкажите, что вы хотите менять:")
            print('1. Имя БД\n'
                "2. Имя пользователя\n"
                "3. Пароль\n"
                "4. Хост\n"
                "Если ничего из этого, выберите любой другой символ, это не важно.")
            selection = input()
            match selection:
                case "1":
                    settings['dbname'] = input("Введите новое: ")
                case "2":
                    settings['user'] = input("Введите новое: ")
                case "3":
                    settings['password'] = input("Введите новое: ")
                case "4":
                    settings['host'] = input("Введите новое: ")
                case _:
                    print("В таком случае ничего больше не изменить...")
                    return

def delete_db():
    print("Что ж... Это ваше решение, я не могу вас остановить.\n" \
    "Назовите, что конкретно потеряло смысл.")
    dbname = input("БД для удаления: ")
    try:
        with shelve.open('settings') as settings:
            user = settings['user']
            password = settings['password']
            host = settings['host']
    except KeyError as e:
        print(e)
        print("Всё опять не так...")
        return
    except Exception as e:
        print(e)
        print('Что-то мне нехорошо...')
        return
    connection_string = "user="+user+" password="+password+" host="+host
    
    try:
        conn = psycopg.connect(connection_string)
        cursor = conn.cursor()
        conn.autocommit = True
        query = 'DROP DATABASE '+dbname
        cursor.execute(query)
    except Exception as e:
        print(e)
        print("Может ещё не всё потеряно...")
        return
    finally:
        cursor.close()
        conn.close()
    print("Ну, вот и всё.")


def m1_execute_sql(connection):
    try:
        with open("migration1.sql", "r") as file:
            queries_list = file.read().split(";")
        with connection.cursor() as cursor:
            for query in queries_list:
                cursor.execute(query)
            connection.commit()
    except FileNotFoundError as e:
        print(e)
        print("А файл миграции где?")
        return
    except Exception as e:
        print(e)
        print('Создать таблицы не удалось. Опять ничего не получается...')
        return


def m1_done_check(connection):
    with connection.cursor() as cursor:
        cursor.execute('''
SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'migrations')
                       ''')
        table_exists = cursor.fetchone()[0]
        return table_exists



def migration1():
    print("Сейчас всё станет лучше. Или не сейчас. Но, наверно, станет. Может быть (вряд ли).")
    try:
        with shelve.open("settings") as settings:
            connection_str = ('dbname='+settings['dbname']+' '
                            + 'user='+settings['user']+' '
                            + 'password='+settings['password']+' '
                            + 'host='+settings['host'])
    except KeyError as e:
        print("У вас там настройки кривые сохранены...")
        return
    except Exception as e:
        print(e)
        print('Что-то пошло не так...')
        return
    try:
        with psycopg.connect(connection_str) as conn:
            if m1_done_check(conn):
                print('А всё уже.')
                return
            else:
                m1_execute_sql(conn)
    except Exception as e:
        print(e)
        print("Что-то мне нехорошо...")
        return
    print("Шалость удалась. Теперь всё хорошо. Пробуйте жить с этим.")


def load_interface():
    print("Чем вам помочь?\n" \
    "1. Настроить базу данных для работы с каталогом игр.\n" \
    "2. Уточнить текущую конфигурацию.\n" \
    "3. Всё больше не имеет смысла.\n"
    "4. У меня всё стало по-другому и не работает, почини.\n")
    selection = input("На какой вариант вы себя чувствуете?\n")
    match selection:
        case "1": create_db()
        case '2': update_settings()
        case "3": delete_db()
        case "4": migration1()
        case _:
            motivation_msg = '''
Знаю, сейчас даже этот выбор кажется неподъемным. 1 или 2, удалить или сохранить — в голове шум, а пальцы не слушаются. 
Но смотри: прямо сейчас нет неправильной кнопки. Есть только ты и этот момент. Если сядешь и просто выдохнешь, ничего не нажимая — это тоже выбор. Правильный. 
Ты не сломался. Ты просто устал настолько, что мозг решил экономить энергию даже на мелочах. Это нормально. Это пройдет. 
Сделай сейчас то, что легче: отодвинь клавиатуру, закрой глаза или просто смотри в одну точку. Мир не рухнет, база подождет. А ты просто побудь. Этого достаточно.
'''
            print(motivation_msg)




def main():
    print("Этот настройщик поможет вам в помощи нам помогать вам.\n")
    load_interface()
    print("Выход из программы помощи в настройке установки.")




if __name__ == "__main__":
    main()