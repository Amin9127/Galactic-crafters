import pygame
pygame.init()
pygame.font.init()

class Buttons():
    def __init__(self,x,y,image,scale_x,scale_y):
        self.image=pygame.transform.scale(image, (200*scale_x, 100*scale_y))
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))


#screen set up
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption('Galactic Crafters')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((900,900))
white=(255,255,255)
surface.fill(white)
game_state='main menu' 

font = pygame.font.Font('Pixeltype.ttf',16)
font_24 = pygame.font.Font('Pixeltype.ttf',24)
font_32 = pygame.font.Font('Pixeltype.ttf',32)
font_50 = pygame.font.Font('Pixeltype.ttf',50)
font_60 = pygame.font.Font('Pixeltype.ttf',60)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#machine info dictionaries
#producer_info={'0.0':['n','copper',1,'right'],}
producer_info={}
#crafter_info={'0.0':['n','circuit',{'input':0},'right']}
crafter_info={}
#conveyor_info={'0.0':['n','','','right]}
conveyor_info={}
#seller_info={'0.0':['n','','','right']}
seller_info={}

temp_info={}
factory_layout=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#blueprints stuff
#material images
copper_img=pygame.image.load('images/copper.png').convert_alpha()
iron_img=pygame.image.load('images/iron.png').convert_alpha()
gold_img=pygame.image.load('images/gold.png').convert_alpha()
aluminium_img=pygame.image.load('images/aluminium.png').convert_alpha()
coal_img=pygame.image.load('images/coal.png').convert_alpha()
lead_img=pygame.image.load('images/lead.png').convert_alpha()
empty_slot_img=pygame.image.load('images/cross.png').convert_alpha()
#item images
circuit_img=pygame.image.load('images/circuit.png').convert_alpha()
ram_img=pygame.image.load('images/ram.png').convert_alpha()
cpu_img=pygame.image.load('images/cpu.png').convert_alpha()
gpu_img=pygame.image.load('images/gpu.png').convert_alpha()
hdd_img=pygame.image.load('images/hdd.png').convert_alpha()
computer_img=pygame.image.load('images/pc.png').convert_alpha()
power_supply_img=pygame.image.load('images/power supply.png').convert_alpha()
motherboard_img=pygame.image.load('images/circuit.png').convert_alpha()

item_imgs={'empty':empty_slot_img,
    'nothing':empty_slot_img,
    'copper':copper_img,'iron':iron_img,'gold':gold_img,
    'aluminium':aluminium_img,'lead':lead_img,'coal':coal_img,
    'circuit':circuit_img,'motherboard':motherboard_img, 'cpu':cpu_img,
    'ram':ram_img,'power supply':power_supply_img,'hdd':hdd_img,
    'battery':empty_slot_img,'engine':empty_slot_img,'super computer':empty_slot_img,
    'gpu':gpu_img,'computer':computer_img,
}

blueprints={
    'circuit':{'copper':3,'gold':1},
    'motherboard':{'circuit':6,'copper':6},
    'battery':{'lead':3,'aluminium':1},
    'cpu':{'aluminium':5,'circuit':2,'gold':3},
    'gpu':{'aluminium':3,'circuit':3,'copper':2},
    'ram':{'circuit':1,'iron':3},
    'power supply':{'aluminium':10,'copper':3,'circuit':1,'iron':3},
    'hdd':{'iron':3,'lead':3,'aluminium':10},
    'computer':{'motherboard':1,'cpu':1,'ram':2,'power supply':1,'hdd':1,'gpu':1},
    'engine':{'aluminium':15,'coal':5},
    'super computer':{'computer':5,'power supply':10,'gpu':10},
}

blueprints_value={
    'nothing':0,
    'circuit':120,
    'motherboard':1400,
    'cpu':700,
    'gpu':800,
    'ram':300,
    'power supply':800,
    'hdd':500,
    'computer':8000,
    'battery':150,
    'engine':600,
    'super computer':80000,
}
bp_ordered_list=list(blueprints.keys())
bp_ordered_list.sort()

bptitles={0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:''}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#play mode
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

have_producer=False
have_crafter=False
have_conveyor=False
have_seller=False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#settings
settings_img=pygame.image.load('images/settings_panel.png').convert_alpha()
settings_surface=pygame.transform.scale(settings_img,(450,500))
transparent_settings_surface=pygame.transform.scale(settings_img,(450,500))
transparent_settings_surface.set_alpha(0)

#settings tab button images
resume_img=pygame.image.load('images/resume.png').convert_alpha()
menu_img=pygame.image.load('images/menu.png').convert_alpha()
#settings tab button instantiation
resume_button=Buttons(480,570,resume_img,0.5,0.5)
menu_button=Buttons(300,570,menu_img,0.5,0.5)
transparent_settings=Buttons(225,150,transparent_settings_surface,2.25,5)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#machine stuff
#sprite images:
producer_img=pygame.image.load('images/producer.png').convert_alpha()
crafter_img=pygame.image.load('images/crafter.png').convert_alpha()
conveyor_img=pygame.image.load('images/conveyor.png').convert_alpha()
seller_img=pygame.image.load('images/seller.png').convert_alpha()

