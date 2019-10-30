#!/usr/bin/env python3

import sys, os, subprocess, time
from random import *
from threading import Event, Thread
from pynput import keyboard
from os.path import exists
from contextlib import redirect_stdout

class Settings(object):
    def __init__(self):
        self.VERBOSE = False
        self.resolution = 3
        self.pieces = 5
        self.border_size = 10
        self.beings = [
                "Human",
                "Human"
                ]
        self.computers = [
                "Zombie",
                "Zombie"
                ]
        self.names = [
                "Player 1",
                "Player 2"
                ]
        self.colors = [
                1,
                4
                ]
        self.hilights = [
                9,
                6
                ]
        self.standart_exits = True
        self.moves = [
                "Up",
                "Down",
                "Left",
                "Right"
                ]
        self.dist_to_center = int(subprocess.run(['tput', 'cols'],
            stdout=subprocess.PIPE).stdout.decode('utf-8')) 
        self.dist_to_center -= 2*(self.border_size+2)*self.resolution  
        self.dist_to_center = int(self.dist_to_center/2)
        self.win_size = int(subprocess.run(['tput', 'cols'],
            stdout=subprocess.PIPE).stdout.decode('utf-8')) 
        self.exit_type = "Broadside"    # Implemented options are:
        #self.exit_type = "Pieces"    # Implemented options are:
                                     # 1) Pieces
                                     # 2) Broadside
        self.Welcome_Text_Files = [
                "welcome_screen_90.txt"
                ]
        self.win_files = [
                "vict_screen.txt",
                "draw.txt"
                ]
        self.Welcome_Sizes = [
                90
                ]
        self.matches = 1
        self.wins = [
                0,
                0
                ]

global settings
settings = Settings()

class Rules(object):
    def __init__(self):
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        self.exits_in_1 = True
        self.exits_in_2 = True
        self.capture = False #[WIP]
        self.explode = False #[WIP]

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def Show_Header():
    if exists(settings.Welcome_Text_Files[0]):
        os.system("clear")
        print("\n" * 2)
        file = open(settings.Welcome_Text_Files[0])
        lines = file_len(settings.Welcome_Text_Files[0])
        for line in range(lines):    
            print(" " * (int((settings.win_size-settings.Welcome_Sizes[0])/2)), end = '')
            print("\033[38;5;%d;1m%s\033[0m" %(39, file.readline()), end='')
        print("\n" * 2)

class Menu_control(object):
    def __init__(self):
        self.hilighted = 0
        self.play = False
        self.options = []
        self.action = None
        self.discart_entering = True
        self.refresh_event = Event()
        self.refresh_completed = Event()

global menu_control
menu_control = Menu_control()

def Show_menu( ):
    while not menu_control.action:
        menu_control.refresh_event.wait()
        menu_control.refresh_completed.set()
        
        os.system("clear")
        Show_Header()
        for i in range(len(menu_control.options)):
            if i == menu_control.hilighted:
                print("> \033[92m%s\033[0m" %menu_control.options[i])
            else:
                print("%s" %menu_control.options[i])

        menu_control.refresh_completed.clear()
        menu_control.refresh_event.clear()

def on_press_menu(key):
    try:
        if key.char == "w" or key.char == "W":
            if menu_control.hilighted == 0 :
                menu_control.hilighted = (len(menu_control.options)-1)
            else:
                menu_control.hilighted -= 1
        elif key.char == "s" or key.char == "S":
            if menu_control.hilighted == (len(menu_control.options)-1):
                menu_control.hilighted = 0
            else:
                menu_control.hilighted +=1
        elif key.char == "d" or key.char == "D":
            pass
        elif key.char == "a" or key.char == "A":
            pass
        else:
            pass
    except AttributeError:
        if key == keyboard.Key.up:
            if menu_control.hilighted == 0 :
                menu_control.hilighted = (len(menu_control.options)-1)
            else:
                menu_control.hilighted -= 1
        elif key == keyboard.Key.down:
            if menu_control.hilighted == (len(menu_control.options)-1):
                menu_control.hilighted = 0
            else:
                menu_control.hilighted +=1
        elif key == keyboard.Key.right:
            pass
        elif key == keyboard.Key.left:
            pass
        else:
            pass
    menu_control.refresh_event.set()
    menu_control.refresh_completed.wait()

def on_release_menu(key):
    if key == keyboard.Key.esc:
        exit(0)
    if key == keyboard.Key.enter:
        menu_control.refresh_event.set()
        if menu_control.discart_entering:
            menu_control.discart_entering = False
        else:
            menu_control.refresh_event.set()
            menu_control.action = True
            return False
    menu_control.refresh_event.set()
    menu_control.refresh_completed.wait()

