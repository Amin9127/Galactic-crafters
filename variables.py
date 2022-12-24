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

revenue =0
previous_revenue=0
money_per_min=0


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
font_34 = pygame.font.Font('Pixeltype.ttf',34)
font_36 = pygame.font.Font('Pixeltype.ttf',36)
font_38 = pygame.font.Font('Pixeltype.ttf',38)
font_40 = pygame.font.Font('Pixeltype.ttf',40)
font_42 = pygame.font.Font('Pixeltype.ttf',38)
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

prices={
    'producer':100,
    'crafter':100,
    'conveyor':50,
    'seller':100,
}

producer_lv =1
crafter_lv =1
conveyor_lv =1
seller_lv =1

producer_upgrades={
    1:[0,'',1],
    2:[100,'K',3],
    3:[1,'M',5],
    4:[5000000,'',10],
}
crafter_upgrades={
    1:[0,'',1],
    2:[1,'M',3],
    3:[5,'M',5],
    4:[50,'M',10],
}
conveyor_upgrades={
    1:[0,'',1],
    2:[100,'K',1.2],
    3:[500000,'',1.4],
    4:[5000000,'',1.6],
}
seller_upgrades={
    1:[0,'',1],
    2:[50,'K',1.1],
    3:[500000,'',1.2],
    4:[5000000,'',1.3],
}
abreviations={
    '':0,
    'K':3,
    'M':6,
    'B':9,
    'T':12,
    'q':15,
    'Q':18,
}
#sprite groups
producer_group=pygame.sprite.Group()
crafter_group=pygame.sprite.Group()
conveyor_group=pygame.sprite.Group()
material_group=pygame.sprite.Group()
item_group=pygame.sprite.Group()
seller_group=pygame.sprite.Group()
smelter_group=pygame.sprite.Group()

green_square_group=pygame.sprite.Group()
arrows_group=pygame.sprite.Group()
blueprints_group=pygame.sprite.Group()

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

cabin_img=pygame.image.load('images/cross.png').convert_alpha()
jet_thruster_img=pygame.image.load('images/cross.png').convert_alpha()
mega_engine_img=pygame.image.load('images/cross.png').convert_alpha()
compressed_coal_img=pygame.image.load('images/cross.png').convert_alpha()
fuel_tank_img=pygame.image.load('images/cross.png').convert_alpha()
rocket_img=pygame.image.load('images/cross.png').convert_alpha()

item_imgs={'empty':empty_slot_img,
    'nothing':empty_slot_img,
    'copper':copper_img,'iron':iron_img,'gold':gold_img,
    'aluminium':aluminium_img,'lead':lead_img,'coal':coal_img,
    'circuit':circuit_img,'motherboard':motherboard_img, 'cpu':cpu_img,
    'ram':ram_img,'power supply':power_supply_img,'hdd':hdd_img,
    'battery':empty_slot_img,'engine':empty_slot_img,'super computer':empty_slot_img,
    'gpu':gpu_img,'computer':computer_img,'cabin':cabin_img,'jet thruster':jet_thruster_img,
    'mega engine':mega_engine_img,'compressed coal':compressed_coal_img,'fuel tank':fuel_tank_img,
    'rocket':rocket_img,
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
    'cabin':{'super computer':3,'copper':100,'iron':100,'aluminium':1000,'circuit':50,'power supply':50},
    'jet thruster':{'aluminium':200,'iron':200,'circuit':50},
    'mega engine':{'engine':100,'aluminium':200},
    'compressed coal':{'coal':10,'lead':10},
    'fuel tank':{'compressed coal':100},
    'rocket':{'jet thruster':4,'fuel tank':8,'mega engine':5,'aluminium':10000,'cabin':1},
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
    'cabin':0,
    'jet thruster':0,
    'mega engine':0,
    'compressed coal':0,
    'fuel tank':0,
    'rocket':0,
}
bp_ordered_list=list(blueprints.keys())
#bp_ordered_list.sort()

bptitles={0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:''}
bptitles2=['nothing','nothing','nothing','nothing','nothing','nothing','nothing','nothing']
choose_bp=False
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
blank_button_img=pygame.image.load('images/button4.png').convert_alpha()
shop_img=pygame.image.load('images/shop.png').convert_alpha()
edit_img=pygame.image.load('images/edit.png').convert_alpha()
blueprints_img=pygame.image.load('images/blueprints.png').convert_alpha()
map_img=pygame.image.load('images/button4.png').convert_alpha()
gui_flat_img=pygame.image.load('images/gui_flat.png').convert_alpha()
#play screen button instantiation
settings_mini_button=Buttons(0,0,settings_mini_img,0.5,0.5)
shop_button = Buttons(800,250,shop_img,0.5,0.5)
edit_button = Buttons(800,300,edit_img,0.5,0.5)
blueprints_button = Buttons(800,350,blueprints_img,0.5,0.5)
map_button = Buttons(800,400,map_img,0.5,0.5)
stats_button= Buttons(780,0,blank_button_img,0.6,0.6)

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
paste_possible=False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#stats
stats_surface=Buttons(200,200,blank_popup_img,2,4)

#scrollbar images
scrollbar_img=pygame.image.load('images/scrollbar.png').convert_alpha()
scrollbar_img=pygame.transform.rotate(scrollbar_img,270)
slider_img=pygame.image.load('images/slider.png').convert_alpha()
#scrollbar button instantiation
scrollbar_button=Buttons(750,150,scrollbar_img,0.25,7)
slider_button=Buttons(750,150,slider_img,0.25,0.5)
slider_drag=False
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
prices={'producer':100,'crafter':100,'conveyor':50,'seller':100,}
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
transparent_popup_button=Buttons(100,150,transparent_popup,3.5,7)

producer_button=Buttons(135,340,producer_img,0.5,0.5)
crafter_button=Buttons(440,340,crafter_img,0.5,0.5)
conveyor_button=Buttons(135,470,conveyor_img,0.5,0.5)
seller_button=Buttons(440,470,seller_img,0.5,0.5)

producer_buy_button=Buttons(115,297,gui_flat_img,1.56,1.34)
crafter_buy_button=Buttons(422,297,gui_flat_img,1.56,1.34)
conveyor_buy_button=Buttons(115,431,gui_flat_img,1.56,1.34)
seller_buy_button=Buttons(422,431,gui_flat_img,1.56,1.34)

machine1_buy_button=Buttons(115,565,gui_flat_img,1.56,1.34)
machine2_buy_button=Buttons(422,565,gui_flat_img,1.56,1.34)
machine3_buy_button=Buttons(115,699,gui_flat_img,1.56,1.34)
machine4_buy_button=Buttons(422,699,gui_flat_img,1.56,1.34)

#upgrades
producer_upgrade_button=Buttons(115,297,gui_flat_img,1.56,1.34)
crafter_upgrade_button=Buttons(422,297,gui_flat_img,1.56,1.34)
conveyor_upgrade_button=Buttons(115,431,gui_flat_img,1.56,1.34)
seller_upgrade_button=Buttons(422,431,gui_flat_img,1.56,1.34)

machine1_upgrade_button=Buttons(115,565,gui_flat_img,1.56,1.34)
machine2_upgrade_button=Buttons(422,565,gui_flat_img,1.56,1.34)
machine3_upgrade_button=Buttons(115,699,gui_flat_img,1.56,1.34)
machine4_upgrade_button=Buttons(422,699,gui_flat_img,1.56,1.34)

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