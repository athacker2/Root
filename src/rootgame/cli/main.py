from rootgame.engine.setup import initialize_game

def main():
    game = initialize_game()

    for _ in range(5):  # Simulate 5 turns for demonstration
        print(f"Turn {game.turn + 1}")
        for i, player in enumerate(game.players):
            player.hand.append(game.deck.draw_card()[0])  # Each player draws one card
            print(f"Player {i + 1} score: {player.score}, hand: {[card.name for card in player.hand]}")
        game.turn += 1

if __name__ == "__main__":
    main()