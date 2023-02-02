# Russian poker text game

_**This is a mini-project - Russian poker with only a text interface to play in the terminal**_ 

#### System dependencies:

python >= 3.9

## Contents and how to use it

1) **main.py** - main script, that you can launch in terminal:  
```commandline
path_to_script/main.py
```

2) **algorythm.py** - script that calculates card combinations. **Do not launch this script**.

## Rules

**_The rules in this version of russian poker is slightly different from original one._**

- At the start of the game you write in your **start money** (only a number) and **the Name**
- You make the bet and only then recive your 5 cards. 
Croupier also receive another 5 cards, but they are not showed to you. 
- You can pass (not play this round, but your bet will not be returned)
- Or you can play and change some card (by typing their numbers). You can change nothing and continue 
Or _for each card you change, you will need to pay the cost of the bet_ 
- After changes, you can pass again.
- If you reach this point, you close your bet by paying double the value of your bet 
- And now you will see cards of Croupier.

  - If Croupier have **no game** (no combination at all), then you win anyway, 
  regardless of the combination of your cards. 
  Your winnings will be your bet and also money for closing the bet (doubled bet) will be returned
  - If Croupier have lower combination than yours, than you win your initial bet and
  depending on your combination you win money for closing the bet 
  (doubled bet) multiplied by the [coefficient](#Coefficients and combinations) of combination
  - If Croupier have higher combination than you, then you lose all your bets (initial bet and money for closing bet)
  - If Croupier have the same combination, then you win only if your combination have a higher card.
    - If Combinations are identical (for example, both Croupier and you have pair of twos), 
    then you win only if there is higher card among another cards that not involved 
    in the combination than Croupier's
    - In this cases winnings are the same - initial bet and doubled net multiplied by 
    [coefficient](#Coefficients and combinations)

## Coefficients and combinations 

| **Combination**      | **Coefficent** |
|----------------------|----------------|
| ONE PAIR or ACE-KING | 1:1            |
| TWO PAIRS            | 2:1            |
| THREE OF A KIND      | 3:1            |
| STRAIGHT             | 4:1            |
| FLUSH                | 5:1            |
| FULL HOUSE           | 7:1            |
| FOUR OF A KIND       | 20:1           |
| STRAIGHT FLUSH       | 50:1           |