# Collect events until released
def begin_listener_menu():
    menu_control.refresh_event.set()
    menu_control.refresh_completed.wait()
    if not menu_control.action:
        with keyboard.Listener(
                on_press=on_press_menu,
                on_release=on_release_menu) as listener:
            listener.join()
        #input()

threads = []
while not menu_control.play:
    menu_control.hilighted = 0
    menu_control.options = [
            "Player vs. Player",
            "Player vs. Zombie",
            "Player vs. Berzerker",
            "Computer vs. Computer",
            "Settings",
            "Configure Rules"
            ]

    threads.append(Thread(target=Show_menu))
    threads[-1].start()
    menu_control.refresh_event.set()
    threads.append(Thread(target=begin_listener_menu))
    threads[-1].start()
    for thread in threads:
        thread.join()
    input()
    del threads[:]
    menu_control.action = None
    menu_control.discart_entering = True

    if menu_control.options[menu_control.hilighted] == "Player vs. Player":
        menu_control.play = True
        settings.beings[0] = "Human"
        settings.beings[1] = "Human"
    elif menu_control.options[menu_control.hilighted] == "Player vs. Zombie":
        menu_control.play = True
        settings.beings[0] = "Human"
        settings.beings[1] = "Zombie"
        settings.names[1] = "Zombie"
    elif menu_control.options[menu_control.hilighted] == "Player vs. Berzerker":
        menu_control.play = True
        settings.beings[0] = "Human"
        settings.beings[1] = "Berzerker"
        settings.names[1] = "Berzerker"
    elif menu_control.options[menu_control.hilighted] == "Computer vs. Computer":
        menu_control.play = True
        for i in range(2):
            valid_opt = False
            while not valid_opt:
                Show_Header()
                print("Select the level of player %d:" %i)
                print("1) Zombie")
                print("2) Berserker")
                ans = input("> ")
                if ans == "1":
                    valid_opt = True
                    settings.beings[i]="Zombie"
                    settings.names[i]="Zombie"
                elif ans == "2":
                    valid_opt = True
                    settings.beings[i]="Berzerker"
                    settings.names[i] = "Berzerker"
                else:
                    print("Invalid option")

        valid_opt = False
        while not valid_opt:
            print("How many games they will be forced to play?")
            ans = (input("> "))
            try:
                settings.matches = int(ans)
                valid_opt = True
            except:
                print("Thats not a number >:c (The machine seems disapointed with you)")
    elif menu_control.options[menu_control.hilighted] == "Settings":
        Show_Header()
        valid_opt = False
        while not valid_opt:
            Show_Header()
            print("1) Display size")
            print("2) Player 1 Name")
            print("3) Player 2 Name")
            print("4) Player 1 color")
            print("5) Player 2 color")
            print("6) Quit")
            ans = input("> ")
            if ans == "1":
                valid_opt2 = False
                while not valid_opt2:
                    print("Type in the desired display size: ( current value: {} )".format(settings.resolution) )
                    ans2 = input("> ")
                    try:
                        settings.resolution = int(ans2)
                        valid_opt2 = True
                        valid_opt = True
                    except:
                        print("Thats not a number >:c (The machine seems disapointed with you)")
            elif ans == "2" or ans == "3":
                print("Type in the new name for player {}: ( current name: {} )".format(int(ans)-1, settings.names[int(ans)-2]) )
                ans2 = input("> ")
                settings.names[int(ans)-2] = ans2
                valid_opt = True
            elif ans == "4" or ans == "5":
                valid_opt2 = False
                while not valid_opt2:
                    print("Type in the new color for player {}:".format(int(ans)-3) )
                    for i in range(10):
                        print( "\033[38;5;{0}m{0} \033[0m".format(i), end='')
                    print("\n")
                    ans2 = input("> ")
                    try:
                        settings.colors[int(ans)-4] = int(ans2)
                        valid_opt2 = True
                        valid_opt = True
                    except:
                        print("Thats not a number >:c (The machine seems disapointed with you)")
            elif ans == "6":
                valid_opt = True
            else:
                print("Invalid option")
    elif menu_control.options[menu_control.hilighted] == "Configure Rules":
        Show_Header()
        valid_opt = False
        while not valid_opt:
            print("1) Invert exits")
            ans2 = input("> ")
            if ans2 == "1":
                try:
                    settings.standart_exits = not settings.standart_exits
                    valid_opt = True
                except:
                    settings.standart_exits = True
                    valid_opt = True
            else:
                print("Invalid option")
    else:
        Show_Header()
        print("\033[91mHow this is even possible?\033[0m")
        exit(1)

    del menu_control.options[:]

    menu_control.action = None
    menu_control.discart_entering = False
    
