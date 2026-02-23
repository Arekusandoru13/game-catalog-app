import psycopg
import re
from game_catalog_exc import *


# Класс "Игра в общем смысле"
class Game:
    """
    Класс Game хранит базовую информацию об игре.

    Свойства:
        title (str): название игры
        platform (str): платформа, на которой выходит игра
        release_date (str): дата выхода в формате YYYY.MM.DD или YYYY.qN
        genres (set[str]): список жанров

    Ограничения:
        - длина title ограничена
        - длина platform ограничена
        - длина одного жанра в genres ограничена
        - release_date должна быть в одном из поддерживаемых форматов
        - жанры должны быть из списка допустимых жанров
        - платформа должна быть из списка допустимых платформ
    """

    # ограничения для соответствия ограничениям в БД
    MAX_TITLE_LENGTH = 30
    MAX_GENRE_LENGTH = 15
    DATE_PATTERNS = [
        r"^\d{4}\.\d{2}\.\d{2}$",   # YYYY.MM.DD
        r"^\d{4}\.\d{2}\.xx$",      # YYYY.MM.xx
        r"^\d{4}\.xx\.xx$",         # YYYY.xx.xx
        r"^\d{4}\.q[1-4]$"          # YYYY.q1
    ]
    VALID_GENRES = {
        "action", "platformer", "fighting", "adventure", "shooter",
        "beat 'em up", "shoot 'em up", "survival", "horror", "rpg",
        "online", "metroidvania", "soulslike", "slasher", "visual novel",
        "interactive movie", "puzzle", "quest", "jrpg", "roguelike",
        "simulation", "strategy", "racing", "music", "unique"
    }
    VALID_PLATFORMS = {
        "pc",
        "dendy", "famicom", "master system",
        "mega drive", "super famicom",
        "game boy", "game gear",
        "saturn", "ps1", "nintendo 64",
        "game boy color",
        "dreamcast", "ps2", "gamecube", "xbox",
        "game boy advande",
        "xbox 360", "ps3", "wii",
        "ds", "psp"
        "wii u", "ps4" "xbox one", "switch",
        "3ds", "ps vita"
        "xbox series", "ps5", "switch 2"
    }

    
    def __init__(self, title: str, platform: str, release_date: str, genres: list[str]):
        """
        Создаёт объект Game с базовой информацией об игре.

        Все входные данные проходят базовую валидацию.
        """
        self.title = title
        self.platform = platform
        self.release_date = release_date
        self.add_genres(genres)    # внутри хранится как множество

    
    @property
    def title(self) -> str:
        """Название игры."""
        return self.__title
    @title.setter
    def title(self, title):
        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValueError("Название игры слишком длинное.")
        if not title:
            raise ValueError("Название игры не может быть пустым.")
        self.__title = title
        
    
    @property
    def platform(self) -> str:
        """Платформа выхода игры."""
        return self.__platform
    @platform.setter
    def platform(self, platform):
        if platform not in Game.VALID_PLATFORMS:
            raise ValueError("Недопустимая платформа.")
        self.__platform = platform
        

    @classmethod
    def _is_valid_date(cls, date_str: str) -> bool:
        return any(re.match(p, date_str) for p in cls.DATE_PATTERNS)


    @property
    def release_date(self) -> str:
        """Дата выхода игры."""
        return self.__release_date
    @release_date.setter
    def release_date(self, release_date):
        if self._is_valid_date(release_date):
            self.__release_date = release_date
        else:
            raise ValueError("Неверный формат даты.")


    @property
    def genres(self) -> set[str]:
        """Набор жанров игры."""
        return self.__genres.copy()
        


    def info(self) -> dict:
        """Возвращает данные игры в виде словаря."""
        return {
            "title": self.title,
            "platform": self.platform,
            "release_date": self.release_date,
            "genres": self.genres
        }
    

    def add_genres(self, genres: list[str]) -> set[str]: 
        """
        Добавляет жанры к игре.

        Аргументы:
            genres (list[str]): список жанров для добавления
        """
        
        set_of_genres = set()
        for genre in genres:
            genre = genre.lower()
            if genre in Game.VALID_GENRES:
                set_of_genres.add(genre)
            else:
                raise ValueError(f"Жанр {genre} отсутствует в списке допустимых жанров.")
        self.__genres = set_of_genres
        #self.genres = self.genres.union(set(genres))

        
    #TODO: строгое удаление
    def remove_genres(self, genres: list[str]):
        self.genres = self.genres.difference(set(genres))

    def clear_genres(self):
        self.genres.clear()
    


class GameInList(Game):
    """
    Класс GameInList хранит информацию об игре как объекте каталога игр.

    Наследует базовые данные игры из Game и дополняет их состоянием
    и комментарием.

    Дополнительные свойства:
        status (str): статус игры в каталоге
        comment (str): комментарий к игре

    Ограничения:
        - status может быть только одним из допустимых значений
    """


    VALID_STATUSES = {'wishlist', 'backlog', 'playing', 'paused', 'completed', 'dropped'}

    def __init__(self, title: str, platform: str, release_date: str,
                 genres: list[str], status: str, comment: str):
        """
        Создаёт объект GameInList представляющий игру в каталоге игр
        с актуальными данными. Расширяет конструктор Game новыми свойствами.

        Дополнительное свойство status также проходит валидацию.
        Свойство comment может содержать любой текст.
        """
        super().__init__(title, platform, release_date, genres)
        self.status = status
        self.comment = comment


    @property
    def status(self) -> str:
        """Текущий статус игры в каталоге."""
        return self.__status
    @status.setter
    def status(self, status):
        if status in self.VALID_STATUSES:
            self.__status = status
        else:
            raise ValueError("Недопустимый статус.")
        
    
    @property
    def comment(self) -> str:
        """Комментарий к игре."""
        return self.__comment
    @comment.setter
    def comment(self, comment):
        self.__comment = comment


    def info(self) -> dict:
        """Возвращает данные игры в каталоге в виде словаря."""
        info_dict = super().info()
        info_dict["status"] = self.status
        info_dict["notes"] = self.comment
        return info_dict



