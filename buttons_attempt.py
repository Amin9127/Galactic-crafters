import pygame 
from sys import exit

class Buttons():
    def __init__(self,x,y,image,scale):
        self.image=pygame.transform.scale(image, (200*scale, 100*scale))
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))


co=[0,1000]

#screen set up
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption('assembly game')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((900,900))
surface.fill('White')

#background images
grid_surface = pygame.image.load('images/grid.png').convert()
grid_surface=pygame.transform.scale(grid_surface,(800,800))

settings_surface=pygame.image.load('images/settings_panel.png').convert()
settings_surface=pygame.transform.scale(settings_surface,(450,500))


#button images
#main menu button images:
play_img = pygame.image.load('images/Play.png').convert_alpha()
controls_img = pygame.image.load('images/Controls.png').convert_alpha()
settings_img = pygame.image.load('images/Settings.png').convert_alpha()
exit_img = pygame.image.load('images/Exit.png').convert_alpha()
back_img = pygame.image.load('images/back.png').convert_alpha()
#play button images:
settings_mini_img=pygame.image.load('images/settings_mini.png').convert_alpha()
#settings tab button images
resume_img=pygame.image.load('images/resume.png').convert_alpha()
menu_img=pygame.image.load('images/menu.png').convert_alpha()


#main menu button instantiation
play_button=Buttons(350,150,play_img,1)
controls_button=Buttons(350,550,controls_img,1)
settings_button=Buttons(350,350,settings_img,1)
exit_button=Buttons(350,750,exit_img,1)
back_button=Buttons(0,0,back_img,1)

#play screen button instantiation
settings_mini_button=Buttons(0,0,settings_mini_img,0.5)
#settings tab button instantiation
resume_button=Buttons(480,570,resume_img,0.5)
menu_button=Buttons(300,570,menu_img,0.5)
click = False
def main_menu():
    run = True
    while run:
        screen.fill((52,78,91))
        co=pygame.mouse.get_pos()
        play_button.draw()
        controls_button.draw()
        settings_button.draw()
        exit_button.draw()

        if play_button.rect.collidepoint(co):
            if click:
                game()
        if controls_button.rect.collidepoint(co):
            if click:
                controls()
        if settings_button.rect.collidepoint(co):
            if click:
                settings()
        if exit_button.rect.collidepoint(co):
            if click:
                pygame.quit()
                exit()

        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                co = pygame.mouse.get_pos()
                if event.button==1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def game():
    run = True
    while run:
        screen.fill((52,78,91))
        co=pygame.mouse.get_pos()
        settings_mini_button.draw()
        screen.blit(grid_surface,(50,100))
        if settings_mini_button.rect.collidepoint(co):
             if click:
                play_bg=screen.copy()
                settings_mini(play_bg)

        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                co = pygame.mouse.get_pos()
                if event.button==1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def controls():
    run = True
    while run:
        screen.fill((52,78,91))
        co=pygame.mouse.get_pos()
        back_button.draw()
        if back_button.rect.collidepoint(co):
             if click:
                run=False

        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                co = pygame.mouse.get_pos()
                if event.button==1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def settings():
    run = True
    while run:
        screen.fill((52,78,91))
        co=pygame.mouse.get_pos()
        back_button.draw()
        if back_button.rect.collidepoint(co):
             if click:
                run=False

        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                co = pygame.mouse.get_pos()
                if event.button==1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def settings_mini(play_bg):
    run = True
    while run:
        screen.fill((52,78,91))
        co=pygame.mouse.get_pos()
        screen.blit(play_bg,(0,0))
        screen.blit(settings_surface,(226,150))
        resume_button.draw()
        menu_button.draw()
        if resume_button.rect.collidepoint(co):
             if click:
                run=False
        if menu_button.rect.collidepoint(co):
             if click:
                main_menu()

        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y=pygame.mouse.get_pos()
                co = pygame.mouse.get_pos()
                if event.button==1:
                    click = True
        pygame.display.update()
        clock.tick(60)
main_menu()