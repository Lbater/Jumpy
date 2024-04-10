#import libraries
import pygame
import random
import os
import button
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy


#initialise pygame
mixer.init()
pygame.init()

#game window dimensions 
SCREEN_WIDTH=400
SCREEN_HEIGHT=600

#create gaem window
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

#set frame rate
clock=pygame.time.Clock()
FPS=60

#load in musioc and sound
pygame.mixer.music.load('assets/MUSIC/music_for_game.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1, 0.0)
jump_fx=pygame.mixer.Sound('assets/MUSIC/jump.mp3')
jump_fx.set_volume(0.2)
death_fx=pygame.mixer.Sound('assets/MUSIC/death.mp3')
death_fx.set_volume(0.3)

#game variables
SCROLL_THRESH=200
GRAVITY=1
MAX_PLATFORMS=10
scroll=0
bg_scroll=0
game_over=False
score=0
fade_counter=0
game_paused=True
menu_state='main'

if os.path.exists('score.txt'):
    with open('score.txt','r') as file:
        high_score=int(file.read())
else:
    high_score=0

#define colours
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
PANEL=(216,189,155)

#define font
font_small=pygame.font.SysFont('Arial Sans', 25)
font_big=pygame.font.SysFont('Arial Sans', 30)
font=pygame.font.SysFont("arialblack", 40)

#load buttons
resume_img=pygame.image.load("buttons/button_resume.png").convert_alpha()
options_img=pygame.image.load("buttons/button_options.png").convert_alpha()
quit_img=pygame.image.load("buttons/button_quit.png").convert_alpha()
video_img=pygame.image.load("buttons/button_video.png").convert_alpha()
audio_img=pygame.image.load("buttons/button_audio.png").convert_alpha()
keys_img=pygame.image.load("buttons/button_keys.png").convert_alpha()
back_img=pygame.image.load("buttons/button_back.png").convert_alpha()

#create button instances
resume_button=button.Button(110, 125, resume_img, 1)
options_button=button.Button(105, 250, options_img, 1)
quit_button=button.Button(142, 375, quit_img, 1)
video_button=button.Button(32, 75, video_img, 1)
audio_button=button.Button(31, 200, audio_img, 1)
keys_button=button.Button(52, 325, keys_img, 1)
back_button=button.Button(138, 450, back_img, 1)

#load imaages
jumpy_image=pygame.image.load('assets/Free/Main Characters/Ninja Frog/Jump.png').convert_alpha()
bg_img=pygame.image.load('assets/Free/Background/Brown.png').convert_alpha()
bg_img=pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
platform_image=pygame.image.load('assets/PNG/Pads/wood.png').convert_alpha()

#beird
bird_sheet_img=pygame.image.load('assets/Enemies/BlueBird/Bird.png').convert_alpha()
bird_sheet=SpriteSheet(bird_sheet_img)


#function for text to screen
def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)
    screen.blit(img, (x,y))

#function for score text
def draw_panel():
    pygame.draw.rect(screen, PANEL,(0, 0, SCREEN_WIDTH, 35))
    pygame.draw.line(screen, BLACK, (0,35), (SCREEN_WIDTH, 35), 2)
    draw_text('SCORE '+str(score), font_small, BLACK, 0, 5)

#function for background
def draw_bg(bg_scroll):
    screen.blit(bg_img, (0,0+bg_scroll))
    screen.blit(bg_img, (0,-600+bg_scroll))

#player class
class Player():
    def __init__(self, x, y):
        self.image=pygame.transform.scale(jumpy_image, (45, 45))
        self.width=25
        self.height=40
        self.rect=pygame.Rect(0, 0, self.width, self.height)
        self.rect.center=(x,y)
        self.vel_y=0
        self.flip=False

    def move(self):
        #reset variables
        scroll=0
        dx=0
        dy=0

        #proccess key presses
        key=pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx=-10
            self.flip=True
        if key[pygame.K_d]:
            dx=10
            self.flip=False

        #gravity
        self.vel_y+=GRAVITY
        dy+=self.vel_y

        #bounds detection
        if self.rect.left+dx<0:
            dx=-self.rect.left
        if self.rect.right+dx>SCREEN_WIDTH:
            dx=SCREEN_WIDTH-self.rect.right

        #check collision with platfornms
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
            #check if above the platform
                if self.rect.bottom<platform.rect.centery:
                    if self.vel_y>0:
                        self.rect.bottom=platform.rect.top
                        dy=0
                        self.vel_y=-20
                        jump_fx.play()



        #check collision with ground
        if self.rect.bottom+dy>SCREEN_HEIGHT:
            game_over=True

        #check if the player has gotten to the top
        if self.rect.top<=SCROLL_THRESH:
            #if player is dropping
            if self.vel_y<0:
                scroll= -dy


        #update rectangle position
        self.rect.x+=dx
        self.rect.y+=dy+scroll

        #update mask (more accurate hitbox)
        self.msk=pygame.mask.from_surface(self.image)

        return scroll
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-12, self.rect.y-5))
        #pygame.draw.rect(screen, WHITE, self.rect, 2) #player hitbox


#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(platform_image, (width, 10))
        self.moving=moving
        self.move_counter=random.randint(0,50)
        self.direction=random.choice([-1,1])
        self.speed=random.randint(1,2)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def update(self, scroll):
        #moving platform side to side
        if self.moving==True:
            self.move_counter+=1
            self.rect.x+=self.direction*self.speed
        
        #change platform direction if moved fully or hits a wall
        if self.move_counter>=100 or self.rect.left<0 or self.rect.right>SCREEN_WIDTH:
            self.direction*=-1
            self.move_counter=0

        #udate platforms up
        self.rect.y+=scroll

        #check if platform is visible
        if self.rect.top>SCREEN_HEIGHT:
            self.kill()


