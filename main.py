import pygame 
import os
import pickle
import sys
import time
#import yfinance as yf

from button_functions import *
from classes import *
from variables import *
pygame.init()
pygame.font.init()

#usual start 1000 money
global money
money=1000

#saves data
def save_data():
    data_file = open("Galactic_Crafters.txt", "wb")
    saved_time=pygame.time.get_ticks()

    data_dict={'producer_info':area_object.producer_info,
                'crafter_info':area_object.crafter_info,
                'conveyor_info':area_object.conveyor_info,
                'seller_info':area_object.seller_info,
                'factory_layout':area_object.factory_layout,
                'producer_lv':area_object.producer_lv,
                'crafter_lv':area_object.crafter_lv,
                'conveyor_lv':area_object.conveyor_lv,
                'seller_lv':area_object.seller_lv,
                'money':money,
                'revenue':revenue,
                'previous_revenue':previous_revenue,
                'money_per_min':money_per_min,
                'materials_supply':area_object.materials_supply,
                'saved_time':saved_time,
}

    pickle.dump(data_dict,data_file,pickle.HIGHEST_PROTOCOL)
    data_file.close()

#check if file called this exists
file_exists = os.path.exists("Galactic_Crafters.txt")

#if so make a file and load all changeable variables to as it would at the start
if file_exists:
    data_file = open("Galactic_Crafters.txt", "rb")
    data_dict = pickle.load(data_file)
    data_file.close()

    #load variable data
    area_object.producer_info = data_dict.get('producer_info')
    area_object.crafter_info = data_dict.get('crafter_info')
    area_object.conveyor_info = data_dict.get('conveyor_info')
    area_object.seller_info = data_dict.get('seller_info')
    area_object.factory_layout = data_dict.get('factory_layout')
    area_object.producer_lv = data_dict.get('producer_lv')
    area_object.crafter_lv = data_dict.get('crafter_lv')
    area_object.conveyor_lv = data_dict.get('conveyor_lv')
    area_object.seller_lv = data_dict.get('seller_lv')
    money=data_dict.get('money')
    revenue = data_dict.get('revenue')
    previous_revenue = data_dict.get('previous_revenue')
    money_per_min = data_dict.get('money_per_min')
    area_object.materials_supply = data_dict.get('materials_supply')
    saved_time=data_dict.get('saved_time')

    #recreate machine sprites
    for decimal_co in list(area_object.producer_info.keys()):
        co = decimal_co.split('.')
        co[0]=int(co[0])
        co[1]=int(co[1])
        new_producer=Producer(co[0],co[1],producer_img,area_object.producer_info)
        area_object.producer_group.add(new_producer)
    for decimal_co in list(area_object.crafter_info.keys()):
        co = decimal_co.split('.')
        co[0]=int(co[0])
        co[1]=int(co[1])
        new_crafter=Crafter(co[0],co[1],crafter_img)
        area_object.crafter_group.add(new_crafter)
    for decimal_co in list(area_object.conveyor_info.keys()):
        co = decimal_co.split('.')
        co[0]=int(co[0])
        co[1]=int(co[1])
        new_conveyor=Conveyor(co[0],co[1],conveyor_img)
        area_object.conveyor_group.add(new_conveyor)
        area_object.conveyor_group.update(conveyor_info)
    for decimal_co in list(area_object.seller_info.keys()):
        co = decimal_co.split('.')
        co[0]=int(co[0])
        co[1]=int(co[1])
        new_seller=Seller(co[0],co[1],seller_img)
        area_object.seller_group.add(new_seller)

else:
    save_data()


#timers
#creates a event every second
seconds_event=pygame.USEREVENT
pygame.time.set_timer(seconds_event,1000)

#creates event every minute
minute_event=pygame.USEREVENT+1
pygame.time.set_timer(minute_event,60000)

last_time=time.time()
 

