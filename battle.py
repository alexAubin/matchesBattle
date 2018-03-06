import os
import glob
from importlib.machinery import SourceFileLoader

def battle(player1, player2):

    allumettes = 30
    current_player = player1

    def other_player(player):
        return player2 if player == player1 else player1

    while allumettes > 1:
        try:
            take = current_player.play(allumettes)
        except:
            take = -1

        # If current player attempts an illegal move, make the other win
        if not isinstance(take, int) or take not in [ 1, 2, 3 ] or take >= allumettes:
            return other_player(current_player)
        #print("pidoupe")
        #print(allumettes)
        allumettes -= take
        #print(allumettes)
        #print("---")
        # If there's only one allumette left, current player won
        if allumettes == 1:
            return current_player

        current_player = other_player(current_player)


def get_players():

    player_modules = [ f for f in glob.glob("/var/www/allumette/app/players/*.py") if not f.endswith("__.py") ]

    return { m.split('/')[-1][:-3]:load(m) for m in player_modules }


def load(module_file):
  
    name = module_file.split('/')[-1][:-3]

    try:
        return SourceFileLoader(name, module_file).load_module()
    except:
        return None




def run_battle():

    print("test1")

    players = get_players()
    print(players)

    results = {}
    for p in players:
        results[p] = {}

    for p1, mod1 in players.items():
        for p2, mod2 in players.items():
            if p1 == p2:
                continue

            if p2 not in results[p1].keys():
                results[p1][p2] = [0,0]
            if p1 not in results[p2].keys():
                results[p2][p1] = [0,0]

            for i in range(0,5):
                win = battle(mod1, mod2)
                results[p1][p2][int(win == mod1)] += 1
                results[p2][p1][int(win == mod2)] += 1

    print(results)

    output = {}
    for p in players:
        output[p] = {}
        output[p]["wins"]   = sum([ v[1] for v in results[p].values() ])
        output[p]["losses"] = sum([ v[0] for v in results[p].values() ])
        
        # print("[{player}] Wins {w} | Looses {l}".format(player=p, w=wins, l=losses))
    return output

