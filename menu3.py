import pygame 
from sys import exit
import time

pygame.init()
pygame.font.init()
lists=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]#,20]
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

class GreenSquare(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/green_square.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.rect=self.image.get_rect(topleft=(x,y))
    
    def update(self,selected_pos):
        self.current_co=self.rect.topleft
        self.layout_x=self.current_co[0]//40
        self.layout_y=self.current_co[1]//40
        if [self.layout_x,self.layout_y] not in selected_pos:
            self.kill()   

class Arrow(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/arrow.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image=pygame.transform.rotate(self.image,90)
        self.image_N=self.image
        self.image_E=pygame.transform.rotate(self.image,270)
        self.image_S=pygame.transform.rotate(self.image,180)
        self.image_W=pygame.transform.rotate(self.image,90)
        self.rect=self.image.get_rect(topleft=(x,y))

        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1]) 
    
    def update(self,selected_machines):
        self.current_co=self.rect.topleft
        self.layout_x=self.current_co[0]//40
        self.layout_y=self.current_co[1]//40
        self.co=[self.layout_x*40,self.layout_y*40]
        self.decimal_co=str(self.layout_x*40)+'.'+str(self.layout_y*40)
        print(self.layout_x,self.layout_y)

        if self.co not in selected_machines:
            self.kill()
            print('hio')
        else:
            if self.decimal_co in producer_info:
                if producer_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif producer_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif producer_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif producer_info[self.decimal_co][0]=='w':
                    self.image=self.image_W

            elif self.decimal_co in crafter_info:
                if crafter_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif crafter_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif crafter_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif crafter_info[self.decimal_co][0]=='w':
                    self.image=self.image_W

            elif self.decimal_co in conveyor_info:
                if conveyor_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif conveyor_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif conveyor_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif conveyor_info[self.decimal_co][0]=='w':
                    self.image=self.image_W

class Blueprints(pygame.sprite.Sprite):
    def  __init__(self,x,y):
        pass
    
class Producer(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/producer.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image_N=self.image
        self.image_E=pygame.transform.rotate(self.image,270)
        self.image_S=pygame.transform.rotate(self.image,180)
        self.image_W=pygame.transform.rotate(self.image,90)

        self.rect=self.image.get_rect(topleft=(x,y))
        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1])

    def update(self):
        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1])
        #print(self.decimal_co,producer_info)

        if self.decimal_co not in producer_info.keys():
            self.kill()
        else:
            if producer_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif producer_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif producer_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif producer_info[self.decimal_co][0]=='w':
                self.image=self.image_W

    def create_material(self,co):
        return Material(co)
        

