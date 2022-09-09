import pygame
from sys import exit
import time
x=0
y=0

producer_group=pygame.sprite.Group()

class Producer(pygame.sprite.Sprite):
    def __init__(self,x,y,producer_list):
        super().__init__()
        self.image=pygame.image.load('images/producer.png').convert_alpha()
        self.image=pygame.transform.rotate(self.image,90)
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.rect=self.image.get_rect(center=(x,y))
        if not pygame.sprite.spritecollideany(self,producer_group):
            print('hi')
            producer_list.append([x,y])
        self.kill()
        print(producer_list)
        print(producer_group)

    def update(self):
        producer_group.draw(screen)

    def create_material(self,co):
        return Material(co) 

class Material(pygame.sprite.Sprite):
    def __init__(self,co):
        global producer_list
        super().__init__()
        self.image=pygame.Surface((10,10))
        self.image.fill((255,0,0 ))
        #for co in producer_list:
        self.rect=self.image.get_rect(center=(co))

    def update(self):
        self.rect.x+=5*dt

        if self.rect.x>=800+200:
            self.kill()

producer_list=[[200,200]]

screen=pygame.display.set_mode((800,800))
pygame.display.set_caption('assembly game')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((800,800))
surface.fill('White')

clock=pygame.time.Clock()
change_event=pygame.USEREVENT
pygame.time.set_timer(change_event,1000)
time_counter=0
bg_surface=pygame.image.load('images/grid.png').convert()
bg_surface=pygame.transform.scale(bg_surface,(800,800))

producer=Producer(200,200,producer_list)
producer_group.add(producer)
material_group=pygame.sprite.Group() 


last_time=time.time()

while True:

    #framerate independence
    dt=time.time() - last_time
    dt*=60
    last_time=time.time()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            
            new_producer=Producer(x,y,producer_list)
            producer_group.add(new_producer)

        if event.type== change_event:
            for co in producer_list:
                material_group.add(Producer.create_material('self',co))


    if game_active:

        screen.blit(bg_surface,(0,0))

        material_group.draw(screen)
        producer_group.draw(screen)	
        producer_group.update()
        material_group.update()


    pygame.display.update() 
    clock.tick(120)