import pygame 
from sys import exit
import time
from button_functions import *
from classes import *
pygame.init()
pygame.font.init()

class Buttons():
    def __init__(self,x,y,image,scale_x,scale_y):
        self.image=pygame.transform.scale(image, (200*scale_x, 100*scale_y))
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))

def draw_money():
    screen.blit(money_panel_img,(200,0))
    counter=0
    money1=money
    abbreviation={0:'',1:'K',2:'M',3:'B',4:'T',5:'q',6:'Q'}
    allowed=True
    while allowed:
        money1=money1//1000
        if money1 >=10:
            counter+=1
        else:
            allowed=False


    money_msg=str(round(money/(1000**(counter)),1))+str(abbreviation[counter])
    money_text=font_50.render(money_msg,None,100)
    money_text_rect=money_text.get_rect(center=(400,38))
    screen.blit(money_text,money_text_rect)

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

        self.decimal_co=str(x)+'.'+str(y) 

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
    def  __init__(self,title_position,y):
        super().__init__()
        self.bp_item_images={0:'empty',1:empty_slot_img,2:empty_slot_img,3:empty_slot_img,4:empty_slot_img,5:empty_slot_img}

        self.image=pygame.image.load('images/gui_flat.png').convert_alpha()
        self.image=pygame.transform.scale(self.image,(300,135))
        self.rect=self.image.get_rect(topleft=blueprint_position[y])

        self.bp_title = bp_ordered_list[title_position]
        self.bp_items=blueprints[self.bp_title].keys()
        self.count=0

        for item in self.bp_items:
            self.bp_item_images[self.count]=item_imgs[item]
            self.count+=1

        #self.text1=font.render(str(text1msg),False,(0,0,0))
        #self.text2=font.render(str(text2msg),False,(0,0,0))
        #self.text3=font.render(str(text3msg),False,(0,0,0))
        #self.text4=font.render(str(text4msg),False,(0,0,0))
        #self.text5=font.render(str(text5msg),False,(0,0,0))
        #self.text6=font.render(str(text6msg),False,(0,0,0))
        

       #self.image.blit(item_imgs[self.bp_item_images[0]],self.rect)
       #self.item_button1=Buttons(co[0],co[1],item_imgs[self.bp_item_images[0]],0.25,0.25)
       #self.item_button2=Buttons(co[0]+40,co[1],item_imgs[self.bp_item_images[1]],0.25,0.25)
       #self.item_button3=Buttons(co[0]+80,co[1],item_imgs[self.bp_item_images[2]],0.25,0.25)
       #self.item_button4=Buttons(co[0],co[1]+40,item_imgs[self.bp_item_images[3]],0.25,0.25)
       #self.item_button5=Buttons(co[0]+40,co[1]+40,item_imgs[self.bp_item_images[4]],0.25,0.25)
       #self.item_button6=Buttons(co[0]+80,co[1]+40,item_imgs[self.bp_item_images[5]],0.25,0.25)

    def update(self):
        self.item_button1.draw()
        #self.item_button2.draw()
        #self.item_button3.draw()
        #self.item_button4.draw()
        #self.item_button5.draw()
        #self.item_button6.draw()
        
#new_bp= Blueprints(2)
#blueprints_group.add(new_bp)
        

        
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
        self.worth=blueprints_value[self.type]

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

        if pygame.sprite.spritecollideany(self,seller_group,pygame.sprite.collide_rect_ratio(1)) and self.crafter_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            money+=self.worth
            


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




#screen set up
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption('assembly game')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((900,900))
white=(255,255,255)
surface.fill(white)
font = pygame.font.Font('Pixeltype.ttf',16)
font_50 = pygame.font.Font('Pixeltype.ttf',50)
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
blueprints={'circuit':{'copper':3,'gold':1},'motherboard':{'circuit':6,'copper':10},'cpu':{},'ram':{},'power supply':{},'hdd':{},'battery':{},'engine':{},}
blueprints_value={'circuit':1,'motherboard':1, 'cpu':1,'ram':1,'power supply':1,'hdd':1,'battery':1,'engine':1}