class Material(pygame.sprite.Sprite):
    def __init__(self,co):
        super().__init__()
        self.image_copper=pygame.image.load('images/copper.png').convert_alpha()
        self.image_iron=pygame.image.load('images/iron.png').convert_alpha()
        self.image_gold=pygame.image.load('images/gold.png').convert_alpha()
        self.image_aluminium=pygame.image.load('images/aluminium.png').convert_alpha()
        self.image_coal=pygame.image.load('images/coal.png').convert_alpha()
        self.image_lead=pygame.image.load('images/lead.png').convert_alpha()
        self.spawn_co=co

        self.decimal_co=str(self.spawn_co[0])+'.'+str(self.spawn_co[1])
 
        if producer_info[self.decimal_co][1]=='copper':
            self.type='copper'
            self.image=self.image_copper
        elif producer_info[self.decimal_co][1]=='iron':
            self.type='iron'
            self.image=self.image_iron
        elif producer_info[self.decimal_co][1]=='gold':
            self.type='gold'
            self.image=self.image_gold
        elif producer_info[self.decimal_co][1]=='aluminium':
            self.type='aluminium'
            self.image=self.image_aluminium
        elif producer_info[self.decimal_co][1]=='lead':
            self.type='lead'
            self.image=self.image_lead
        elif producer_info[self.decimal_co][1]=='coal':
            self.type='coal'
            self.image=self.image_coal
        
        self.image=pygame.transform.scale(self.image,(20,20))

        self.amount= producer_info[self.decimal_co][2]
        self.rect=self.image.get_rect(center=(self.spawn_co[0]+20,self.spawn_co[1]+20))
        self.count=0
        self.producer_thrust=True
        self.conveyor_thrust=False
        self.previous_conveyor_pos=''  
   
    def update(self):
        self.this_producer_info=producer_info.get(self.decimal_co)
        if self.conveyor_thrust==False and self.producer_thrust==False:

            if pygame.sprite.spritecollideany(self,conveyor_group,pygame.sprite.collide_rect_ratio(1)):
                self.x= ((self.rect.x)//40)*40
                self.y= (((self.rect.y))//40)*40
                self.decimal_co=str(self.x)+'.'+str(self.y)
                if self.decimal_co!=self.previous_conveyor_pos:
                    self.conveyor_direction=conveyor_info.get(self.decimal_co)
                    self.conveyor_thrust=True
                    self.producer_thrust=False
                    self.count=0
                    self.previous_conveyor_pos=self.decimal_co
        self.count+=1
        

        if self.count<8 and self.producer_thrust==True:
            if self.this_producer_info is None:
                pass
            elif self.this_producer_info[0]=='n':
                self.rect.y-=5#*dt
            elif self.this_producer_info[0]=='e':
                self.rect.x+=5#*dt
            elif self.this_producer_info[0]=='s':
                self.rect.y+=5#*dt
            elif self.this_producer_info[0]=='w':
                self.rect.x-=5#*dt
        else:
            self.producer_thrust=False

        if self.count<16 and self.conveyor_thrust==True:
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
            self.conveyor_thrust=False

        if pygame.sprite.spritecollideany(self,crafter_group,pygame.sprite.collide_rect_ratio(1)):
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            if self.type in crafter_info[self.decimal_co][2]:
                self.stored_amount=crafter_info[self.decimal_co][2][self.type]
                crafter_info[self.decimal_co][2].update({self.type:self.stored_amount+self.amount})
            else:
                crafter_info[self.decimal_co][2].update({self.type:self.amount})

        if self.rect.x>1000:
            self.kill()
        elif self.rect.x<0:
            self.kill()
        elif self.rect.y>1000:
            self.kill()
        elif self.rect.y<0:
            self.kill()
        
    
class Items(pygame.sprite.Sprite):
    def __init__(self,co,item):
        super().__init__()
        self.image_circuit=pygame.image.load('images/circuit.png').convert_alpha()
        if item == 'circuit':
            self.image=self.image_circuit
            self.type='circuit'
        elif item == 'cell':
            self.image=self.image_cell
            self.type='cell'
        elif item == 'ram':
            self.image=self.image_cell
            self.type='ram'
        
        self.spawn_co=co
        self.image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect(center=(self.spawn_co[0]+20,self.spawn_co[1]+20))
        self.amount= 1
        self.count=0
        self.crafter_thrust=True
        self.conveyor_thrust=False
        self.previous_conveyor_pos=''
        self.decimal_co=str(co[0])+'.'+str(co[1])

    def update(self):
        self.this_crafter_info=crafter_info.get(self.decimal_co)
        if self.conveyor_thrust==False and self.crafter_thrust==False:
            if pygame.sprite.spritecollideany(self,conveyor_group,pygame.sprite.collide_rect_ratio(1)):
                self.x= ((self.rect.x)//40)*40
                self.y= (((self.rect.y))//40)*40
                self.decimal_co=str(self.x)+'.'+str(self.y)
                if self.decimal_co!=self.previous_conveyor_pos:
                    self.conveyor_direction=conveyor_info.get(self.decimal_co)
                    self.conveyor_thrust=True
                    self.crafter_thrust=False
                    self.count=0
                    self.previous_conveyor_pos=self.decimal_co
        self.count+=1
        

        if self.count<8 and self.crafter_thrust==True:
            if self.this_crafter_info is None:
                pass
            elif self.this_crafter_info[0]=='n':
                self.rect.y-=5#*dt
            elif self.this_crafter_info[0]=='e':
                self.rect.x+=5#*dt
            elif self.this_crafter_info[0]=='s':
                self.rect.y+=5#*dt
            elif self.this_crafter_info[0]=='w':
                self.rect.x-=5#*dt
        else:
            self.crafter_thrust=False

        if self.count<16 and self.conveyor_thrust==True:
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
            self.conveyor_thrust=False

        if pygame.sprite.spritecollideany(self,crafter_group,pygame.sprite.collide_rect_ratio(1)) and self.crafter_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            if self.type in crafter_info[self.decimal_co][2]:
                self.stored_amount=crafter_info[self.decimal_co][2][self.type]
                crafter_info[self.decimal_co][2].update({self.type:self.stored_amount+self.amount})
            else:
                crafter_info[self.decimal_co][2].update({self.type:self.amount})

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
        self.image_N=self.image
        self.image_E=pygame.transform.rotate(self.image,270)
        self.image_S=pygame.transform.rotate(self.image,180)
        self.image_W=pygame.transform.rotate(self.image,90)

        self.rect=self.image.get_rect(topleft=(x,y))
        self.decimal_co=str(x)+'.'+str(y)

    def update(self):
        
        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1])
        
        if self.decimal_co not in crafter_info:
            self.kill()
        else:
            if crafter_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif crafter_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif crafter_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif crafter_info[self.decimal_co][0]=='w':
                self.image=self.image_W

            self.item=crafter_info[self.decimal_co][1]
            self.item_bp=list(blueprints[self.item].keys())
            self.item_bp_components=len(self.item_bp)
            self.components_fulfilled=0
            self.craft=False

            for x in self.item_bp:
                if crafter_info[self.decimal_co][2].get(x)is not None:
                    if crafter_info[self.decimal_co][2].get(x)>=blueprints[self.item][x]:
                        self.components_fulfilled +=1
                else:
                    self.components_fulfilled=0
                    
            if self.components_fulfilled==self.item_bp_components:
                self.craft=True
            else:
                return False

            if self.craft==True:
                for x in self.item_bp:
                    crafter_info[self.decimal_co][2][x]-=blueprints[self.item][x]
                    self.co=self.decimal_co.split('.')
                    self.co[0]=int(self.co[0])
                    self.co[1]=int(self.co[1])
                self.craft=False
                print('crafted')
                return True
            else:
                return False

    def create_item(self):
        return Items(self.co,self.item)

class Conveyor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/conveyor.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image_N=self.image
        self.image_E=pygame.transform.rotate(self.image,270)
        self.image_S=pygame.transform.rotate(self.image,180)
        self.image_W=pygame.transform.rotate(self.image,90)
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
            elif conveyor_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif conveyor_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif conveyor_info[self.decimal_co][0]=='w':
                self.image=self.image_W
    
#screen set up
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption('assembly game')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((900,900))
white=(255,255,255)
surface.fill(white)
font = pygame.font.Font('Pixeltype.ttf',16)

#bars images
copper_img=pygame.image.load('images/copper.png').convert_alpha()
iron_img=pygame.image.load('images/iron.png').convert_alpha()
gold_img=pygame.image.load('images/gold.png').convert_alpha()
aluminium_img=pygame.image.load('images/aluminium.png').convert_alpha()
coal_img=pygame.image.load('images/coal.png').convert_alpha()
lead_img=pygame.image.load('images/lead.png').convert_alpha()
empty_slot_img=pygame.image.load('images/cross.png').convert_alpha()
#item images
circuit_img=pygame.image.load('images/circuit.png').convert_alpha()

crafter_inv_images={1:empty_slot_img,2:empty_slot_img,3:empty_slot_img,4:empty_slot_img,5:empty_slot_img,6:empty_slot_img,}
item_imgs={'empty':empty_slot_img,'copper':copper_img,'iron':iron_img,'gold':gold_img,'aluminium':aluminium_img,'lead':lead_img,'coal':coal_img,'circuit':circuit_img}
blueprints={'circuit':{'copper':3,'gold':1},'motherboard':{'circuit':6,'copper':10},'cpu':{},'ram':{},'power supply':{},'hdd':{},'cell':{},'engine':{},}
bp_ordered_list=['circuit','motherboard','ram','cpu','power supply','hdd','battery','engine']


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
selected_machines=[]
selection=''

producer_group=pygame.sprite.Group()
crafter_group=pygame.sprite.Group()
conveyor_group=pygame.sprite.Group()
material_group=pygame.sprite.Group()
items_group=pygame.sprite.Group()
green_square_group=pygame.sprite.Group()
arrows_group=pygame.sprite.Group()

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
transparent_popup.set_alpha(50)

#scrollbar images
scrollbar_img=pygame.image.load('images/scrollbar.png').convert_alpha()
scrollbar_img=pygame.transform.rotate(scrollbar_img,270)
slider_img=pygame.image.load('images/slider.png').convert_alpha()
#scrollbar button instantiation
scrollbar_button=Buttons(750,150,scrollbar_img,0.25,7)
slider_button=Buttons(750,150,slider_img,0.25,0.5)
slider_drag=False

#producer popup images:
producer_popup_img=pygame.image.load('images/gui_flat.png').convert_alpha()
producer_popup_surface=pygame.transform.scale(producer_popup_img,(200,225))
transparent_producer_popup_surface=pygame.transform.scale(producer_popup_img,(200,225))
transparent_producer_popup_surface.set_alpha(0)

#blueprint tabs images:
blueprint_tab_img=pygame.image.load('images/gui_flat.png').convert_alpha()
blueprint_tab_surface=pygame.transform.scale(blueprint_tab_img,(200,225))

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
shop_img=pygame.image.load('images/shop.png').convert_alpha()
edit_img=pygame.image.load('images/edit.png').convert_alpha()
blueprints_img=pygame.image.load('images/blueprints.png').convert_alpha()
map_img=pygame.image.load('images/button4.png').convert_alpha()
#play screen button instantiation
settings_mini_button=Buttons(0,0,settings_mini_img,0.5,0.5)
shop_button = Buttons(800,250,shop_img,0.5,0.5)
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
transparent_popup=Buttons(100,150,transparent_popup,3.5,7)
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

current_slider_pos=150



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
                elif transparent_grid_button.rect.collidepoint(co):
                    x,y=co[0],co[1]
                    x=(x//40)
                    y=(y-100)//40
                    if factory_layout[x][y]==1:
                        producer_cos=list(producer_info.keys())
                        crafter_cos=list(crafter_info.keys())
                        conveyor_cos=list(conveyor_info.keys())
                        x*=40
                        y*=40
                        decimal_co=str(x)+'.'+str(y)
                        if decimal_co in producer_cos:
                            co = [x+40,y+100]
                            selected_co=co
                            transparent_producer_popup=Buttons(co[0],co[1],transparent_producer_popup_surface,1,2.25)
                            copper_button=Buttons(co[0],co[1],copper_img,0.5,0.5)
                            iron_button=Buttons(co[0]+90,co[1],iron_img,0.5,0.5)
                            gold_button=Buttons(co[0],co[1]+40,gold_img,0.5,0.5)
                            aluminium_button=Buttons(co[0]+90,co[1]+40,aluminium_img,0.5,0.5)
                            coal_button=Buttons(co[0],co[1]+80,coal_img,0.5,0.5)
                            lead_button=Buttons(co[0]+90,co[1]+80,lead_img,0.5,0.5)
                            game_state='producer_popup'

                        elif decimal_co in crafter_cos:
                            co=[x+40,y+100]
                            for item in crafter_info[decimal_co][2]:
                                quantity = crafter_info[decimal_co][2][item]
                            
                            item_types=len(crafter_info[decimal_co][2].keys())
                            item_types_list=list(crafter_info[decimal_co][2].keys())

                            crafter_inv_item1='empty'
                            crafter_inv_item2='empty'
                            crafter_inv_item3='empty'
                            crafter_inv_item4='empty'
                            crafter_inv_item5='empty'
                            crafter_inv_item6='empty'
                            text1msg=0
                            text2msg=0
                            text3msg=0                                                                                                                    
                            text4msg=0
                            text5msg=0
                            text6msg=0


                            if item_types==0:
                                pass
                            elif item_types==1:
                                crafter_inv_item1=item_types_list[0]
                            elif item_types==2:
                                crafter_inv_item1=item_types_list[0]
                                crafter_inv_item2=item_types_list[1] 
                            elif item_types==3:
                                crafter_inv_item1=item_types_list[0]
                                crafter_inv_item2=item_types_list[1]
                                crafter_inv_item3=item_types_list[2]
                            elif item_types==4:
                                crafter_inv_item1=item_types_list[0]
                                crafter_inv_item2=item_types_list[1]
                                crafter_inv_item3=item_types_list[2]
                                crafter_inv_item4=item_types_list[3]
                            elif item_types==5:
                                crafter_inv_item1=item_types_list[0]
                                crafter_inv_item2=item_types_list[1]
                                crafter_inv_item3=item_types_list[2]
                                crafter_inv_item4=item_types_list[3]
                                crafter_inv_item5=item_types_list[4]
                            elif item_types==6:
                                crafter_inv_item1=item_types_list[0]
                                crafter_inv_item2=item_types_list[1]
                                crafter_inv_item3=item_types_list[2]
                                crafter_inv_item4=item_types_list[3]
                                crafter_inv_item5=item_types_list[4]
                                crafter_inv_item6=item_types_list[5]

                            if crafter_inv_item1=='empty':
                                text1msg=0
                            else:
                                text1msg=crafter_info[decimal_co][2][crafter_inv_item1]

                            if crafter_inv_item2=='empty':
                                text2msg=0
                            else:
                                text2msg=crafter_info[decimal_co][2][crafter_inv_item2]

                            if crafter_inv_item3=='empty':
                                text3msg=0
                            else:
                                text3msg=crafter_info[decimal_co][2][crafter_inv_item3]

                            if crafter_inv_item4=='empty':
                                text4msg=0
                            else:
                                text4msg=crafter_info[decimal_co][2][crafter_inv_item4]

                            if crafter_inv_item5=='empty':
                                text5msg=0
                            else:
                                text5msg=crafter_info[decimal_co][2][crafter_inv_item5]

                            if crafter_inv_item6=='empty':
                                text6msg=0
                            else:
                                text6msg=crafter_info[decimal_co][2][crafter_inv_item6]
                            
                            text1=font.render(str(text1msg),False,(0,0,0))
                            text2=font.render(str(text2msg),False,(0,0,0))
                            text3=font.render(str(text3msg),False,(0,0,0))
                            text4=font.render(str(text4msg),False,(0,0,0))
                            text5=font.render(str(text5msg),False,(0,0,0))
                            text6=font.render(str(text6msg),False,(0,0,0))
                            
                                
                            inv_button1=Buttons(co[0],co[1],item_imgs[crafter_inv_item1],0.25,0.25)
                            inv_button2=Buttons(co[0]+40,co[1],item_imgs[crafter_inv_item2],0.25,0.25)
                            inv_button3=Buttons(co[0]+80,co[1],item_imgs[crafter_inv_item3],0.25,0.25)
                            inv_button4=Buttons(co[0],co[1]+40,item_imgs[crafter_inv_item4],0.25,0.25)
                            inv_button5=Buttons(co[0]+40,co[1]+40,item_imgs[crafter_inv_item5],0.25,0.25)
                            inv_button6=Buttons(co[0]+80,co[1]+40,item_imgs[crafter_inv_item6],0.25,0.25)

                            co = [x+40,y+100]
                            selected_co=co
                            transparent_crafter_popup=Buttons(co[0],co[1],transparent_producer_popup_surface,1,2.25)
                            
                            game_state='crafter_popup'
                        elif decimal_co in conveyor_cos:
                            pass
                else:
                    pass 
            
            elif game_state=='producer_popup':
                if transparent_producer_popup.rect.collidepoint(co) == False:
                    game_state='play'
                elif copper_button.rect.collidepoint(co):
                    producer_info[decimal_co][1]='copper'
                    game_state='play'
                elif iron_button.rect.collidepoint(co):
                    producer_info[decimal_co][1]='iron'
                    game_state='play'
                elif gold_button.rect.collidepoint(co):
                    producer_info[decimal_co][1]='gold'
                    game_state='play'
                elif aluminium_button.rect.collidepoint(co):
                    producer_info[decimal_co][1]='aluminium'
                    game_state='play'
                elif coal_button.rect.collidepoint(co):
                    producer_info[decimal_co][1]='coal'
                    game_state='play'
                elif lead_button.rect.collidepoint(co):
                    producer_info[decimal_co][1]='lead'
                    game_state='play'
            
            elif game_state=='crafter_popup':
                if transparent_crafter_popup.rect.collidepoint(co) == False:
                    game_state='play'   
                #eli     f          

            elif game_state=='ingame_settings':
                if menu_button.rect.collidepoint(co):
                    game_state= 'main menu'
                elif resume_button.rect.collidepoint(co):
                    game_state='play'
                elif transparent_settings.rect.collidepoint(co) == False:
                    game_state='play'
                    
            elif game_state =='controls':
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
                elif slider_button.rect.collidepoint(co):
                    if event.button == 1: 
                        slider_drag=True
                        mouse_y=co[1]
                        offset_y=slider_button.rect.y-mouse_y    

            elif game_state=='blueprints':
                if transparent_popup.rect.collidepoint(co) == False:
                    game_state ='play'
                elif slider_button.rect.collidepoint(co):
                    if event.button == 1: 
                        slider_drag=True
                        mouse_y=co[1]
                        offset_y=slider_button.rect.y-mouse_y

            elif game_state=='shop confirm':
                if transparent_grid_button.rect.collidepoint(co):
                    grid_surface_copy=play_grid_bg
                    slider_drag=True
                    y=(y-100)//40
                    x=(x//40)

                    if factory_layout[x][y]==0:
                        if [x,y] in selected_pos:
                            selected_pos.remove([x,y])
                            selection='delete'
                            green_square_group.update(selected_pos)

                        else:
                            selected_pos.append([x,y])
                            new_GreenSquare=GreenSquare(x*40,y*40)
                            green_square_group.add(new_GreenSquare)
                            selection='place'

                    
                    green_square_group.draw(grid_surface_copy)
                    print('selected pos',selected_pos)

                elif confirm_button.rect.collidepoint(co):
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
                            crafter_info[decimal_co]=['n','circuit',{}]
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

                elif cancel_button.rect.collidepoint(co  ):
                    game_state='play'
                    selected_pos=[]

            elif game_state=='edit':
                if transparent_grid_button.rect.collidepoint(co):
                    slider_drag=True
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
                                selected_producers.remove(co)
                                selected_machines.remove(co)
                                arrows_group.update(selected_machines)
                                print(selected_machines)
                                selection='remove'
                                print(selected_producers,'selected producers')
                            else:
                                selected_producers.append(co)
                                selected_machines.append(co)
                                new_arrow = Arrow(int(co[0]),int(co[1]))
                                arrows_group.add(new_arrow)
                                selection='select'
                                print(selected_producers,'selected producers')

                        elif decimal_co in crafter_cos:
                            if co in selected_crafters:
                                selected_crafters.remove(co)
                                selected_machines.remove(co)
                                arrows_group.update(selected_machines)
                                selection='remove'
                            else:
                                selected_crafters.append(co)
                                selected_machines.append(co)
                                new_arrow = Arrow(int(co[0]),int(co[1]))
                                arrows_group.add(new_arrow)
                                selection='select'
                                print(selected_crafters,'selected crafters')

                        elif decimal_co in conveyor_cos:
                            if co in selected_conveyors:
                                selected_conveyors.remove(co) 
                                selected_machines.remove(co)
                                arrows_group.update(selected_machines)
                                selection='remove'
                            else:
                                selected_conveyors.append(co)
                                selected_machines.append(co)
                                new_arrow = Arrow(int(co[0]),int(co[1]))
                                arrows_group.add(new_arrow)
                                selection='select'
                                print(selected_conveyors,'selected connveyors')
                        
                        grid_surface_copy= grid_surface.copy()
                        screen.blit(grid_surface_copy,(0,100))
                        rotate_button.draw()
                        delete_button.draw()
                        confirm_button.draw()
                        cancel_button.draw()
                        producer_group.draw(grid_surface_copy)
                        crafter_group.draw(grid_surface_copy)
                        conveyor_group.draw(grid_surface_copy)
                        material_group.draw(grid_surface_copy) 
                        arrows_group.draw(grid_surface_copy)
                    
                    else:
                        pass

                elif rotate_button.rect.collidepoint(co):
                    for pos in selected_producers:
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        
                        if producer_info[decimal_co][0]=='n':
                            producer_info[decimal_co][0]='e'
                        elif producer_info[decimal_co][0]=='e':
                            producer_info[decimal_co][0]='s'
                        elif producer_info[decimal_co][0]=='s':
                            producer_info[decimal_co][0]='w'
                        elif producer_info[decimal_co][0]=='w':
                            producer_info[decimal_co][0]='n'

                    for pos in selected_crafters:
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        
                        if crafter_info[decimal_co][0]=='n':
                            crafter_info[decimal_co][0]='e'
                        elif crafter_info[decimal_co][0]=='e':
                            crafter_info[decimal_co][0]='s'
                        elif crafter_info[decimal_co][0]=='s':
                            crafter_info[decimal_co][0]='w'
                        elif crafter_info[decimal_co][0]=='w':
                            crafter_info[decimal_co][0]='n'

                    for pos in selected_conveyors:
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        
                        if conveyor_info[decimal_co]=='n':
                            conveyor_info[decimal_co]='e'
                        elif conveyor_info[decimal_co]=='e':
                            conveyor_info[decimal_co]='s'
                        elif conveyor_info[decimal_co]=='s':
                            conveyor_info[decimal_co]='w'
                        elif conveyor_info[decimal_co]=='w':
                            conveyor_info[decimal_co]='n'

                    #redraw rotated machines
                    producer_group.update()
                    crafter_group.update()
                    conveyor_group.update()
                    arrows_group.update(selected_machines)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    arrows_group.draw(grid_surface_copy)
                    print(producer_info)
                
                elif delete_button.rect.collidepoint(co):
                    print(selected_producers,'to delete')
                    for pos in selected_producers:
                        print(pos[0]/40)
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        producer_info.pop(decimal_co)
                    for pos in selected_crafters:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        conveyor_info.pop(decimal_co)

                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_machines=[]

                    grid_surface_copy= grid_surface.copy()
                    producer_group.update()
                    crafter_group.update()
                    conveyor_group.update()
                    arrows_group.update(selected_machines)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)

                elif confirm_button.rect.collidepoint(co):
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_machines=[]
                    arrows_group.update(selected_machines)  

                elif cancel_button.rect.collidepoint(co):
                    grid_surface_copy= grid_surface.copy()
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_machines=[]
                    arrows_group.update(selected_machines)

            
        elif event.type==pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                slider_drag=False

        elif event.type==pygame.MOUSEMOTION:
            co=pygame.mouse.get_pos()
            if slider_drag:
                if game_state=='blueprints':
                
                    if offset_y+mouse_y<150:
                            slider_button.rect.top=150
                    elif offset_y+mouse_y>800:
                        slider_button.rect.top=800
                    else:
                        mouse_y=co[1]
                        slider_button.rect.y=mouse_y+offset_y
                    current_slider_pos = slider_button.rect.y -150
                    bp_rotations=round(((len(lists)-8)/2)+1)
                                
                    #bp_rotations=round(((20-6)/2)+1)
                    print(current_slider_pos)
                    for x in range(1,bp_rotations+1):
                        scrollbar_section=(x*(round(650/bp_rotations)))
                        if current_slider_pos<scrollbar_section and current_slider_pos>((x-1)*(round(650/bp_rotations))):
                            print(scrollbar_section,'sections',((x-1)*(round(650/bp_rotations))))
                            bp_position = x*2
                            print(bp_position,'position')
                            list_length = len(lists)%8
                            print(len(lists),list_length,'remainder')
                            if (bp_position-1)<(len(lists)-(len(lists)%8)):
                                for y in range(0,8):
                                    print(lists[y+bp_position-2],'this')
                            else:
                                for x in range(list_length):
                                    print(lists[x],'this')

                elif game_state=='shop confirm':
                    print(selected_pos)
                    if transparent_grid_button.rect.collidepoint(co):
                        x=(co[0]//40)
                        y=(co[1]-100)//40
                        if factory_layout[x][y]==0:                      
                            if [x,y] not in selected_pos:
                                if selection=='place':
                                    selected_pos.append([x,y])
                                    new_GreenSquare=GreenSquare(x*40,y*40)
                                    green_square_group.add(new_GreenSquare)
                        
                            else:
                                if selection=='delete':
                                    selected_pos.remove([x,y])  
                                    green_square_group.update(selected_pos)
                                    
                        green_square_group.update(selected_pos)
                        green_square_group.draw(grid_surface_copy)
                        screen.blit(grid_surface_copy,(0,100))
                            
                elif game_state=='edit':
                        if transparent_grid_button.rect.collidepoint(co):
                            x=(co[0]//40)
                            y=(co[1]-100)//40
                            co =[x*40,y*40]
                            decimal_co=str(co[0])+'.'+str(co[1])
                            if factory_layout[x][y]==1:
                                if selection=='select':
                                    if decimal_co in producer_cos:
                                        if co not in selected_producers:
                                            selected_producers.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]))
                                            arrows_group.add(new_arrow)

                                    elif decimal_co in crafter_cos:
                                        if co not in selected_crafters:
                                            selected_crafters.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]))
                                            arrows_group.add(new_arrow)

                                    elif decimal_co in conveyor_cos:
                                        if co not in selected_conveyors:
                                            selected_conveyors.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]))
                                            arrows_group.add(new_arrow)

                                elif selection =='remove':
                                    if co in selected_machines:
                                        if decimal_co in producer_cos:
                                            if co in selected_producers:
                                                selected_producers.remove(co)
                                                selected_machines.remove(co)
                                                arrows_group.update(selected_machines)

                                        elif decimal_co in crafter_cos:
                                            if co in selected_producers:
                                                selected_crafters.remove(co)
                                                selected_machines.remove(co)
                                                arrows_group.update(selected_machines)


                                        elif decimal_co in conveyor_cos:
                                            if co in selected_producers:
                                                selected_conveyors.remove(co)   
                                                selected_machines.remove(co)  
                                                arrows_group.update(selected_machines)

                                        grid_surface_copy= grid_surface.copy()
                                        screen.blit(grid_surface_copy,(0,100))
                                        rotate_button.draw()
                                        delete_button.draw()
                                        confirm_button.draw()
                                        cancel_button.draw()
                                        producer_group.draw(grid_surface_copy)
                                        crafter_group.draw(grid_surface_copy)
                                        conveyor_group.draw(grid_surface_copy)
                                        material_group.draw(grid_surface_copy) 
                                        arrows_group.draw(grid_surface_copy)      
                                        print(selected_producers)    


    if game_state =='main menu':
        screen.blit(main_menu_bg,(0,0))
        play_button.draw()
        controls_button.draw()
        settings_button.draw()
        exit_button.draw()

    elif game_state=='play':
        if have_producer: 
            producer_group.update()
            material_group.update()

        if have_crafter:
            items_group.update()
            for crafter in crafter_group:
                if crafter.update()==True:
                    #crafter_group.update()==True:
                    items_group.add(crafter.create_item())
                    print(items_group)
       
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
        items_group.draw(grid_surface_copy)
        
        screen.blit(grid_surface_copy,(0,100))
        #copy screen
        play_grid_bg=grid_surface_copy.copy()
        play_bg=screen.copy()

    elif game_state=='producer_popup':
        screen.blit(grid_surface_copy,(0,100))
        screen.blit(producer_popup_surface,selected_co)
        transparent_producer_popup.draw()
        copper_button.draw()
        iron_button.draw()
        gold_button.draw()
        aluminium_button.draw()
        coal_button.draw()
        lead_button.draw()
    
    elif game_state=='crafter_popup':
        screen.blit(grid_surface_copy,(0,100))
        screen.blit(producer_popup_surface,selected_co)
        transparent_crafter_popup.draw()
        screen.blit(text1,(selected_co[0]+40,selected_co[1]+20))
        screen.blit(text2,(selected_co[0]+80,selected_co[1]+20))
        screen.blit(text3,(selected_co[0]+120,selected_co[1]+20))
        screen.blit(text4,(selected_co[0]+40,selected_co[1]+60))
        screen.blit(text5,(selected_co[0]+80,selected_co[1]+60))
        screen.blit(text6,(selected_co[0]+120,selected_co[1]+60))
        
        inv_button1.draw()
        inv_button2.draw()
        inv_button3.draw()
        inv_button4.draw()
        inv_button5.draw()
        inv_button6.draw()

    elif game_state=='shop':
        screen.blit(play_bg,(0,0))
        screen.blit(shop_surface,(100,150))
        transparent_popup.draw()
        producer_button.draw()
        crafter_button.draw()
        conveyor_button.draw()
        scrollbar_button.draw()
        slider_button.draw()

    elif game_state=='blueprints':
        screen.blit(play_bg,(0,0))
        screen.blit(shop_surface,(100,150))
        transparent_popup.draw()
        scrollbar_button.draw()
        slider_button.draw()
        blueprint_button1=Buttons(120,300,blueprint_tab_surface,1.5,1.25)
        blueprint_button2=Buttons(430,300,blueprint_tab_surface,1.5,1.25)
        blueprint_button3=Buttons(120,425,blueprint_tab_surface,1.5,1.25)
        blueprint_button4=Buttons(430,425,blueprint_tab_surface,1.5,1.25)
        blueprint_button5=Buttons(120,550,blueprint_tab_surface,1.5,1.25)
        blueprint_button6=Buttons(430,550,blueprint_tab_surface,1.5,1.25)
        blueprint_button7=Buttons(120,675,blueprint_tab_surface,1.5,1.25)
        blueprint_button8=Buttons(430,675,blueprint_tab_surface,1.5,1.25)
        blueprint_button1.draw()
        blueprint_button2.draw()
        blueprint_button3.draw()
        blueprint_button4.draw()
        blueprint_button5.draw()
        blueprint_button6.draw()
        blueprint_button7.draw()
        blueprint_button8.draw()

    elif game_state=='shop confirm':
        screen.blit(grid_surface_copy,(0,100))
        transparent_grid_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        green_square_group.update(selected_pos)
        green_square_group.draw(grid_surface_copy)
        
    elif game_state=='edit':
        screen.blit(grid_surface_copy,(0,100))
        rotate_button.draw()
        delete_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        arrows_group.draw(grid_surface_copy)
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
    clock.tick(60)

