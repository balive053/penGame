import random, time
class penGame:

    def __init__(self):
        self.switch = 0
        self.num_pencils = 0
        self.player_mode = 'Quit'
        # list of bot responces
        self.bot_phrases = [
                'Hmmm....', 
                'Hmm, let\'s see', 
                '*Yawn*', 
                'Is that the best you can do?',
                'My grandmother would have made a better move than that... and she\'s just a kettle...',
                'What shall we do with the drunken sailor, early in the mornin! Got any rum?',
                'Even AI bots get bored, quit while you\'re not that far behind',
                'Have you ever seen an AI bot juggling with one hand while it kicks your ass with the other?'
                ]


    def int_checker(self, input_val, message=''):
        """
        Check is value for starting number of pencils is an int
        input : input_val - player input for number of starting pencils to be checked
                message (optional) - message to return if value is not type int
        output : self.input_val (int) - - return value if it is of class 'int' for use
        """
        try:
            self.input_val = int(input_val)
 
        except:
            self.input_val = input(message)
            self.int_checker(self.input_val, message)
        return int(self.input_val)
    

    def positive_checker(self, input_val, message=''):
        """
        Check if value for starting number of pencils is positive (input_val > 0)
        input : input_val - player input for number of starting pencils to be checked
                message (optional) - message to return if value is not positive
        output : self.input_val (int) - return value if it is positive for use
        """
        if input_val > 0:
            return input_val 
        else:
            self.input_val = input(message)
            self.input_val = self.int_checker(self.input_val, message)
            self.positive_checker(self.input_val, message)
        return self.input_val


    def bot_move(self, num_pencils):
        """
        To make move for The Bot based on optimizing it's chace of winning
        input : num_pencils (int) - number of pencils currently on board
        output : to_remove (int) - optimal amount The Bot has selected to remove
        """
        ## Calculate optimal amount to remove based on condition of board
        ideal = (num_pencils-1) % 4
        # ensure only 1 pencil is taken if only 1 remains on board
        if num_pencils == 1:
            to_remove = 1
        elif ideal == 0:
            return random.randint(1,3)
        elif ideal == 1 or ideal == 2 or ideal == 3:
            to_remove = ideal
        # if no optimal choice is available, make a random move within parametres 
        else:
            to_remove = random.randint(1,3)
        return to_remove
    

    def player_selector(self):
        '''
        To get Player 1 (and Player 2 if multi-player)'s names and decide who will start game
        input : None
        output : choice (String) - Player 1's name
                 other (String) - Player 2 or The Bot's name
        '''
        
        if self.player_mode == 'm' or self.player_mode == 'M':
            self.player_name = input("Enter Player 1's name?\n")
            self.other = input("Enter Player 2's name?\n")
        else:
            self.player_name = input("Please enter your name:\n")
            self.other = 'The Bot'
            
        choice = input(f'Who will go the first, "{self.player_name}" or the "{self.other}"?:\n')
        while (choice != self.player_name) and (choice != self.other):
            choice = input(f"Choose between '{self.player_name}' and '{self.other}'\n")
        other = self.other if choice == self.player_name else self.player_name
        return choice, other


    def player_switcher(self, choice, other):
        '''
        To call correct player based on who's turn it is using a simple switch counter
        input : choice (String) - Player 1's name
                other (String) - Player 2 or The Bot's name
        output : remove (int) - amount of pencils to be removed
        '''
        if choice == self.player_name:
            if (self.switch % 2) == 0:
                remove = input(f"{choice}'s turn:\n") 
            else:
                # call for multiplayer
                if self.player_mode == 'm' or self.player_mode == 'M':
                    remove = input(f"{other}'s turn:\n")
                # call for simgle player
                else:
                    remove = self.bot_move(self.num_pencils)
                    # select a snarky resonse for the bot 
                    print(f"{other}'s turn:")
                    responce_choice = random.randint(0,7)
                    print(self.bot_phrases[responce_choice])
                    time.sleep(1.5)
                print(remove)
        else:
            if (self.switch % 2) == 0:
                # call for multiplayer
                if self.player_mode == 'm' or self.player_mode == 'M':
                    remove = input(f"{other}'s turn:\n")
                # call for simgle player
                else:
                    remove = self.bot_move(self.num_pencils)
                    print(f"{choice}'s turn:")
                    # select a snarky resonse for the bot 
                    responce_choice = random.randint(0,7)
                    print(self.bot_phrases[responce_choice])
                    time.sleep(1.5)
                print(remove)
            else:
                remove = input(f"{other}'s turn:\n")        
        self.switch += 1
        return remove


    def player_value_checker(self, remove):
        '''
        To confirm choice of amount of pencils to pick up is within game limits :
        Values must be between 1:3 and <= total amount of pencils currently on board
        input : remove (int) - amount of pencils to be removed
        output : remove (int) - amount of pencils to be removed
        '''
        int_check = False 
        while int_check == False:
            try:
                remove = int(remove)
                # check between 1-3 pencils are taken per turn
                while (remove > 3 or remove < 1):
                    remove = int(input("Possible values: '1', '2', '3'\n"))
                # check to make sure enough pencils remain on baord
                while (remove > self.num_pencils or remove < 1):
                    remove = int(input("There aren't that many pencils left! Try again:\n"))
                int_check = True
            except:
                remove = input("Possible values: '1', '2', '3'\n")
        return remove
        

    def turn_checker(self, remove, choice, other):
        '''
        To decide if game has ended or if not to change players turn
        input : remove (int) - amount of pencils to be removed
                choice (String) - Player 1's name
                other (String) - Player 2 or The Bot's name
        output : None - ends game or changes player turn
        '''
        self.num_pencils -= remove
        # print winner message if all pencils are removed else print board
        if self.num_pencils == 0:
            if (self.switch % 2) == 0:
                print(f"{choice} won!") 
                self.reset_game()
            else: 
                print(f"{other} won!")
                self.reset_game()
        else:
            print('|'*self.num_pencils, f'  ({self.num_pencils} pencils remain)')

    def reset_game(self):
        '''
        To ask player if they would like a new game or to exit
        input : None
        output : None - main menu is called or game is exited
        '''
        new_game = input('Would you like to play again? (y/n)\n')
        if new_game == 'y' or new_game == 'Y':
            self.switch = 0
            self.main_menu()
        elif new_game == 'n' or new_game == 'N':
            pass
        else:
            print("Please type 'y' for a new game or 'n' to exit\n")
            self.reset_game()

    def run(self):
        '''
        To run main program
        input : None
        output : None - runs program
        '''
        ## Set up game start conditions
        # Get number of pencils to use and check input makes logical sense
        self.num_pencils = input('How many pencils would you like to use:\n') 
        self.num_pencils = self.int_checker(self.num_pencils,
                                message = 'The number of pencils should be numeric\n') 
        self.num_pencils = self.positive_checker(self.num_pencils, 
                                message = 'The number of pencils should be a positive number\n') 
        # Get player names
        player_choice, player_other = self.player_selector()
        print('|'*self.num_pencils)

        # Keep calling functions for player turns until pencils are all gone
        while self.num_pencils > 0:
            to_remove = self.player_switcher(player_choice, player_other)
            to_remove = self.player_value_checker(to_remove)
            self.turn_checker(to_remove, player_choice, player_other)


    def main_menu(self):
        '''
        Calls Main Menu for game to gather game mode (single or multi-player)
        input : None
        output : None
        '''
        print('''
        What kind of game would you like to play? 

        Multi-player against a friend (if you have any!), 
        or Single Player against a snarky AI bot of dubious intelligence?
        (Type "s" for Single or "m" for Multi-player, "r" to see the rules,
        or "Quit" to chicken out and go home while you're still ahead''')
        # Get info from player for game type
        self.player_mode = input()
        if self.player_mode == 'S' or self.player_mode == 's':
            self.run()
        elif self.player_mode == 'M' or self.player_mode == 'm':
            self.player_mode = 'M'
            self.run()
        elif self.player_mode == 'R' or self.player_mode == 'r':
            print("""
            The aim of the game is not to pick up the last pencil.
            The board will have pencils placed on it. You can choose to pick up between 1-3 pencils every turn.
            The player who picks up the last pencil loses.
            """)
            input('Press any key to continue')
            self.main_menu()
        elif self.player_mode == 'Quit':
            pass
        else:
            self.main_menu()
            
# Create and run game
game = penGame()
game.main_menu()