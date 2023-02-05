import pygame

class Bullet2 : 
    def __init__(self, x, y , to_x, to_y ) :
        self.pos = [x,y,10,10]
        self.to = [to_x , to_y ]
        self.color = (0, 190 , 0)

    def update_and_draw(self , dt, screen ) : 
        width , height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt*self.to[0]) % width
        self.pos[1] = (self.pos[1] + dt*self.to[1]) % height
        pygame.draw.rect(screen, self.color, self.pos )  # 사각형 모양의 총알 : bullet2