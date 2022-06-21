import random
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt 
'''
    Color cards:
        Single color:
            green: 6
            red: 6
            purple: 5
            orange: 6
            yellow: 6
            blue: 6
        Double colors:
            green: 3
            red: 4
            purple: 4
            orange: 3
            yellow: 4
            blue: 4
    Special Cards:
        Popsicle (red)
        Lollipop (purple)
        Chocolate (brown)
        Gingerbread man
        Ice Cream
        Cupcake
        Gummy Star
    Map: 
        RPYBOGRP(Cupcake)YBOGRPYBOG(Ice Cream)RPYBOGRPYBOGRPYBOGRPY(Gummy Star)BOGRPYBOGRPYBOGRPYBOGRPYBO(Gingerbread)
           |                                          |           |              |              |
           1                                          2           3              4              5 
        GRPYBOGRPYBOGRPYBOGRPY(Lollipop)BOGRPYBOG(Popsicle)RPYBOGRPYBOGRP(Chocolate)BOGRPYBOGRPYBOG(Rainbow)
              |
              6
    Special passes:
        Peppermint pass: 1---> 5
        Gummy pass 2---> 3
    Licorice:
        Positions: 4 (index = 44), 6 (index = 75)
    Players:
        Red, Yellow, Green, Blue pawns
'''
## STEP 1: Record all cards
colors = ['green', 'red', 'purple', 'orange', 'yellow', 'blue']
num_cards_single_color = [6, 6, 5, 6, 6, 6]
num_cards_double_colors = [3, 4, 4, 3, 4, 4]
single_color_cards = [color + '_x1' for color, num_card in zip(colors, num_cards_single_color) for i in range(num_card)]
double_color_cards = [color + '_x2' for color, num_card in zip(colors, num_cards_double_colors) for i in range(num_card)] 
special_cards = ['cupcake', 'ice_cream', 'gummy_star','gingerbread', 'lollipop', 'popsicle', 'chocolate']
all_cards = single_color_cards + double_color_cards + special_cards

## STEP 2: Construct the map
map_string = 'RPYBOGRP YBOGRPYBOG RPYBOGRPYBOGRPYBOGRPY BOGRPYBOGRPYBOGRPYBOGRPYBO GRPYBOGRPYBOGRPYBOGRPY BOGRPYBOG RPYBOGRPYBOGRP BOGRPYBOGRPYBOG'
map_list = []
special_cards_dict = dict() 
color_map = {'R': 'red', 'P': 'purple', 'Y': 'yellow', 'B': 'blue', 'O': 'orange', 'G': 'green'}
special_card_pointer = 0
for index, s in enumerate(map_string):
    if s != ' ':
        map_list.append(color_map[s])
    else:
        special_card = special_cards[special_card_pointer]
        map_list.append(special_card)
        special_cards_dict[special_card] = (index, special_card, False)
        special_card_pointer += 1
map_list.append('goal')

INDEX_GOAL = 132 
LICORICE_INDEXES = [44, 75]
# Peppermint pass 3, blue --> 59, yellow
# Gummy pass 28, yellow --> 40, yellow 

def a_single_move(card_drawn, current_pos):
    # current_pos e.g (0, 'red', False)
    cur_index, cur_color, _ = current_pos
    if cur_index == INDEX_GOAL:
        return (INDEX_GOAL, 'win', False)
    map_list_right = deepcopy(map_list[cur_index + 1:])
    if card_drawn in special_cards_dict:
        return special_cards_dict[card_drawn]
    else:
        color, num_colors = card_drawn.split('_')
        num_colors = int(num_colors[-1])    
        if num_colors == 1:
            if color not in map_list_right:
                return (INDEX_GOAL, 'win', False)
            for i, c in enumerate(map_list_right):
                if c == color:
                    if cur_index + i + 1  == 3: # peppermint pass 
                        return (59, 'yellow', False)
                    elif cur_index + i + 1 == 28: # gummy pass 
                        return (40, 'yellow', False)
                    return (cur_index + i + 1, c, False)
        else:
            if map_list_right.count(color) < num_colors:
                return (INDEX_GOAL, 'win', False)
            count_colors = num_colors - 1
            for i, c in enumerate(map_list_right):
                if c == color:
                    if count_colors:
                        count_colors -= 1
                        continue 
                    else:
                        if cur_index + i + 1  == 3: # peppermint pass
                            return (59, 'yellow', False)
                        elif cur_index + i + 1 == 28: # gummy pass 
                            return (40, 'yellow', False)
                        return (cur_index + i + 1, c, False)


