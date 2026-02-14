from rootgame.engine.card import DominanceCard, AmbushCard, EffectCard, ItemCard
from rootgame.engine.types import Suit

BASE_GAME_DECK = [
    DominanceCard(Suit.Fox),
    DominanceCard(Suit.Mouse),
    DominanceCard(Suit.Rabbit),
    DominanceCard(Suit.Bird),

    AmbushCard(Suit.Fox),
    AmbushCard(Suit.Mouse),
    AmbushCard(Suit.Rabbit),
    AmbushCard(Suit.Bird),
    AmbushCard(Suit.Bird),

    EffectCard(
        name="Royal Claim",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Bird: 4},
    ),
    EffectCard(
        name="Sappers",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Mouse: 1},
    ),
    EffectCard(
        name="Sappers",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Mouse: 1},
    ),
    EffectCard(
        name="Armorers",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Fox: 1},
    ),
    EffectCard(
        name="Armorers",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Fox: 1},
    ),
    EffectCard(
        name="Brutal Tactics",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Fox: 2},
    ),
    EffectCard(
        name="Brutal Tactics",
        suit=Suit.Bird,
        persistent=True,
        crafting_requirements={Suit.Fox: 2},
    ),
    EffectCard(
        name="Better Burrow Bank",
        suit=Suit.Rabbit,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 2},
    ),
    EffectCard(
        name="Better Burrow Bank",
        suit=Suit.Rabbit,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 2},
    ),
    EffectCard(
        name="Command Warren",
        suit=Suit.Rabbit,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 2},
    ),
    EffectCard(
        name="Command Warren",
        suit=Suit.Rabbit,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 2},
    ),
    EffectCard(
        name="Cobbler",
        suit=Suit.Rabbit,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 2},
    ),
    EffectCard(
        name="Cobbler",
        suit=Suit.Rabbit,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 2},
    ),
    EffectCard(
        name="Codebreakers",
        suit=Suit.Mouse,
        persistent=True,
        crafting_requirements={Suit.Mouse: 1},
    ),
    EffectCard(
        name="Codebreakers",
        suit=Suit.Mouse,
        persistent=True,
        crafting_requirements={Suit.Mouse: 1},
    ),
    EffectCard(
        name="Scouting Party",
        suit=Suit.Mouse,
        persistent=True,
        crafting_requirements={Suit.Mouse: 2},
    ),
    EffectCard(
        name="Scouting Party",
        suit=Suit.Mouse,
        persistent=True,
        crafting_requirements={Suit.Mouse: 2},
    ),
    EffectCard(
        name="Stand and Deliver",
        suit=Suit.Fox,
        persistent=True,
        crafting_requirements={Suit.Mouse: 3},
    ),
    EffectCard(
        name="Stand and Deliver",
        suit=Suit.Fox,
        persistent=True,
        crafting_requirements={Suit.Mouse: 3},
    ),
    EffectCard(
        name="Tax Collector",
        suit=Suit.Fox,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 1, Suit.Fox: 1, Suit.Mouse: 1},
    ),
    EffectCard(
        name="Tax Collector",
        suit=Suit.Fox,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 1, Suit.Fox: 1, Suit.Mouse: 1},
    ),
    EffectCard(
        name="Tax Collector",
        suit=Suit.Fox,
        persistent=True,
        crafting_requirements={Suit.Rabbit: 1, Suit.Fox: 1, Suit.Mouse: 1},
    ),

    EffectCard(
        name="Favor of the Foxes",
        suit=Suit.Fox,
        persistent=False,
        crafting_requirements={Suit.Fox: 3},
    ),
    EffectCard(
        name="Favor of the Mice",
        suit=Suit.Mouse,
        persistent=False,
        crafting_requirements={Suit.Mouse: 3},
    ),
    EffectCard(
        name="Favor of the Rabbits",
        suit=Suit.Rabbit,
        persistent=False,
        crafting_requirements={Suit.Rabbit: 3},
    ),

    ItemCard(
        item="Crossbow",
        suit=Suit.Bird,
        crafting_requirements={Suit.Fox: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Crossbow",
        suit=Suit.Mouse,
        crafting_requirements={Suit.Fox: 1},
        crafting_VP=1,
    ),

    ItemCard(
        item="Tea",
        suit=Suit.Rabbit,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=2,
    ),
    ItemCard(
        item="Tea",
        suit=Suit.Mouse,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=2,
    ),
    ItemCard(
        item="Tea",
        suit=Suit.Fox,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=2,
    ),

    ItemCard(
        item="Bag",
        suit=Suit.Bird,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Bag",
        suit=Suit.Rabbit,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Bag",
        suit=Suit.Mouse,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Bag",
        suit=Suit.Fox,
        crafting_requirements={Suit.Mouse: 1},
        crafting_VP=1,
    ),

    ItemCard(
        item="Boots",
        suit=Suit.Bird,
        crafting_requirements={Suit.Rabbit: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Boots",
        suit=Suit.Rabbit,
        crafting_requirements={Suit.Rabbit: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Boots",
        suit=Suit.Mouse,
        crafting_requirements={Suit.Rabbit: 1},
        crafting_VP=1,
    ),
    ItemCard(
        item="Boots",
        suit=Suit.Fox,
        crafting_requirements={Suit.Rabbit: 1},
        crafting_VP=1,
    ),

    ItemCard(
        item="Coins",
        suit=Suit.Rabbit,
        crafting_requirements={Suit.Rabbit: 2},
        crafting_VP=3,
    ),
    ItemCard(
        item="Coins",
        suit=Suit.Mouse,
        crafting_requirements={Suit.Rabbit: 2},
        crafting_VP=3,
    ),
    ItemCard(
        item="Coins",
        suit=Suit.Fox,
        crafting_requirements={Suit.Rabbit: 2},
        crafting_VP=3,
    ),

    ItemCard(
        item="Sword",
        suit=Suit.Bird,
        crafting_requirements={Suit.Fox: 2},
        crafting_VP=2,
    ),
    ItemCard(
        item="Sword",
        suit=Suit.Mouse,
        crafting_requirements={Suit.Fox: 2},
        crafting_VP=2,
    ),
    ItemCard(
        item="Sword",
        suit=Suit.Fox,
        crafting_requirements={Suit.Fox: 2},
        crafting_VP=2,
    ),

    ItemCard(
        item="Hammer",
        suit=Suit.Fox,
        crafting_requirements={Suit.Fox: 1},
        crafting_VP=2,
    ),
]