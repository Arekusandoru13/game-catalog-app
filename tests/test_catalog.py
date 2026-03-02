from game_catalog import *

catalog = GameCatalog()
empty_list = catalog.game_catalog

print(empty_list)
# добавляем игру
add_result = catalog.add_game("Stellar Blade", "PS5", "2024", ["Action", "RPG", "Hack&Slash"], "Playing")
print(f"Status: {add_result[0]}\n"
      f"Game_ID: {add_result[1]}")
# если всё ещё пуст, значит возвращает копию
print("Сейчас спрошу переменную ещё раз")
print(empty_list)
print()
# пробуем добавить ту же игру второй раз
add_result = catalog.add_game("Stellar Blade", "PS5", "2024", ["Action", "RPG", "Hack&Slash"], "Playing")
print(f"Status: {add_result[0]}\n"
      f"Game_ID: {add_result[1]}")

# пробуем получить игру
print(catalog.get_game('stllrbldps5'))

# добавляем вторую игру
add_result = catalog.add_game("Stellar Blade 2", "PC", "2028", ["Action", "RPG", "Hack&Slash"])
print(f"Status: {add_result[0]}\n"
      f"Game_ID: {add_result[1]}")

# проверяем весь каталог
print(catalog.game_catalog)

# удаляем игру
print(catalog.delete_game('stllrbldps5'))

# проверяем весь каталог
print(catalog.game_catalog)

# пробуем изменить игру, которой нет
try:
    print(catalog.update_game('fsfa', {}))
except Exception as e:
    print(e)

# пробуем изменить игру, которая есть
new_data = {
    "platform" : "PS5",
    "year" : "2029"
}
catalog.update_game("stllrbld2pc", new_data)
print(catalog.get_game('stllrbld2pc'))
