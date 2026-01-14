from game_catalog import *

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
        print(f"Игра успешно добавлена с ID {add_result[1]}")
    else:
        print(f"Такая игра уже существует с ID {add_result[1]}")


def get_game_cli(catalog):
    id = input("Введите ID игры: ")
    try:
        game_data = catalog.get_game(id)
    except Exception as e:
        print(e)
        return
    for k, v in game_data.items():
        print(f"{k.title()}: {v}")
    

def main():
    print("Мой каталог игр.")
    catalog = GameCatalog()

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
            case "0": break
            case _: print("Неподдерживаемый ввод."); continue

    print("Выход из программы.")




if __name__ == "__main__":
    main()