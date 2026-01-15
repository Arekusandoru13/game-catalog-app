from game_catalog import *

CATALOG_FILENAME = "game_catalog.json"

def add_game_cli(catalog):
    print("Введите данные игры: ")
    title = input("Название: ")
    platform = input("Платформа: ")
    year = input("Год выхода: ")
    genres = []
    genres_str = input("Укажите жанры через запятую с пробелом:\n")
    genres = genres_str.split(", ")
    status = input("Статус добавленной игры: ")
    comment = input("Комментарий: ")
    add_result = catalog.add_game(title, platform, year, genres, status, comment)
    if add_result[0]:
        print(f"\nИгра успешно добавлена с ID {add_result[1]}")
    else:
        print(f"\nТакая игра уже существует с ID {add_result[1]}")


def get_game_cli(catalog):
    id = input("Введите ID игры: ")
    try:
        game_data = catalog.get_game(id)
    except Exception as e:
        print(e)
        return
    for k, v in game_data.items():
        print(f"{k.title()}: {v}")
    return id
    

def update_genres_cli():
    match input("1. Добавить жанры\n"
                "2. Удалить жанры\n"
                "3. Очистить жанры\n"):
        case "1": key = "add"
        case "2": key = "delete"
        case "3": return "clear"
        case _: print("Некорректный ввод."); return

    genres_str = input("Укажите жанры через запятую с пробелом:\n")
    genres = genres_str.split(", ")
    return {key: genres}


def update_game_cli(catalog):
    id = get_game_cli(catalog)
    if not id: return

    new_data = {}
    while True:
        selection = input("Какие данные нужно обновить?\n"
                          "1. Название\n"
                          "2. Платформа\n"
                          "3. Год выхода\n"
                          "4. Жанры\n"
                          "5. Статус\n"
                          "6. Комментарий\n"
                          "0. Отменить изменения\n"
                          "+. Применить изменения\n")
        match selection:
            case "1":
                new_data["title"] = input("Введите новое название: ")
            case "2":
                new_data["platform"] = input("Введите новую платформу: ")
            case "3":
                new_data["year"] = input("Введите новый год выхода: ")
            case "4":
                new_data["genres"] = update_genres_cli()
            case "5":
                new_data["status"] = input("Введите новый статус: ")
            case "6":
                new_data["comment"] = input("Введите новый комментарий:\n")
            case "0": return
            case "+": break
            case _: print ("Некорректный ввод.")

    for k in list(new_data):
        if not new_data[k]: del new_data[k]
    print(new_data)
    catalog.update_game(id, new_data)
    print("Данные игры обновлены.")


def delete_game_cli(catalog):
    pass


def show_all_games(catalog):
    print(catalog.game_catalog)


def main():
    print("Мой каталог игр.")
    catalog = GameCatalog()
    try:
        catalog.load_from_file(CATALOG_FILENAME)
    except Exception as e:
        print(e)

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
            case _: print("Неподдерживаемый ввод."); continue

    print("Сохранение в файл.")
    try:
        catalog.save_to_file(CATALOG_FILENAME)
    except Exception as e:
        print(e)
    print("Выход из программы.")




if __name__ == "__main__":
    main()