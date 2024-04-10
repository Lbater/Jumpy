import pygame
import button

pygame.init()

#create display window
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')

#game variables
game_paused=False
menu_state='main'

#define fonts
font=pygame.font.SysFont("arialblack", 40)

#define colours
WHITE=(255, 255, 255)

#load buttons
resume_img=pygame.image.load("buttons/button_resume.png").convert_alpha()
options_img=pygame.image.load("buttons/button_options.png").convert_alpha()
quit_img=pygame.image.load("buttons/button_quit.png").convert_alpha()
video_img=pygame.image.load("buttons/button_video.png").convert_alpha()
audio_img=pygame.image.load("buttons/button_audio.png").convert_alpha()
keys_img=pygame.image.load("buttons/button_keys.png").convert_alpha()
back_img=pygame.image.load("buttons/button_back.png").convert_alpha()

#create button instances
resume_button=button.Button(304, 125, resume_img, 1)
options_button=button.Button(297, 250, options_img, 1)
quit_button=button.Button(336, 375, quit_img, 1)
video_button=button.Button(226, 75, video_img, 1)
audio_button=button.Button(225, 200, audio_img, 1)
keys_button=button.Button(246, 325, keys_img, 1)
back_button=button.Button(332, 450, back_img, 1)

def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)
    screen.blit(img, (x, y))

run=True
while run:

    screen.fill((52, 78, 91))
    
    #check if game is paused
    if game_paused==True:
        #check menu state
        if menu_state=='main':
            #draw pause screen buttons
            if resume_button.draw(screen):
                game_paused=False
            if options_button.draw(screen):
                menu_state='options'
            if quit_button.draw(screen):
                run=False
        #check if the options menu is open
        if menu_state=='options':
            #draw the different options buttons
            if video_button.draw(screen):
                print('video settings')
            if audio_button.draw(screen):
                print('audio settings')
            if keys_button.draw(screen):
                print('change key bindings')
            if back_button.draw(screen):
                menu_state='main'
    else:
        draw_text("Press SPACE to pause", font, WHITE, 160, 250)

    #event handler
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                game_paused=True
        #quit game
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
pygame.quit()