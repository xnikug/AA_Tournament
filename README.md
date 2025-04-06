# Pseudo-Random Strategy

This strategy simulates pseudo-random behavior based on the history of moves in a prisoner's dilemma game.

## Strategy Explanation

The strategy evaluates the history of moves for both the player and the opponent and uses this information to decide whether to cooperate or defect. It is a mean algorithm. Below is a breakdown of the strategy's steps:

1. **Initialization:**
   - The strategy starts by considering the last 20 moves of both the player and the opponent to generate an initial hash value. This helps introduce variability into the strategy based on the most recent history.

2. **Snap Decision:**
   - There is a 1 in 21 chance (based on a mathematical check) that the strategy will decide to defect (`0`). This introduces randomness without using any external random number generators.

3. **Pseudo-Random Decision:**
   - If the opponent has defected in the recent rounds, the strategy will make a pseudo-random decision to either cooperate or defect. This is done by applying a mathematical hash to a small portion of the history.

4. **Default Cooperation:**
   - If the opponent has not defected recently, the strategy defaults to cooperating (`1`).