def play_a_two_player_game(game_cards, 
                           player_1_pos = (-1, None, False), 
                           player_2_pos = (-1, None, False)):
    # player_pos (index, color, is_stuck)
    while game_cards:
        if player_1_pos[2] == False:
            player_1_pos = a_single_move(game_cards.pop(), player_1_pos)
            if player_1_pos[0] in LICORICE_INDEXES:
                player_1_pos[2] == True
        else:
            player_1_pos[2] == False 

        if player_2_pos[2] == False:
            player_2_pos = a_single_move(game_cards.pop(), player_2_pos)
            if player_2_pos[0] in LICORICE_INDEXES:
                player_2_pos[2] == True
        else:
            player_2_pos[2] == False     

        if player_1_pos[1] == 'win':
            return [1, 2]

        if player_2_pos[1] == 'win':
            return [2, 1]  

def play_a_three_player_game(game_cards, 
                             player_1_pos = (-1, None, False), 
                             player_2_pos = (-1, None, False), 
                             player_3_pos = (-1, None, False)):
    while game_cards:
        if player_1_pos[2] == False:
            player_1_pos = a_single_move(game_cards.pop(), player_1_pos)
            if player_1_pos[0] in LICORICE_INDEXES:
                player_1_pos[2] == True
        else:
            player_1_pos[2] == False 

        if player_2_pos[2] == False:
            player_2_pos = a_single_move(game_cards.pop(), player_2_pos)
            if player_2_pos[0] in LICORICE_INDEXES:
                player_2_pos[2] == True
        else:
            player_2_pos[2] == False 

        if player_3_pos[2] == False:
            player_3_pos = a_single_move(game_cards.pop(), player_3_pos)
            if player_3_pos[0] in LICORICE_INDEXES:
                player_3_pos[2] == True
        else:
            player_3_pos[2] == False 

        if player_1_pos[1] == 'win':
            ranks = play_a_two_player_game(game_cards, player_2_pos, player_3_pos)
            if ranks == [1, 2]:
                return [1, 2, 3]
            else:
                return [1, 3, 2]

        if player_2_pos[1] == 'win':
            ranks = play_a_two_player_game(game_cards, player_3_pos, player_1_pos)
            if ranks == [1,2]:
                return [3, 1, 2]
            else:
                return [2, 1, 3]

        if player_3_pos[1] == 'win':
            ranks = play_a_two_player_game(game_cards, player_1_pos, player_2_pos)
            if ranks == [1,2]:
                return [2, 3, 1]
            else:
                return [3, 2, 1]