run=True
while run:
    #framerate independence currently not in use
    dt=time.time() - last_time
    dt*=60
    last_time=time.time()

    screen.fill((52,78,91))
    screen.blit(play_bg_img,(0,0))


    

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            save_data()
            pygame.quit()
            sys.exit()  

        if event.type ==seconds_event:






       

            #code below ran every second
            if game_state in ('play','shop supply'):
                screen.blit(grid_surface,(0,100))
                producer_cos=list(area_object.producer_info.keys())
                #creates new material every second and reduces it from supply
                for x in producer_cos:
                    co = x.split('.')
                    co[0]=int(co[0])
                    co[1]=int(co[1])
                    created_material=area_object.producer_info[x][1]
                    material_quantity =area_object.producer_info[x][2]
                    if area_object.materials_supply[created_material]>=material_quantity:
                        area_object.materials_supply[created_material]=area_object.materials_supply[created_material]-material_quantity
                        area_object.material_group.add(Producer.create_material('self',co,area_object.producer_info))

                #creates the new item every second if possible
                for crafter in area_object.crafter_group:
                    amount_maybe=crafter.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    if amount_maybe!=False:
                        item_group.add(crafter.create_item(blueprints_value,item_imgs,amount_maybe))

        #updates the money per min variable every minute
        if event.type==minute_event:
            money_per_min=revenue-previous_revenue
            previous_revenue=revenue

            #data = yf.download("GBP=X", period="1d", interval="1d",progress=False)
            #gbp_usd= data.Close
            #print(round(float(gbp_usd),2),'gbp/usd')                 

            #data = yf.download("HG=F", period="1d", interval="1d",progress=False)
            #copper_value = data.Close
            #print(round(float(copper_value),2),'copper')  
            #
            #data = yf.download("IRON", period="1d", interval="1d",progress=False)
            #iron_value = data.Close
            #print(round(float(iron_value),2),'iron')  

            #data = yf.download("GC=F", period="1d", interval="1d",progress=False)
            #gold_value = data.Close
            #print(round(float(gold_value),2),'gold per ounce usd')

            #data = yf.download("ALI=F", period="1d", interval="1d",progress=False)
            #aluminium_value = data.Close
            #print(round(float(aluminium_value),2),'aluminium per tonne usd')

            #data = yf.download("PL=F", period="1d", interval="1d",progress=False)
            #lead_value = data.Close
            #print(round(float(lead_value),2),'lead per tonne usd')             

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
                    game_state='shop machines'
                elif event.key == pygame.K_e:
                    game_state='edit'
                elif event.key == pygame.K_b:
                    game_state='temp shop'
                    slider_button.rect.top=150
                    for blueprint in area_object.blueprints_group:
                        blueprint.kill()

                    for y in range(0,8):
                        bptitles2[y]=bp_ordered_list[y]
                        new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
                        area_object.blueprints_group.add(new_bp)

                        
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

            elif game_state=='shop machines':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'play'
                elif event.key == pygame.K_u:
                    game_state='shop upgrades'
                elif event.key == pygame.K_s:
                    game_state='shop supply'                    
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

            elif game_state=='shop upgrades':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'play'
                elif event.key == pygame.K_m:
                    game_state='shop machines'
                elif event.key == pygame.K_s:
                    game_state='shop supply'  

            elif game_state=='shop supply':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'play'
                elif event.key == pygame.K_u:
                    game_state='shop upgrades'
                elif event.key == pygame.K_m:
                    game_state='shop machines'        

            elif game_state == 'blueprints':
                if event.key == pygame.K_ESCAPE:    
                    game_state= 'play'
                    slider_button.rect.top=150
     
            elif game_state == 'shop confirm':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'shop'
                elif event.key == pygame.K_RETURN:
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,Producer,Crafter,Conveyor,Seller,money,area_object)
                    selected_pos=[]
                    game_state='play' 

            elif game_state == 'edit':
                if event.key==pygame.K_BACKSPACE:
                    
                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_sellers=[]
                    selected_machines=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)

                elif event.key ==pygame.K_RETURN:
                    #sends the user back to play and empties related variables
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_machines=[]
                    selected_sellers=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)  

                elif event.key ==pygame.K_ESCAPE:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_machines=[]
                    selected_sellers=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)  
                
                elif event.key ==pygame.K_r:
                    rotate(crafter_upgrades,blueprints,selected_producers,selected_machines,selected_crafters,selected_conveyors,selected_sellers,grid_surface_copy,area_object)
                elif event.key ==pygame.K_x:
                    #delete(area_object.factory_layout,selected_producers,area_object.producer_info,area_object.producer_group,area_object.crafter_info,selected_crafters,area_object.crafter_group,selected_conveyors,conveyor_info,area_object.conveyor_group,area_object.arrows_group,area_object.material_group,grid_surface)
                    #deletes selected machines
                    for pos in selected_producers:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.producer_info.pop(decimal_co)
                    for pos in selected_crafters:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.conveyor_info.pop(decimal_co)
                    for pos in selected_sellers:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.seller_info.pop(decimal_co)

                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_sellers=[]
                    selected_machines=[]


                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.update(area_object.producer_info)
                    area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    area_object.conveyor_group.update(conveyor_info)
                    area_object.seller_group.update(area_object.seller_info)
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)

                elif event.key ==pygame.K_LEFT:
                    move('left',selected_producers,selected_crafters,selected_conveyors,selected_sellers,selected_machines,Arrow,area_object)

                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.update(area_object.producer_info)
                    area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    area_object.conveyor_group.update(conveyor_info)
                    area_object.seller_group.update(area_object.seller_info)
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    area_object.arrows_group.draw(grid_surface_copy)

                elif event.key ==pygame.K_UP:
                    move('up',selected_producers,selected_crafters,selected_conveyors,selected_sellers,selected_machines,Arrow,area_object)


                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.update(area_object.producer_info)
                    area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    area_object.conveyor_group.update(conveyor_info)
                    area_object.seller_group.update(area_object.seller_info)
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    area_object.arrows_group.draw(grid_surface_copy)
                
                elif event.key==pygame.K_RIGHT:                    
                    move('right',selected_producers,selected_crafters,selected_conveyors,selected_sellers,selected_machines,Arrow,area_object)


                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.update(area_object.producer_info)
                    area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    area_object.conveyor_group.update(conveyor_info)
                    area_object.seller_group.update(area_object.seller_info)
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    area_object.arrows_group.draw(grid_surface_copy)

                elif event.key ==pygame.K_DOWN:
                    move('down',selected_producers,selected_crafters,selected_conveyors,selected_sellers,selected_machines,Arrow,area_object)


                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.update(area_object.producer_info)
                    area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    area_object.conveyor_group.update(conveyor_info)
                    area_object.seller_group.update(area_object.seller_info)
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    area_object.arrows_group.draw(grid_surface_copy)        

                elif event.key==pygame.K_c:
                    minimum_co_x =800
                    maximum_co_x =0
                    minimum_co_y =900
                    maximum_co_y =100
                    copied_machines=selected_machines
                    consise_copied_machines=[]
                    copied_producers=len(selected_producers)
                    copied_crafters=len(selected_crafters)
                    copied_conveyors=len(selected_conveyors)
                    copied_sellers=len(selected_sellers)

                    for co in selected_machines:
                        if co[0] < minimum_co_x:
                            minimum_co_x =co[0]
                        if co[0] > maximum_co_x:
                            maximum_co_x =co[0]

                        if co[1] < minimum_co_y:
                            minimum_co_y =co[1]
                        if co[1] > maximum_co_y:
                            maximum_co_y =co[1]
                    
                    x_range=maximum_co_x-minimum_co_x+40
                    y_range=maximum_co_y-minimum_co_y+40

                    #create 2d array of the minimum size
                    consise_layout = [[0 for x in range(x_range//40)] for y in range(y_range//40)] 

                    for cos in selected_machines:
                        decimal_co=str(cos[0])+'.'+str(cos[1])

                        #store consise positions which are only relative to consise layout.
                        consise_co=[(cos[0]-minimum_co_x)//40,(cos[1]-minimum_co_y)//40]
                        consise_copied_machines.append(consise_co)

                        layout_co=[(cos[0]-minimum_co_x)//40,(cos[1]-minimum_co_y)//40]
                        if cos in selected_producers:
                            consise_layout[layout_co[1]][layout_co[0]]={'producer':area_object.producer_info[decimal_co]}
                            print(consise_layout[layout_co[1]][layout_co[0]])
                        elif cos in selected_crafters:
                            copied_c_info=area_object.crafter_info[decimal_co]
                            copied_c_info[2]={}
                            consise_layout[layout_co[1]][layout_co[0]]={'crafter':copied_c_info}
                        elif cos in selected_conveyors:
                            consise_layout[layout_co[1]][layout_co[0]]={'conveyor':conveyor_info[decimal_co]}
                        elif cos in selected_sellers:
                            consise_layout[layout_co[1]][layout_co[0]]={'seller':area_object.seller_info[decimal_co]}
                
                    #for x in consise_layout:
                    #    for y in x:
                    #        print(y,end = " ")
                    #    print()
                    
                elif event.key==pygame.K_v:
                    game_state='edit paste'

            elif game_state=='edit paste':
                if event.key==pygame.K_ESCAPE:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_sellers=[]
                    selected_machines=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info) 

                elif event.key==pygame.K_RETURN:
                    copy_price = copied_producers*prices['producer']+copied_crafters*prices['crafter']+copied_conveyors*prices['conveyor']+copied_sellers*prices['seller']
                    if paste_possible==True and money>=copy_price:
                        for cos in consise_copied_machines:
                            pos=[cos[0]*40,cos[1]*40]

                            copied_info=consise_layout[cos[1]][cos[0]]
                            copied_keys=list(copied_info.keys())
                            copied_machine=copied_keys[0]

                            if copied_machine=='producer':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                area_object.producer_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_producer=Producer(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],producer_img,area_object.producer_info)
                                area_object.producer_group.add(new_producer)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='crafter':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                area_object.crafter_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_crafter=Crafter(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],crafter_img)
                                area_object.crafter_group.add(new_crafter)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='conveyor':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                conveyor_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_conveyor=Conveyor(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],conveyor_img)
                                area_object.conveyor_group.add(new_conveyor)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='seller':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                area_object.seller_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_seller=Seller(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],seller_img)
                                area_object.seller_group.add(new_seller)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                        paste_possible=False
                        money-=copy_price
                        area_object.producer_group.update(area_object.producer_info)
                        area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                        area_object.conveyor_group.update(conveyor_info)
                        area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                        area_object.seller_group.update(area_object.seller_info)        
            
            elif game_state=='map':
                if event.key==pygame.K_ESCAPE:
                    game_state='play'

            elif game_state=='credits':
                if event.key==pygame.K_ESCAPE:
                    game_state='play'

            elif game_state=='stats':
                if event.key==pygame.K_ESCAPE:
                    game_state='play'
 
            save_data()