#producer popup images:
producer_popup_img=pygame.image.load('images/gui_flat.png').convert_alpha()
producer_popup_surface=pygame.transform.scale(producer_popup_img,(200,225))
transparent_producer_popup_surface=pygame.transform.scale(producer_popup_img,(200,225))
transparent_producer_popup_surface.set_alpha(0)


#background images
main_menu_bg=pygame.image.load('images/background.png').convert_alpha()
main_menu_bg=pygame.transform.scale(main_menu_bg,(900,900))
grid_img = pygame.image.load('images/grid.png').convert_alpha()
grid_surface=pygame.transform.scale(grid_img,(800,800))
transparent_grid=pygame.transform.scale(grid_img,(800,800))
transparent_grid.set_alpha(0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#miscellaneous
blank_popup_img=pygame.image.load('images/panel8.png').convert_alpha()
shop_surface=pygame.transform.scale(blank_popup_img,(650,700))
blueprint_surface=pygame.transform.scale(blank_popup_img,(650,700))
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
blueprint_title_position={0:[140,310],1:[450,310],2:[140,445],3:[450,445],4:[140,580],5:[450,580],6:[140,715 ],7:[450,715]}
titles_done_rotation = -1
been_to_tempshop=False

#blueprint tabs images:
blueprint_tab_img=pygame.image.load('images/gui_flat.png').convert_alpha()
blueprint_tab_surface=pygame.transform.scale(blueprint_tab_img,(200,225))

#money panel
money_panel_img=pygame.image.load('images/panel3.png').convert_alpha()
#money_panel_surface=pygame.transform.scale(money_panel_img,(400,70))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#edit stuff
#edit button images:
rotate_img =pygame.image.load('images/rotate.png').convert_alpha()
delete_img =pygame.image.load('images/delete.png').convert_alpha()
#edit button instantiation
rotate_button=Buttons(800,400,rotate_img,0.5,0.5)
delete_button=Buttons(800,450,delete_img,0.5,0.5)
cancel_move=False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#shop stuff
#shop button images:
mini_exit_img=pygame.image.load('images/mini_exit.png').convert_alpha()
gui_flat_img=pygame.image.load('images/gui_flat.png').convert_alpha()
#shop tabs button instantiation
machines_button=Buttons(114,172,gui_flat_img,1.05,1.15)
upgrades_button=Buttons(320,172,gui_flat_img,1.05,1.15)
supply_button=Buttons(526,172,gui_flat_img,1.05,1.15)
machines_lable=font_60.render('Machines',False,(0,0,0))
upgrades_lable=font_60.render('upgrades',False,(0,0,0))
supply_lable=font_60.render('supply',False,(0,0,0))


#machinery shop button instantiation
mini_exit_button=Buttons(250,400,mini_exit_img,0.5,0.5)
transparent_popup=Buttons(100,150,transparent_popup,3.5,7)
producer_button=Buttons(130,310,producer_img,0.5,0.5)
crafter_button=Buttons(230,310,crafter_img,0.5,0.5)
conveyor_button=Buttons(330,310,conveyor_img,0.5,0.5)
seller_button=Buttons(430,310,seller_img,0.5,0.5)
#upgrades

#supply
materials_supply={'copper':0,'iron':0,'gold':0,'aluminium':0,'lead':0,'coal':0}

copper_supply_button=Buttons(115,297,gui_flat_img,1,0.9)
iron_supply_button=Buttons(115,387,gui_flat_img,1,0.9)
gold_supply_button=Buttons(115,477,gui_flat_img,1,0.9)
aluminium_supply_button=Buttons(115,567,gui_flat_img,1,0.9)
lead_supply_button=Buttons(115,657,gui_flat_img,1,0.9)
coal_supply_button=Buttons(115,747,gui_flat_img,1,0.9)

copper_shop_button=Buttons(300,297,copper_img,1,0.9)
iron_shop_button=Buttons(300,387,iron_img,1,0.9)
gold_shop_button=Buttons(300,477,gold_img,1,0.9)
aluminium_shop_button=Buttons(300,567,aluminium_img,1,0.9)
lead_shop_button=Buttons(300,657,lead_img,1,0.9)
coal_shop_button=Buttons(300,747,coal_img,1,0.9)

material_buy1=Buttons(530,297,gui_flat_img,1,0.9)
material_buy10=Buttons(530,387,gui_flat_img,1,0.9)
material_buy100=Buttons(530,477,gui_flat_img,1,0.9)
material_buy1000=Buttons(530,567,gui_flat_img,1,0.9)
selected_material='none'

##shop confirm button images:
confirm_img=pygame.image.load('images/confirm.png').convert_alpha()
cancel_img=pygame.image.load('images/cancel.png').convert_alpha()
green_square_img=pygame.image.load('images/green_square.png').convert_alpha()
#shop confirm button instantiation 
transparent_grid_button=Buttons(0,100,transparent_grid,4,8)
confirm_button=Buttons(800,800,confirm_img,0.5,0.5)
cancel_button=Buttons(800,850,cancel_img,0.5,0.5)

selected_producers=[]
selected_crafters=[]
selected_conveyors=[]
selected_sellers=[]
selected_machines=[]
selected_pos=[]
selection=''