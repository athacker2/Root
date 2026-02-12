from rootgame.engine.game import Game
from rootgame.cli.map_renderer import make_renderer
from rootgame.shared.shared_types import *
from rootgame.engine.actions import *

def main():
    game = Game()
    renderer = make_renderer(edges=game.get_board_edges())

    for _ in range(5):  # Simulate 5 rounds for demonstration
        for i, player in enumerate(game.players):
            
            while(True):
                print(f"Player {i + 1}'s turn. Current phase: {game.current_phase.name}")
                print(renderer.render(game.get_clearing_state()))
                
                print(f"Player {i + 1} hand: {[card.name for card in player.hand]}")

                legal_actions = game.get_legal_actions(player)
                print(f"Player {i + 1} actions: - {player.faction.faction_name}")
                for(j, action) in enumerate(legal_actions):
                    print(f"{j}: {action}")

                chosen_action = None
                while(not(game.is_action_legal(player, chosen_action))):
                    chosen_action = input(f"Player {i + 1}, choose an action: ")

                    # Convert string action to corresponding Action object
                    if(chosen_action.startswith("MOVE")):
                        _, num_units, src, dest = chosen_action.split(" ")
                        chosen_action = MoveAction(int(num_units), int(src), int(dest))
                    elif(chosen_action.startswith("BATTLE")):
                        player_map = {"M": game.players[0], "E": game.players[1]}
                        _, clearing_id, defender = chosen_action.split(" ")
                        chosen_action = BattleAction(int(clearing_id), player, player_map[defender])
                    elif(chosen_action.startswith("RECRUIT")):
                        if(player.faction.faction_name == "marquise_de_cat"):
                            chosen_action = MarquiseRecruitAction()
                        else:
                            _, clearing_id, num_units = chosen_action.split(" ")
                            chosen_action = RecruitAction(int(clearing_id), int(num_units))
                    elif(chosen_action.startswith("PLAY CARD")):
                        _, _, card_idx = chosen_action.split(" ")
                        chosen_action = PlayCardAction(int(card_idx))
                    elif(chosen_action == "END PHASE"):
                        chosen_action = EndPhaseAction()
                    elif(chosen_action.startswith("ADD WOOD")):
                        chosen_action = AddWoodToSawmillsAction()
                    elif(chosen_action.startswith("MARCH")):
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

                turn_over = game.apply_action(player, chosen_action)
            
                print("-" * 50)  # Separator for readability

                if turn_over:
                    break
            


if __name__ == "__main__":
    main()