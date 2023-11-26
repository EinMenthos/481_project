import pygame

class Popup:
    """Class used to create pop-ups."""
    def __init__(self, screen, position, buttons, message='', size=(600, 600)):
        """Initialize a pop-up."""
        self._screen = screen
        self._message = message
        self._buttons = buttons
        self._position = position
        self._size = size
        self._color = (191, 228, 252)
        self._rect = pygame.Rect(position[0], position[1], size[0], size[1])

    @property
    def rect(self):
        """Return the bounding rect"""
        return self._rect

    @property
    def buttons(self):
        """Return a list of the pop-up's buttons"""
        return self._buttons

    def draw(self):
        """Draw the pop-up."""
        font = pygame.font.Font(None, int(self._size[1] * 0.10))
        text = font.render(self._message, True, (0,0,0))
        textpos = text.get_rect()
        textpos.centerx = self.rect.centerx
        textpos.centery = self.rect.centery - 103

        surface = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (191, 228, 252, 60), surface.get_rect())
        self._screen.blit(surface, self.rect)
        self._screen.blit(text, textpos)
        for button in self._buttons:
            button.draw()

    def process_events(self, event):
        """Process the game events."""
        for button in self._buttons:
            button.process_events(event)

    def update_message(self, message):
        """Update the pop-up's message"""
        self._message = message