class Piece(object):
    def __init__(self, color, hilight, name, position):
        self.color = color  #Recomended values: 1 to 6
        self.hilighted_color = hilight
        self.symbol = name
        self.position = position
        self.alive = True
        self.bold = True
        self.hilighted = False
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class No_Piece(object):
    pass

class Player(object):
    def __init__(self):
        self.name = "Player"
        self.Pieces = [None] * settings.pieces
        self.rules = Rules()
        self.color = 1

class Human(Player):
    def __init__(self, name, color):
        super(Human, self).__init__()
        self.name = name
        self.color = color

class Zombie(Player):
    def __init__(self, name, color):
        super(Zombie, self).__init__()
        self.name = name
        self.color = color
        self.Zombie_Moves = []
        self.Zombie_Pieces = []
        self.Zombie_delay = 0.03

class Berzerker(Player):
    def __init__(self, name, color):
        super(Berzerker, self).__init__()
        self.name = name
        self.color = color
        self.good_move = None
        self.Berzerker_Moves = []
        self.Berzerker_Pieces = []
        self.Berzerker_Good_Pieces = []
        self.Berzerker_delay = 0.03

class Square(object):
    def __init__(self):
        self.color = 0
        self.symbol = "  "
        self.bold = False
        self.occupiable = False
        self.occupied = False
        self.occupant = No_Piece()

class Quinine(Square):
    def __init__(self):
        super(Quinine, self).__init__()
        self.color = 0

class Border(Square):
    def __init__(self):
        super(Border, self).__init__()
        self.color = 0

class Start1(Square):
    def __init__(self):
        super(Start1, self).__init__()
        self.color = 0

class Start2(Square):
    def __init__(self):
        super(Start2, self).__init__()
        self.color = 0

class Exit1(Square):
    def __init__(self):
        super(Exit1, self).__init__()
        self.color = 0
        if settings.standart_exits:
            self.symbol = "\033[38;5;%d;1m >\033[0m" %(settings.colors[0])
        else: 
            self.symbol = "\033[38;5;%d;1m >\033[0m" %(settings.colors[1])
 
        self.occupiable = True

class Exit2(Square):
    def __init__(self):
        super(Exit2, self).__init__()
        self.color = 0
        if settings.standart_exits:
            self.symbol = "\033[38;5;%d;1m >\033[0m" %(settings.colors[1])
        else: 
            self.symbol = "\033[38;5;%d;1m >\033[0m" %(settings.colors[0])
        self.occupiable = True

class Empty_Odd(Square):
    def __init__(self):
        super(Empty_Odd, self).__init__()
        self.color = 240
        self.occupiable = True

class Empty_Even(Square):
    def __init__(self):
        super(Empty_Even, self).__init__()
        self.color = 250
        self.occupiable = True

class Board(object):
    def __init__(self):
        self.side = settings.border_size+2
        self.pieces = settings.pieces
        self.leftover = settings.border_size - self.pieces
        self.size = self.side**2

        self.Quinines = [
                0,
                self.side-1,
                self.side**2-self.side,
                self.side**2-1
                ]

        self.Starts1 = []
        for i in range(
                self.Quinines[0]+(self.leftover+1),
                self.Quinines[1]
                ):
            self.Starts1.append(i)

        self.Starts2 = []
        for i in range(
                self.Quinines[0]+(self.leftover+1)*self.side,
                self.Quinines[2],
                self.side
                ):
            self.Starts2.append(i)

        self.Exits1 = []
        if settings.exit_type == "Broadside":
            for i in range(
                    self.Quinines[2]+1,
                    self.Quinines[3]
                    ):
                self.Exits1.append(i)
        elif settings.exit_type == "Pieces":
            for i in range(
                    self.Quinines[2]+(self.leftover+1),
                    self.Quinines[3]
                    ):
                self.Exits1.append(i)

        self.Exits2 = []
        if settings.exit_type == "Broadside":
            for i in range(self.Quinines[1]+self.side,
                    self.Quinines[3],
                    self.side
                    ):
                self.Exits2.append(i)
        elif settings.exit_type == "Pieces":
            for i in range(self.Quinines[1]+(self.leftover+1)*self.side,
                    self.Quinines[3],
                    self.side
                    ):
                self.Exits2.append(i)


        self.Leftovers = []
        # From Starting Positions
        for i in range(
                self.Quinines[0]+1,
                self.Quinines[0]+1+self.leftover
                ):
            self.Leftovers.append(i)
        for i in range(
                self.Quinines[0],
                self.Quinines[0]+(self.leftover+1)*self.side,
                self.side
                ):
            self.Leftovers.append(i)
        # From Exits
        if settings.exit_type == "Pieces":
            for i in range(
                    self.Quinines[2]+1,
                    self.Quinines[2]+1+self.leftover,
                    ):
                self.Leftovers.append(i)

            for i in range(
                    self.Quinines[1], 
                    self.Quinines[1]+(self.leftover+1)*self.side,
                    self.side
                    ):
                self.Leftovers.append(i)
        elif settings.exit_type == "Broadside":
            pass
        else:
            pass

        self.Squares = [None] * self.size

        invert = 0
        for i in range(self.size):
            if (i+1) % (self.side) and not self.size % 2 :
                invert+=1
            if i in self.Quinines:
                self.Squares[i]=Quinine()
            elif i in self.Starts1:
                self.Squares[i]=Start1()
            elif i in self.Starts2:
                self.Squares[i]=Start2()
            elif i in self.Exits1:
                self.Squares[i]=Exit1()
            elif i in self.Exits2:
                self.Squares[i]=Exit2()
            elif i in self.Leftovers:
                self.Squares[i]=Border()
            else :
                if not self.size % 2:
                    if (i+invert) % 2:
                        self.Squares[i]=Empty_Even()
                        if (i+1) % (self.side):
                            invert+=1
                    else :
                        self.Squares[i]=Empty_Odd()
                        if (i+1) % (self.side):
                            invert+=1
                else:
                    if i % 2:
                        self.Squares[i]=Empty_Even()
                    else :
                        self.Squares[i]=Empty_Odd()

