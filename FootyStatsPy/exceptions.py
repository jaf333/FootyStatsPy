class InvalidStat(Exception):
    def __init__(self, param, invalid_value, possible_values):
        super().__init__(fValue {invalid_value} for param {param} is invalid. Possible values are {possible_values}.nEl valor {invalid_value} para el parámetro {param} no es válido. Los valores válidos son: {possible_values})

class InvalidLeagueException(Exception):
    def __init__(self, league, possible_leagues_list):
        self.message = fLeague {league} is not valid for any of the possible leagues {possible_leagues_list}.
        super().__init__(self.message)
        
class InvalidSeasonException(Exception):
    def __init__(self, season, possible_seasons_list):
        self.message = fSeason {season} is not valid for any of the possible seasons for this league {possible_seasons_list}.
        super().__init__(self.message)

class PlayerDoesntHaveInfo(Exception):
    def __init__(self, path):
        self.message = fPlayer in path {path} doesnt have percentiles or similarities in his scouting report, try with another one.
El jugador en el path {path} no tiene percentiles o similitudes en su reporte de scouting, pruebe con otro."
        super().__init__(self.message)

class MatchDoesntHaveInfo(Exception):
    def __init__(self, path):
        self.message = f"Match in path {path} doesnt have enough information for this functions, try with another one.nEl partido en el path {path} no tiene la información para estas funciones, pruebe con otro.
        super().__init__(self.message)
        
class InvalidStrType(Exception):
    def __init__(self, param):
        self.message = f{param} must be a string.n{param} debe ser un string
        super().__init__(self.message)