def play_a_four_player_game(game_cards, 
                            player_1_pos = (-1, None, False), 
                            player_2_pos = (-1, None, False), 
                            player_3_pos = (-1, None, False),
                            player_4_pos = (-1, None, False)):
    while game_cards:
        if player_1_pos[2] == False:
            player_1_pos = a_single_move(game_cards.pop(), player_1_pos)
            if player_1_pos[0] in LICORICE_INDEXES:
                player_1_pos[2] == True
        else:
            player_1_pos[2] == False 

        if player_2_pos[2] == False:
            player_2_pos = a_single_move(game_cards.pop(), player_2_pos)
            if player_2_pos[0] in LICORICE_INDEXES:
                player_2_pos[2] == True
        else:
            player_2_pos[2] == False 

        if player_3_pos[2] == False:
            player_3_pos = a_single_move(game_cards.pop(), player_3_pos)
            if player_3_pos[0] in LICORICE_INDEXES:
                player_3_pos[2] == True
        else:
            player_3_pos[2] == False 

        if player_4_pos[2] == False:
            player_4_pos = a_single_move(game_cards.pop(), player_4_pos)
            if player_4_pos[0] in LICORICE_INDEXES:
                player_4_pos[2] == True
        else:
            player_4_pos[2] == False

        if player_1_pos[1] == 'win':
            ranks = play_a_three_player_game(game_cards, player_2_pos, player_3_pos, player_4_pos)
            d = {'player_1_rank': 1}
            d['player_2_rank'] = ranks[0] + 1
            d['player_3_rank'] = ranks[1] + 1
            d['player_4_rank'] = ranks[2] + 1
            return [d[key] for key in ['player_1_rank', 'player_2_rank', 'player_3_rank', 'player_4_rank']]

        if player_2_pos[1] == 'win':
            ranks = play_a_three_player_game(game_cards, player_3_pos, player_4_pos, player_1_pos)
            d = {'player_2_rank': 1}
            d['player_3_rank'] = ranks[0] + 1
            d['player_4_rank'] = ranks[1] + 1
            d['player_1_rank'] = ranks[2] + 1
            return [d[key] for key in ['player_1_rank', 'player_2_rank', 'player_3_rank', 'player_4_rank']]

        if player_3_pos[1] == 'win':
            ranks = play_a_three_player_game(game_cards, player_4_pos, player_1_pos, player_2_pos)
            d = {'player_3_rank': 1}
            d['player_4_rank'] = ranks[0] + 1
            d['player_1_rank'] = ranks[1] + 1
            d['player_2_rank'] = ranks[2] + 1
            return [d[key] for key in ['player_1_rank', 'player_2_rank', 'player_3_rank', 'player_4_rank']]

        if player_4_pos[1] == 'win':
            ranks = play_a_three_player_game(game_cards, player_1_pos, player_2_pos, player_3_pos)
            d = {'player_4_rank': 1}
            d['player_1_rank'] = ranks[0] + 1
            d['player_2_rank'] = ranks[1] + 1
            d['player_3_rank'] = ranks[2] + 1
            return [d[key] for key in ['player_1_rank', 'player_2_rank', 'player_3_rank', 'player_4_rank']]

def play_multiple_games(num_games_played, num_players):
    def prepare_cards():
        # prepare cards
        NUM_DECK_CARDS = 10
        cur_cards = []
        for i in range(NUM_DECK_CARDS):
            cur_deck = deepcopy(all_cards)
            random.shuffle(cur_deck)
            cur_cards += cur_deck
        return cur_cards

    if num_players == 2:
        count_player_1_wins, count_player_2_wins = 0, 0
        for i in range(num_games_played):
            print ('playing a {} player game, current processing game #{}'.format(num_players, i))
            results = play_a_two_player_game(prepare_cards())
            if results[0] == 1:
                count_player_1_wins += 1
            elif results[1] == 1:
                count_player_2_wins += 1
        return  [count_player_1_wins / num_games_played, 
                    count_player_2_wins / num_games_played]

    if num_players == 3:
        count_player_1_wins, count_player_2_wins, count_player_3_wins = 0, 0, 0
        for i in range(num_games_played):
            print ('playing a {} player game, current processing game #{}'.format(num_players, i))
            results = play_a_three_player_game(prepare_cards())
            if results[0] == 1:
                count_player_1_wins += 1
            elif results[1] == 1:
                count_player_2_wins += 1
            elif results[2] == 1:
                count_player_3_wins += 1
        return [count_player_1_wins / num_games_played, 
                count_player_2_wins / num_games_played,
                count_player_3_wins / num_games_played]

    if num_players == 4:
        count_player_1_wins, count_player_2_wins, count_player_3_wins, count_player_4_wins = 0, 0, 0, 0
        for i in range(num_games_played):
            print ('playing a {} player game, current processing game #{}'.format(num_players, i))
            results = play_a_four_player_game(prepare_cards())
            if results[0] == 1:
                count_player_1_wins += 1
            elif results[1] == 1:
                count_player_2_wins += 1
            elif results[2] == 1:
                count_player_3_wins += 1
            elif results[3] == 1:
                count_player_4_wins += 1

        return [count_player_1_wins / num_games_played, 
                count_player_2_wins / num_games_played,
                count_player_3_wins / num_games_played,
                count_player_4_wins / num_games_played]