# Класс "Каталог игр"
class GameCatalog:
    """
    Класс GameCatalog управляет добавлением и извлечением данных о играх
    из каталога. Позволяет добавить, удалить, прочитать и обновить данные
    об игре в каталоге.
    """
    def __init__(self, connection_string):
        """
        Создаёт объект GameCatalog, принимает строку с параметрами 
        для установки соединения с БД.
        """
        self.__connection_string = connection_string


    def __enter__(self):
        self.connection = psycopg.connect(self.__connection_string)
        print('connection opened')
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print('connection closed')
    

    # Генерируем ID из названия, используя только первую букву, согласные и цифры.
    @staticmethod
    def _generate_game_id(title, platform):
        id = title.lower().lstrip()
        id = id.replace(" ", "")
        id = GameCatalog._delete_vowels_for_id(id + platform.lower())
        return id


    # Удаляет все знаки кроме согласных и цифр из строки.
    @staticmethod
    def _delete_vowels_for_id(id_str):
        new_id = id_str[:1]
        for letter in id_str[1:]:
            if (letter in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                          'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
            or letter.isdigit()):
                new_id = new_id + letter
        return new_id


    def add_game(self, title: str, platform: str, release_date: str, 
                 genres: list[str], status="wishlist", comment="") -> tuple[int, str]:
        """
        Добавляет игру с указанными параметрами в каталог.

        Аргументы:
            title (str): название игры
            platform (str): название платформы
            release_date (str): дата релиза
            genres (list[str]): список жанров игры
            status (str): статус в каталоге, необязательный параметр,
                по умолчанию Wishlist
            comment (str): комментарий к игре, необязательный параметр,
                по умолчанию пустая строка

        Возвращает:
            tuple[int, str] - код операции и id новой игры

        Выбрасывает:
            GameExistsError - если игра с получившимся ID существует
        """

        new_game_id = GameCatalog._generate_game_id(title, platform)
        game_exists = self.get_game(new_game_id)
        if game_exists:
            raise GameExistsError(new_game_id)
        
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


    def get_game(self, game_id: str) -> GameInList | None:
        """
        Извлекает данные игры из каталога по её game_id.

        Возвращает:
            GameInList - если игра найдена
            None - если игра отсутствует
        """
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
            return game


    def delete_game(self, game_id: str) -> dict:
        """
        Удаляет игру с указанным game_id из каталога, возвращает её данные
        в виде словаря.
        """
        game = self.get_game(game_id)
        if not game:
            raise GameNotFoundError(game_id)
        
        query = (t'''
            DELETE FROM game_catalog WHERE game_id={game_id};
               ''')
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

        return game.info()

# TODO: реализовать
    @staticmethod
    def _update_genres(game: GameInList, genres_operations: dict):
        """
        Обновляет жанры у объекта GameInList согласно словарю.
        
        Аргументы:
            game (GameInList): игра, у которой нужно обновить данные
            genres_operations (dict): словарь с данными для обновления,
                может содержать ключи add и remove, внутри которых
                необходимые жанры для добавления и удаления, при наличии ключа
                clear словарь очищается
        """
        if "remove" in genres_operations:
            game.remove_genres(genres_operations["remove"])
        if "clear" in genres_operations:
            game.clear_genres()
        if "add" in genres_operations:
            game.add_genres(genres_operations["add"])



    # TODO: при обновлении названия и платформы сгенерировать новый ID
    # TODO: привести к единообразному виду исключения
    def update_game(self, game_id: str, new_data: dict) -> int|str:
        """
        Обновляет данные игры.

        Аргументы:
            game_id (str): ID игры, данные которой нужно обновить
            new_data (dict): словарь с необходимыми для обновления полями

        Возвращает:
            0 - если данные обновить не удалось
            str - актуальный ID изменяемой игры

        Выбрасывает:
            Exception - если игры с указанным ID нет в каталоге

        TODO: Привести возвращаемое значение к одному виду,
        все ошибки обрабатывать через исключения.
        """
        edited_game = self.get_game(game_id)
        if not edited_game:
            raise GameNotFoundError(game_id)
        edited_game_info = edited_game.info()
        # Собираем подходящие данные, которые нужно обновить
        updates = dict()
        for k in edited_game_info:
            if k in new_data:
                updates[k] = new_data[k]
        # Если данных для обновления нет или передали косячный new_data - выходим
        if not updates:
            return 0
        # Форматируем список жанров
        if 'genres' in updates:
            GameCatalog._update_genres(edited_game, updates['genres'])
            updates['genres'] = list(edited_game.genres)
        # Надо обновить game_id?
        need_new_id = False
        if 'title' in updates:
            title = updates['title']
            need_new_id = True
        else:
            title = edited_game_info["title"]
        if 'platform' in updates:
            platform = updates['platform']
            need_new_id = True
        else:
            platform = edited_game_info['platform']
        if need_new_id:
            updates['game_id'] = GameCatalog._generate_game_id(title, platform)
        
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


    def get_all_games(self) -> dict:
        """
        Получает список всех игр в каталоге в виде словаря
        вида [game_id: title].
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''
                SELECT game_id, title
                FROM game_catalog;
                           ''')
            
            all_games_dict = {}
            for game_id, title in cursor:
                all_games_dict[game_id] = title
        return all_games_dict