# Класс "Игра в списке игр"

class Game:
    def __init__(self, title, platform, year):
        self.title = title
        self.platform = platform
        self.year = year


    def info(self):
        return f"Title: {self.title}\nPlatform: {self.platform}\nYear: {self.year}"
    

game1 = Game("Stellar Blade", "PS5", "2024")

print(game1.info())