# plotting
def plot_winning_probabilites(num_players):
    num_games = [1, 2, 3, 4, 5, 6] # 10**4
    player_1_win_pct = []
    player_2_win_pct = []
    player_3_win_pct = []
    player_4_win_pct = []
    for num_game in num_games:
        if num_players == 2:
            p1_win, p2_win = play_multiple_games(10**num_game, 2)
            player_1_win_pct.append(p1_win)
            player_2_win_pct.append(p2_win)

        elif num_players == 3:
            p1_win, p2_win, p3_win = play_multiple_games(10**num_game, 3)
            player_1_win_pct.append(p1_win)
            player_2_win_pct.append(p2_win)
            player_3_win_pct.append(p3_win)

        elif num_players == 4:
            p1_win, p2_win, p3_win, p4_win = play_multiple_games(10**num_game, 4)
            player_1_win_pct.append(p1_win)
            player_2_win_pct.append(p2_win)
            player_3_win_pct.append(p3_win)
            player_4_win_pct.append(p4_win)

    player_1_win_pct = np.array(player_1_win_pct)
    player_2_win_pct = np.array(player_2_win_pct)
    player_3_win_pct = np.array(player_3_win_pct)
    player_4_win_pct = np.array(player_4_win_pct)

    print (player_1_win_pct)
    print (player_2_win_pct)
    print (player_3_win_pct)
    print (player_4_win_pct)

    if num_players == 2:
        probability_res = np.array([player_1_win_pct, player_2_win_pct])
        np.savetxt('{}_player_game_simulation_res.txt'.format(num_players), probability_res)
    elif num_players == 3:
        probability_res = np.array([player_1_win_pct, player_2_win_pct, player_3_win_pct])
        np.savetxt('{}_player_game_simulation_res.txt'.format(num_players), probability_res)
    elif num_players == 4:
        probability_res = np.array([player_1_win_pct, player_2_win_pct, player_3_win_pct, player_4_win_pct])
        np.savetxt('{}_player_game_simulation_res.txt'.format(num_players), probability_res)

    width = 0.5
    fig, ax = plt.subplots(figsize = (10, 8))
    if num_players == 2:
        ax.hlines(y=[0.5], xmin=-0.1, xmax=len(num_games) + width, colors='black', linestyles='--', lw=1)
        ax.bar(num_games, player_2_win_pct, width, label='Player_2_win_probability')
        ax.bar(num_games, player_1_win_pct, width, bottom = player_2_win_pct, label='Player_1_win_probability')
    elif num_players == 3:
        ax.hlines(y=[1./3, 2./3], xmin=-0.1, xmax=len(num_games) + width, colors='black', linestyles='--', lw=1)
        ax.bar(num_games, player_3_win_pct, width, label='Player_3_win_probability')
        ax.bar(num_games, player_2_win_pct, width, bottom = player_3_win_pct,  label='Player_2_win_probability')
        ax.bar(num_games, player_1_win_pct, width, bottom = player_3_win_pct + player_2_win_pct, label='Player_1_win_probability')
    elif num_players == 4:
        ax.hlines(y=[0.25, 0.50, 0.75], xmin=-0.1, xmax=len(num_games) + width, colors='black', linestyles='--', lw=1)
        ax.bar(num_games, player_4_win_pct, width, label='Player_4_win_probability')
        ax.bar(num_games, player_3_win_pct, width, bottom = player_4_win_pct, label='Player_3_win_probability')
        ax.bar(num_games, player_2_win_pct, width, bottom = player_4_win_pct + player_3_win_pct, label='Player_2_win_probability')
        ax.bar(num_games, player_1_win_pct, width, bottom = player_4_win_pct + player_3_win_pct + player_2_win_pct, label='Player_1_win_probability') 

    ax.set_ylabel('Winning Probability', fontsize = 20)
    ax.set_title('Candy Land - Chance of winning for {} players'.format(num_players), fontsize = 20)
    ax.set_xlabel('number of games played, at exponential form of 10', fontsize = 20)
    ax.legend()
    plt.tight_layout()
    plt.savefig('simulation_results_{}_players.png'.format(num_players), dpi = 900)

if __name__ == '__main__':
    plot_winning_probabilites(2)
    plot_winning_probabilites(3)
    plot_winning_probabilites(4)
    



