from rootgame.engine.game import Game
from rootgame.cli.map_renderer import make_renderer


def main():
    game = Game()
    renderer = make_renderer()

    for _ in range(5):  # Simulate 5 rounds for demonstration
        for i, player in enumerate(game.players):
            
            while(True):
                print(f"Player {i + 1}'s turn. Current phase: {game.current_phase.name}")
                print(renderer.render(game.get_clearing_state()))
                
                print(f"Player {i + 1} hand: {[card.name for card in player.hand]}")

                legal_actions = game.get_legal_actions(player)
                print(f"Player {i + 1} actions: - {player.character.name}")
                for(j, action) in enumerate(legal_actions):
                    print(f"{j}: {action}")

                chosen_action = ""
                while(not(game.is_action_legal(player, chosen_action))):
                    chosen_action = input(f"Player {i + 1}, choose an action: ")
                    if not(game.is_action_legal(player, chosen_action)):
                        print("Invalid action. Please choose a legal action.")

                turn_over = game.apply_action(player, chosen_action)
            
                print("-" * 50)  # Separator for readability

                if turn_over:
                    break
            


if __name__ == "__main__":
    main()