bp_ordered_list=['circuit','motherboard','ram','cpu','power supply','hdd','battery','engine']#,'item 9','item 10','item 11','item 12']
lists=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
bptitles2=['nothing','nothing','nothing','nothing','nothing','nothing','nothing','nothing']
bptitles={0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:''}
factory_layout=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
selected_pos=[]

#producer_info={'0.0':['n','copper',1],}
producer_info={}
#crafter_info={'0.0':['n','circuit',{'input':0}]}
crafter_info={}
#conveyor_info={'0.0':'n'}
conveyor_info={}
#seller_info=['0.0':'n']
seller_info={}

global money
money=0


selected_producers=[]
selected_crafters=[]
selected_conveyors=[]
selected_sellers=[]
selected_machines=[]
selection=''

producer_group=pygame.sprite.Group()
crafter_group=pygame.sprite.Group()
conveyor_group=pygame.sprite.Group()
material_group=pygame.sprite.Group()
items_group=pygame.sprite.Group()
seller_group=pygame.sprite.Group()

green_square_group=pygame.sprite.Group()
arrows_group=pygame.sprite.Group()
blueprints_group=pygame.sprite.Group()

have_producer=False
have_crafter=False
have_conveyor=False
have_seller=False


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
blueprint_position={0:[20,145],1:[330,145],2:[20,280],3:[330,280],4:[20,415],5:[330,415],6:[20,550 ],7:[330,550]}
titles_done_rotation = -1

