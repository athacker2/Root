from rootgame.engine.types import Player, GameState, Deck, TurnPhase
from rootgame.engine.BoardLogic import build_board

def initialize_game():
    # Initialize players, board, and game state
    players = [Player() for _ in range(2)]  # Assuming 2 players for now
    board = build_board()

    deck = Deck(cards=[])
    deck.initialize_deck()
    deck.shuffle_deck()

    for player in players:
        player.score = 0  # Initialize player scores
        player.hand = deck.draw_card(5)  # Each player starts with 5 cards

    game_state = GameState(players=players, board=board, deck=deck)
    
    return game_state

def get_legal_actions(game_state: GameState, player: Player):
    legal_actions = ["march", "end phase"]

    for card in player.hand:
        legal_actions.append(f"play card: {card.name}")
    
    return legal_actions

def apply_action(game_state: GameState, player: Player, action: str):
    # Check if is legal action
    if(action not in get_legal_actions(game_state, player)):
        raise("Illegal Action Received")

    if action == "march":
        print("marching troops")
    elif action.startswith("play card"):
        card = action.split(": ")[1]
        player.hand = [c for c in player.hand if c.name != card]  # Remove the card from player's hand
        print(f"Playing card: {card}")
    elif action == "end phase":
        if(game_state.current_phase is TurnPhase.BIRDSONG):
            game_state.current_phase = TurnPhase.DAYLIGHT
            return False
        elif game_state.current_phase is TurnPhase.DAYLIGHT:
            game_state.current_phase = TurnPhase.EVENING
            return False
        elif game_state.current_phase is TurnPhase.EVENING:
            game_state.current_phase = TurnPhase.BIRDSONG
            game_state.turn += 1
            return True

    return False
    