#---------------------------------------------------------------------------------------
        #all button check and what the button does in this if elif ladder
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(area_object.producer_info)
            print(earth.producer_info)
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
                    sys.exit()

            elif game_state=='play':
                if settings_mini_button.rect.collidepoint(co):
                    game_state='ingame_settings'
                
                elif shop_button.rect.collidepoint(co):
                    game_state='shop machines'
                
                elif edit_button.rect.collidepoint(co):
                    game_state='edit'
                
                elif blueprints_button.rect.collidepoint(co):
                    game_state='temp shop'
                    slider_button.rect.top=150
                    for blueprint in area_object.blueprints_group:
                        blueprint.kill()

                    for y in range(0,8):
                        bptitles2[y]=bp_ordered_list[y]
                        new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
                        area_object.blueprints_group.add(new_bp)

                elif map_button.rect.collidepoint(co):
                    game_state='map'
                
                elif transparent_grid_button.rect.collidepoint(co):
                    x,y=co[0],co[1]
                    x=(x//40)
                    y=(y-100)//40
                    if area_object.factory_layout[y][x]==1:
                        producer_cos=list(area_object.producer_info.keys())
                        crafter_cos=list(area_object.crafter_info.keys())
                        conveyor_cos=list(conveyor_info.keys())
                        x*=40
                        y*=40
                        decimal_co=str(x)+'.'+str(y)
                        co = [x+40,y+100]
                        if decimal_co in producer_cos:

                            if x==680:
                                co = [co[0]-240,co[1]]
                            elif x==720:
                                co = [co[0]-240,co[1]]
                            elif x==760:
                                co = [co[0]-240,co[1]]
                            
                            if y==600:
                                co = [co[0],co[1]-180]
                            elif y==640:
                                co = [co[0],co[1]-180]
                            elif y==680:
                                co = [co[0],co[1]-180]
                            elif y==720:
                                co = [co[0],co[1]-180]
                            elif y==760:
                                co = [co[0],co[1]-180]
                            elif y==800:
                                co = [co[0],co[1]-180]

                            selected_co=co
                            transparent_producer_popup=Buttons(co[0],co[1],transparent_producer_popup_surface,1,2.25)
                            selected_material_button=Buttons(co[0]+45,co[1]+20,item_imgs[area_object.producer_info[decimal_co][1]],0.5,0.5)
                            current_output_txt=font_24.render('Current Output: ',False,(0,0,0))
                            
                            copper_button=Buttons(co[0],co[1]+90,copper_img,0.5,0.5)
                            iron_button=Buttons(co[0]+90,co[1]+90,iron_img,0.5,0.5)
                            gold_button=Buttons(co[0],co[1]+130,gold_img,0.5,0.5)
                            aluminium_button=Buttons(co[0]+90,co[1]+130,aluminium_img,0.5,0.5)
                            coal_button=Buttons(co[0],co[1]+170,coal_img,0.5,0.5)
                            lead_button=Buttons(co[0]+90,co[1]+170,lead_img,0.5,0.5)
                            game_state='producer_popup'

                        elif decimal_co in crafter_cos:
                            if x==680:
                                co = [co[0]-240,co[1]]
                            elif x==720:
                                co = [co[0]-240,co[1]]
                            elif x==760:
                                co = [co[0]-240,co[1]]
                            
                            if y==600:
                                co = [co[0],co[1]-180]
                            elif y==640:
                                co = [co[0],co[1]-180]
                            elif y==680:
                                co = [co[0],co[1]-180]
                            elif y==720:
                                co = [co[0],co[1]-180]
                            elif y==760:
                                co = [co[0],co[1]-180]
                            elif y==800:
                                co = [co[0],co[1]-180]

                            
                            item_types=len(area_object.crafter_info[decimal_co][2].keys())
                            item_types_list=list(area_object.crafter_info[decimal_co][2].keys())
                        

                            crafter_inv_items=['empty','empty','empty','empty','empty','empty']
                            crafter_inv_quantities=['','','','','','']

                            for i in range(item_types):
                                crafter_inv_items[i]=item_types_list[i]
                                crafter_inv_quantities[i]=str(area_object.crafter_info[decimal_co][2][item_types_list[i]])
                                
                            inv_button1=Buttons(co[0],co[1]+30,item_imgs[crafter_inv_items[0]],0.25,0.25)
                            inv_button2=Buttons(co[0]+40,co[1]+30,item_imgs[crafter_inv_items[1]],0.25,0.25)
                            inv_button3=Buttons(co[0]+80,co[1]+30,item_imgs[crafter_inv_items[2]],0.25,0.25)
                            inv_button4=Buttons(co[0],co[1]+70,item_imgs[crafter_inv_items[3]],0.25,0.25)
                            inv_button5=Buttons(co[0]+40,co[1]+70,item_imgs[crafter_inv_items[4]],0.25,0.25)
                            inv_button6=Buttons(co[0]+80,co[1]+70,item_imgs[crafter_inv_items[5]],0.25,0.25)


                            bp_item_types=len(blueprints[area_object.crafter_info[decimal_co][1]].keys())
                            bp_items_list=list(blueprints[area_object.crafter_info[decimal_co][1]].keys())

                            bp_items=['empty','empty','empty','empty','empty','empty']
                            bp_item_quantities=['','','','','','']

                            for i in range (bp_item_types):
                                bp_items[i]=bp_items_list[i]
                                bp_item_quantities[i]=str(blueprints[area_object.crafter_info[decimal_co][1]][bp_items_list[i]])

                            bp_item_button1=Buttons(co[0],co[1]+140,item_imgs[bp_items[0]],0.25,0.25)
                            bp_item_button2=Buttons(co[0]+40,co[1]+140,item_imgs[bp_items[1]],0.25,0.25)
                            bp_item_button3=Buttons(co[0]+80,co[1]+140,item_imgs[bp_items[2]],0.25,0.25)
                            bp_item_button4=Buttons(co[0],co[1]+180,item_imgs[bp_items[3]],0.25,0.25)
                            bp_item_button5=Buttons(co[0]+40,co[1]+180,item_imgs[bp_items[4]],0.25,0.25)
                            bp_item_button6=Buttons(co[0]+80,co[1]+180,item_imgs[bp_items[5]],0.25,0.25)

                            item_button=Buttons(co[0]+140,co[1]+165,item_imgs[area_object.crafter_info[decimal_co][1]],0.15,0.15)


                            selected_co=co
                            transparent_crafter_popup=Buttons(co[0],co[1],transparent_producer_popup_surface,1,2.25)
                            last_selected_crafter = decimal_co
                            
                            game_state='crafter_popup'
                        elif decimal_co in conveyor_cos:
                            pass
                
                elif stats_button.rect.collidepoint(co):
                    game_state='stats'
                
                else:
                    pass 
            
            elif game_state=='producer_popup':
                if transparent_producer_popup.rect.collidepoint(co) == False:
                    game_state='play'
                elif copper_button.rect.collidepoint(co):
                    area_object.producer_info[decimal_co][1]='copper'
                    game_state='play'
                elif iron_button.rect.collidepoint(co):
                    area_object.producer_info[decimal_co][1]='iron'
                    game_state='play'
                elif gold_button.rect.collidepoint(co):
                    area_object.producer_info[decimal_co][1]='gold'
                    game_state='play'
                elif aluminium_button.rect.collidepoint(co):
                    area_object.producer_info[decimal_co][1]='aluminium'
                    game_state='play'
                elif coal_button.rect.collidepoint(co):
                    area_object.producer_info[decimal_co][1]='coal'
                    game_state='play'
                elif lead_button.rect.collidepoint(co):
                    area_object.producer_info[decimal_co][1]='lead'
                    game_state='play'
            
            elif game_state=='crafter_popup':
                if transparent_crafter_popup.rect.collidepoint(co) == False:
                    game_state='play'   
                elif item_button.rect.collidepoint(co):
                    game_state='temp shop'
                    slider_button.rect.top=150

                    print('choose bp')
                    choose_bp = True     

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

            elif game_state=='shop machines':
                if upgrades_button.rect.collidepoint(co):
                    game_state = 'shop upgrades'
                elif supply_button.rect.collidepoint(co):
                    game_state = 'shop supply'
                elif producer_buy_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='producer'
                elif crafter_buy_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='crafter' 
                elif conveyor_buy_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='conveyor'
                elif seller_buy_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='seller'
                elif transparent_popup_button.rect.collidepoint(co) == False:
                    game_state ='play'
                elif slider_button.rect.collidepoint(co):
                    if event.button == 1: 
                        slider_drag=True
                        mouse_y=co[1]
                        offset_y=slider_button.rect.y-mouse_y
                        
            elif game_state=='shop upgrades':
                if machines_button.rect.collidepoint(co):
                    game_state = 'shop machines'
                elif supply_button.rect.collidepoint(co):
                    game_state = 'shop supply'
                elif producer_upgrade_button.rect.collidepoint(co):
                    if money>=producer_upgrades[area_object.producer_lv+1][0]*10**abreviations[producer_upgrades[area_object.producer_lv+1][1]]:
                        money-=producer_upgrades[area_object.producer_lv+1][0]*10**abreviations[producer_upgrades[area_object.producer_lv+1][1]]
                        area_object.producer_lv+=1
                        producer_cos=list(area_object.producer_info.keys())
                        for cos in producer_cos:
                            area_object.producer_info[cos][2]=producer_upgrades[area_object.producer_lv][2]
                elif crafter_upgrade_button.rect.collidepoint(co):
                    if money>=crafter_upgrades[area_object.crafter_lv+1][0]*10**abreviations[crafter_upgrades[area_object.crafter_lv+1][1]]:
                        money-=crafter_upgrades[area_object.crafter_lv+1][0]*10**abreviations[crafter_upgrades[area_object.crafter_lv+1][1]]
                        area_object.crafter_lv+=1
                elif conveyor_upgrade_button.rect.collidepoint(co):
                    if money>=conveyor_upgrades[area_object.conveyor_lv+1][0]*10**abreviations[conveyor_upgrades[area_object.conveyor_lv+1][1]]:
                        money-=conveyor_upgrades[area_object.conveyor_lv+1][0]*10**abreviations[conveyor_upgrades[area_object.conveyor_lv+1][1]]
                        area_object.conveyor_lv+=1
                elif seller_upgrade_button.rect.collidepoint(co):
                    if money>=seller_upgrades[area_object.seller_lv+1][0]*10**abreviations[seller_upgrades[area_object.seller_lv+1][1]]:
                        money-=seller_upgrades[area_object.seller_lv+1][0]*10**abreviations[seller_upgrades[area_object.seller_lv+1][1]]
                        area_object.seller_lv+=1
                elif transparent_popup_button.rect.collidepoint(co) == False:
                    game_state ='play'

            elif game_state=='shop supply':
                if machines_button.rect.collidepoint(co):
                    game_state = 'shop machines'
                elif upgrades_button.rect.collidepoint(co):
                    game_state = 'shop upgrades'
                elif transparent_popup_button.rect.collidepoint(co) == False:
                    game_state ='play'
                elif copper_shop_button.rect.collidepoint(co):
                    selected_material='copper'
                elif iron_shop_button.rect.collidepoint(co):
                    selected_material='iron'
                elif gold_shop_button.rect.collidepoint(co):
                    selected_material='gold'
                elif aluminium_shop_button.rect.collidepoint(co):
                    selected_material='aluminium'
                elif lead_shop_button.rect.collidepoint(co):
                    selected_material='lead'
                elif coal_shop_button.rect.collidepoint(co):
                    selected_material='coal' 
                if selected_material!='none':

                    if material_buy1.rect.collidepoint(co):
                        if money>=10:
                            money-=10
                            area_object.materials_supply[selected_material]=area_object.materials_supply[selected_material]+1
                    elif material_buy10.rect.collidepoint(co):
                        if money>=100:
                            money-=100
                            area_object.materials_supply[selected_material]=area_object.materials_supply[selected_material]+10
                    elif material_buy100.rect.collidepoint(co):
                        if money>=1000:
                            money-=1000                        
                            area_object.materials_supply[selected_material]=area_object.materials_supply[selected_material]+100
                    elif material_buy1000.rect.collidepoint(co):
                        if money>=10000:
                            money-=10000                        
                            area_object.materials_supply[selected_material]=area_object.materials_supply[selected_material]+1000
                    elif material_buy10000.rect.collidepoint(co):
                        if money>=100000:
                            money-=100000                        
                            area_object.materials_supply[selected_material]=area_object.materials_supply[selected_material]+10000

            elif game_state=='blueprints':
                if transparent_popup_button.rect.collidepoint(co) == False:
                    game_state ='play'
                    print('click',scrollbar_button.rect.collidepoint(co))
                if slider_button.rect.collidepoint(co):
                    print('click slider')
                    if event.button == 1: 
                        slider_drag=True
                        mouse_y=co[1]
                        offset_y=slider_button.rect.y-mouse_y
  
                print(choose_bp)
                if choose_bp == True:
                    
                    for bp in area_object.blueprints_group:
                        if bp.rect.collidepoint(co):
                            selected_bp =bp.bp_title
                            area_object.crafter_info[last_selected_crafter][1]=selected_bp
                            game_state='play'
                            print(area_object.crafter_info,'new bp selected')
                            choose_bp=False
                                 
            elif game_state=='shop confirm':
                if event.button==3:
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,Producer,Crafter,Conveyor,Seller,money,area_object)
                    selected_pos=[]
                    game_state = 'play'

                elif transparent_grid_button.rect.collidepoint(co):
                    if event.button ==1:
                        grid_surface_copy=play_grid_bg
                        slider_drag=True
                        y=(y-100)//40
                        x=(x//40)

                        if area_object.factory_layout[y][x]==0:
                            if [x,y] in selected_pos:
                                selected_pos.remove([x,y])
                                selection='delete'
                                area_object.green_square_group.update(selected_pos)

                            else:
                                selected_pos.append([x,y])
                                new_GreenSquare=GreenSquare(x*40,y*40)
                                area_object.green_square_group.add(new_GreenSquare)
                                selection='place'

                        grid_surface_copy= grid_surface.copy()
                        area_object.green_square_group.draw(grid_surface_copy)



                elif confirm_button.rect.collidepoint(co):
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,Producer,Crafter,Conveyor,Seller,money,area_object)
                    selected_pos=[]
                    game_state = 'play'
                elif cancel_button.rect.collidepoint(co):
                    game_state='play'
                    selected_pos=[]

            elif game_state=='edit paste':
                if event.button==3:
                    copy_price = copied_producers*prices['producer']+copied_crafters*prices['crafter']+copied_conveyors*prices['conveyor']+copied_sellers*prices['seller']
                    if paste_possible==True and money>=copy_price:
                        for cos in consise_copied_machines:
                            pos=[cos[0]*40,cos[1]*40]

                            copied_info=consise_layout[cos[1]][cos[0]]
                            copied_keys=list(copied_info.keys())
                            copied_machine=copied_keys[0]

                            if copied_machine=='producer':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                area_object.producer_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_producer=Producer(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],producer_img,area_object.producer_info)
                                area_object.producer_group.add(new_producer)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='crafter':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                copied_info[copied_keys[0]][2]={}
                                area_object.crafter_info[decimal_co]=copied_info[copied_keys[0]]
                                new_crafter=Crafter(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],crafter_img)
                                area_object.crafter_group.add(new_crafter)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='conveyor':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                conveyor_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_conveyor=Conveyor(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],conveyor_img)
                                area_object.conveyor_group.add(new_conveyor)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='seller':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                area_object.seller_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_seller=Seller(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],seller_img)
                                area_object.seller_group.add(new_seller)
                                area_object.factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                        paste_possible=False
                        area_object.producer_group.update(area_object.producer_info)
                        area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                        area_object.conveyor_group.update(conveyor_info)
                        area_object.seller_group.update(area_object.seller_info)

                elif event.button==2:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_sellers=[]
                    selected_machines=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)

                elif transparent_grid_button.rect.collidepoint(co):
                    if event.button==1:
                        for sprite in area_object.green_square_group:
                            sprite.kill()

                        x= co[0]
                        y= co[1]                      
                        layout_x=(x//40)   
                        layout_y=(y-100)//40
                        paste_start=[layout_x,layout_y]
                        paste_possible=True

                        #check if paste in position allowed.
                        for cos in consise_copied_machines:
                            new_GreenSquare=GreenSquare((cos[0]+layout_x)*40,(cos[1]+layout_y)*40)
                            area_object.green_square_group.add(new_GreenSquare)

                            if cos[1]+layout_y <0 or cos[1]+layout_y >19 or cos[0]+layout_x<0 or cos[0]+layout_x >19:
                                paste_possible=False
                            elif area_object.factory_layout[cos[1]+layout_y][cos[0]+layout_x]==1:
                                paste_possible =False
                        print(paste_possible)

            elif game_state=='edit': 
                if event.button==3:
                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    item_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_sellers=[]
                    selected_machines=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)         

                elif event.button==2:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_machines=[]
                    selected_sellers=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)  

                elif transparent_grid_button.rect.collidepoint(co):
                    if event.button==1:

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
                        producer_cos=list(area_object.producer_info.keys())
                        crafter_cos=list(area_object.crafter_info.keys())
                        conveyor_cos=list(conveyor_info.keys())
                        seller_cos=list(area_object.seller_info.keys())

                        if area_object.factory_layout[layout_y][layout_x]==1:
                            if decimal_co in producer_cos:
                                if co in selected_producers:
                                    selected_producers.remove(co)
                                    selected_machines.remove(co)
                                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    selection='remove'
                                else:
                                    selected_producers.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    area_object.arrows_group.add(new_arrow)
                                    selection='select'

                            elif decimal_co in crafter_cos:
                                if co in selected_crafters:
                                    selected_crafters.remove(co)
                                    selected_machines.remove(co)
                                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    selection='remove'
                                else:
                                    selected_crafters.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    area_object.arrows_group.add(new_arrow)
                                    selection='select'

                            elif decimal_co in conveyor_cos:
                                if co in selected_conveyors:
                                    selected_conveyors.remove(co) 
                                    selected_machines.remove(co)
                                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    selection='remove'
                                else:
                                    selected_conveyors.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    area_object.arrows_group.add(new_arrow)
                                    selection='select'

                            elif decimal_co in seller_cos:
                                if co in selected_sellers:
                                    selected_sellers.remove(co) 
                                    selected_machines.remove(co)
                                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    selection='remove'
                                else:
                                    selected_sellers.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                    area_object.arrows_group.add(new_arrow)
                                    selection='select'
                            
                            grid_surface_copy= grid_surface.copy()
                            screen.blit(grid_surface_copy,(0,100))
                            rotate_button.draw()
                            delete_button.draw()
                            confirm_button.draw()
                            cancel_button.draw()
                            area_object.producer_group.draw(grid_surface_copy)
                            area_object.crafter_group.draw(grid_surface_copy)
                            area_object.conveyor_group.draw(grid_surface_copy)
                            area_object.seller_group.draw(grid_surface_copy)
                            item_group.draw(grid_surface_copy)
                            area_object.material_group.draw(grid_surface_copy) 
                            area_object.arrows_group.draw(grid_surface_copy)
                        
                elif rotate_button.rect.collidepoint(co):
                    rotate(crafter_upgrades,blueprints,selected_producers,selected_machines,selected_crafters,selected_conveyors,selected_sellers,grid_surface_copy,area_object)
      
                elif delete_button.rect.collidepoint(co):
                    #delete(area_object.factory_layout,selected_producers,area_object.producer_info,area_object.producer_group,selected_crafters,area_object.crafter_info,area_object.crafter_group,selected_conveyors,conveyor_info,area_object.conveyor_group,area_object.arrows_group,area_object.material_group,grid_surface)
                    for pos in selected_producers:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.producer_info.pop(decimal_co)
                    for pos in selected_crafters:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        conveyor_info.pop(decimal_co)
                    for pos in selected_sellers:
                        area_object.factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        area_object.seller_info.pop(decimal_co)


                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_machines=[]
                    selected_sellers=[]

                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.update(area_object.producer_info)
                    area_object.crafter_group.update(area_object.crafter_info,blueprints,crafter_upgrades,area_object.crafter_lv)
                    area_object.conveyor_group.update(conveyor_info)
                    area_object.seller_group.update(area_object.seller_info)
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    item_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)

                elif confirm_button.rect.collidepoint(co):
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_sellers=[]
                    selected_machines=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info) 

                elif cancel_button.rect.collidepoint(co):

                    grid_surface_copy= grid_surface.copy()
                    area_object.producer_group.draw(grid_surface_copy)
                    area_object.crafter_group.draw(grid_surface_copy)
                    area_object.conveyor_group.draw(grid_surface_copy)
                    area_object.seller_group.draw(grid_surface_copy)
                    area_object.material_group.draw(grid_surface_copy)
                    item_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_sellers=[]
                    selected_machines=[]
                    area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)

            elif game_state=='stats':
                if stats_surface.rect.collidepoint(co) == False:
                    reset_counter=0
                    game_state='play'
                elif credits_button.rect.collidepoint(co):
                    game_state='credits'
                elif reset_button.rect.collidepoint(co):

                    reset_counter+=1
                    print(reset_counter)
                    if reset_counter==3:
                        
                        
                        area_object.producer_info={}
                        area_object.crafter_info={}
                        conveyor_info={}
                        area_object.seller_info={}
                        temp_info={}
                        area_object.factory_layout=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
                        area_object.producer_lv =1
                        area_object.crafter_lv =1
                        area_object.conveyor_lv =1
                        area_object.seller_lv =1
                        #usual start 1000
                        money=1000
                        revenue =0
                        previous_revenue=0
                        money_per_min=0
                        saved_time=0
                        area_object.materials_supply={'copper':0,'iron':0,'gold':0,'aluminium':0,'lead':0,'coal':0}

                        for producer in area_object.producer_group:
                            producer.kill()
                        for crafter in area_object.crafter_group:
                            crafter.kill()
                        for conveyor in area_object.conveyor_group:
                            conveyor.kill()
                        for seller in area_object.seller_group:
                            seller.kill()                                                                                    

                        for material in area_object.material_group:
                            material.kill()
                        for item in area_object.item_group:
                            item.kill()

                        data_dict={'producer_info':area_object.producer_info,
                                'crafter_info':area_object.crafter_info,
                                'conveyor_info':area_object.conveyor_info,
                                'seller_info':area_object.seller_info,
                                'factory_layout':area_object.factory_layout,
                                'producer_lv':area_object.producer_lv,
                                'crafter_lv':area_object.crafter_lv,
                                'conveyor_lv':area_object.conveyor_lv,
                                'seller_lv':area_object.seller_lv,
                                'money':money,
                                'revenue':revenue,
                                'previous_revenue':previous_revenue,
                                'money_per_min':money_per_min,
                                'area_object.materials_supply':area_object.materials_supply,
                                'saved_time':saved_time,
                        }     

                        save_data()
                        reset_counter=0
                        game_state='play'                                               
            
            elif game_state=='map':
                if earth_button.rect.collidepoint(co):
                    current_location='earth'
                elif mars_button.rect.collidepoint(co):
                    current_location='mars'
                print(current_location)
                area_object=map_locations[current_location]

            save_data()
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
                    #number of rotations has 8 per screen so -8 shows 2 new at a time so /2 and +1 for extra partition
                    bp_rotations=round(((len(bp_ordered_list)-8)/2))+1 

                    for x in range(1,bp_rotations+1):
                        
                        scrollbar_section=(x*(round(650/bp_rotations)))
                        if current_slider_pos<scrollbar_section and current_slider_pos>((x-1)*(round(650/bp_rotations))):

                            #if titles have already been made for the same section
                            if titles_done_rotation==x:
                                pass
                            else:
                                for blueprint in area_object.blueprints_group:
                                    blueprint.kill()
                                current_rotation=x
                                print((x-1)*(round(650/bp_rotations)),'sections',scrollbar_section)
                                bp_position = (x*2)-2
                                remaining_bp=len(bp_ordered_list)-(bp_position+8)
                                if x == bp_rotations and len(bp_ordered_list)%2 ==1:
                                    for y in range(0,6):
                                        bptitles2[y]=bp_ordered_list[y+bp_position]
                                        new_bp= Blueprints(y+bp_position,y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
                                        area_object.blueprints_group.add(new_bp)
                                    
                                        
                                    bptitles2[6]=bp_ordered_list[len(bp_ordered_list)-1]
                                    new_bp= Blueprints(len(bp_ordered_list)-1,6,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
                                    area_object.blueprints_group.add(new_bp)
                                    bptitles2[7]='nothing'
                                    new_bp= Blueprints(-1,7,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
                                    area_object.blueprints_group.add(new_bp)
                                
                                else:
                                    for y in range(0,8):
                                        bptitles2[y]=bp_ordered_list[y+bp_position]
                                        new_bp= Blueprints((y+bp_position),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
                                        area_object.blueprints_group.add(new_bp)
                                titles_done_rotation = x
                                print('done')
                        

                    bp_title1=font.render(str(bptitles2[0]),True,(0,0,0))
                    bp_title2=font.render(str(bptitles2[1]),False,(0,0,0))
                    bp_title3=font.render(str(bptitles2[2]),False,(0,0,0))
                    bp_title4=font.render(str(bptitles2[3]),False,(0,0,0))
                    bp_title5=font.render(str(bptitles2[4]),False,(0,0,0))
                    bp_title6=font.render(str(bptitles2[5]),False,(0,0,0))
                    bp_title7=font.render(str(bptitles2[6]),False,(0,0,0))
                    bp_title8=font.render(str(bptitles2[7]),False,(0,0,0))

                elif game_state=='shop confirm':
                    if transparent_grid_button.rect.collidepoint(co):
                        x=(co[0]//40)
                        y=(co[1]-100)//40
                        if area_object.factory_layout[y][x]==0:                      
                            if [x,y] not in selected_pos:
                                if selection=='place':
                                    selected_pos.append([x,y])
                                    new_GreenSquare=GreenSquare(x*40,y*40)
                                    area_object.green_square_group.add(new_GreenSquare)
                        
                            else:
                                if selection=='delete':
                                    selected_pos.remove([x,y])  
                                    area_object.green_square_group.update(selected_pos)
                        #area_object.green_square_group.update(selected_pos)
                        grid_surface_copy= grid_surface.copy()
                        screen.blit(grid_surface_copy,(0,100))
                        area_object.green_square_group.draw(grid_surface_copy)
                                                 
                elif game_state=='edit':
                        if transparent_grid_button.rect.collidepoint(co):

                            x=(co[0]//40)
                            y=(co[1]-100)//40
                            co =[x*40,y*40]
                            decimal_co=str(co[0])+'.'+str(co[1])
                            if area_object.factory_layout[y][x]==1:
                                if selection=='select':
                                    if decimal_co in producer_cos:
                                        if co not in selected_producers:
                                            selected_producers.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                            area_object.arrows_group.add(new_arrow)

                                    elif decimal_co in crafter_cos:
                                        if co not in selected_crafters:
                                            selected_crafters.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                            area_object.arrows_group.add(new_arrow)

                                    elif decimal_co in conveyor_cos:
                                        if co not in selected_conveyors:
                                            selected_conveyors.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                            area_object.arrows_group.add(new_arrow)

                                    elif decimal_co in seller_cos:
                                        if co not in selected_sellers:
                                            selected_sellers.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
                                            area_object.arrows_group.add(new_arrow)


                                elif selection =='remove':
                                    if co in selected_machines:
                                        if decimal_co in producer_cos:
                                            if co in selected_producers:
                                                selected_producers.remove(co)
                                                selected_machines.remove(co)
                                                area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)

                                        elif decimal_co in crafter_cos:
                                            if co in selected_producers:
                                                selected_crafters.remove(co)
                                                selected_machines.remove(co)
                                                area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)


                                        elif decimal_co in conveyor_cos:
                                            if co in selected_producers:
                                                selected_conveyors.remove(co)   
                                                selected_machines.remove(co)  
                                                area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)

                                        elif decimal_co in seller_cos:
                                            if co in selected_sellers:
                                                selected_sellers.remove(co)   
                                                selected_machines.remove(co)  
                                                area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)


                                        grid_surface_copy= grid_surface.copy()
                                        screen.blit(grid_surface_copy,(0,100))
                                        rotate_button.draw()
                                        delete_button.draw()
                                        confirm_button.draw()
                                        cancel_button.draw()
                                        area_object.producer_group.draw(grid_surface_copy)
                                        area_object.crafter_group.draw(grid_surface_copy)
                                        area_object.conveyor_group.draw(grid_surface_copy)
                                        area_object.item_group.draw(grid_surface_copy) 
                                        area_object.material_group.draw(grid_surface_copy) 
                                        area_object.seller_group.draw(grid_surface_copy)
                                        area_object.arrows_group.draw(grid_surface_copy)      


#---------------------------------------------------------------------------------------
#what is drawn on each game state is below
    if game_state =='main menu':
        screen.blit(main_menu_bg,(0,0))
        play_button.draw()
        controls_button.draw()
        settings_button.draw()
        exit_button.draw()

    elif game_state=='play':
        for material in area_object.material_group:
            maybe_money = material.update(area_object.seller_lv,seller_upgrades,area_object.conveyor_lv,conveyor_upgrades,area_object.producer_info,conveyor_info,area_object.conveyor_group,area_object.crafter_info,area_object.crafter_group,area_object.seller_group,smelter_group,blueprints_value,money)
            maybe_money=float(maybe_money)
            if maybe_money.is_integer():
                revenue+=(maybe_money-money)
                money=maybe_money
        
        for item in area_object.item_group:
            maybe_money=item.update(area_object.seller_lv,seller_upgrades,area_object.conveyor_lv,conveyor_upgrades,area_object.crafter_info,area_object.conveyor_group,conveyor_info,area_object.crafter_group,area_object.seller_group,money)
            if maybe_money.is_integer():
                revenue+=(maybe_money-money)
                money=maybe_money



       
        screen.fill((52,78,91))
        screen.blit(play_bg_img,(0,0))

        #buttons
        settings_mini_button.draw()
        shop_button.draw()
        edit_button.draw()
        blueprints_button.draw()
        map_button.draw()

        grid_surface_copy= grid_surface.copy()

        #machine stuff
        area_object.producer_group.draw(grid_surface_copy)
        area_object.crafter_group.draw(grid_surface_copy)
        area_object.conveyor_group.draw(grid_surface_copy)
        area_object.seller_group.draw(grid_surface_copy)
        #materials
        area_object.material_group.draw(grid_surface_copy)
        area_object.item_group.draw(grid_surface_copy)


        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)

        screen.blit(grid_surface_copy,(0,100))
        #copy screen
        play_grid_bg=grid_surface_copy.copy()
        play_bg=screen.copy()

    elif game_state=='producer_popup':
        screen.blit(grid_surface_copy,(0,100))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)


        screen.blit(producer_popup_surface,selected_co)
        transparent_producer_popup.draw()
        draw_text('Current Output: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+10,screen,False)
        draw_text(str(area_object.producer_info[decimal_co][2]),font_24,(0,0,0),selected_co[0]+135,selected_co[1]+50,screen,False)

        draw_text('Select New Output: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+80,screen,False)



        selected_material_button.draw()
        copper_button.draw()
        iron_button.draw()
        gold_button.draw()
        aluminium_button.draw()
        coal_button.draw()
        lead_button.draw()
    
    elif game_state=='crafter_popup':
        screen.blit(grid_surface_copy,(0,100))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)

        screen.blit(producer_popup_surface,selected_co)
        transparent_crafter_popup.draw()

        draw_text('Inventory: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+10,screen,False)
        draw_text('Selected Blueprint: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+110,screen,False)
        draw_text(area_object.crafter_info[decimal_co][1],font_24,(0,0,0),selected_co[0]+10,selected_co[1]+125,screen,False)


        draw_text(crafter_inv_quantities[0],font,(0,0,0),selected_co[0]+40,selected_co[1]+50,screen,False)
        draw_text(crafter_inv_quantities[1],font,(0,0,0),selected_co[0]+80,selected_co[1]+50,screen,False)
        draw_text(crafter_inv_quantities[2],font,(0,0,0),selected_co[0]+120,selected_co[1]+50,screen,False)
        draw_text(crafter_inv_quantities[3],font,(0,0,0),selected_co[0]+40,selected_co[1]+90,screen,False)
        draw_text(crafter_inv_quantities[4],font,(0,0,0),selected_co[0]+80,selected_co[1]+90,screen,False)
        draw_text(crafter_inv_quantities[5],font,(0,0,0),selected_co[0]+120,selected_co[1]+90,screen,False)

        inv_button1.draw()
        inv_button2.draw()
        inv_button3.draw()
        inv_button4.draw()
        inv_button5.draw()
        inv_button6.draw()


        #blueprint components
        bp_item_button1.draw()
        bp_item_button2.draw()
        bp_item_button3.draw()
        bp_item_button4.draw()
        bp_item_button5.draw()
        bp_item_button6.draw()

        item_button.draw()

        draw_text(bp_item_quantities[0],font,(0,0,0),selected_co[0]+40,selected_co[1]+160,screen,False)
        draw_text(bp_item_quantities[1],font,(0,0,0),selected_co[0]+80,selected_co[1]+160,screen,False)
        draw_text(bp_item_quantities[2],font,(0,0,0),selected_co[0]+120,selected_co[1]+160,screen,False)
        draw_text(bp_item_quantities[3],font,(0,0,0),selected_co[0]+40,selected_co[1]+200,screen,False)
        draw_text(bp_item_quantities[4],font,(0,0,0),selected_co[0]+80,selected_co[1]+200,screen,False)
        draw_text(bp_item_quantities[5],font,(0,0,0),selected_co[0]+120,selected_co[1]+200,screen,False)

    elif game_state=='shop machines':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)
        shop_surface_copy=shop_surface.copy()
        screen.blit(shop_surface_copy,(100,150))

        machines_button.draw()
        upgrades_button.draw()
        supply_button.draw()
        screen.blit(machines_lable,(130,210))
        screen.blit(upgrades_lable,(335,210))
        screen.blit(supply_lable,(570,210))

        scrollbar_button.draw()
        slider_button.draw()

        producer_buy_button.draw()
        crafter_buy_button.draw()
        conveyor_buy_button.draw()
        seller_buy_button.draw()
        machine1_buy_button.draw()
        machine2_buy_button.draw()
        machine3_buy_button.draw()
        machine4_buy_button.draw()

        producer_button.draw()
        crafter_button.draw()
        conveyor_button.draw()
        seller_button.draw()

        draw_text('Buy Producer',font_32,(0,0,0),245,320,screen,False)
        draw_text('Outputs Materials',font_32,(0,0,0),245,350,screen,False)
        draw_text('Price: 100 each',font_32,(0,0,0),245,380,screen,False)

        draw_text('Buy Crafter',font_32,(0,0,0),550,320,screen,False)
        draw_text('Crafts Items',font_32,(0,0,0),550,350,screen,False)
        draw_text('Price: 100 each',font_32,(0,0,0),550,380,screen,False)

        draw_text('Buy Conveyor',font_32,(0,0,0),245,450,screen,False)
        draw_text('Moves Items',font_32,(0,0,0),245,480,screen,False)
        draw_text('Price: 50 each',font_32,(0,0,0),245,510,screen,False)

        draw_text('Buy Seller',font_32,(0,0,0),550,450,screen,False)
        draw_text('Sells Items',font_32,(0,0,0),550,480,screen,False)
        draw_text('Price: 100 each',font_32,(0,0,0),550,510,screen,False)                

    elif game_state=='shop upgrades':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)
        shop_surface_copy=shop_surface.copy()
        screen.blit(shop_surface_copy,(100,150))

        machines_button.draw()
        upgrades_button.draw()
        supply_button.draw()
        screen.blit(machines_lable,(130,210))
        screen.blit(upgrades_lable,(335,210))
        screen.blit(supply_lable,(570,210))


        producer_upgrade_button.draw()
        crafter_upgrade_button.draw()
        conveyor_upgrade_button.draw()
        seller_upgrade_button.draw()
        machine1_upgrade_button.draw()
        machine2_upgrade_button.draw()
        machine3_upgrade_button.draw()
        machine4_upgrade_button.draw()

        producer_button.draw()
        crafter_button.draw()
        conveyor_button.draw()
        seller_button.draw()


        draw_text('Producer',font_32,(0,0,0),245,320,screen,False)
        draw_text(('Output '+str(producer_upgrades[area_object.producer_lv+1][2])+' Materials'),font_32,(0,0,0),245,350,screen,False)
        draw_text(('Price: '+str(producer_upgrades[area_object.producer_lv+1][0])+producer_upgrades[area_object.producer_lv+1][1]),font_32,(0,0,0),245,380,screen,False)
        draw_text('Buy Upgrade',font_36,(0,0,0),245,405,screen,False)

        draw_text('Crafter',font_32,(0,0,0),550,320,screen,False)
        draw_text(('Craft '+str(crafter_upgrades[area_object.crafter_lv+1][2])+' at once'),font_32,(0,0,0),550,350,screen,False)
        draw_text(('Price: '+str(crafter_upgrades[area_object.crafter_lv+1][0])+crafter_upgrades[area_object.crafter_lv+1][1]),font_32,(0,0,0),550,380,screen,False)
        draw_text('Buy Upgrade',font_36,(0,0,0),550,405,screen,False)

        draw_text('Conveyor',font_32,(0,0,0),245,450,screen,False)
        draw_text(('Move Items +'+str(round((conveyor_upgrades[area_object.conveyor_lv+1][2]-1)*100))+'%'),font_32,(0,0,0),245,480,screen,False)
        draw_text(('Price: '+str(conveyor_upgrades[area_object.conveyor_lv+1][0])+conveyor_upgrades[area_object.conveyor_lv+1][1]),font_32,(0,0,0),245,510,screen,False)
        draw_text('Buy Upgrade',font_36,(0,0,0),245,535,screen,False)

        draw_text('Seller',font_32,(0,0,0),550,450,screen,False)
        draw_text(('Sell Items for +'+str(round(((seller_upgrades[area_object.seller_lv+1][2])-1)*100))+'%'),font_32,(0,0,0),550,480,screen,False)
        draw_text(('Price: '+str(seller_upgrades[area_object.seller_lv+1][0])+seller_upgrades[area_object.seller_lv+1][1]),font_32,(0,0,0),550,510,screen,False) 
        draw_text('Buy Upgrade',font_36,(0,0,0),550,535,screen,False)  

        scrollbar_button.draw()
        slider_button.draw()

    elif game_state=='shop supply':
        area_object.producer_group.update(area_object.producer_info)
        for material in area_object.material_group:
            maybe_money = material.update(area_object.seller_lv,seller_upgrades,area_object.conveyor_lv,conveyor_upgrades,area_object.producer_info,conveyor_info,area_object.conveyor_group,area_object.crafter_info,area_object.crafter_group,area_object.seller_group,smelter_group,blueprints_value,money)
            maybe_money=float(maybe_money)
            if maybe_money.is_integer():
                money=maybe_money
        
        for item in item_group:
            maybe_money=item.update(area_object.seller_lv,seller_upgrades,area_object.conveyor_lv,conveyor_upgrades,area_object.crafter_info,area_object.conveyor_group,conveyor_info,area_object.crafter_group,area_object.seller_group,money)
            if maybe_money.is_integer():
                money=maybe_money


        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)
        shop_surface_copy=shop_surface.copy()
        screen.blit(shop_surface_copy,(100,150))

        machines_button.draw()
        upgrades_button.draw()
        supply_button.draw()
        screen.blit(machines_lable,(130,210))
        screen.blit(upgrades_lable,(335,210))
        screen.blit(supply_lable,(570,210))


        copper_supply_button.draw()
        iron_supply_button.draw()
        gold_supply_button.draw()
        aluminium_supply_button.draw()
        lead_supply_button.draw()
        coal_supply_button.draw()


        copper_shop_button.draw()
        iron_shop_button.draw()
        gold_shop_button.draw()
        aluminium_shop_button.draw()
        lead_shop_button.draw()
        coal_shop_button.draw()

        material_buy1.draw()
        material_buy10.draw()
        material_buy100.draw()
        material_buy1000.draw()
        material_buy10000.draw()

        #left side text
        copper_lable1=font_32.render(('Copper remaining:'),False,(0,0,0))
        copper_lable2=font_50.render(str(area_object.materials_supply['copper']),False,(0,0,0)) 
        copper_lable2_rect=copper_lable2.get_rect(center=(210,350))
        screen.blit(copper_lable2,copper_lable2_rect)
        screen.blit(copper_lable1,(130,305))

        iron_lable1=font_32.render(('Iron remaining:'),False,(0,0,0))
        iron_lable2=font_50.render(str(area_object.materials_supply['iron']),False,(0,0,0)) 
        iron_lable2_rect=iron_lable2.get_rect(center=(210,440))
        screen.blit(iron_lable2,iron_lable2_rect)
        screen.blit(iron_lable1,(140,395))

        gold_lable1=font_32.render(('Gold remaining:'),False,(0,0,0))
        gold_lable2=font_50.render(str(area_object.materials_supply['gold']),False,(0,0,0)) 
        gold_lable2_rect=gold_lable2.get_rect(center=(210,530))
        screen.blit(gold_lable2,gold_lable2_rect)
        screen.blit(gold_lable1,(140,485))        

        aluminium_lable1=font_32.render(('Aluminium remaining:'),False,(0,0,0))
        aluminium_lable2=font_50.render(str(area_object.materials_supply['aluminium']),False,(0,0,0)) 
        aluminium_lable2_rect=aluminium_lable2.get_rect(center=(210,620))
        screen.blit(aluminium_lable2,aluminium_lable2_rect)
        screen.blit(aluminium_lable1,(124,575))        

        lead_lable1=font_32.render(('Lead remaining:'),False,(0,0,0))
        lead_lable2=font_50.render(str(area_object.materials_supply['lead']),False,(0,0,0)) 
        lead_lable2_rect=lead_lable2.get_rect(center=(210,720))
        screen.blit(lead_lable2,lead_lable2_rect)
        screen.blit(lead_lable1,(140,675))

        coal_lable1=font_32.render(('Coal remaining:'),False,(0,0,0))
        coal_lable2=font_50.render(str(area_object.materials_supply['coal']),False,(0,0,0)) 
        coal_lable2_rect=coal_lable2.get_rect(center=(210,810))
        screen.blit(coal_lable2,coal_lable2_rect)
        screen.blit(coal_lable1,(140,765))        

        #right side texts
        if selected_material=='aluminium':
            material_text ='alum'
        elif selected_material=='copper':
            material_text ='copp'
        else:
            material_text=selected_material

        buy1_lable1=font_32.render(('Buy 1 '+str(material_text)+' Costs:'),False,(0,0,0))
        buy1_lable2=font_50.render('10',False,(0,0,0)) 
        screen.blit(buy1_lable1,(540,305))
        screen.blit(buy1_lable2,(615,340)) 

        buy10_lable1=font_32.render(('Buy 10 '+str(material_text)+' Costs:'),False,(0,0,0))
        buy10_lable2=font_50.render('100',False,(0,0,0)) 
        screen.blit(buy10_lable1,(540,395))
        screen.blit(buy10_lable2,(610,440))  

        buy100_lable1=font_32.render(('Buy 100 '+str(material_text)+' Costs:'),False,(0,0,0))
        buy100_lable2=font_50.render('1000',False,(0,0,0)) 
        screen.blit(buy100_lable1,(540,485))
        screen.blit(buy100_lable2,(600,530)) 
         
        buy1000_lable1=font_32.render(('Buy 1k '+str(material_text)+' Costs:'),False,(0,0,0))
        buy1000_lable2=font_50.render('10000',False,(0,0,0)) 
        screen.blit(buy1000_lable1,(540,575))
        screen.blit(buy1000_lable2,(595,620))  

        buy1000_lable1=font_32.render(('Buy 1k '+str(material_text)+' Costs:'),False,(0,0,0))
        buy1000_lable2=font_50.render('10000',False,(0,0,0)) 
        screen.blit(buy1000_lable1,(540,575))
        screen.blit(buy1000_lable2,(595,620))  

        draw_text('Buy 10k '+str(material_text)+' Costs:',font_32,(0,0,0),540,665,screen,False)
        draw_text('100k',font_50,(0,0,0),600,710,screen,False)







        scrollbar_button.draw()
        slider_button.draw()

    elif game_state=='blueprints':
        shop_bg_copy=shop_bg.copy()
        
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)


        area_object.blueprints_group.draw(shop_bg_copy)

        
        screen.blit(shop_bg_copy,(0,0))
        #transparent_popup_button.draw()
        scrollbar_button.draw()
        slider_button.draw()
        area_object.blueprints_group.update(screen,item_imgs)

    elif game_state=='shop confirm':
        grid_surface_copy=grid_surface.copy()
        
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)
        machines_price_button=Buttons(800,500,gui_flat_img,0.5,1)
        machines_price_button.draw()

        machine_price_lable1=font_24.render(('Price:'),False,(0,0,0))
        machine_price_lable2=font_24.render(str(len(selected_pos)*prices[selected_machine]),False,(0,0,0))
        screen.blit(machine_price_lable1,(805,505))
        screen.blit(machine_price_lable2,(805,525))

        transparent_grid_button.draw()
        #machine stuff
        area_object.producer_group.draw(grid_surface_copy)
        area_object.crafter_group.draw(grid_surface_copy)
        area_object.conveyor_group.draw(grid_surface_copy)
        area_object.seller_group.draw(grid_surface_copy)
        #materials
        area_object.material_group.draw(grid_surface_copy)        
        area_object.item_group.draw(grid_surface_copy)
        
        confirm_button.draw()
        cancel_button.draw()
        area_object.green_square_group.update(selected_pos)
        area_object.green_square_group.draw(grid_surface_copy)
        screen.blit(grid_surface_copy,(0,100))
        
    elif game_state=='edit':
        screen.blit(grid_surface_copy,(0,100))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)
        rotate_button.draw()
        delete_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        area_object.arrows_group.update(selected_machines,area_object.producer_info,area_object.crafter_info,conveyor_info,area_object.seller_info)
        area_object.arrows_group.draw(grid_surface_copy)
        if have_producer: 
            area_object.producer_group.update(area_object.producer_info)

    elif game_state=='edit paste':
        grid_surface_copy2=grid_surface_copy.copy()
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button)
        area_object.green_square_group.draw(grid_surface_copy2)
        area_object.producer_group.draw(grid_surface_copy2)
        area_object.crafter_group.draw(grid_surface_copy2)
        area_object.conveyor_group.draw(grid_surface_copy2)
        area_object.seller_group.draw(grid_surface_copy2)
        screen.blit(grid_surface_copy2,(0,100))

    elif game_state=='map':
        earth_button.draw()
        mars_button.draw()
        draw_text('Earth',font,(0,0,0),110,55,screen,False)
        draw_text('Mars',font,(0,0,0),110,130,screen,False)
        

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

        draw_text('Guide',font_60,(255,255,255),150,120,screen,False)
        draw_text('Keybinds',font_60,(255,255,255),600,120,screen,False)


        screen.blit(producer_img,(50,200))
        draw_text('Producer:outputs materials towards ',font_32,(255,255,255),100,200,screen,False)
        draw_text('arrow. choose its output by clicking it',font_32,(255,255,255),100,220,screen,False)

        screen.blit(crafter_img,(50,250))
        draw_text('Crafter: choose blueprint by clicking it',font_32,(255,255,255),100,250,screen,False)
        draw_text('-> click bottom right image -> choose bp ',font_32,(255,255,255),100,270,screen,False)

        screen.blit(conveyor_img,(50,300))
        draw_text('Conveyor:moves anything on it',font_32,(255,255,255),100,300,screen,False)
        draw_text('in the direction of the arrows.',font_32,(255,255,255),100,320,screen,False)

        screen.blit(seller_img,(50,350))
        draw_text('Seller: sells anything inputted into it',font_32,(255,255,255),100,350,screen,False)
        draw_text('takes input from all directions',font_32,(255,255,255),100,370,screen,False)        

        draw_text('Goal: craft the rocket',font_32,(255,255,255),100,800,screen,False)
        draw_text('Goal: get gud lol',font_32,(57,83,96),100,820,screen,False)

        draw_text('Esc : goes to previous page',font_32,(255,255,255),500,200,screen,False)
        draw_text('Enter : confirm changes',font_32,(255,255,255),500,220,screen,False)

        draw_text('S : goes to shop page',font_32,(255,255,255),500,250,screen,False)
        draw_text('1 : select producer',font_32,(255,255,255),500,270,screen,False)
        draw_text('2 : select crafter',font_32,(255,255,255),500,290,screen,False)
        draw_text('3 : select conveyor',font_32,(255,255,255),500,310,screen,False)
        draw_text('4 : select seller',font_32,(255,255,255),500,330,screen,False)
        draw_text('M : goes to machine tab',font_32,(255,255,255),500,350,screen,False)
        draw_text('U : goes to upgrade tab',font_32,(255,255,255),500,370,screen,False)
        draw_text('S : goes to supply tab',font_32,(255,255,255),500,390,screen,False)

        draw_text('E : goes to edit mode',font_32,(255,255,255),500,420,screen,False)
        draw_text('W : move selected machines up',font_32,(255,255,255),500,440,screen,False)
        draw_text('A : move selected machines left',font_32,(255,255,255),500,460,screen,False)
        draw_text('S : move selected machines right',font_32,(255,255,255),500,480,screen,False)
        draw_text('D : move selected machines down',font_32,(255,255,255),500,500,screen,False)
        draw_text('X : Delete selected machines',font_32,(255,255,255),500,520,screen,False)
        draw_text('C : copy selected machines',font_32,(255,255,255),500,540,screen,False)
        draw_text('V : paste mode and click where to place',font_32,(255,255,255),500,560,screen,False)

        draw_text('B : goes to blueprint mode',font_32,(255,255,255),500,590,screen,False)
        draw_text('m : goes to map mode',font_32,(255,255,255),500,610,screen,False)

        draw_text('right click : confirm changes',font_32,(255,255,255),500,640,screen,False)
        draw_text('middle click : goes to previous page',font_32,(255,255,255),500,660,screen,False)
               
    elif game_state =='settings':
        back_button.draw()
 
    elif game_state=='temp shop':
        screen.blit(play_bg,(0,0))
        screen.blit(blueprint_surface,(100,150))
        shop_bg=screen.copy()
        for blueprint in area_object.blueprints_group:
            blueprint.kill()

        for y in range(0,8):
            bptitles2[y]=bp_ordered_list[y]
            new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font)
            area_object.blueprints_group.add(new_bp)
        game_state='blueprints'

    elif game_state=='stats':
        screen.blit(grid_surface_copy,(0,100))
        stats_surface.draw()
        #gets current play time and transorms it into days hours minutes and seconds.
        current_time=pygame.time.get_ticks()+saved_time
        current_time =current_time//1000
        total_m =current_time//60
        total_h =current_time//3600
        total_d =current_time//(3600*24)
        current_d=total_d
        current_h=(current_time-((current_time//(3600*24))*3600*24))//3600
        current_m=(current_time-((current_time//(3600))*3600))//60
        current_s=(current_time-((current_time//(60))*60))


        #gets revenue and transorms it into abbreviated version
        counter=0
        revenue1=revenue
        abbreviation={0:'',1:'K',2:'M',3:'B',4:'T',5:'q',6:'Q'}
        allowed=True
        while allowed:
            revenue1=revenue1//1000
            if revenue1 >=10:
                counter+=1
            else:
                allowed=False

        draw_text('Statistics',font_60,(0,0,0),310,230,screen,False)
        draw_text('Revenue: '+ str(round(revenue/(1000**(counter)),1))+str(abbreviation[counter]),font_40,(255,255,255),210,300,screen,False)
        draw_text('Total play time: '+str(current_d)+'d '+str(current_h)+'h '+str(current_m)+'m '+str(current_s)+'s',font_40,(255,255,255),210,350,screen,False)
        draw_text('Skill level: Trash ',font_40,(255,255,255),210,400,screen,False)
        
        credits_button.draw()
        reset_button.draw()

        draw_text('Credits',font_24,(255,255,255),270,520,screen,False)
        draw_text('Reset Data',font_20,(255,255,255),470,510,screen,False)
        draw_text('Clicks Left: '+str(3-reset_counter),font_20,(255,255,255),465,525,screen,False)

    elif game_state=='credits':
        draw_text('Credits',font_100,(255,255,255),340,100,screen,False)

        draw_text('Amin, The Almighty Overlord',font_90,(255,255,255),450,200,screen,True)

        draw_text('Krish, The Legendary Gamer',font_70,(255,255,255),450,300,screen,True)
        draw_text('Destroyer Of Worlds, Ben',font_70,(255,255,255),450,350,screen,True)
        draw_text('Marwan, The Undead',font_70,(255,255,255),450,400,screen,True)
        draw_text('Noah, The Scary Pikachu',font_70,(255,255,255),450,450,screen,True)
        draw_text('Abdul Muhaymin, The Cool Guy',font_70,(255,255,255),450,500,screen,True)
        draw_text('Sofian G, Greatest Morrocan Of All Time',font_70,(255,255,255),450,550,screen,True)



        draw_text('Siblings, The Feature Delaying Time Wasting Testers',font_50,(255,255,255),450,700,screen,True)
        
        draw_text(' ',font_60,(255,255,255),390,100,screen,True)
        
    pygame.display.update()
    clock.tick(60)