#player instance
jumpy=Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-150)

#create sprite groups
platform_group=pygame.sprite.Group()
enemy_group=pygame.sprite.Group()

#create starting platforms
platfrom=Platform(SCREEN_WIDTH//2-50, SCREEN_HEIGHT-50, 100, False)
platform_group.add(platfrom)

#game loop
run=True
while run:
    clock.tick(FPS)

    #check if game is paused
    if game_paused==True:
        pygame.mixer.music.stop()
        #check menu state
        if menu_state=='main':
            screen.fill(BLACK)
            #draw pause screen buttons
            if resume_button.draw(screen):
                game_paused=False
                pygame.mixer.music.load('assets/MUSIC/music_for_game.mp3')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1, 0.0)
            if options_button.draw(screen):
                menu_state='options'
            if quit_button.draw(screen):
                run=False
        #check if the options menu is open
        if menu_state=='options':
            screen.fill(BLACK)
            #draw teh different options buttons
            if video_button.draw(screen):
                draw_text('Yeah that doesnt work', font_big, WHITE, 85, 50)
            if audio_button.draw(screen):
                draw_text('Yeah that doesnt work', font_big, WHITE, 85, 175)
            if keys_button.draw(screen):
                draw_text('Yeah that doesnt work', font_big, WHITE, 85, 300)
            if back_button.draw(screen):
                menu_state='main'
    else:
        if game_over==False:
            #movement
            scroll=jumpy.move()

            #draw background
            bg_scroll+=scroll
            if bg_scroll>=600:
                bg_scroll=0
            draw_bg(bg_scroll)
            
            #generates platforms
            if len(platform_group)<MAX_PLATFORMS:
                p_w=random.randint(40,60)
                p_x=random.randint(0, SCREEN_WIDTH-p_w)
                p_y=platfrom.rect.y-random.randint(80,120)
                p_type=random.randint(1,2)
                if p_type==1 and score>500:
                    p_moving=True
                else:
                    p_moving=False
                platfrom=Platform(p_x, p_y, p_w, p_moving)
                platform_group.add(platfrom)


            #update platforms
            platform_group.update(scroll)

            #generate enemies
            if len(enemy_group)==0 and score>1500:
                enemy=Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
                enemy_group.add(enemy)

            #update enemy
            enemy_group.update(scroll, SCREEN_WIDTH)

            #update score
            if scroll>0:
                score+=scroll

            #draw line at previous highscore
            pygame.draw.line(screen, BLACK, (0, score-high_score+SCROLL_THRESH), (SCREEN_WIDTH, score-high_score+SCROLL_THRESH), 3)
            draw_text('HIGH SCORE', font_small, BLACK, SCREEN_WIDTH-130, score-high_score+SCROLL_THRESH)

            #draw panel
            draw_panel()

            #draw sprites
            platform_group.draw(screen)
            enemy_group.draw(screen)
            jumpy.draw()

            #temp enemy hitbox (use if needed)
            #for enemy in enemy_group:
                #pygame.draw.rect(screen, WHITE, enemy.rect, 2)
            
            #check game over
            if jumpy.rect.top>SCREEN_HEIGHT:
                game_over=True
                death_fx.play()
            #check collision with beird
            if pygame.sprite.spritecollide(jumpy, enemy_group, False): #checks if tehre was a collision
                if pygame.sprite.spritecollide(jumpy, enemy_group, False, pygame.sprite.collide_mask): #checks if it was with bird and not just open air near the bird but in the hitbox
                    game_over=True
                    death_fx.play()

        else:
            pygame.mixer.music.stop()
            if fade_counter<SCREEN_WIDTH:
                fade_counter+=5
                for y in range(0,6, 2):
                    pygame.draw.rect(screen, BLACK, (0, y*100, fade_counter, SCREEN_HEIGHT/6))
                    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH-fade_counter, (y+1)*100, SCREEN_WIDTH, SCREEN_HEIGHT/6))
            else:
                draw_text('GAME OVER!', font_big, RED, 130, 200)
                draw_text('SCORE: '+str(score), font_big, BLUE, 130, 250)
                draw_text('PRESS SPACE TO PLAY AGAIN!', font_big, WHITE, 40, 300)
                key=pygame.key.get_pressed()
                #update high score
                if score>high_score:
                    high_score=score
                    with open('score.txt','w') as file:
                        file.write(str(high_score))
                if key[pygame.K_SPACE]:
                    #reset variables
                    game_over=False
                    score=0
                    scroll=0
                    fade_counter=0
                    pygame.mixer.music.load('assets/MUSIC/music_for_game.mp3')
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(-1, 0.0)
                    #reposition jumopy
                    jumpy=Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-150)
                    #reset enemies
                    enemy_group.empty()
                    #reset platforms
                    platform_group.empty()
                    platfrom=Platform(SCREEN_WIDTH//2-50, SCREEN_HEIGHT-50, 100, False)
                    platform_group.add(platfrom)

    #event handler
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                game_paused=True
        if event.type==pygame.QUIT:
            run=False
            if score>high_score:
                high_score=score
                with open('score.txt','w') as file:
                    file.write(str(high_score))

    #update display window
    pygame.display.update()

pygame.quit()