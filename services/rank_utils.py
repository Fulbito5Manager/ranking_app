from models.player_model import Player

def determine_rank(points):
    try:
        if points < 0:
            points = 0;
    
        if points > 150:
            return 'Gold'
        elif points > 100:
            return 'Silver'
        elif points > 50:
            return 'Bronze'
        else:
            return 'Iron'
    except Exception as e:
        print("Points is not a valid data: ", e)
        return None

def get_rank_by_players_id(team, player_data=""):
        
        if team:
            try:
                team_ranking_points = []
                for player_id in team:

                        player = Player.query.filter_by(id=player_id).first()

                        if player: 
                            team_ranking_points.append(player.points)

                        else:
                            raise Exception("Missing Player.")
                            
                return team_ranking_points
                
            except Exception as e:
                print("Could not fetch player:", e)
                return None
            
        else:
            print("Team invdalid data.")
            return None

def is_team_winner(winner_team_id, team_id):
        match_result= ""

        if winner_team_id != "":

            if team_id == winner_team_id:
                match_result = "W"  # Win
            elif winner_team_id == None:
                match_result = "Tie"
            else:
                match_result = "L"  # Loss
            return match_result
        else:
            print("Could not get result from empty string.")
            return None