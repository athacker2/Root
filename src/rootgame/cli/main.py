from rootgame.engine.game import Game
from rootgame.cli.map_renderer import make_renderer
from rootgame.shared.shared_types import *
from rootgame.engine.actions import *

def main():
    game = Game()
    renderer = make_renderer(edges=game.get_board_edges())

    while(game.round < 10):
        for i, player in enumerate(game.players):
            curr_round = game.round
            while(game.round == curr_round):
                print(f"Player {i + 1}'s turn. Current phase: {game.current_phase.name}")
                print(renderer.render(game.get_clearing_state()))
                
                print(f"Player {i + 1} hand: {[card.name for card in player.hand]}")

                if(player.faction.faction_name == "eyrie_dynasties"):
                    print(f"Current Decree:")
                    print(f"Recruit: {[card.suit.__str__() for card in player.faction.get_remaining_decree(DecreeOption.Recruit)]}")
                    print(f"Move: {[card.suit.__str__() for card in player.faction.get_remaining_decree(DecreeOption.Move)]}")
                    print(f"Battle: {[card.suit.__str__() for card in player.faction.get_remaining_decree(DecreeOption.Battle)]}")
                    print(f"Build: {[card.suit.__str__() for card in player.faction.get_remaining_decree(DecreeOption.Build)]}")

                legal_actions = game.get_legal_actions(player)
                print(f"Player {i + 1} actions: - {player.faction.faction_name}")
                for(j, action) in enumerate(legal_actions):
                    print(f"{j}: {action}")

                chosen_action = None
                while(not(game.is_action_legal(player, chosen_action))):
                    chosen_action = input(f"Player {i + 1}, choose an action: ")

                    if(chosen_action == "END PHASE"):
                        chosen_action = EndPhaseAction()
                    elif(chosen_action == "DRAW"):
                        chosen_action = DrawCardAction()
                    elif(chosen_action.startswith("DISCARD")):
                        _, *card_idxs = chosen_action.split(" ")
                        if(not all(idx.isdigit() for idx in card_idxs)):
                            continue
                        chosen_action = DiscardCardAction([int(idx) for idx in card_idxs])

                    elif(player.faction.faction_name == "marquise_de_cat"):
                        if(chosen_action.startswith("RECRUIT")):
                            chosen_action = MarquiseRecruitAction()
                        elif(chosen_action.startswith("BATTLE")):
                            player_map = {"E": game.players[0], "M": game.players[1]}
                            _, clearing_id, defender = chosen_action.split(" ")
                            chosen_action = BattleAction(int(clearing_id), player, player_map[defender])
                        elif(chosen_action.startswith("ADD WOOD")):
                            chosen_action = AddWoodToSawmillsAction()
                        elif(chosen_action.startswith("MARCH")):
                            if(len(chosen_action.split(" ")) != 7):
                                continue
                            _, num_units_one, src_one, dest_one, num_units_two, src_two, dest_two = chosen_action.split(" ")
                            move_one = MoveAction(int(num_units_one), int(src_one), int(dest_one))
                            move_two = MoveAction(int(num_units_two), int(src_two), int(dest_two))
                            chosen_action = MarchAction(move_one, move_two)
                        elif(chosen_action.startswith("BUILD")):
                            _, clearing_id, building_name = chosen_action.split(" ")
                            if(not (clearing_id.isdigit())):
                                continue
                            building_map = {"SAWMILL": BuildingType.SAWMILL, "WORKSHOP": BuildingType.WORKSHOP, "RECRUITER": BuildingType.RECRUITER}
                            chosen_action = MarquiseBuildAction(int(clearing_id), building_map[building_name])
                    elif(chosen_action.startswith("OVERWORK")):
                        _, clearing_id, card_idx = chosen_action.split(" ")
                        if(not (clearing_id.isdigit() and card_idx.isdigit())):
                            continue
                        chosen_action = MarquiseOverworkAction(int(clearing_id), int(card_idx))

                    elif(player.faction.faction_name == "eyrie_dynasties"):
                        if(chosen_action.startswith("ADD TO DECREE")):
                            _, _, _, card_idx, option = chosen_action.split(" ")
                            if(not card_idx.isdigit()):
                                continue
                            option_map = {"RECRUIT": DecreeOption.Recruit, "MOVE": DecreeOption.Move, "BATTLE": DecreeOption.Battle, "BUILD": DecreeOption.Build}
                            if(not option in option_map.keys()):
                                continue
                            chosen_action = EyrieAddToDecreeAction(int(card_idx), option_map[option])
                        elif(chosen_action.startswith("RECRUIT")):
                            _, clearing_id = chosen_action.split(" ")
                            if(not clearing_id.isdigit()):
                                continue
                            chosen_action = EyrieRecruitAction(int(clearing_id))
                        elif(chosen_action.startswith("MOVE")):
                            _, num_units, src, dest = chosen_action.split(" ")
                            if(not num_units.isdigit() or not src.isdigit() or not dest.isdigit()):
                                continue
                            chosen_action = EyrieMoveAction(int(num_units), int(src), int(dest))
                        elif(chosen_action.startswith("BATTLE")):
                            if(not len(chosen_action.split(" ") == 3)):
                                continue
                            player_map = {"E": game.players[0], "M": game.players[1]}
                            _, clearing_id, defender = chosen_action.split(" ")
                            if(not clearing_id.isdigit()):
                                continue
                            if(not defender in player_map.keys()):
                                continue
                            chosen_action = EyrieBattleAction(int(clearing_id), player, player_map[defender])
                        elif(chosen_action.startswith("BUILD")):
                            _, clearing_id = chosen_action.split(" ")
                            if(not clearing_id.isdigit()):
                                continue
                            chosen_action = EyrieBuildAction(int(clearing_id))
                        elif(chosen_action.startswith("TURMOIL")):
                            chosen_action = EyrieTurmoilAction()

                game.apply_action(player, chosen_action)
            
                print("-" * 50)  # Separator for readability
            


if __name__ == "__main__":
    main()