def Show_Board( board ):
    if type(board) is not Board:
        print("Tried to print object that is no a board")
    centering_distance = int( (settings.win_size - len( "%s vs. %s" %(settings.names[0], settings.names[1])) )/2 )
    os.system("clear")
    print("-" * settings.win_size)
    print("\n" * 2)
    print(" " * centering_distance, end='')
    print("\033[38;5;%d;1m%s\033[0m vs. \033[38;5;%d;1m%s\033[0m "
            %(settings.colors[0], settings.names[0],
                settings.colors[1], settings.names[1])
            )
    print("\n" * 2)
    print("-" * settings.win_size)
    print("\n" * 2)
    for line in range(0 , board.size, board.side):
        for y in range(settings.resolution):
            print(" " * settings.dist_to_center, end='')
            for col in range(board.side):
                for x in range(settings.resolution):
                    if x == y and x == int((settings.resolution)/2): #Symbol condition
                        if board.Squares[line+col].occupied and board.Squares[line+col].occupant.alive: 
                            if board.Squares[line+col].occupant.hilighted:
                                print("\033[48;5;%d;1m%s\033[0m" 
                                    %(board.Squares[line+col].occupant.hilighted_color,
                                        board.Squares[line+col].occupant.symbol),
                                    end='' )
                            else:
                                print("\033[48;5;%d;1m%s\033[0m" 
                                    %(board.Squares[line+col].occupant.color,
                                        board.Squares[line+col].occupant.symbol),
                                    end='' )
                        else:
                            if board.Squares[line+col].color:
                                print("\033[48;5;%d;1m%s\033[0m"
                                        %(board.Squares[line+col].color,
                                            board.Squares[line+col].symbol),
                                        end='' )
                            else:
                                print("\033[1m%s\033[0m"
                                        %(board.Squares[line+col].symbol),
                                        end='' )
                    else: #Same thing without the symbol
                        # Its worth to mention: Since the size of the name of the pieces
                        # is 2 char long, there should be 2 spaces. If the code were to
                        # support an arbitrary piece name, changes should be made here and
                        # in the very definitions of the symbols to adapt the number of white
                        # spaces in every case dinamicly. This will be inplemented in the very end
                        # of the development
                        if board.Squares[line+col].occupied and board.Squares[line+col].occupant.alive:
                            if board.Squares[line+col].occupant.hilighted:
                                print("\033[48;5;%dm  \033[0m" 
                                        %(board.Squares[line+col].occupant.hilighted_color),
                                        end='' )
                            else:
                                print("\033[48;5;%dm  \033[0m" 
                                        %(board.Squares[line+col].occupant.color),
                                        end='' )
                        else:
                            if board.Squares[line+col].color:
                                print("\033[48;5;%dm  \033[0m"
                                        %(board.Squares[line+col].color),
                                        end='' )
                            else:
                                print("\033[0m  \033[0m", end='' )
            print()
    print()
 
class Selection_control(object):
    def __init__(self):
        self.hovered = 0
        self.Available_Pieces = []
        self.action = None
        self.discart_entering = False
        self.refresh_event = Event()
        self.refresh_completed = Event()

global selection_control
selection_control = Selection_control()

