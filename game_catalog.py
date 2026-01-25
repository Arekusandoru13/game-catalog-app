import json
import psycopg


# Класс "Игра в общем смысле"
class Game:
    def __init__(self, title, platform, release_date, genres):
        # TODO: проверить на пустые значения, выбросить исключение
        # TODO: переделать в свойства
        self.title = title
        self.platform = platform
        self.release_date = release_date
        self.genres = set(genres)


    def info(self):
        return {
            "title": self.title,
            "platform": self.platform,
            "release_date": self.release_date,
            "genres": self.genres
        }
    

    # TODO: Проверки и список допустимых жанров
    def add_genres(self, genres): 
        self.genres = self.genres.union(set(genres))

    def delete_genres(self, genres):
        self.genres = self.genres.difference(set(genres))

    def clear_genres(self):
        self.genres.clear()
    


# TODO: Класс "Игра в каталоге игр", список допустимых статусов, список допустимых жанров и проверки этого
class GameInList(Game):
    def __init__(self, title, platform, release_date, genres, status, comment):
        super().__init__(title, platform, release_date, genres)
        if status:
            self.status = status
        else:
            self.status = "Wishlist"
        self.comment = comment


    def info(self):
        info_dict = super().info()
        info_dict["status"] = self.status
        info_dict["notes"] = self.comment
        return info_dict



# Класс "Каталог игр"
class GameCatalog:
    def __init__(self, connection_string):
        self.__connection_string = connection_string


    def __enter__(self):
        self.connection = psycopg.connect(self.__connection_string)
        print('connection opened')
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print('connection closed')



    # Работа с файлом
    def load_from_file(self, path):
        try:
            with open(path, "r") as file:
                imported_catalog = json.load(file)
                for game_dict in imported_catalog.values():
                    self.add_game(game_dict.get("title"),
                                  game_dict.get("platform"),
                                  game_dict.get("release_date"),
                                  game_dict.get("genres"),
                                  game_dict.get("status"),
                                  game_dict.get("notes"))
        except FileNotFoundError as e:
            raise e
        
    def save_to_file(self, path):
        try:
            with open(path, "w") as file:
                json.dump(self.__game_catalog_serializer(),
                                                file,
                                                indent=2)
        except Exception as e:
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


    # Изменяет id уже имеющейся игры
    def __change_game_id(self, game_id):
        edited_game = self.__game_catalog.pop(game_id)
        new_game_id = GameCatalog.__generate_game_id(edited_game.title, edited_game.platform)
        self.__game_catalog[new_game_id] = edited_game


    def check_game_existence(self, game_id):
        pass


    # Добавляет игру. Возвращает код операции и game_id
    def add_game(self, title, platform, release_date, genres, status="Wishlist", comment=""):
        # Генерируем ID
        new_game_id = GameCatalog.__generate_game_id(title, platform)
        #TODO: надо ли делать выход через исключение?
        # Если игра есть, ошибка
        game_info = self.get_game(new_game_id)
        if game_info:
            return (0, new_game_id)
        # Создаём объект Game и добавляем в каталог
        try:
            new_game = GameInList(title, platform, release_date, genres, status, comment)
        except Exception as e:
            raise e
        query = (t'''
            INSERT INTO game_catalog (game_id, title, platform, release_date, 
                                      genres, status, notes) 
            VALUES ({new_game_id}, {new_game.title}, {new_game.platform}, {new_game.release_date}, 
                    {list(new_game.genres)}, {new_game.status}, {new_game.comment});
               ''')
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
        return (1, new_game_id)


    # Возвращает словарь с данными об игре
    def get_game(self, game_id):
        with self.connection.cursor() as cursor:
            cursor.execute('''
                SELECT title, platform, release_date, genres, status, notes
                FROM game_catalog WHERE game_id=%s;
                ''', 
                (game_id,))
            if cursor.rowcount == 0:
                return None
            title, platform, release_date, genres, status, commentary = cursor.fetchone()
            game = GameInList(title, platform, release_date, genres, status, commentary)
            return game.info()


    # Удаляет игру с указанным ID, возвращает словарь с данными удалённой игры
    def delete_game(self, game_id):
        game_info = self.get_game(game_id)
        if not game_info:
            raise Exception("Нет такой игры.")
        
        query = (t'''
            DELETE FROM game_catalog WHERE game_id={game_id};
               ''')
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

        return game_info


    def update_genres(old_genres_list, genres_operations_dict):
        pass

    # принимает ID игры и словарь с полями для обновления
    # TODO: при обновлении названия и платформы сгенерировать новый ID
    def update_game(self, game_id, new_data):
        edited_game = self.get_game(game_id)
        if not edited_game:
            raise Exception("Нет такой игры.")
        # Собираем подходящие данные, которые нужно обновить
        updates = dict()
        for k in edited_game:
            if k in new_data:
                updates[k] = new_data[k]
        # Если данных для обновления нет или передали косячный new_data - выходим
        if not updates:
            return 0
        # Форматируем список жанров
        if 'genres' in updates:
            updates['genres'] = GameCatalog.update_genres(edited_game['genres'], updates['genres'])
        # Надо обновить game_id?
        need_new_id = False
        if 'title' in updates:
            title = updates['title']
            need_new_id = True
        else:
            title = edited_game["title"]
        if 'platform' in updates:
            platform = updates['platform']
            need_new_id = True
        else:
            platform = edited_game['platform']
        if need_new_id:
            updates['game_id'] = GameCatalog.__generate_game_id(title, platform)
        
        # TODO: собрать в один запрос
        with self.connection.cursor() as cursor:
            for key, value in updates.items():
                cursor.execute(
                    psycopg.sql.SQL(
                        "UPDATE game_catalog SET {}=(%s) WHERE game_id=%s"
                    ).format(psycopg.sql.Identifier(key)), (value, game_id)
            )        
        self.connection.commit()

        if need_new_id: return updates["game_id"]
        else: return game_id


    def get_all_games(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''
                SELECT game_id, title
                FROM game_catalog;
                           ''')
            
            all_games_dict = {}
            for game_id, title in cursor:
                all_games_dict[game_id] = title
        return all_games_dict


    # Свойство для получения полного списка (может быть медленным) (obsolete)
    @property
    def game_catalog(self):
        return self.__game_catalog.copy()

