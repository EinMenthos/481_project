class Player:
    """Creates a player for Connect 4"""
    def __init__(self, 
        color, 
        is_human,
        ef_mode=False, 
        ev1_set=False, 
        ev2_set=False,
        ev3_set=False,
        ev4_set=False,
        ev5_set=False,
        ev6_set=False):
        """Initialize the Player"""
        self._color = color
        self._is_human = is_human
        self._ef_mode = ef_mode
        self._ev1_set = ev1_set
        self._ev2_set = ev2_set
        self._ev3_set = ev3_set
        self._ev4_set = ev4_set
        self._ev5_set = ev5_set
        self._ev5_set = ev6_set


    @property
    def color(self):
        """Returns the player's color"""
        return self._color

    @property
    def is_human(self):
        """Returns true if player is human"""
        return self._is_human
    
    @property
    def ef_mode(self):
        """Returns True if player's evaluation function is customized"""
        return self._ef_mode
    
    @property
    def ev1_set(self):
        """Returns True if player is using Evaluation Function 1"""
        return self._ev1_set
    
    @property
    def ev1_set(self):
        """Returns True if player is using Evaluation Function 1"""
        return self._ev1_set
    
    @property
    def ev1_set(self):
        """Returns True if player is using Evaluation Function 1"""
        return self._ev1_set
    
    @property
    def ev2_set(self):
        """Returns True if player is using Evaluation Function 2"""
        return self._ev2_set
    
    @property
    def ev3_set(self):
        """Returns True if player is using Evaluation Function 3"""
        return self._ev3_set
    
    @property
    def ev4_set(self):
        """Returns True if player is using Evaluation Function 4"""
        return self._ev4_set
    
    @property
    def ev5_set(self):
        """Returns True if player is using Evaluation Function 5"""
        return self._ev5_set
    
    @property
    def ev6_set(self):
        """Returns True if player is using Evaluation Function 6"""
        return self._ev6_set
    