def Show_selection( board, player ):
    if type(board) is not Board:
        print("Tried to print object that is no a board")
    while not selection_control.action:
        selection_control.refresh_event.wait()
        selection_control.refresh_completed.set()
        
        Show_Board( board )

        print("Its \033[38;5;%d;1m%s\033[0m turn. Please select a piece"
                %(player.color, player.name)
                )
        selection_control.refresh_completed.clear()
        selection_control.refresh_event.clear()

# Selection Keyboard control
def on_press_selection(key):
    try:
        if key.char == "w" or key.char == "W":
            pass
        elif key.char == "s" or key.char == "S":
            pass
        elif key.char == "d" or key.char == "D":
            selection_control.Available_Pieces[selection_control.hovered].hilighted = False
            if selection_control.hovered == 0 :
                selection_control.hovered = (len(selection_control.Available_Pieces)-1)
            else:
                selection_control.hovered -= 1
            selection_control.Available_Pieces[selection_control.hovered].hilighted = True
        elif key.char == "a" or key.char == "A":
            selection_control.Available_Pieces[selection_control.hovered].hilighted = False
            if selection_control.hovered == (len(selection_control.Available_Pieces)-1):
                selection_control.hovered = 0
            else:
                selection_control.hovered +=1
            selection_control.Available_Pieces[selection_control.hovered].hilighted = True
        else:
            pass
    except AttributeError:
        if key == keyboard.Key.up:
            pass
        elif key == keyboard.Key.down:
            pass
        elif key == keyboard.Key.right:
            selection_control.Available_Pieces[selection_control.hovered].hilighted = False
            if selection_control.hovered == (len(selection_control.Available_Pieces)-1):
                selection_control.hovered = 0
            else:
                selection_control.hovered += 1
            selection_control.Available_Pieces[selection_control.hovered].hilighted = True 
        elif key == keyboard.Key.left:
            selection_control.Available_Pieces[selection_control.hovered].hilighted = False
            if selection_control.hovered == 0 :
                selection_control.hovered = (len(selection_control.Available_Pieces)-1)
            else:
                selection_control.hovered -= 1
            selection_control.Available_Pieces[selection_control.hovered].hilighted = True
        else:
            pass
    selection_control.refresh_event.set()
    selection_control.refresh_completed.wait()

def on_release_selection(key):
    if key == keyboard.Key.esc:
        exit(0)
    if key == keyboard.Key.enter:
        selection_control.refresh_event.set()
        if selection_control.discart_entering:
            selection_control.discart_entering = False
        else:
            selection_control.refresh_event.set()
            selection_control.action = True
            return False
    selection_control.refresh_event.set()
    selection_control.refresh_completed.wait()

# Collect events until released
def begin_listener_selection():
    selection_control.refresh_event.set()
    selection_control.refresh_completed.wait()
    if not selection_control.action:
        with keyboard.Listener(
                on_press=on_press_selection,
                on_release=on_release_selection) as listener:
            listener.join()
        #input()

class Movement_control(object):
    def __init__(self):
        self.Available_Moves = []
        self.action = None
        self.move = None
        self.refresh_event = Event()
        self.refresh_completed = Event()

global movement_control
movement_control = Movement_control()

#movement_control.refresh_event = Event()
def Show_movement( board ):
    if type(board) is not Board:
        print("Tried to print object that is no a board")
        return 1
    while not movement_control.action:
        movement_control.refresh_event.wait()
        movement_control.refresh_completed.set()

        Show_Board( board )

        print("Select the direction to move the piece")
        movement_control.refresh_completed.clear()
        movement_control.refresh_event.clear()

# Movement keyboard control
def on_press_movement(key):
    try:
        if key.char == "w" or key.char == "W":
            if "Up" in movement_control.Available_Moves:
                movement_control.move = "Up"
        elif key.char == "s" or key.char == "S":
            if "Down" in movement_control.Available_Moves:
                movement_control.move = "Down"
        elif key.char == "d" or key.char == "D":
            if "Right" in movement_control.Available_Moves:
                movement_control.move = "Right"
        elif key.char == "a" or key.char == "A":
            if "Left" in movement_control.Available_Moves:
                movement_control.move = "Left"
        else:
            pass
    except AttributeError:
        if key == keyboard.Key.up:
            if "Up" in movement_control.Available_Moves:
                movement_control.move = "Up"
        elif key == keyboard.Key.down:
            if "Down" in movement_control.Available_Moves:
                movement_control.move = "Down"
        elif key == keyboard.Key.right:
            if "Right" in movement_control.Available_Moves:
                movement_control.move = "Right"
        elif key == keyboard.Key.left:
            if "Left" in movement_control.Available_Moves:
                movement_control.move = "Left" 
        else:
            pass
    movement_control.refresh_event.set()
    movement_control.refresh_completed.wait()

