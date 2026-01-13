import game_catalog as GC


game1 = GC.Game("Stellar Blade", "PS5", "2024", {"Action", "RPG", "Hack&Slash"})
game2 = GC.Game("Stellar Blade 2", "PC", "2028", {"Action", "RPG"})
catalog = GC.GameCatalog()

print(game1.info())
print(catalog.get_full_list())
print(catalog.add_game(game1, 'Wishlist'))
print(catalog.add_game(game1, 'Playing'))
print(catalog.get_game('stllrbldps5'))
print(catalog.add_game(game2, "Wishlist"))
print(catalog.get_full_list())
print(catalog.delete_game('stllrbldps5'))
print(catalog.get_full_list())
print(catalog.update_game('fsfa', {}))

new_data = {
    "platform" : "PS5",
    "year" : "2029"
}
print(catalog.update_game("stllrbld2pc", new_data))
print(catalog.get_full_list())