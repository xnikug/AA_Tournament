def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    """
    Strategy for round 2 of the prisoner's dilemma tournament.
    
    Args:
        opponent_id: ID of the current opponent
        my_history: Dictionary of my past moves against all opponents
        opponents_history: Dictionary of all opponents' past moves against me
    
    Returns:
        tuple: (move, next_opponent)
            move: 0 for defect, 1 for cooperate
            next_opponent: ID of the next opponent to face
    """
    # Get the current opponent's history and my history with them
    current_opponent_history = opponents_history.get(opponent_id, [])
    my_history_with_opponent = my_history.get(opponent_id, [])
    
    # Track defection count for the current opponent
    defection_count = 0
    for move in current_opponent_history:
        if move == 0:  # If the opponent defected
            defection_count += 1
        else:
            defection_count = max(0, defection_count - 0.5)  # Gradually forgive cooperation
    
    # Generate pseudo-randomness based on combined history
    combined_history = str(my_history_with_opponent[-20:]) + str(current_opponent_history[-20:])
    total = hash(combined_history)
    
    # Decide on the move
    move = 1  # Default to cooperation
    
    # Have a one in 17 chance to defect randomly (snap)
    if hash(total * 663937) % 17 == 0:
        move = 0  # Defect
    
    # If the opponent has been defecting, be more likely to defect
    elif defection_count >= 1:
        recent_history = str(my_history_with_opponent[-5:]) + str(current_opponent_history[-5:])
        total_recent = hash(recent_history)
        if (total_recent % 3) == 0:  # 1 in 3 chance to defect
            move = 0  # Defect
    
    # --- CHOOSE NEXT OPPONENT ---
    # Get all available opponent IDs
    all_opponents = set(opponents_history.keys())
    
    # Find eligible opponents (haven't reached 200 rounds yet)
    eligible_opponents = [op_id for op_id in all_opponents 
                         if len(my_history.get(op_id, [])) < 200]
    
    # Remove current opponent if we've already played 200 rounds with them
    if opponent_id in eligible_opponents and len(my_history.get(opponent_id, [])) >= 199:  # 199 because we're about to add one more
        eligible_opponents.remove(opponent_id)
    
    # If no eligible opponents, return any opponent (shouldn't happen in properly configured game)
    if not eligible_opponents:
        return (move, next(iter(all_opponents)))
    
    # Find opponents we haven't played yet from the eligible ones
    unplayed_opponents = [op_id for op_id in eligible_opponents 
                         if not opponents_history.get(op_id, [])]
    
    # If we have unplayed opponents, choose one of them
    if unplayed_opponents:
        # Choose based on a hash of the current state to ensure deterministic but varied selection
        selection_hash = hash(str(my_history) + str(opponent_id))
        next_opponent = unplayed_opponents[selection_hash % len(unplayed_opponents)]
    else:
        # Calculate cooperation rates for eligible opponents
        cooperation_rates = {}
        for op_id in eligible_opponents:
            history = opponents_history.get(op_id, [])
            if history:  # Only consider opponents we've played against
                cooperation_rate = sum(history) / len(history)
                cooperation_rates[op_id] = cooperation_rate
        
        # 20% chance to stick with current opponent if eligible and we've played them before
        if opponent_id in cooperation_rates and hash(str(my_history) + str(opponents_history)) % 5 == 0:
            next_opponent = opponent_id
        # Otherwise, prefer the opponent with the highest cooperation rate
        elif cooperation_rates:
            # Sort by cooperation rate (highest first)
            sorted_opponents = sorted(cooperation_rates.items(), key=lambda x: x[1], reverse=True)
            next_opponent = sorted_opponents[0][0]
        else:
            # Fallback: choose any eligible opponent
            selection_hash = hash(str(my_history) + str(opponent_id))
            next_opponent = eligible_opponents[selection_hash % len(eligible_opponents)]
    
    return (move, next_opponent)