def on_release_movement(key):
    movement_control.refresh_event.set()
    if key == keyboard.Key.esc:
        exit(0)
    if movement_control.move:
        movement_control.refresh_event.set()
        selection_control.Available_Pieces[selection_control.hovered].hilighted = False
        movement_control.action = True
        return False
    else:
        pass
    movement_control.refresh_event.set()
    movement_control.refresh_completed.wait()

# Collect events until released
def begin_listener_movement():
    movement_control.refresh_event.set()
    movement_control.refresh_completed.wait()
    if not movement_control.action:
        with keyboard.Listener(
                on_press=on_press_movement,
                on_release=on_release_movement) as listener:
            listener.join()
        #input()

class Movements(object):
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def Test_Move(self, piece, option):
        location = self.player.Pieces[piece].position

        if option == "Up":
            location_new = location - settings.border_size - 2
            if location in range(self.board.Quinines[0], self.board.Quinines[1]+1):
                return False
            if self.player.rules.up == False:
                return False

        elif option == "Down":
            location_new = location+settings.border_size + 2
            if location in range(self.board.Quinines[2], self.board.Quinines[3]+1):
                return False
            if self.player.rules.down == False:
                return False

        elif option == "Left":
            location_new = location - 1
            if location == 0:
                return False
            if self.player.rules.left == False:
                return False

        elif option == "Right":
            location_new = location + 1
            if location == (self.board.size-1):
                return False
            if self.player.rules.right == False:
                return False
        else:
            return False

        if self.board.Squares[location_new].occupiable == False:
            return False
        elif self.board.Squares[location_new].occupied:
            return False
        elif self.player.rules.exits_in_1 and location_new in self.board.Exits2:
            return False
        elif self.player.rules.exits_in_2 and location_new in self.board.Exits1:
            return False
        else:
            return True

    def Move(self, piece, option):
        location = self.player.Pieces[piece].position
        if option == "Up":
            location_new = location - settings.border_size - 2
        elif option == "Down": 
            location_new = location + settings.border_size + 2
        elif option == "Left":
            location_new = location - 1
        elif option == "Right":
            location_new = location + 1
        else:
            print("Invalid option")
            location_new=location
 
        self.board.Squares[location].occupied = False
        self.board.Squares[location].occupant = No_Piece()

        self.player.Pieces[piece].position = location_new

        self.board.Squares[location_new].occupied = True
        self.board.Squares[location_new].occupant = self.player.Pieces[piece]

        if location_new in self.board.Exits1+self.board.Exits2:
            self.board.Squares[location_new].occupied = False
            self.board.Squares[location_new].occupant = No_Piece()

            self.player.Pieces[piece].alive = False

def Turn_Victory_Screen(player):
        print("\033[38;5;%d;1m%s\033[0m wins the game! Congratulations!"
                %(player.color, player.name)
                )

def Victory_Screen():
    result = 0 # 0 if there is a winner, 1 if draw
    winner_color = 0
    if settings.wins[0] > settings.wins[1]:
        winner_color = settings.colors[0]
        message = "\033[38;5;%d;1m%s\033[0m wins the game! \033[38;5;%d;1m%s\033[0m looks sad :c Final score: \033[38;5;%d;1m%d\033[0m \033[38;5;%d;1m%d\033[0m" %(settings.colors[0], settings.names[0], settings.colors[1], settings.names[1], settings.colors[0], settings.wins[0], settings.colors[1], settings.wins[1] )
        result = 0
    elif settings.wins[1] > settings.wins[0]:
        winner_color = settings.colors[1]
        message = "\033[38;5;%d;1m%s\033[0m wins the game! \033[38;5;%d;1m%s\033[0m looks sad :c Final score: \033[38;5;%d;1m%d\033[0m \033[38;5;%d;1m%d\033[0m" %(settings.colors[1], settings.names[1], settings.colors[0], settings.names[0], settings.colors[0], settings.wins[0], settings.colors[1], settings.wins[1] )
        result = 0
    else :
        winner_color = 216
        message = "The game ends in a draw! Final score: \033[38;5;%d;1m%d\033[0m \033[38;5;%d;1m%d\033[0m" %(settings.colors[0], settings.wins[0], settings.colors[1], settings.wins[1] )
        result = 1

    centering_distance = int((settings.win_size-len(message))/2)
    os.system("clear")
    print("\n" * 2)
    print(" " * centering_distance, end='')
    print("%s" %(message), end='')
    print("\n" * 2)
    file = open(settings.win_files[result])
    lines = file_len(settings.win_files[result])
    for line in range(lines):
        line_string = file.readline()
        print(" " * centering_distance, end='')
        print("\033[38;5;%d;1m%s\033[0m" %(winner_color, line_string), end='')
    print("\n" * 2)

