from rootgame.engine.EngineLogic import *


def main():
    game = initialize_game()

    for _ in range(5):  # Simulate 5 rounds for demonstration
        for i, player in enumerate(game.players):
            
            while(True):
                print(f"Player {i + 1}'s turn. Current phase: {game.current_phase.name}")
                legal_actions = get_legal_actions(game, player)
                print(f"Player {i + 1} actions:")
                for(j, action) in enumerate(legal_actions):
                    print(f"{j}: {action}")

                chosen_action = -1
                while(chosen_action not in range(len(legal_actions))):
                    try:
                        chosen_action = int(input(f"Player {i + 1}, choose an action: "))
                        if chosen_action not in range(len(legal_actions)):
                            print("Invalid action. Please choose a legal action.")
                    except ValueError:
                        print("Please enter a valid integer for the action.")

                turn_over = apply_action(game, player, legal_actions[chosen_action])
            
                print("-" * 50)  # Separator for readability

                if turn_over:
                    break
            


if __name__ == "__main__":
    main()