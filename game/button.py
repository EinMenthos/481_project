import pygame

class Button:
    """Creates a clickable button"""
    def __init__(
        self, screen, center, text, value, width, height, color, border_radius=20
    ):
        """Create an instance of a button"""
        self._screen = screen
        self._center = center
        self._value = value
        self._width = width
        self._height = height
        self._color = color
        self._original_color = color
        self._border_radius = border_radius
        self._rect =  pygame.Rect(
            self._center[0] - self._width,  self._center[1] - self._height, self._width, self._height
        )
        self._clicked = False
        # set the text
        font = pygame.font.Font(None, int(height / 1.5))
        self._text = font.render(text, True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self._rect.centerx
        self._textpos.centery = self._rect.centery

    @property
    def rect(self):
        """Returns the bounding rect"""
        return self._rect
    
    @property
    def value(self):
        """Returns the button's value"""
        return self._value
    
    @property
    def clicked(self):
        """Returns true if button has been clicked"""
        return self._clicked
    
    def draw(self):
        """Draw the button"""
        pygame.draw.rect(self._screen, self._color, self._rect, border_radius=self._border_radius)
        self._screen.blit(self._text, self._textpos)

    def process_events(self, event):
        """Determine if button is being clicked."""
        point = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            # Change the color of the button if the mouse is hovering over it
            if self.rect.collidepoint(point[0], point[1]):
                self._color = (255, 0, 0)
            else:
                self._color = self._original_color
    
        # Represent the button being clicked
        if self.rect.collidepoint(point) and event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed():
                self._clicked = True