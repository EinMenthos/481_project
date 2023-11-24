class Player:
    """Creates a player for Connect 4"""
    def __init__(self, color, is_human, eval_func=0):
        """Initialize the Player"""
        self._color = color
        self._is_human = is_human
        self._eval_func = eval_func

    @property
    def color(self):
        """Returns the player's color"""
        return self._color

    @property
    def is_human(self):
        """Returns true if player is human"""
        return self._is_human
    
    @property
    def eval_func(self):
        """Returns the player's evaluation function to be used for minimax"""
        return self._eval_func
    
