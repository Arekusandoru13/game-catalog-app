# Класс "Игра в списке игр"

class Game:
    def __init__(self, title, platform, year, genres):
        self.title = title
        self.platform = platform
        self.year = year
        self.genres = genres


    def info(self):
        return f"Title: {self.title}\nPlatform: {self.platform}\nYear: {self.year}\nGenres: {self.genres}"
    
    # TODO: Обновление и удаление жанров
    def add_genres(self, genres): pass
    def delete_genres(self, genres): pass
    def clear_genres(self): pass
    

class GameCatalog:
    def __init__(self):
        self.__game_catalog = dict()


    # Генерируем ID из названия, используя только первую букву, согласные и цифры.
    def __generate_game_id(game):
        id = game.title.lower().lstrip()
        id = id.replace(" ", "")
        id = GameCatalog.__delete_vowels_for_id(id + game.platform.lower())
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

    def add_game(self, new_game, status, comment = ""):
        new_game_id = GameCatalog.__generate_game_id(new_game)
        # Если игра есть, ошибка, либо можно вернуть кортеж (неуспешная операция, ID игры)
        if new_game_id in self.__game_catalog:
            return f"Ошибка. Игра с ID {new_game_id} уже существует!"
        # Если есть игра с таким же названием и платформой, предложить обновить данные.
        for id, game_in_catalog in enumerate(self.__game_catalog):
            if (game_in_catalog[id][0].title == new_game.title
            and game_in_catalog[id][0].platform == new_game.platform):
                return f'''Найдена игра с таким же названием на этой платформе.
                Используйте update_game, чтобы обновить данные.'''
            
        self.__game_catalog[new_game_id] = [new_game, status, comment]
        return f"Игра {new_game.title} добавлена в каталог с ID {new_game_id}."


    def get_game(self, game_id):
        if game_id not in self.__game_catalog:
            return "Игры с указанным ID нет в каталоге."
        return self.__game_catalog[game_id][0].info()

    def delete_game(self, game_id):
        if game_id not in self.__game_catalog:
            return "Игры с указанным ID нет в каталоге."
        deleted_entry = self.__game_catalog.pop(game_id)
        # Можно вернуть ещё и игру, пока без этого.
        return f"Игра с ID {game_id} удалена."

    # принимает ID игры и словарь с полями для обновления
    # TODO: при обновлении названия и платформы сгенерировать новый ID
    def update_game(self, game_id, new_data):
        if game_id not in self.__game_catalog:
            return "Игры с указанным ID нет в каталоге."
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

