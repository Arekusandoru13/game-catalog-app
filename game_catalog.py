# Класс "Игра в общем смысле"
class Game:
    def __init__(self, title, platform, year, genres):
        # TODO: проверить на пустые значения, выбросить исключение
        # TODO: переделать в свойства
        self.title = title
        self.platform = platform
        self.year = year
        self.genres = genres


    def info(self):
        return {
            "title": self.title,
            "platform": self.platform,
            "year": self.year,
            "genres": self.genres
        }
    
    # TODO: Обновление и удаление жанров
    def add_genres(self, genres): pass
    def delete_genres(self, genres): pass
    def clear_genres(self): pass
    
# TODO: Класс "Игра в каталоге игр", список допустимых статусов, список допустимых жанров и проверки этого
class GameInList(Game):
    def __init__(self, title, platform, year, genres, status = "Wishlist", comment = ""):
        super().__init__(title, platform, year, genres)
        self.status = status
        self.comment = comment


    def info(self):
        info_dict = super().info()
        info_dict["status"] = self.status
        info_dict["comment"] = self.comment
        return info_dict



# Класс "Каталог игр"
class GameCatalog:
    def __init__(self):
        # Игры хранятся в формате game_id : game_in_list
        self.__game_catalog = dict()


    # Генерируем ID из названия, используя только первую букву, согласные и цифры.
    def __generate_game_id(title, platform):
        id = title.lower().lstrip()
        id = id.replace(" ", "")
        id = GameCatalog.__delete_vowels_for_id(id + platform.lower())
        return id

    # Удаляет все знаки кроме согласных и цифр из строки.
    def __delete_vowels_for_id(id_str):
        new_id = id_str[:1]
        for letter in id_str[1:]:
            if (letter in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                          'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
            or letter.isdigit()):
                new_id = new_id + letter
        return new_id

    # Добавляет игру. Возвращает код операйии и game_id
    def add_game(self, title, platform, year, genres, status, comment):
        # Генерируем ID
        new_game_id = GameCatalog.__generate_game_id(title, platform)
        #TODO: сделать выход через исключение
        # Если игра есть, ошибка
        if new_game_id in self.__game_catalog:
            return (0, new_game_id)
        # Создаём объект Game и добавляем в каталог
        try:
            new_game = GameInList(title, platform, year, genres, status, comment)
        except Exception as e:
            raise e
        self.__game_catalog[new_game_id] = new_game
        return (1, new_game_id)

    # Возвращает список данных игры
    def get_game(self, game_id):
        if game_id not in self.__game_catalog:
            return None
        return self.__game_catalog[game_id].info()

    # Удаляет игру с указанным ID, возвращает удалённую игру
    def delete_game(self, game_id):
        if game_id not in self.__game_catalog:
            return None
        deleted_game = self.__game_catalog.pop(game_id)
        return deleted_game


    # принимает ID игры и словарь с полями для обновления
    # TODO: при обновлении названия и платформы сгенерировать новый ID
    def update_game(self, game_id, new_data):
        if game_id not in self.__game_catalog:
            raise Exception("Нет такой игры.")
        edited_game = self.__game_catalog[game_id]
        if "title" in new_data:
            edited_game[0].title = new_data["title"]
        if "platform" in new_data:
            edited_game[0].platform = new_data["platform"]
        if "year" in new_data:
            edited_game[0].year = new_data["year"]
        if "genres" in new_data:
            if "add" in new_data["genres"]:
                edited_game[0].add_genres(new_data["genres"]["add"])
            if "delete" in new_data["genres"]:
                edited_game[0].delete_genres(new_data["genres"]["delete"])
            if "clear" in new_data["genres"]:
                edited_game[0].clear_genres()
        if "status" in new_data:
            edited_game[1] = new_data["status"]
        if "comment" in new_data:
            edited_game[2] = new_data["comment"]
        return "Данные обновлены."


    def get_full_list(self):
        if not self.__game_catalog:
            return "Каталог пуст."
        # Формируем список отформатированных строк для каждой игры
        '''all_listed_games = [f"{game[0].info()}\n"
                            + "Статус: {game[1]}\n"
                            + "Комментарий: {game[2]}"
                            + "ID: {id}" for id, game in self.__game_catalog.items()]'''
        all_listed_games = list()
        for id, game in self.__game_catalog.items():
            all_listed_games.append(f"{game[0].info()}\n"
            + f"ID: {id}\n"
            + f"Статус: {game[1]}\n"
            + f"Комментарий: {game[2]}\n")
        return "\n".join(all_listed_games)

