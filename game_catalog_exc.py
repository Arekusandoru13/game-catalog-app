class GameCatalogError(Exception):
    """Базовое исключение для каталога игр."""
    pass

class GameExistsError(GameCatalogError):
    """Игра уже существует в каталоге."""
    def __init__(self, game_id):
        self.game_id = game_id
        super().__init__(f"Игра с game_id {game_id} уже есть в каталоге!")
    


class GameNotFoundError(GameCatalogError):
    """Игра не найдена в каталоге."""
    def __init__(self, game_id):
        self.game_id = game_id
        super().__init__(f"Игра с game_id {game_id} не найдена в каталоге!")
