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
        """Returns bounding rect"""
        return self._rect
    
    @property
    def center(self):
        """Returns the sprite's center"""
        return self._center
    
    def draw(self):
        """Draw the sprite"""
        self._screen.blit(self._sprite, self.rect)