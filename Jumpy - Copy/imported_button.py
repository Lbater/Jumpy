import pygame
import button

#create display window
SCREEN_WIDTH=800
SCREEN_HEIGHT=500

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button image
start_img=pygame.image.load('assets/Buttons/start_btn.png').convert_alpha()
exit_img=pygame.image.load('assets/Buttons/exit_btn.png').convert_alpha()

#create button instances
start_button=button.Button(100, 200, start_img, 0.8)
exit_button=button.Button(450, 200, exit_img, 0.8)

#game loop
run=True
while run:
     
    screen.fill((202, 228, 241))

    #draws the button
    if start_button.draw(screen):
        print('something')
    elif exit_button.draw(screen):
        run=False

     #event handler
    for event in pygame.event.get():
        #quit game
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
pygame.quit()