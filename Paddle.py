import pygame

class Paddle:
    def __init__(self, screen, x, y, width, height, screen_width, screen_height):
        self.screen = screen

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dy = 0

        self.s_width = screen_width
        self.s_height = screen_height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt):
        if self.dy > 0:
            if self.rect.y + self.height < self.s_height:
                self.rect.y += self.dy*dt
        else:
            if self.rect.y >= 0:
                self.rect.y += self.dy*dt

    def render(self,color):
        pygame.draw.rect(self.screen, color, self.rect)