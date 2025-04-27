# Pseudo-Random Strategy

This strategy simulates pseudo-random behavior based on the history of moves in a prisoner's dilemma game.

## Strategy Explanation

The strategy evaluates the history of moves for both the player and the opponent and uses this information to decide whether to cooperate or defect. It is a mean algorithm. Below is a breakdown of the strategy's steps:

1. **Initialization:**
   - The strategy starts by considering the last 20 moves of both the player and the opponent to generate an initial hash value. This helps introduce variability into the strategy based on the most recent history.

2. **Snap Decision:**
   - There is a 1 in 17 chance (based on a mathematical check) that the strategy will decide to defect (`0`). This introduces randomness without using any external random number generators.

3. **Pseudo-Random Decision:**
   - If the opponent has defected in the recent rounds, the strategy will make a pseudo-random decision to either cooperate or defect. This is done by applying a mathematical hash to a small portion of the history.

4. **Default Cooperation:**
   - If the opponent has not defected recently, the strategy defaults to cooperating (`1`).

## Part 2: Advanced Multi-Opponent Strategy

The second strategy expands on the first by handling multiple opponents and selecting which opponent to play against next.

```python
def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    # Implementation details...
```

### Strategy Explanation

1. **Move Decision:**
   - Similar to Part 1, the strategy uses hash-based pseudo-randomness and opponent defection analysis to decide whether to cooperate or defect.
   - The defection counter now decays gradually when opponents cooperate.

2. **Opponent Selection:**
   - The strategy intelligently selects the next opponent to play against based on several criteria:

3. **Eligibility Check:**
   - Filters opponents that haven't been played against 200 times yet.
   - Ensures the current opponent isn't selected again if we're about to complete 200 rounds with them.

4. **New Opponent Priority:**
   - Prioritizes opponents that haven't been played against at all.
   - Uses a hash-based selection to choose randomly among unplayed opponents.

5. **Cooperative Opponent Preference:**
   - For opponents already played against, calculates a cooperation rate.
   - Generally prefers to play against more cooperative opponents.
   - Occasionally stays with the current opponent regardless of their cooperation rate.

6. **Fallback Selection:**
   - If no clear selection criteria apply, uses a hash-based random selection among eligible opponents.

## Technical Implementation

- `hash(str(history))` converts move histories into large integer values
- Modulo operations (`% 17` and `% 3`) creates some probability distributions
