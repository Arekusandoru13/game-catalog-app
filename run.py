from game_catalog import *
import shelve

CATALOG_FILENAME = "game_catalog.json"
CONNECTION_STRING = "dbname=gamesdb user=postgres password=postgresPaseu host=localhost"

def add_game_cli(catalog):
    print("Введите данные игры: ")
    title = ''
    while not title:
        title = input("Название: ").strip()
    platform = ''
    while not platform:
        platform = input("Платформа: ").strip().lower()
        if platform not in GameInList.VALID_PLATFORMS:
            print("Данной платформы нет в списке допустимых. " \
            "Укажите корректную платформу.")
            platform = ''
    release_date = ''
    while not release_date:
        release_date = input("Дата выхода: ").strip().lower()
        if not Game._is_valid_date(release_date):
            print("Неверный формат даты. " \
            "Укажите дату в формате yyyy.mm.dd или yyyy.qx.")
            release_date = ''
    genres = []
    while not genres:
        genres_str = input("Укажите жанры через запятую с пробелом:\n").strip().lower()
        genres = genres_str.split(", ")
        for g in genres[:]:
            if g not in GameInList.VALID_GENRES:
                genres = []
                print(f"Жанра {g} нет в списке допустимых жанров. "\
                      "Укажите только допустимые жанры.")
                break
    status = ''
    while not status:
        print("Статус добавленной игры:\n" \
        "1 - Wishlist\n" \
        "2 - Backlog\n" \
        "3 - Playing\n" \
        "4 - Paused\n" \
        "5 - Completed\n" \
        "6 - Dropped")
        selection = input().strip()
        match selection:
            case "1": status = "wishlist"
            case "2": status = "backlog"
            case "3": status = "playing"
            case "4": status = "paused"
            case "5": status = "completed"
            case "6": status = "dropped"
            case _:
                print("О, вы особенный...")
                status = "wishlist"
    notes = input("Комментарий: ")
    try:
        adding_result = catalog.add_game(title, platform, release_date, genres, status, notes)
    except Exception as e:
        print(type(e))
        print(e)
        return
    print(f"\nИгра успешно добавлена с ID {adding_result}")



def get_game_cli(catalog):
    id = input("Введите ID игры: ")
    try:
        game = catalog.get_game(id)
    except Exception as e:
        print(e)
        return
    game_dict = game.info()
    for k, v in game_dict.items():
        print(f"{k.title()}: {v}")
    return id
    

def update_genres_cli():
    match input("1. Добавить жанры\n"
                "2. Удалить жанры\n"
                "3. Очистить жанры\n"):
        case "1": key = "add"
        case "2": key = "remove"
        case "3": return {"clear":''}
        case _: print("Некорректный ввод."); return

    genres_str = input("Укажите жанры через запятую с пробелом:\n").strip().lower()
    genres = genres_str.split(", ")
    return {key: genres}


def update_game_cli(catalog):
    id = get_game_cli(catalog)
    if not id: return

    new_data = {}
    while True:
        selection = input("\nКакие данные нужно обновить?\n"
                          "1. Название\n"
                          "2. Платформа\n"
                          "3. Дата выхода\n"
                          "4. Жанры\n"
                          "5. Статус\n"
                          "6. Комментарий\n"
                          "0. Отменить изменения\n"
                          "+. Применить изменения\n")
        match selection:
            case "1":
                new_data["title"] = input("Введите новое название: ").strip()
            case "2":
                new_data["platform"] = input("Введите новую платформу: ").strip().lower()
            case "3":
                new_data["release_date"] = input("Введите новую дату выхода в формате YYYY.MM.DD: ").strip().lower()
            case "4":
                new_data["genres"] = update_genres_cli()
            case "5":
                new_data["status"] = input("Введите новый статус: ").strip().lower()
            case "6":
                new_data["notes"] = input("Введите новый комментарий:\n")
            case "0": return
            case "+": break
            case _: print ("Некорректный ввод.")

    for k in list(new_data):
        if not new_data[k]: del new_data[k]
    try:
        id = catalog.update_game(id, new_data)
    except Exception as e:
        print(e)
        return
    print(f"Данные игры с ID {id} обновлены.")


def delete_game_cli(catalog):
    id = input("Введите ID игры: ")
    try:
        game_data = catalog.delete_game(id)
    except Exception as e:
        print(e)
        return
    print(f"Игра {game_data.title} удалена из каталога.\n")

def show_all_games(catalog):
    all_games_dict = catalog.get_all_games()
    if not all_games_dict:
        print("Список пуст.")
        return
    print("\nВсе игры в каталоге:")
    for game_id, game_title in all_games_dict.items():
        print(f"{game_id:>30} - {game_title}")


def load_interface(catalog):
    rage = 0
    while True:
        print("\nВыберите действие:\n"
              "1. Добавить игру в каталог.\n"
              "2. Просмотреть игру по ID.\n"
              "3. Обновить данные игры.\n"
              "4. Удалить игру из каталога.\n"
              "5. Отобразить весь каталог.\n"
              "0. Выход из программы.\n")
        selector = input("Ваш выбор: ")
        
        match selector:
            case "1": add_game_cli(catalog)
            case "2": get_game_cli(catalog)
            case "3": update_game_cli(catalog)
            case "4": delete_game_cli(catalog)
            case "5": show_all_games(catalog)
            case "0": break
            case _: 
                rage += 1
                if rage < 10:
                    print("Неподдерживаемый ввод.")
                else:
                    print("НУ ТЫ СМОТРИ ЧЁ ЖМЁШЬ-ТО!")
                continue



def main():
    print("Мой каталог игр.")
    try:
        with shelve.open('settings') as settings:
            connection_str = ('dbname='+settings['dbname']+' '
                              + 'user='+settings['user']+' '
                              + 'password='+settings['password']+' '
                              + 'host='+settings['host'])
    except KeyError as e:
        print(e)
        print('Погоди, не торопись. Запусти setup_db и создай новую бд либо настрой параметры подключения к имеющейся.')
        return
    try:
        with GameCatalog(connection_str) as catalog:
            load_interface(catalog)
    except psycopg.OperationalError as e:
        print(e)
        print("Соединение установить не удалось, обновите данные через setup_db.")
        return
    


    print("Выход из программы.")




if __name__ == "__main__":
    main()