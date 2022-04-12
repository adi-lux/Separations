from separator import Separator

def main():
    print("Loading...")
    game_state = Separator() # A Separator is the object in which you play games
    print("Welcome to Separations! In this game, you try to bridge the gap between")
    print("the first and last word using progressively more similar words")
    while play_game(game_state) == True:
        game_state.reset()
    print("Thank you for playing!")

def play_game(game : Separator):
    print(f"Start Word: {game.start_word()}")
    print(f"End Word: {game.end_word()}")
    while not game.finished():
        new_guess = input("Guess a word! ")
        game.guess_word(new_guess.strip().lower())
        
        print(f"\n{game}")
     

    again = ""
    while (again != 'y' and again != 'n'):
        again = input("Do you want to play Again? Y/N ").strip().lower()
    if (again == 'y'):
        return True
    else:
        return False

        
    


if __name__ == "__main__":
    main()