# Setting things up
matches = 0
while matches < settings.matches:
    output_file_name = "./jogo_da_ciencia_data/game_%d.dat" %(matches)
    output_file = open( output_file_name, 'w')

    # Initializes the board and the players
    board = Board()

    players = [None] * 2
    player_moves = [None] * 2
    for i in range(2):
        if settings.beings[i] == "Human":
            players[i] = Human(settings.names[i], settings.colors[i])
        elif settings.beings[i] == "Zombie":
            players[i] = Zombie(settings.names[i], settings.colors[i])
        elif settings.beings[i] == "Berzerker":
            players[i] = Berzerker(settings.names[i], settings.colors[i])
        else:
            players[i] = Player(settings.names[i], settings.colors[i])
        player_moves[i] = Movements( board, players[i] )
        if i == 0:
            for piece in range(settings.pieces):
                players[i].Pieces[piece] = Piece(players[i].color,
                        settings.hilights[i],
                        "p%d" %piece,
                        board.Starts1[piece])
                players[i].Pieces[piece].position = board.Starts1[piece]
                board.Squares[board.Starts1[piece]].occupied = True
                board.Squares[board.Starts1[piece]].occupant = players[i].Pieces[piece]
        else:
            for piece in range(settings.pieces):
                players[i].Pieces[piece] = Piece(players[i].color,
                        settings.hilights[i],
                        "g%d" %piece,
                        board.Starts2[piece])
                players[i].Pieces[piece].position = board.Starts2[piece]
                board.Squares[board.Starts2[piece]].occupied = True
                board.Squares[board.Starts2[piece]].occupant = players[i].Pieces[piece]


    players[0].rules.up = False
    if settings.standart_exits:
        players[0].rules.exits_in_2 = False
        players[1].rules.exits_in_1 = False
    else:
        players[0].rules.exits_in_1 = False
        players[1].rules.exits_in_2 = False

    game_time = 0
    victor = False
    turn = 0
    while not victor:
        if type(players[turn]) is Human:
            for piece in range(settings.pieces):
                if players[turn].Pieces[piece].alive:
                    for move in settings.moves:
                        if player_moves[turn].Test_Move(piece, move):
                            movement_control.Available_Moves.append(move)
                    if len(movement_control.Available_Moves) > 0:
                        selection_control.Available_Pieces.append(players[turn].Pieces[piece])
                    del movement_control.Available_Moves[:]
                else:
                    pass

            if len(selection_control.Available_Pieces) == 0: #Skips turn
                del threads[:]
                del movement_control.Available_Moves[:]
                del selection_control.Available_Pieces[:]
                if type(players[turn]) is Human:
                        input()
                if turn == 0:
                    turn = 1
                else:
                    turn = 0

            movement_control.action = False
            movement_control.move = None
            selection_control.action = False

            selection_control.hovered = 0
            selection_control.Available_Pieces[selection_control.hovered].hilighted = True

            threads.append(Thread(target=Show_selection, args=(board, players[turn])))
            threads[-1].start()
            threads.append(Thread(target=begin_listener_selection))
            threads[-1].start()

            for thread in threads:
                thread.join()
            del threads[:]

            del movement_control.Available_Moves[:]

            piece = -1
            for pos in range(settings.pieces):
                if players[turn].Pieces[pos].symbol == selection_control.Available_Pieces[selection_control.hovered].symbol:
                    piece = pos
                else:
                    pass
            if piece == -1:
                print("Failed to locate piece")
                input()
                exit(1)
            else:
                pass 

            for move in settings.moves:
                if player_moves[turn].Test_Move(piece, move):
                    movement_control.Available_Moves.append(move)

            threads.append(Thread(target=Show_movement, args=(board,)))
            threads[-1].start()
            threads.append(Thread(target=begin_listener_movement))
            threads[-1].start()

            for thread in threads:
                thread.join()

            player_moves[turn].Move(piece, movement_control.move)

            del threads[:]
            del movement_control.Available_Moves[:]
            del selection_control.Available_Pieces[:]


            movement_control.action = False
            movement_control.move = None
            selection_control.action = False
        elif type(players[turn]) is Zombie:
            if settings.VERBOSE:
                Show_Board( board )
                print("Its \033[38;5;%d;1m%s\033[0m turn. It's (trying) to think..."
                        %(players[turn].color, players[turn].name)
                        )
                time.sleep(players[turn].Zombie_delay)

            for piece in range(settings.pieces):
                if players[turn].Pieces[piece].alive:
                    for move in settings.moves:
                        if player_moves[turn].Test_Move(piece, move):
                            players[turn].Zombie_Moves.append(move)
                    if len(players[turn].Zombie_Moves) > 0:
                        players[turn].Zombie_Pieces.append(piece)
                    del players[turn].Zombie_Moves[:]
                else:
                    pass

            if len(players[turn].Zombie_Pieces) == 0: #Skips turn
                del players[turn].Zombie_Moves[:]
                del players[turn].Zombie_Pieces[:]
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
                continue

            del players[turn].Zombie_Moves[:]

            piece_pos = randint(0, (len(players[turn].Zombie_Pieces)-1) )

            for move in settings.moves:
                if player_moves[turn].Test_Move(players[turn].Zombie_Pieces[piece_pos], move):
                    players[turn].Zombie_Moves.append(move)
            
            try:
                move_pos = randint(0, (len(players[turn].Zombie_Moves)-1) )
            except ValueError:
                print("Selected piece: ", piece_pos)
                print(players[turn].Zombie_Pieces,
                        players[turn].Zombie_Moves)
                input()
                exit(0)

            player_moves[turn].Move(players[turn].Zombie_Pieces[piece_pos],  players[turn].Zombie_Moves[move_pos])

            del players[turn].Zombie_Pieces[:]
            del players[turn].Zombie_Moves[:]
        elif type(players[turn]) is Berzerker:
            if settings.VERBOSE:
                Show_Board( board )
                print("Its \033[38;5;%d;1m%s\033[0m turn. It's (trying) to think..."
                        %(players[turn].color, players[turn].name)
                        )
                time.sleep(players[turn].Berzerker_delay)

            if turn == 0:
                players[turn].good_move = "Down"
            else:
                players[turn].good_move = "Right"
                
            for piece in range(settings.pieces):
                if players[turn].Pieces[piece].alive:
                    for move in settings.moves:
                        if player_moves[turn].Test_Move(piece, move):
                            players[turn].Berzerker_Moves.append(move)
                    if len(players[turn].Berzerker_Moves) > 0:
                        if players[turn].good_move in players[turn].Berzerker_Moves:
                            players[turn].Berzerker_Good_Pieces.append(piece)
                        players[turn].Berzerker_Pieces.append(piece)
                    del players[turn].Berzerker_Moves[:]
                else:
                    pass

            if len(players[turn].Berzerker_Pieces) == 0: #Skips turn
                del players[turn].Berzerker_Moves[:]
                del players[turn].Berzerker_Pieces[:]
                del players[turn].Berzerker_Good_Pieces[:]
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
                continue

            del players[turn].Berzerker_Moves[:]

            if len(players[turn].Berzerker_Good_Pieces) > 0:
                piece_pos = randint(0, (len(players[turn].Berzerker_Good_Pieces)-1) )
                player_moves[turn].Move(players[turn].Berzerker_Good_Pieces[piece_pos] , players[turn].good_move)
            else:
                piece_pos = randint(0, (len(players[turn].Berzerker_Pieces)-1) )
                for move in settings.moves:
                    if player_moves[turn].Test_Move(players[turn].Berzerker_Pieces[piece_pos], move):
                        players[turn].Berzerker_Moves.append(move)
                move_pos = randint(0, (len(players[turn].Berzerker_Moves)-1) )
                player_moves[turn].Move(players[turn].Berzerker_Pieces[piece_pos], players[turn].Berzerker_Moves[move_pos])

            del players[turn].Berzerker_Pieces[:]
            del players[turn].Berzerker_Good_Pieces[:]
            del players[turn].Berzerker_Moves[:]
        else:
            pass

        output_line = ''
        for i in range(board.size):
            if board.Squares[i].occupied:
                if board.Squares[i].occupant in players[turn].Pieces:
                    output_line += str(turn+1)
                else:
                    if turn == 0:
                        output_line += '2'
                    else:
                        output_line += '1'
            else:
                output_line += '0'
        output_line += "\t"
        output_line += str(game_time)
        output_line += "\n"
        output_file.write(output_line)
        
        if type(players[turn]) is Human:
                input()
        alive_pieces = settings.pieces
        
        for piece in players[turn].Pieces:
            if not piece.alive:
                alive_pieces -= 1

        if alive_pieces == 0:
            if settings.VERBOSE:
                Show_Board(board)
                Turn_Victory_Screen(players[turn])
                time.sleep(0.2)
            victor = True
            matches += 1
            settings.wins[turn] += 1
            del players[:]
            del player_moves[:]
            output_file.close()
        else:
            pass

        game_time += 1
        if turn == 0:
            turn = 1
        else:
            turn = 0

Victory_Screen()

exit(0)
