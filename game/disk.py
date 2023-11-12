import pygame

class Disk(pygame.sprite.Sprite):
    """Creates a disk game piece"""
    # save and load the images
    _images = {'red': pygame.image.load('game/red_disk.bmp'), 
        'yellow': pygame.image.load('game/yellow_disk.bmp')}

    def __init__(self, screen, color, center, width):
        """Initialize the disk based on color"""
        pygame.sprite.Sprite.__init__(self)
        self._screen = screen
        self._color = color
        self._center = center
        self._width = width
        # set the sprite
        self._sprite = Disk._images[color]
        # get the bounding rect of the sprite
        self._rect = self._sprite.get_rect()
        self._rect.topleft = center

    @property
    def rect(self):
        """Returns bounding rect"""
        return self._rect
    
    def draw(self):
        """Draw the sprite"""
        self._screen.blit(self._sprite, self.rect.topleft)
