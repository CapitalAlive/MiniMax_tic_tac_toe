import sys
import random


def print_table(t):
    print("---------\n|", t[0], t[1], t[2], "|\n|", t[3], t[4], t[5], "|\n|", t[6], t[7], t[8], "|\n---------")


def next_player(_table):
    return "O" if _table.count("X") > _table.count("O") else "X"


def is_it_the_end(_table, _current_player):
    print_table(_table)
    if is_terminal_move(_current_player, _table) is True:
        print(_current_player, "wins")
        run_game()
    elif is_terminal_move(_current_player, _table) == "draw":
        print("Draw")
        run_game()


def is_terminal_move(_current_player, _table, cell_index=None):
    win_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 6, 4]]
    index_list = table_status(_table, _current_player)
    index_list.append(cell_index)
    for e in win_list:
        if e[0] in index_list and e[1] in index_list and e[2] in index_list:
            return True
    if _table.count("X") + _table.count("O") == 9:
        return "draw"
    return False


def ai_plays_easy(_table, statement=True):
    if statement is True:
        print('Making move level "easy"')
    return random.choice(table_status(_table, "empty"))


def ai_plays_medium(_table, _current_player):
    print('Making move level "medium"')
    # time.sleep(2)
    for iteration in range(2):
        if iteration == 1:
            _current_player = "O" if _current_player == "X" else "X"
        for i in table_status(_table, "empty"):
            if is_terminal_move(_current_player, _table, i) is True:
                return i
    return ai_plays_easy(_table, False)


def ai_plays_hard(tb, index=None, mini_max="min", root=0):
    _table = list(tb)
    cur_list = dict()
    mini_max = "max" if mini_max == "min" else "min"
    possible_plays = table_status(_table, "empty")
    if len(possible_plays) == 1 and root == 0:
        return possible_plays[0]
    _current_player = next_player(_table)
    for play_index in possible_plays:
        _table = list(tb)
        _table[play_index] = _current_player
        terminal_move = is_terminal_move(_current_player, _table, play_index)
        if terminal_move is False:
            try:
                cur_list.update({play_index: ai_plays_hard(_table, None, mini_max, root + 1)})
            except Exception:
                cur_list = {play_index: ai_plays_hard(_table, None, mini_max, root + 1)}
        elif terminal_move is True:
            return 1 if mini_max == "max" else -1
        elif terminal_move == "draw":
            return 0
    returning_index = max(cur_list, key=cur_list.get) if mini_max == "max" else min(cur_list, key=cur_list.get)
    if index is None:
        return cur_list[returning_index]
    else:
        return returning_index


def user_plays(_table):
    xy = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    while True:
        try:
            _coordinates = input("Enter the coordinates:").split()
            x = int(_coordinates[0]) - 1
            y = int(_coordinates[1]) - 1
            if x not in [0, 1, 2] or y not in [0, 1, 2]:
                print("Coordinates should be from 1 to 3!")
                continue
            else:
                if _table[xy[x][y]] != " ":
                    print("This cell is occupied! Choose another one!")
                    continue
                return xy[x][y]
        except Exception:
            print("You should enter numbers!")
            continue


def table_status(_table, lis="all"):
    x_i, o_i, empty_i = [], [], []
    for index in range(len(_table)):
        if _table[index] == "X":
            x_i.append(index)
        elif _table[index] == "O":
            o_i.append(index)
        elif _table[index] == " ":
            empty_i.append(index)
    return x_i if lis == "X" else (o_i if lis == "O" else (empty_i if lis == "empty" else (x_i, o_i, empty_i, "lol")))


def game_menu():
    options = ["easy", "medium", "hard", "user"]
    while True:
        menu = input("Input command: ").split()
        try:
            if menu[0] == "exit":
                sys.exit()
            elif menu[0] == "start":
                if menu[1] in options and menu[2] in options:
                    return menu[1], menu[2]
        except IndexError:
            pass
        print("Bad parameters!")


def make_a_play(difficulty_level, _table, _current_player):
    if difficulty_level == "user":
        return user_plays(_table)
    elif difficulty_level == "easy":
        return ai_plays_easy(_table)
    elif difficulty_level == "medium":
        return ai_plays_medium(_table, _current_player)
    elif difficulty_level == "hard":
        print('Making move level "hard"')
        return ai_plays_hard(_table, True)


def run_game():
    table = [x for x in "         "]
    difficulty_x, difficulty_o = game_menu()
    print_table(table)
    while True:
        current_player = next_player(table)
        difficulty = difficulty_x if current_player == "X" else difficulty_o
        table_index = make_a_play(difficulty, table, current_player)
        table[table_index] = current_player
        is_it_the_end(table, current_player)


run_game()
