import pygame 
from sys import exit
import time

class Buttons():
    def __init__(self,x,y,image,scale_x,scale_y):
        self.image=pygame.transform.scale(image, (200*scale_x, 100*scale_y))
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))

def draw_text(text,font,text_colour,x,y):
    img=font.render(text,True,text_colour)
    screen.blit(img,(x,y))


class Producer(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/producer.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image_N=pygame.transform.rotate(self.image,180)
        self.image_E=pygame.transform.rotate(self.image,90)
        self.image_S=self.image
        self.image_W=pygame.transform.rotate(self.image,270)

        self.rect=self.image.get_rect(topleft=(x,y))

        self.decimal_co=str(x)+'.'+str(y)

    def update(self):
        self.current_co=self.rect.topleft
        x= self.current_co[0]
        y= self.current_co[1]
        self.decimal_co=str(x)+'.'+str(y)

        if self.decimal_co not in producer_info.keys():
            self.kill()
        else:
            if producer_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif producer_info[decimal_co][0]=='e':
                self.image=self.image_E
            elif producer_info[decimal_co][0]=='s':
                self.image=self.image_S
            elif producer_info[decimal_co][0]=='w':
                self.image=self.image_W

    def create_material(self,co):
        return Material(co)
    def rotate(self):
        self.image=pygame.transform.rotozoom(self.image,90,1)
        self.rect=self.image.get_rect(topleft=(x,y))
        

class Material(pygame.sprite.Sprite):
    def __init__(self,co):
        global producer_info,conveyor_info#,conveyor_group

        super().__init__()
        self.image=pygame.Surface((10,10))
        self.image.fill((255,0,0 ))
        self.rect=self.image.get_rect(center=(co[0]+20,co[1]+20))
        self.count=0
        self.producer_thrust=True
        self.conveyor_thrust=False

    def update(self):
        
        x,y=co[0],co[1]
        decimal_co=str(x)+'.'+str(y)
        this_producer_info=producer_info.get(decimal_co)
        conveyor_cos=list(conveyor_info.keys())

        if pygame.sprite.spritecollideany(self,conveyor_group):
            #if pygame.sprite.collide_rect_ratio(1)(self.rect,conveyor_group):
            #    print('full collision')
            print(self.rect.x,self.rect.y,'xy')
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            print(self.x,self.y,'cso')
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.conveyor_direction=conveyor_info[self.decimal_co]
            print(conveyor_info)
            self.conveyor_thrust=True
            self.producer_thrust=False
            self.count=0

        self.count+=1
        print(self.rect.x,self.rect.y,'y')
        

        if self.count<8 and self.producer_thrust==True:
            if this_producer_info is None:
                pass
            elif this_producer_info[0]=='n':
                self.rect.y-=5#*dt
            elif this_producer_info[0]=='e':
                self.rect.x+=5#*dt
            elif this_producer_info[0]=='s':
                self.rect.y+=5#*dt
            elif this_producer_info[0]=='w':
                self.rect.x-=5#*dt
        else:
            pass

        if self.count<8 and self.conveyor_thrust==True:
            if self.conveyor_direction=='n':
                self.rect.y-=5
            elif self.conveyor_direction=='e':
                self.rect.x+=5
            elif self.conveyor_direction=='s':
                self.rect.y+=5
            elif self.conveyor_direction=='w':
                self.rect.x-=5
            self.count+=1
        else:
            #self.conveyor_thrust=False
            pass


        if self.rect.x>1000:
            self.kill()
        elif self.rect.x<0:
            self.kill()
        elif self.rect.y>1000:
            self.kill()
        elif self.rect.y<0:
            self.kill()

class Crafter(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/crafter.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image_N=pygame.transform.rotate(self.image,180)
        self.image_E=pygame.transform.rotate(self.image,90)
        self.image_S=self.image
        self.image_W=pygame.transform.rotate(self.image,270)

        self.rect=self.image.get_rect(topleft=(x,y))

        self.decimal_co=str(x)+'.'+str(y)

    def update(self):
        self.current_co=self.rect.topleft
        x= self.current_co[0]
        y= self.current_co[1]
        self.decimal_co=str(x)+'.'+str(y)

        if self.decimal_co not in crafter_info.keys():
            self.kill()
        else:
            if crafter_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif crafter_info[decimal_co][0]=='e':
                self.image=self.image_E
            elif crafter_info[decimal_co][0]=='s':
                self.image=self.image_S
            elif crafter_info[decimal_co][0]=='w':
                self.image=self.image_W

class Conveyor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/conveyor.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image_N=pygame.transform.rotate(self.image,180)
        self.image_E=pygame.transform.rotate(self.image,90)
        self.image_S=self.image
        self.image_W=pygame.transform.rotate(self.image,270)

        self.rect=self.image.get_rect(topleft=(x,y))

        self.decimal_co=str(x)+'.'+str(y)

    def update(self):
        self.current_co=self.rect.topleft
        x= self.current_co[0]
        y= self.current_co[1]
        self.decimal_co=str(x)+'.'+str(y)

        if self.decimal_co not in conveyor_info.keys():
            self.kill()
        else:
            if conveyor_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif conveyor_info[decimal_co][0]=='e':
                self.image=self.image_E
            elif conveyor_info[decimal_co][0]=='s':
                self.image=self.image_S
            elif conveyor_info[decimal_co][0]=='w':
                self.image=self.image_W
    

factory_layout=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
selected_pos=[]


#producer_info={'0.0':['n','copper',1],}
producer_info={}
#crafter_info={'0.0':['n','circuit',{'input':0}]}
crafter_info={}
#conveyor_info={'0.0':'n'}
conveyor_info={}


selected_producers=[]
selected_crafters=[]
selected_conveyors=[]


producer_group=pygame.sprite.Group()
crafter_group=pygame.sprite.Group()
conveyor_group=pygame.sprite.Group()
material_group=pygame.sprite.Group()


have_producer=False
have_crafter=False
have_conveyor=False

#output factory layout
'''
for x in factory_layout:
    for y in x:
        print(y,end='')
    print()
'''

#screen set up
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption('assembly game')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((900,900))
white=(255,255,255)
surface.fill(white)

#background images
main_menu_bg=pygame.image.load('images/background.png').convert_alpha()
main_menu_bg=pygame.transform.scale(main_menu_bg,(900,900))
grid_img = pygame.image.load('images/grid.png').convert_alpha()
grid_surface=pygame.transform.scale(grid_img,(800,800))
transparent_grid=pygame.transform.scale(grid_img,(800,800))
transparent_grid.set_alpha(0)


settings_img=pygame.image.load('images/settings_panel.png').convert_alpha()
settings_surface=pygame.transform.scale(settings_img,(450,500))
transparent_settings_surface=pygame.transform.scale(settings_img,(450,500))
transparent_settings_surface.set_alpha(0)

blank_popup_img=pygame.image.load('images/panel8.png').convert_alpha()
shop_surface=pygame.transform.scale(blank_popup_img,(650,700))
transparent_popup = pygame.transform.scale(blank_popup_img,(650,700))
transparent_popup.set_alpha(0)

#sprite images:
producer_img=pygame.image.load('images/producer.png').convert_alpha()
crafter_img=pygame.image.load('images/crafter.png').convert_alpha()
conveyor_img=pygame.image.load('images/conveyor.png').convert_alpha()

#button images
#main menu button images:
play_img = pygame.image.load('images/Play.png').convert_alpha()
controls_img = pygame.image.load('images/Controls.png').convert_alpha()
settings_img = pygame.image.load('images/Settings.png').convert_alpha()
exit_img = pygame.image.load('images/Exit.png').convert_alpha()
back_img = pygame.image.load('images/back.png').convert_alpha()
#main menu button instantiation
play_button=Buttons(350,150,play_img,1,1)
controls_button=Buttons(350,550,controls_img,1,1)
settings_button=Buttons(350,350,settings_img,1,1)
exit_button=Buttons(350,750,exit_img,1,1)
back_button=Buttons(0,0,back_img,1,1)


#play button images:
settings_mini_img=pygame.image.load('images/settings_mini.png').convert_alpha()
blank_popup_img=pygame.image.load('images/button4.png').convert_alpha()
edit_img=pygame.image.load('images/button4.png').convert_alpha()
blueprints_img=pygame.image.load('images/button4.png').convert_alpha()
map_img=pygame.image.load('images/button4.png').convert_alpha()
#play screen button instantiation
settings_mini_button=Buttons(0,0,settings_mini_img,0.5,0.5)
shop_button = Buttons(800,250,blank_popup_img,0.5,0.5)
edit_button = Buttons(800,300,edit_img,0.5,0.5)
blueprints_button = Buttons(800,350,blueprints_img,0.5,0.5)
map_button = Buttons(800,400,map_img,0.5,0.5)


#settings tab button images
resume_img=pygame.image.load('images/resume.png').convert_alpha()
menu_img=pygame.image.load('images/menu.png').convert_alpha()
#settings tab button instantiation
resume_button=Buttons(480,570,resume_img,0.5,0.5)
menu_button=Buttons(300,570,menu_img,0.5,0.5)
transparent_settings=Buttons(225,150,transparent_settings_surface,2.25,5)


#shop button images:
mini_exit_img=pygame.image.load('images/mini_exit.png').convert_alpha()
#shop button instantiation
mini_exit_button=Buttons(250,400,mini_exit_img,0.5,0.5)
transparent_popup=Buttons(100,150,transparent_popup,3.25,7)
producer_button=Buttons(130,310,producer_img,0.5,0.5)
crafter_button=Buttons(230,310,crafter_img,0.5,0.5)
conveyor_button=Buttons(330,310,conveyor_img,0.5,0.5)

#shop confirm button images:
confirm_img=pygame.image.load('images/confirm.png').convert_alpha()
cancel_img=pygame.image.load('images/cancel.png').convert_alpha()
green_square_img=pygame.image.load('images/green_square.png').convert_alpha()
#shop confirm button instantiation 
transparent_grid_button=Buttons(0,100,transparent_grid,4,8)
confirm_button=Buttons(800,800,confirm_img,0.5,0.5)
cancel_button=Buttons(800,850,cancel_img,0.5,0.5)


#edit button images:
rotate_img =pygame.image.load('images/rotate.png').convert_alpha()
delete_img =pygame.image.load('images/delete.png').convert_alpha()
#edit button instantiation
rotate_button=Buttons(800,400,rotate_img,0.5,0.5)
delete_button=Buttons(800,450,delete_img,0.5,0.5)










#timers
change_event=pygame.USEREVENT
pygame.time.set_timer(change_event,1000)

last_time=time.time()
#main game
game_state='main menu'  

run=True
while run:
    #framerate independence
    dt=time.time() - last_time
    dt*=60
    last_time=time.time()

    screen.fill((52,78,91))

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type ==change_event:
            if game_state=='play':
                screen.blit(grid_surface,(0,100))
                producer_cos=list(producer_info.keys())
                for x in producer_cos:
                    co = x.split('.')
                    co[0]=int(co[0])
                    co[1]=int(co[1])
                    material_group.add(Producer.create_material('self',co))

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            co=pygame.mouse.get_pos()
            if game_state=='main menu':
                    if play_button.rect.collidepoint(co): 
                        game_state='play'
                    elif controls_button.rect.collidepoint(co):
                        game_state='controls'
                    elif settings_button.rect.collidepoint(co):
                        game_state='settings'
                    elif exit_button.rect.collidepoint(co):
                        pygame.quit()
                        exit()

            elif game_state=='play':
                if settings_mini_button.rect.collidepoint(co):
                    game_state='ingame_settings'
                elif shop_button.rect.collidepoint(co):
                    game_state='shop'
                elif edit_button.rect.collidepoint(co):
                    game_state='edit'    
                elif blueprints_button.rect.collidepoint(co):
                    game_state='blueprints'
                elif map_button.rect.collidepoint(co):
                    game_state='map'
                else:
                    pass

            elif game_state=='ingame_settings':
                if menu_button.rect.collidepoint(co):
                    game_state= 'main menu'
                elif resume_button.rect.collidepoint(co):
                    game_state='play'
                elif transparent_settings.rect.collidepoint(co) == False:
                    game_state='play'
                    
            elif game_state == 'controls':
                if back_button.rect.collidepoint(co):
                    game_state='main menu'

            elif game_state=='settings':
                if back_button.rect.collidepoint(co):
                    game_state='main menu'

            elif game_state=='shop':
                if producer_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='producer'
                elif crafter_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='crafter' 
                elif conveyor_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='conveyor'
                elif transparent_popup.rect.collidepoint(co) == False:
                    game_state ='play'

            elif game_state=='blueprints':
                if transparent_popup.rect.collidepoint(co) == False:
                    game_state ='play'

            elif game_state=='shop confirm':
                if confirm_button.rect.collidepoint(co):
                    game_state='play'
                    screen.blit(grid_surface,(0,100))
                    for co in selected_pos:
                        x= co[0]*40
                        y= co[1]*40
                        
                        decimal_co=str(x)+'.'+str(y)
                        str(decimal_co)
                        print(decimal_co)
                        if selected_machine =='producer':
                            producer_info[decimal_co]=['n','copper',1]
                            new_producer=Producer(x,y)
                            producer_group.add(new_producer)
                            factory_layout[co[0]][co[1]]=1
                            have_producer=True
                        elif selected_machine=='crafter':
                            crafter_info[decimal_co]=['n','nothing',{'input':0}]
                            new_crafter=Crafter(x,y)
                            crafter_group.add(new_crafter)
                            factory_layout[co[0]][co[1]]=1
                            have_crafter=True
                        elif selected_machine=='conveyor':
                            conveyor_info[decimal_co]='n'
                            new_conveyor=Conveyor(x,y)
                            conveyor_group.add(new_conveyor)
                            factory_layout[co[0]][co[1]]=1
                            have_conveyor=True
                            print(conveyor_info)
                    selected_pos=[]


                elif cancel_button.rect.collidepoint(co):
                    game_state='play'
                elif transparent_grid_button.rect.collidepoint(co):
                    y=(y-100)//40
                    x=(x//40)
                    if [x,y] in selected_pos:
                        selected_pos.remove([x,y])
                    else:
                        selected_pos.append([x,y])
                    for co in selected_pos:
                        x= co[0]*40
                        y= co[1]*40
                        #draw green squares
                        pygame.draw.rect(grid_surface_copy, (0,255,0), pygame.Rect(x,y, 40, 40))
                        screen.blit(grid_surface_copy,(0,100))
                    print('selected pos',selected_pos)

            elif game_state=='edit':
                if transparent_grid_button.rect.collidepoint(co):
                    x= co[0]
                    y= co[1]
                    layout_y=(y-100)//40
                    layout_x=(x//40)
                    decimal_co=str(layout_x)+'.'+str(layout_y)
                    x=layout_x*40
                    y=layout_y*40
                    co =[x,y]
                    decimal_co=str(x)+'.'+str(y)
                    print(decimal_co,'selected')
                    producer_cos=list(producer_info.keys())
                    crafter_cos=list(crafter_info.keys())
                    conveyor_cos=list(conveyor_info.keys())

                    if factory_layout[layout_x][layout_y]==1:
                        if decimal_co in producer_cos:
                            
                            if co in selected_producers:
                                co =[x,y]
                                selected_producers.pop(co)
                            selected_producers.append((x,y))
                            print(selected_producers,'selected producers')
                        elif decimal_co in crafter_cos:
                            selected_crafters.append((x,y))
                            print(selected_crafters,'selected crafters')
                        elif decimal_co in conveyor_cos:
                            selected_conveyors.append((x,y))
                            print(selected_conveyors)

                elif rotate_button.rect.collidepoint(co):
                    print(producer_info)
                    for co in selected_producers:
                        decimal_co=str(co[0])+'.'+str(co[1])
                        
                        if producer_info[decimal_co][0]=='n':
                            producer_info[decimal_co][0]='e'
                        elif producer_info[decimal_co][0]=='e':
                            producer_info[decimal_co][0]='s'
                        elif producer_info[decimal_co][0]=='s':
                            producer_info[decimal_co][0]='w'
                        elif producer_info[decimal_co][0]=='w':
                            producer_info[decimal_co][0]='n'

                    for co in selected_crafters:
                        decimal_co=str(co[0])+'.'+str(co[1])
                        
                        if crafter_info[decimal_co][0]=='n':
                            crafter_info[decimal_co][0]='e'
                        elif crafter_info[decimal_co][0]=='e':
                            crafter_info[decimal_co][0]='s'
                        elif crafter_info[decimal_co][0]=='s':
                            crafter_info[decimal_co][0]='w'
                        elif crafter_info[decimal_co][0]=='w':
                            crafter_info[decimal_co][0]='n'

                    for co in selected_conveyors:
                        decimal_co=str(co[0])+'.'+str(co[1])
                        
                        if conveyor_info[decimal_co]=='n':
                            conveyor_info[decimal_co]='e'
                        elif conveyor_info[decimal_co]=='e':
                            conveyor_info[decimal_co]='s'
                        elif conveyor_info[decimal_co]=='s':
                            conveyor_info[decimal_co]='w'
                        elif conveyor_info[decimal_co]=='w':
                            conveyor_info[decimal_co]='n'

                    #redraw rotated machines
                    grid_surface_copy= grid_surface.copy()
                    producer_group.update()
                    crafter_group.update()
                    conveyor_group.update()
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                

                elif delete_button.rect.collidepoint(co):
                    print(selected_producers,'to delete')
                    for co in selected_producers:
                        decimal_co=str(co[0])+'.'+str(co[1])
                        producer_info.pop(decimal_co)
                    for co in selected_crafters:
                        decimal_co=str(co[0])+'.'+str(co[1])
                        crafter_info.pop(decimal_co)
                    for co in selected_conveyors:
                        decimal_co=str(co[0])+'.'+str(co[1])
                        conveyor_info.pop(decimal_co)

                    grid_surface_copy= grid_surface.copy()
                    producer_group.update()
                    crafter_group.update()
                    conveyor_group.update()
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     

                elif confirm_button.rect.collidepoint(co):
                    game_state='play'

                elif cancel_button.rect.collidepoint(co):
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]

    if game_state =='main menu':
        screen.blit(main_menu_bg,(0,0))
        play_button.draw()
        controls_button.draw()
        settings_button.draw()
        exit_button.draw()

    elif game_state=='play':
        if have_producer: 
            producer_group.update()
            #for material in material_group:
            material_group.update()
 
            #for material in material_group:
            #    if material.count<9:
            #        material.update()
            #        #material.count+=1
            #        #print(material.count)
            #    else:
            #           pass


        if have_crafter:
            crafter_group.update()
       
        screen.fill((52,78,91))
        #buttons
        settings_mini_button.draw()
        shop_button.draw()
        edit_button.draw()
        blueprints_button.draw()
        map_button.draw()

        grid_surface_copy= grid_surface.copy()


        #machine stuff
        producer_group.draw(grid_surface_copy)
        crafter_group.draw(grid_surface_copy)
        conveyor_group.draw(grid_surface_copy)
        #materials
        material_group.draw(grid_surface_copy)
        
        screen.blit(grid_surface_copy,(0,100))

        #copy screen
        play_bg=screen.copy()

    
    elif game_state=='shop':
        screen.blit(play_bg,(0,0))
        screen.blit(shop_surface,(100,150))
        transparent_popup.draw()
        producer_button.draw()
        crafter_button.draw()
        conveyor_button.draw()

    elif game_state=='blueprints':
        screen.blit(play_bg,(0,0))
        screen.blit(shop_surface,(100,150))
        transparent_popup.draw()

    elif game_state=='shop confirm':
        screen.blit(grid_surface_copy,(0,100))
        transparent_grid_button.draw()
        confirm_button.draw()
        cancel_button.draw()

    elif game_state=='edit':
        screen.blit(grid_surface_copy,(0,100))
        rotate_button.draw()
        delete_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        if have_producer: 
            producer_group.update()

    elif game_state=='ingame_settings':
        screen.blit(play_bg,(0,0))
        screen.blit(settings_surface,(225,150))
        transparent_settings.draw()
        menu_button.draw()
        resume_button.draw()

    elif game_state =='controls':
        back_button.draw()

    elif game_state =='settings':
        back_button.draw()
 
    pygame.display.update()
    clock.tick(120)