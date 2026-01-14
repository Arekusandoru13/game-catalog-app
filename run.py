import game_catalog as g_cat

def add_game_cli():
    print("Введите данные игры: ")
    title = input("Название: ")
    platform = input("Платформа: ")
    year = input("Год выхода: ")
    genres = []
    genres_str = input("Укажите жанры через запятую с пробелом:\n")
    genres = genres_str.split(", ")
    status = input("Статус добавленной игры: ")
    comment = input("Комментарий: ")




def main():
    print("Мой каталог игр.")
    catalog = g_cat.GameCatalog()

    while True:
        print("Выберите действие:\n"
              "1. Добавить игру в каталог.\n"
              "2. Просмотреть игру.\n"
              "3. Обновить данные игры.\n"
              "4. Удалить игру из каталога.\n"
              "5. Отобразить весь каталог.\n"
              "0. Выход из программы.\n")
        selector = input("Ваш выбор: ")

        match selector:
            case "1": add_game_cli()
            case "0": break
            case _: print("Неподдерживаемый ввод."); continue

    print("Выход из программы.")




if __name__ == "__main__":
    main()