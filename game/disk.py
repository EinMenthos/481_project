import pygame

class Disk(pygame.sprite.Sprite):
    """Creates a disk game piece"""
    # save and load the images
    _images = {'red': pygame.image.load('game/red_disk.bmp'), 
        'yellow': pygame.image.load('game/yellow_disk.bmp'),
        'white': pygame.image.load('game/white_disk.bmp')}

    def __init__(self, screen, color, center, width):
        """Initialize the disk based on color"""
        pygame.sprite.Sprite.__init__(self)
        self._screen = screen
        self._color = color
        self._center = center
        self._width = width
        # create the sprite
        self._sprite = pygame.transform.scale(Disk._images[color], (width, width))
        # get the bounding rect of the sprite
        self._rect = self._sprite.get_rect()
        self._rect.center = center # set the center

    @property
    def rect(self):
        """Returns the disk's bounding rect"""
        return self._rect
    
    @property
    def screen(self):
        """Returns the disk's screen"""
    
    @property
    def center(self):
        """Returns the disk's center"""
        return self._center
    
    @property
    def color(self):
        """Return the disk's color"""
        return self._color
    
    @property
    def width(self):
        """Return the disk's width"""
        return self._width
    
    @center.setter
    def center(self, center):
        """Setter to update the disk's center""" 
        self._center = center
        self._rect.center = center
    
    @color.setter
    def color(self, color):
        """Update sprite to match the new color"""
        self._sprite = pygame.transform.scale(Disk._images[color], (self._width, self._width))
        self._color = color

    def is_empty(self):
        """Returns True if the disk is empty (is white)"""
        if self._color != 'white':
            return False
        return True

    def draw(self):
        """Draw the sprite"""
        self._screen.blit(self._sprite, self.rect)