#money panel
money_panel_img=pygame.image.load('images/panel3.png').convert_alpha()
#money_panel_surface=pygame.transform.scale(money_panel_img,(400,70))

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
seller_img=pygame.image.load('images/seller.png').convert_alpha()

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
seller_button=Buttons(430,310,seller_img,0.5,0.5)

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

        #all keybinds check and what it does in this if elif ladder
        if event.type == pygame.KEYDOWN:

            if game_state=='main menu':
                if event.key == pygame.K_p:
                    game_state='play'
                elif event.key==pygame.K_c:
                    game_state='controls'
                elif event.key==pygame.K_s:
                    game_state='settings'
                elif event.key==pygame.K_q:
                    pygame.quit()
                    exit()

            elif game_state == 'play':
                if event.key == pygame.K_ESCAPE:
                    game_state='ingame_settings'
                elif event.key == pygame.K_s:
                    game_state='shop'
                elif event.key == pygame.K_e:
                    game_state='edit'
                elif event.key == pygame.K_b:
                    game_state='blueprints'
                elif event.key == pygame.K_m:
                    game_state='map'

            elif game_state=='ingame settings':
                if event.key == pygame.K_ESCAPE:
                    game_state='main menu'
                elif event.key == pygame.K_SPACE:
                    game_state='play'
             
            elif game_state=='controls':
                if event.key == pygame.K_ESCAPE:
                    game_state='main menu'

            elif game_state == 'settings':
                if event.key == pygame.K_ESCAPE:
                    game_state='main menu'

            elif game_state=='shop':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'play'
                elif event.key == pygame.K_1:
                    game_state='shop confirm'
                    selected_machine='producer'
                elif event.key == pygame.K_2:
                    game_state='shop confirm'
                    selected_machine='crafter'
                elif event.key == pygame.K_3:
                    game_state='shop confirm'
                    selected_machine='conveyor'
                elif event.key == pygame.K_4:
                    game_state='shop confirm'
                    selected_machine='seller'

            elif game_state == 'blueprints':
                if event.key == pygame.K_ESCAPE:    
                    game_state= 'play'
            
            elif game_state == 'shop confirm':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'shop'
                elif event.key == pygame.K_RETURN:
                    print('enter')
                    game_state = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout)
                    selected_pos=[]

            elif game_state == 'edit':
                if event.key==pygame.K_BACKSPACE:
                    
                    grid_surface_copy= grid_surface.copy()
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_sellers=[]
                    selected_machines=[]
                    arrows_group.update(selected_machines)

                elif event.key ==pygame.K_RETURN:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_machines=[]
                    selected_sellers=[]
                    arrows_group.update(selected_machines)  
                
                elif event.key ==pygame.K_r:
                    rotate(selected_producers,selected_machines,arrows_group,material_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy)
                elif event.key ==pygame.K_x:
                    #delete(factory_layout,selected_producers,producer_info,producer_group,crafter_info,selected_crafters,crafter_group,selected_conveyors,conveyor_info,conveyor_group,arrows_group,material_group,grid_surface)
                    print(selected_producers,'to delete')
                    print(producer_info)
                    for pos in selected_producers:
                        print(pos[0]/40)
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        producer_info.pop(decimal_co)
                    print(producer_info)
                    for pos in selected_crafters:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        conveyor_info.pop(decimal_co)
                    for pos in selected_sellers:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        seller_info.pop(decimal_co)

                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_sellers=[]
                    selected_machines=[]


                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update()
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
            
            elif game_state=='map':
                if event.key==pygame.K_ESCAPE:
                    game_state='play'
 
 
 #¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬           
        #all button check and what the button does in this if elif ladder
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

                    bp_title1=font.render(str(lists[0]),False,(0,0,0))
                    bp_title2=font.render(str(lists[1]),False,(0,0,0))
                    bp_title3=font.render(str(lists[2]),False,(0,0,0))
                    bp_title4=font.render(str(lists[3]),False,(0,0,0))
                    bp_title5=font.render(str(lists[4]),False,(0,0,0))
                    bp_title6=font.render(str(lists[5]),False,(0,0,0))
                    bp_title7=font.render(str(lists[6]),False,(0,0,0))
                    bp_title8=font.render(str(lists[7]),False,(0,0,0))

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
                #elif          

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
                elif seller_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='seller'
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
                    game_state = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout)
                    selected_pos=[]
                elif cancel_button.rect.collidepoint(co):
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
                    seller_cos=list(seller_info.keys())

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
                    
                elif rotate_button.rect.collidepoint(co):
                    rotate(selected_producers,selected_machines,arrows_group,material_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy)
      
                elif delete_button.rect.collidepoint(co):
                    #delete(factory_layout,selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,arrows_group,material_group,grid_surface)
                    print(selected_producers,'to delete')
                    print(producer_info)
                    for pos in selected_producers:
                        print(pos[0]/40)
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        producer_info.pop(decimal_co)
                    print(producer_info)
                    for pos in selected_crafters:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        conveyor_info.pop(decimal_co)
                    for pos in selected_sellers:
                        factory_layout[int(pos[0]/40)][int(pos[1]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        seller_info.pop(decimal_co)


                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_machines=[]
                    selected_sellers=[]

                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update()
                    conveyor_group.update(conveyor_info)
                    arrows_group.update(selected_machines)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)

                elif confirm_button.rect.collidepoint(co):
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_sellers=[]
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

                    #slider movement mechanism
                    if offset_y+mouse_y<150:
                            slider_button.rect.top=150
                    elif offset_y+mouse_y>800:
                        slider_button.rect.top=800
                    else:
                        mouse_y=co[1]
                        slider_button.rect.y=mouse_y+offset_y

                    #blueprint rotation algorithm
                    current_slider_pos = slider_button.rect.y -150
                    bp_rotations=round(((len(lists)-8)/2)+1)  
                    for x in range(1,bp_rotations+1):
                        
                        scrollbar_section=(x*(round(650/bp_rotations)))
                        if current_slider_pos<scrollbar_section and current_slider_pos>((x-1)*(round(650/bp_rotations))):

                            if titles_done_rotation==x:
                                pass
                            else:
                                current_rotation=x
                                print((x-1)*(round(650/bp_rotations)),'sections',scrollbar_section)
                                bp_position = (x*2)-2
                                remaining_bp=len(lists)-(bp_position+8)
                                if remaining_bp<=1:
                                    for y in range(0,6):
                                        bptitles2[y]=lists[y+bp_position]
                                        #new_bp= Blueprints(y+bp_position,y)
                                        #blueprints_group.add(new_bp)
                                        

                                        
                                    bptitles2[6]=lists[len(lists)-1]
                                    bptitles2[7]='nothing'

                                
                                else:
                                    for y in range(0,8):
                                        bptitles2[y]=lists[y+bp_position]
                                        #new_bp= Blueprints((y+bp_position),y)
                                        #print(y)
                                        #blueprints_group.add(new_bp)
                                titles_done_rotation = x
                                print('done')
                        

                    bp_title1=font.render(str(bptitles2[0]),False,(0,0,0))
                    bp_title2=font.render(str(bptitles2[1]),False,(0,0,0))
                    bp_title3=font.render(str(bptitles2[2]),False,(0,0,0))
                    bp_title4=font.render(str(bptitles2[3]),False,(0,0,0))
                    bp_title5=font.render(str(bptitles2[4]),False,(0,0,0))
                    bp_title6=font.render(str(bptitles2[5]),False,(0,0,0))
                    bp_title7=font.render(str(bptitles2[6]),False,(0,0,0))
                    bp_title8=font.render(str(bptitles2[7]),False,(0,0,0))

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

                                    elif decimal_co in seller_cos:
                                        if co not in selected_sellers:
                                            selected_sellers.append(co)
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

                                        elif decimal_co in seller_cos:
                                            if co in selected_sellers:
                                                selected_sellers.remove(co)   
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
                                        seller_group.draw(grid_surface_copy)
                                        arrows_group.draw(grid_surface_copy)      


#¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
#what is drawn on each game state is below
    if game_state =='main menu':
        screen.blit(main_menu_bg,(0,0))
        play_button.draw()
        controls_button.draw()
        settings_button.draw()
        exit_button.draw()

    elif game_state=='play':

        producer_group.update(producer_info)
        material_group.update(conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group)

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
        seller_group.draw(grid_surface_copy)
        #materials
        material_group.draw(grid_surface_copy)
        items_group.draw(grid_surface_copy)


        draw_money()

        screen.blit(grid_surface_copy,(0,100))
        #copy screen
        play_grid_bg=grid_surface_copy.copy()
        play_bg=screen.copy()

    elif game_state=='producer_popup':
        screen.blit(grid_surface_copy,(0,100))
        draw_money()


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
        draw_money()

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
        draw_money()

        
        transparent_popup.draw()
        producer_button.draw()
        crafter_button.draw()
        conveyor_button.draw()
        seller_button.draw()
        scrollbar_button.draw()
        slider_button.draw()

    elif game_state=='blueprints':
        screen.blit(play_bg,(0,0))
        draw_money()

        screen.blit(shop_surface,(100,150))
        transparent_popup.draw()
        scrollbar_button.draw()
        slider_button.draw()

        shop_surface_copy= shop_surface.copy()

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

        
        screen.blit(bp_title1,(140,320))
        screen.blit(bp_title2,(450,320))
        screen.blit(bp_title3,(140,445))
        screen.blit(bp_title4,(450,445))
        screen.blit(bp_title5,(140,570))
        screen.blit(bp_title6,(450,580))
        screen.blit(bp_title7,(140,695))
        screen.blit(bp_title8,(450,695))

        #new_bp=Blueprints(1)
        #blueprints_group.add(new_bp)
        #blueprints_group.draw(blueprint_tab_surface)
        #blueprints_group.update()
        screen.blit(blueprint_tab_surface,(100,150))


    elif game_state=='shop confirm':
        screen.blit(grid_surface_copy,(0,100))
        draw_money()

        transparent_grid_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        green_square_group.update(selected_pos)
        green_square_group.draw(grid_surface_copy)
        
    elif game_state=='edit':
        draw_money()

        screen.blit(grid_surface_copy,(0,100))
        rotate_button.draw()
        delete_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        arrows_group.draw(grid_surface_copy)
        if have_producer: 
            producer_group.update(producer_info)

    elif game_state=='ingame_settings':
        screen.blit(money_panel_img,(200,0))
        money_text=font_50.render(str(money),None,100)
        money_text_rect=money_text.get_rect(center=(400,38))
        screen.blit(money_text,money_text_rect)
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

