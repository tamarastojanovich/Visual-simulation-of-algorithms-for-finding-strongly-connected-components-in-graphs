import pygame
class Button:
    def __init__(self,x,y,width,height,text,font_sz,basecolor,hovercolor,text_color):
        pygame.init()
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,width,height)
        self.height=height
        self.width=width
        self.text=text
        self.font=font_sz
        self.basecolor=basecolor
        self.hovercolor=hovercolor
        self.text_color=text_color
        self.font = pygame.font.SysFont("ebrima", font_sz)
        self.is_hovered = False

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(x, y)
        
    def is_clicked(self):
        x, y = pygame.mouse.get_pos()
        return self.rect.collidepoint(x,y)

    def draw(self, screen:pygame.Surface):
        button_color = self.hovercolor if self.is_hovered else self.basecolor
        pygame.draw.rect(screen, button_color, self.rect,border_radius=50)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)