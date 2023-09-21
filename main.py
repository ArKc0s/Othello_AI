from interface.game_window import GameWindow

if __name__ == "__main__":
    game = GameWindow()
    mode = game.main_menu()

    if mode:
        game.run(mode)
    else:
        game.quit()