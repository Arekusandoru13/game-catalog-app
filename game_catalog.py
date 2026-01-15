import json

# Класс "Игра в общем смысле"
class Game:
    def __init__(self, title, platform, year, genres):
        # TODO: проверить на пустые значения, выбросить исключение
        # TODO: переделать в свойства
        self.title = title
        self.platform = platform
        self.year = year
        self.genres = set(genres)


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
    def __init__(self, title, platform, year, genres, status, comment):
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


    # Работа с файлом
    def load_from_file(self, path):
        try:
            with open(path, "r") as file:
                imported_catalog = json.load(file)
                for game_dict in imported_catalog.values():
                    self.add_game(game_dict.get("title"),
                                  game_dict.get("platform"),
                                  game_dict.get("year"),
                                  game_dict.get("genres"),
                                  game_dict.get("status"),
                                  game_dict.get("comment"))
        except FileNotFoundError as e:
            raise e
        
    def save_to_file(self, path):
        try:
            with open(path, "w") as file:
                self.__game_catalog = json.dump(self.__game_catalog_serializer(),
                                                file,
                                                indent=2)
        except FileNotFoundError as e:
            raise e
        

    # Преобразуем данные в словари и списки для сохранения в json
    def __game_catalog_serializer(self):
        serialized_dict = {}
        for id, game in self.__game_catalog.items():
            serialized_dict[id] = game.info()
            serialized_dict[id]["genres"] = list(serialized_dict[id]["genres"])
        return serialized_dict
    

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


    # Добавляет игру. Возвращает код операции и game_id
    def add_game(self, title, platform, year, genres, status="Wishlist", comment=""):
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
            raise Exception("Нет такой игры.")
        return self.__game_catalog[game_id].info()


    # Удаляет игру с указанным ID, возвращает удалённую игру
    def delete_game(self, game_id):
        if game_id not in self.__game_catalog:
            raise Exception("Нет такой игры.")
        deleted_game = self.__game_catalog.pop(game_id)
        return deleted_game


    # принимает ID игры и словарь с полями для обновления
    # TODO: при обновлении названия и платформы сгенерировать новый ID
    def update_game(self, game_id, new_data):
        if game_id not in self.__game_catalog:
            raise Exception("Нет такой игры.")
        edited_game = self.__game_catalog[game_id]
        if "title" in new_data:
            edited_game.title = new_data["title"]
        if "platform" in new_data:
            edited_game.platform = new_data["platform"]
        if "year" in new_data:
            edited_game.year = new_data["year"]
        if "genres" in new_data:
            if "add" in new_data["genres"]:
                edited_game.add_genres(new_data["genres"]["add"])
            if "delete" in new_data["genres"]:
                edited_game.delete_genres(new_data["genres"]["delete"])
            if "clear" in new_data["genres"]:
                edited_game.clear_genres()
        if "status" in new_data:
            edited_game.status = new_data["status"]
        if "comment" in new_data:
            edited_game.comment = new_data["comment"]
        return 1



    # Свойство для получения полного списка (может быть медленным)
    @property
    def game_catalog(self):
        return self.__game_catalog.copy()

