import pygame
from player import Player
from bullet import Bullet
from bullet2 import Bullet2
from bullet3 import Bullet3
import random as rnd
import math
import time


def collision(obj1 , obj2 ) :
    if math.sqrt( (obj1.pos[0] - obj2.pos[0])**2 + 
                  (obj1.pos[1] - obj2.pos[1])**2 ) < 20 : 
        return True

    return False


def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

    
scores = []  

with open("scores.txt", "r") as f : 
    for line in f : 
        scores.append(float(line))  # scores.txt에 저장되어 있는 점수를 리스트에 저장

scores.sort(reverse = True)   


pygame.init()
WIDTH, HEIGHT = 1000, 800

clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("총알 피하기")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_image = pygame.image.load('bg.jpg')
bg_pos_x, bg_pos_y = -500,-500 

exps = []
exps.append(pygame.image.load('1.png'))
exps.append(pygame.image.load('2.png'))
exps.append(pygame.image.load('3.png'))

player = Player(WIDTH/2, HEIGHT/2)

# 총알1 
bullets = []
for i in range(7):
    bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))

# 총알2 
bullets2 = []
for i in range(7):
    bullets2.append(Bullet2(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))
    
# 총알3 
bullets3 = []
for i in range(7):
    bullets3.append(Bullet3(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))
    
    
time_for_adding_bullets = 0 
time_for_adding_bullets2 = 0
time_for_adding_bullets3 = 0 

playtime  = 0 

time.sleep(5)
clock.tick(FPS)

pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

x = 0
running = True
gameover = False
is_saved = False

exp = False # 총알 맞았을때 사용할 변수
t = [0,1]  # 총알 맞았을때 그림 효과 재생 시간을 지정하기 위한 리스트


# 생명력 도입 
life = 5

while running:
    
    dt = clock.tick(FPS)
    
    
    if gameover == False : 
        playtime += dt

        
        # 총알 수 늘리기 ( bullet, bullet2, bullet3 모두 )
        
        time_for_adding_bullets += dt
        time_for_adding_bullets2 += dt
        time_for_adding_bullets3 += dt
        
        if time_for_adding_bullets >= 2000 : 
            bullets.append(Bullet(0 , rnd.random()*HEIGHT , rnd.random()-0.5 , rnd.random()-0.5))
            time_for_adding_bullets -= 2000
            
        if time_for_adding_bullets2 >= 2000 : 
            bullets2.append(Bullet2(0 , rnd.random()*HEIGHT , rnd.random()-0.5 , rnd.random()-0.5))
            time_for_adding_bullets2 -= 2000
            
        if time_for_adding_bullets3 >= 2000 : 
            bullets3.append(Bullet3(0 , rnd.random()*HEIGHT , rnd.random()-0.5 , rnd.random()-0.5))
            time_for_adding_bullets3 -= 2000


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, -1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, 1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, 1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, -1)

    
    screen.fill((0,0,0)) 

    # 비행기의 움직임에 따라 배경그림이 움직이도록  
    screen.blit(bg_image , (bg_pos_x ,bg_pos_y ))
    bg_pos_x -= dt*player.to[0] * 0.2
    bg_pos_y -= dt*player.to[1] * 0.2
    
    # 생명력을 나타내는 막대기 ( 생명이 줄어들수록 초록 막대기의 크기 감소 )
    pygame.draw.rect(screen, (0,255,0) , [520, 10 , 300 , 30 ])
    pygame.draw.rect(screen, (255,0,0), [520,10, 60*(5- math.ceil(life)),30])
    

    player.update(dt, screen)
    player.draw(screen)


    for b in bullets : 
        b.update_and_draw(dt, screen)
        
    for b2 in bullets2 : 
        b2.update_and_draw(dt, screen)
    
    for b3 in bullets3 : 
        b3.update_and_draw(dt, screen)
    
                                       # Bullets : bullet , bullet2, bullet3의 총 개수         # 생명력 점수
    txt = f"Time : {playtime/1000:.1f}, Bullets : {len(bullets)+len(bullets2)+len(bullets3)} , Life : {math.ceil(life)}"
    draw_text(txt, 32, (10,10), (225,225,225))

    
    # 총알에 맞았을 때 오른쪽 상단에 터지는 그림 효과를 나타냄
    if exp :
        screen.blit(exps[(playtime//50)% len(exps)], (840,2))
        if len(t) == 2 : 
            t.append(playtime/1000)
    
    if len(t) == 3 : 
        if (playtime/1000) - t[2] >  0.7 :  # 0.7초간 그림 효과 재생
            exp = False
            t.pop()
        
    if gameover : 
        # 점수 저장하기
        if not is_saved : 
            thistime = playtime/1000
            scores.append(thistime)
            scores.sort(reverse = True )
            is_saved = True
            if len(scores) > 10 : 
                scores = scores[:10]  # 상위 10개의 점수만 저장하기
            with open("scores.txt", "w") as f :
                for s in scores :
                    f.write(f"{s}\n")
            
            
        txt = "Game over"
        draw_text(txt , 100, (WIDTH/2-300 ,HEIGHT/2-50), (255,255,255)) 
        # 현재 기록이 순위권일때와 아닐때의 색상을 다르게해서 출력
        if thistime in scores : 
            draw_text(f"time : {playtime/1000:.1f}" , 50, (WIDTH/2+70 ,HEIGHT/2+50), (255,255,0))
        else : 
            draw_text(f"time : {playtime/1000:.1f}" , 50, (WIDTH/2+70 ,HEIGHT/2+50), (255,255,255))
        
    
    pygame.display.update()


    # 충돌 체크
    if life > 0 : 
 
        # 비행기와 총알1과의 거리 측정 및 효과음 발생
        for b in bullets:
            if collision(player, b):
                end_sound = pygame.mixer.Sound('endsound.wav')  
                pygame.mixer.Sound.play(end_sound)
                exp = True  # 터지는 그림 효과를 위해 exp를 True로 바꿔줌
                life -= 0.2 # 총알의 종류에 따라 생명력의 차감 정도가 다름
        
        # 비행기와 총알2와의 거리 측정 및 효과음 발생
        for b2 in bullets2:
            if collision(player, b2):
                end_sound = pygame.mixer.Sound('endsound.wav') 
                pygame.mixer.Sound.play(end_sound)
                exp = True # 터지는 그림 효과를 위해 exp를 True로 바꿔줌
                life -= 0.4 # 총알 종류에 따라 생명력의 차감 정도가 다름
                
        # 비행기와 총알3와의 거리 측정 및 효과음 발생
        for b3 in bullets3:
            if collision(player, b3):
                end_sound = pygame.mixer.Sound('endsound.wav') 
                pygame.mixer.Sound.play(end_sound)
                exp = True # 터지는 그림 효과를 위해 exp를 True로 바꿔줌
                life -= 0.3 # 총알 종류에 따라 생명력의 차감 정도가 다름
                
        
    else :
        gameover = True  # life가 0 이하로 떨어지면 gameover
            