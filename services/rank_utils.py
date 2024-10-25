def determine_rank(points):
    # Simplified rank determination logic // Needs modification
    if points > 150:
        return 'Gold'
    elif points > 100:
        return 'Silver'
    elif points > 50:
        return 'Bronze'
    else:
        return 'Iron'

def get_rank_by_players_id(team, player_data=""):
        
        from models.player_model import Player
        team_ranking_points = []

        for player_id in team:
            player = Player.query.filter_by(id=player_id).first()

            if player: 
                team_ranking_points.append(player.points)
            # if player_id == player_data['id']:
            #     team_ranking_points.append(player_data['points'])  # Use provided player_data for the specific player so mock data dont overwrite player_data
            # else:
            #     other_player_data = get_player_by_id(player_id)  # Fetch data for other players
            #     team_ranking_points.append(other_player_data['points'])
        return team_ranking_points

def is_team_winner(winner_team_id, team_id):
        match_result= ""

        if team_id == winner_team_id:
            match_result = "W"  # Win
        elif winner_team_id == None:
            match_result = "Tie"
        else:
            match_result = "L"  # Loss
        return match_result