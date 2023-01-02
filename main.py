import pygame 
import os
import pickle
from sys import exit
import time
from button_functions import *
from classes import *
from variables import *
pygame.init()
pygame.font.init()

global money
#usual start 1000 money
money=1000

file_exists = os.path.exists("Galactic_Crafters.txt")

if file_exists == True:
    data_load = open("Galactic_Crafters.txt", "r")
    data1 = pickle.load(game_data)
else:
    game_data = open("Galactic_Crafters.txt", "w")



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

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()          
        if event.type ==seconds_event:
            if game_state in ('play','shop supply'):
                screen.blit(grid_surface,(0,100))
                producer_cos=list(producer_info.keys())
                for x in producer_cos:
                    co = x.split('.')
                    co[0]=int(co[0])
                    co[1]=int(co[1])
                    created_material=producer_info[x][1]
                    material_quantity =producer_info[x][2]
                    if materials_supply[created_material]>=material_quantity:
                        materials_supply[created_material]=materials_supply[created_material]-material_quantity
                        material_group.add(Producer.create_material('self',co,producer_info))

                for crafter in crafter_group:
                    amount_maybe=crafter.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    if amount_maybe!=False:
                        item_group.add(crafter.create_item(blueprints_value,item_imgs,amount_maybe))

        if event.type==minute_event:
            money_per_min=revenue-previous_revenue
            previous_revenue=revenue

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
                    for blueprint in blueprints_group:
                        blueprint.kill()

                    for y in range(0,8):
                        bptitles2[y]=bp_ordered_list[y]
                        new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                        blueprints_group.add(new_bp)

                        
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
                    print('enter')
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_lv,producer_upgrades,crafter_lv,crafter_upgrades,conveyor_lv,conveyor_upgrades,seller_lv,seller_upgrades,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout,money)
                    selected_pos=[]
                    game_state='play' 

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
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)

                elif event.key ==pygame.K_RETURN:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_machines=[]
                    selected_sellers=[]
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)  
                
                elif event.key ==pygame.K_r:
                    rotate(crafter_upgrades,crafter_lv,blueprints,selected_producers,selected_machines,arrows_group,material_group,item_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy)
                elif event.key ==pygame.K_x:
                    #delete(factory_layout,selected_producers,producer_info,producer_group,crafter_info,selected_crafters,crafter_group,selected_conveyors,conveyor_info,conveyor_group,arrows_group,material_group,grid_surface)
                    print(selected_producers,'to delete')
                    print(producer_info)
                    for pos in selected_producers:
                        print(pos[0]/40)
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        producer_info.pop(decimal_co)
                    print(producer_info)
                    for pos in selected_crafters:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        conveyor_info.pop(decimal_co)
                    for pos in selected_sellers:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        seller_info.pop(decimal_co)

                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_sellers=[]
                    selected_machines=[]


                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)

                elif event.key ==pygame.K_LEFT:
                    move('left',selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,selected_machines,factory_layout,arrows_group,Arrow)

                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    arrows_group.draw(grid_surface_copy)

                elif event.key ==pygame.K_UP:
                    move('up',selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,selected_machines,factory_layout,arrows_group,Arrow)


                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    arrows_group.draw(grid_surface_copy)
                
                elif event.key==pygame.K_RIGHT:                    
                    move('right',selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,selected_machines,factory_layout,arrows_group,Arrow)


                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    arrows_group.draw(grid_surface_copy)

                elif event.key ==pygame.K_DOWN:
                    move('down',selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,selected_machines,factory_layout,arrows_group,Arrow)


                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    arrows_group.draw(grid_surface_copy)        

                elif event.key==pygame.K_c:
                    minimum_co_x =400
                    maximum_co_x =0
                    minimum_co_y =400
                    maximum_co_y =0
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
                            consise_layout[layout_co[1]][layout_co[0]]={'producer':producer_info[decimal_co]}
                            print(consise_layout[layout_co[1]][layout_co[0]])
                        elif cos in selected_crafters:
                            copied_c_info=crafter_info[decimal_co]
                            copied_c_info[2]={}
                            consise_layout[layout_co[1]][layout_co[0]]={'crafter':copied_c_info}
                        elif cos in selected_conveyors:
                            consise_layout[layout_co[1]][layout_co[0]]={'conveyor':conveyor_info[decimal_co]}
                        elif cos in selected_sellers:
                            consise_layout[layout_co[1]][layout_co[0]]={'seller':seller_info[decimal_co]}
                
                    for x in consise_layout:
                        for y in x:
                            print(y,end = " ")
                        print()
                    
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
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info) 

                elif event.key==pygame.K_RETURN:
                    print('return pressed')
                    copy_price = copied_producers*prices['producer']+copied_crafters*prices['crafter']+copied_conveyors*prices['conveyor']+copied_sellers*prices['seller']
                    if paste_possible==True and money>=copy_price:
                        print('this',producer_info)
                        for cos in consise_copied_machines:
                            pos=[cos[0]*40,cos[1]*40]

                            copied_info=consise_layout[cos[1]][cos[0]]
                            copied_keys=list(copied_info.keys())
                            copied_machine=copied_keys[0]

                            if copied_machine=='producer':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                producer_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_producer=Producer(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],producer_img,producer_info)
                                producer_group.add(new_producer)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='crafter':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                crafter_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_crafter=Crafter(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],crafter_img)
                                crafter_group.add(new_crafter)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='conveyor':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                conveyor_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_conveyor=Conveyor(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],conveyor_img)
                                conveyor_group.add(new_conveyor)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='seller':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                seller_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_seller=Seller(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],seller_img)
                                seller_group.add(new_seller)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                        paste_possible=False
                        money-=copy_price
                            
            elif game_state=='map':
                if event.key==pygame.K_ESCAPE:
                    game_state='play'

            elif game_state=='stats':
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
                    game_state='shop machines'
                
                elif edit_button.rect.collidepoint(co):
                    game_state='edit'
                
                elif blueprints_button.rect.collidepoint(co):
                    game_state='temp shop'
                    slider_button.rect.top=150
                    for blueprint in blueprints_group:
                        blueprint.kill()

                    for y in range(0,8):
                        bptitles2[y]=bp_ordered_list[y]
                        new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                        blueprints_group.add(new_bp)

                elif map_button.rect.collidepoint(co):
                    game_state='map'
                
                elif transparent_grid_button.rect.collidepoint(co):
                    x,y=co[0],co[1]
                    x=(x//40)
                    y=(y-100)//40
                    if factory_layout[y][x]==1:
                        producer_cos=list(producer_info.keys())
                        crafter_cos=list(crafter_info.keys())
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
                            selected_material_button=Buttons(co[0]+45,co[1]+20,item_imgs[producer_info[decimal_co][1]],0.5,0.5)
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

                            
                            item_types=len(crafter_info[decimal_co][2].keys())
                            item_types_list=list(crafter_info[decimal_co][2].keys())
                        

                            crafter_inv_items=['empty','empty','empty','empty','empty','empty']
                            crafter_inv_quantities=['0','0','0','0','0','0']

                            for i in range(item_types):
                                crafter_inv_items[i]=item_types_list[i]
                                crafter_inv_quantities[i]=str(crafter_info[decimal_co][2][item_types_list[i]])
                                
                            inv_button1=Buttons(co[0],co[1]+30,item_imgs[crafter_inv_items[0]],0.25,0.25)
                            inv_button2=Buttons(co[0]+40,co[1]+30,item_imgs[crafter_inv_items[1]],0.25,0.25)
                            inv_button3=Buttons(co[0]+80,co[1]+30,item_imgs[crafter_inv_items[2]],0.25,0.25)
                            inv_button4=Buttons(co[0],co[1]+70,item_imgs[crafter_inv_items[3]],0.25,0.25)
                            inv_button5=Buttons(co[0]+40,co[1]+70,item_imgs[crafter_inv_items[4]],0.25,0.25)
                            inv_button6=Buttons(co[0]+80,co[1]+70,item_imgs[crafter_inv_items[5]],0.25,0.25)


                            bp_item_types=len(blueprints[crafter_info[decimal_co][1]].keys())
                            bp_items_list=list(blueprints[crafter_info[decimal_co][1]].keys())

                            bp_items=['empty','empty','empty','empty','empty','empty']
                            bp_item_quantities=['0','0','0','0','0','0']

                            for i in range (bp_item_types):
                                bp_items[i]=bp_items_list[i]
                                bp_item_quantities[i]=str(blueprints[crafter_info[decimal_co][1]][bp_items_list[i]])

                            bp_item_button1=Buttons(co[0],co[1]+140,item_imgs[bp_items[0]],0.25,0.25)
                            bp_item_button2=Buttons(co[0]+40,co[1]+140,item_imgs[bp_items[1]],0.25,0.25)
                            bp_item_button3=Buttons(co[0]+80,co[1]+140,item_imgs[bp_items[2]],0.25,0.25)
                            bp_item_button4=Buttons(co[0],co[1]+180,item_imgs[bp_items[3]],0.25,0.25)
                            bp_item_button5=Buttons(co[0]+40,co[1]+180,item_imgs[bp_items[4]],0.25,0.25)
                            bp_item_button6=Buttons(co[0]+80,co[1]+180,item_imgs[bp_items[5]],0.25,0.25)

                            item_button=Buttons(co[0]+140,co[1]+165,item_imgs[crafter_info[decimal_co][1]],0.15,0.15)


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
                elif item_button.rect.collidepoint(co):
                    game_state='temp shop'
                    slider_button.rect.top=150


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
                    if money>=producer_upgrades[producer_lv+1][0]*10**abreviations[producer_upgrades[producer_lv+1][1]]:
                        money-=producer_upgrades[producer_lv+1][0]*10**abreviations[producer_upgrades[producer_lv+1][1]]
                        producer_lv+=1
                        producer_cos=list(producer_info.keys())
                        for cos in producer_cos:
                            producer_info[cos][2]=producer_upgrades[producer_lv][2]
                elif crafter_upgrade_button.rect.collidepoint(co):
                    if money>=crafter_upgrades[crafter_lv+1][0]*10**abreviations[crafter_upgrades[crafter_lv+1][1]]:
                        money-=crafter_upgrades[crafter_lv+1][0]*10**abreviations[crafter_upgrades[crafter_lv+1][1]]
                        crafter_lv+=1
                elif conveyor_upgrade_button.rect.collidepoint(co):
                    if money>=conveyor_upgrades[conveyor_lv+1][0]*10**abreviations[conveyor_upgrades[conveyor_lv+1][1]]:
                        money-=conveyor_upgrades[conveyor_lv+1][0]*10**abreviations[conveyor_upgrades[conveyor_lv+1][1]]
                        conveyor_lv+=1
                elif seller_upgrade_button.rect.collidepoint(co):
                    if money>=seller_upgrades[seller_lv+1][0]*10**abreviations[seller_upgrades[seller_lv+1][1]]:
                        money-=seller_upgrades[seller_lv+1][0]*10**abreviations[seller_upgrades[seller_lv+1][1]]
                        seller_lv+=1
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
                            materials_supply[selected_material]=materials_supply[selected_material]+1
                    elif material_buy10.rect.collidepoint(co):
                        if money>=100:
                            money-=100
                            materials_supply[selected_material]=materials_supply[selected_material]+10
                    elif material_buy100.rect.collidepoint(co):
                        if money>=1000:
                            money-=1000                        
                            materials_supply[selected_material]=materials_supply[selected_material]+100
                    elif material_buy1000.rect.collidepoint(co):
                        if money>=10000:
                            money-=10000                        
                            materials_supply[selected_material]=materials_supply[selected_material]+1000

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
  

                if choose_bp == True:
                    for bp in blueprints_group:
                        if bp.rect.collidepoint(co):
                            selected_bp =bp.bp_title
                            crafter_info[last_selected_crafter][1]=selected_bp
                            game_state='play'
                            print(crafter_info,'new bp selected')
                    choose_bp=False
                                 
            elif game_state=='shop confirm':
                if event.button==3:
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_lv,producer_upgrades,crafter_lv,crafter_upgrades,conveyor_lv,conveyor_upgrades,seller_lv,seller_upgrades,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout,money)
                    selected_pos=[]
                    print(crafter_info)
                    game_state = 'play'

                elif transparent_grid_button.rect.collidepoint(co):
                    if event.button ==1:
                        grid_surface_copy=play_grid_bg
                        slider_drag=True
                        y=(y-100)//40
                        x=(x//40)

                        if factory_layout[y][x]==0:
                            if [x,y] in selected_pos:
                                selected_pos.remove([x,y])
                                selection='delete'
                                green_square_group.update(selected_pos)

                            else:
                                selected_pos.append([x,y])
                                new_GreenSquare=GreenSquare(x*40,y*40)
                                green_square_group.add(new_GreenSquare)
                                selection='place'

                        grid_surface_copy= grid_surface.copy()
                        green_square_group.draw(grid_surface_copy)
                        print('selected pos',selected_pos)



                elif confirm_button.rect.collidepoint(co):
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_lv,producer_upgrades,crafter_lv,crafter_upgrades,conveyor_lv,conveyor_upgrades,seller_lv,seller_upgrades,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout,money)
                    selected_pos=[]
                    print(crafter_info)
                    game_state = 'play'
                elif cancel_button.rect.collidepoint(co):
                    game_state='play'
                    selected_pos=[]

            elif game_state=='edit paste':
                if event.button==3:
                    copy_price = copied_producers*prices['producer']+copied_crafters*prices['crafter']+copied_conveyors*prices['conveyor']+copied_sellers*prices['seller']
                    if paste_possible==True and money>=copy_price:
                        print('this',producer_info)
                        for cos in consise_copied_machines:
                            pos=[cos[0]*40,cos[1]*40]

                            copied_info=consise_layout[cos[1]][cos[0]]
                            copied_keys=list(copied_info.keys())
                            copied_machine=copied_keys[0]

                            if copied_machine=='producer':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                producer_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_producer=Producer(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],producer_img,producer_info)
                                producer_group.add(new_producer)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='crafter':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                crafter_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_crafter=Crafter(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],crafter_img)
                                crafter_group.add(new_crafter)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='conveyor':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                conveyor_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_conveyor=Conveyor(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],conveyor_img)
                                conveyor_group.add(new_conveyor)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                            elif copied_machine=='seller':
                                decimal_co=str(paste_start[0]*40+pos[0])+'.'+str(paste_start[1]*40+pos[1])
                                seller_info[decimal_co]=copied_info[copied_keys[0]].copy()
                                new_seller=Seller(paste_start[0]*40+pos[0],paste_start[1]*40+pos[1],seller_img)
                                seller_group.add(new_seller)
                                factory_layout[paste_start[1]+cos[1]][paste_start[0]+cos[0]]=1
                        paste_possible=False

                elif event.button==2:
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_sellers=[]
                    selected_machines=[]
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)

                elif transparent_grid_button.rect.collidepoint(co):
                    if event.button==1:
                        for sprite in green_square_group:
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
                            green_square_group.add(new_GreenSquare)

                            if cos[1]+layout_y <0 or cos[1]+layout_y >19 or cos[0]+layout_x<0 or cos[0]+layout_x >19:
                                paste_possible=False
                            elif factory_layout[cos[1]+layout_y][cos[0]+layout_x]==1:
                                paste_possible =False
                        print(paste_possible)

            elif game_state=='edit': 
                if event.button==3:
                    grid_surface_copy= grid_surface.copy()
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_sellers=[]
                    selected_machines=[]
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)         

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
                        producer_cos=list(producer_info.keys())
                        crafter_cos=list(crafter_info.keys())
                        conveyor_cos=list(conveyor_info.keys())
                        seller_cos=list(seller_info.keys())

                        if factory_layout[layout_y][layout_x]==1:
                            if decimal_co in producer_cos:
                                if co in selected_producers:
                                    selected_producers.remove(co)
                                    selected_machines.remove(co)
                                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                                    print(selected_machines)
                                    selection='remove'
                                    print(selected_producers,'selected producers')
                                else:
                                    selected_producers.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                    arrows_group.add(new_arrow)
                                    selection='select'
                                    print(selected_producers,'selected producers')

                            elif decimal_co in crafter_cos:
                                if co in selected_crafters:
                                    selected_crafters.remove(co)
                                    selected_machines.remove(co)
                                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                                    selection='remove'
                                else:
                                    selected_crafters.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                    arrows_group.add(new_arrow)
                                    selection='select'
                                    print(selected_crafters,'selected crafters')

                            elif decimal_co in conveyor_cos:
                                if co in selected_conveyors:
                                    selected_conveyors.remove(co) 
                                    selected_machines.remove(co)
                                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                                    selection='remove'
                                else:
                                    selected_conveyors.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                    arrows_group.add(new_arrow)
                                    selection='select'
                                    print(selected_conveyors,'selected connveyors')

                            elif decimal_co in seller_cos:
                                if co in selected_sellers:
                                    selected_sellers.remove(co) 
                                    selected_machines.remove(co)
                                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                                    selection='remove'
                                else:
                                    selected_sellers.append(co)
                                    selected_machines.append(co)
                                    new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                    arrows_group.add(new_arrow)
                                    selection='select'
                                    print(selected_sellers,'selected sellers')
                            
                            grid_surface_copy= grid_surface.copy()
                            screen.blit(grid_surface_copy,(0,100))
                            rotate_button.draw()
                            delete_button.draw()
                            confirm_button.draw()
                            cancel_button.draw()
                            producer_group.draw(grid_surface_copy)
                            crafter_group.draw(grid_surface_copy)
                            conveyor_group.draw(grid_surface_copy)
                            seller_group.draw(grid_surface_copy)
                            item_group.draw(grid_surface_copy)
                            material_group.draw(grid_surface_copy) 
                            arrows_group.draw(grid_surface_copy)
                        
                elif rotate_button.rect.collidepoint(co):
                    rotate(crafter_upgrades,crafter_lv,blueprints,selected_producers,selected_machines,arrows_group,material_group,item_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy)
      
                elif delete_button.rect.collidepoint(co):
                    #delete(factory_layout,selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,arrows_group,material_group,grid_surface)
                    print(selected_producers,'to delete')
                    print(producer_info)
                    for pos in selected_producers:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        producer_info.pop(decimal_co)
                    print(producer_info)
                    for pos in selected_crafters:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        crafter_info.pop(decimal_co)
                    for pos in selected_conveyors:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        conveyor_info.pop(decimal_co)
                    for pos in selected_sellers:
                        factory_layout[int(pos[1]/40)][int(pos[0]/40)]=0
                        decimal_co=str(pos[0])+'.'+str(pos[1])
                        seller_info.pop(decimal_co)


                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]     
                    selected_machines=[]
                    selected_sellers=[]

                    grid_surface_copy= grid_surface.copy()
                    producer_group.update(producer_info)
                    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    item_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)

                elif confirm_button.rect.collidepoint(co):
                    game_state='play'
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[] 
                    selected_sellers=[]
                    selected_machines=[]
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info) 

                elif cancel_button.rect.collidepoint(co):

                    grid_surface_copy= grid_surface.copy()
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    item_group.draw(grid_surface_copy)
                    selected_producers=[]
                    selected_crafters=[]
                    selected_conveyors=[]
                    selected_sellers=[]
                    selected_machines=[]
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)

            elif game_state=='stats':
                if stats_surface.rect.collidepoint(co) == False:
                    game_state='play'
        
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
                                for blueprint in blueprints_group:
                                    blueprint.kill()
                                current_rotation=x
                                print((x-1)*(round(650/bp_rotations)),'sections',scrollbar_section)
                                bp_position = (x*2)-2
                                remaining_bp=len(bp_ordered_list)-(bp_position+8)
                                if x == bp_rotations and len(bp_ordered_list)%2 ==1:
                                    for y in range(0,6):
                                        bptitles2[y]=bp_ordered_list[y+bp_position]
                                        new_bp= Blueprints(y+bp_position,y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                                        blueprints_group.add(new_bp)
                                    
                                        
                                    bptitles2[6]=bp_ordered_list[len(bp_ordered_list)-1]
                                    new_bp= Blueprints(len(bp_ordered_list)-1,6,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                                    blueprints_group.add(new_bp)
                                    bptitles2[7]='nothing'
                                    new_bp= Blueprints(-1,7,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                                    blueprints_group.add(new_bp)
                                    print('six')
                                
                                else:
                                    for y in range(0,8):
                                        bptitles2[y]=bp_ordered_list[y+bp_position]
                                        new_bp= Blueprints((y+bp_position),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                                        blueprints_group.add(new_bp)
                                    print('eights')
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
                    print(selected_pos)
                    if transparent_grid_button.rect.collidepoint(co):
                        x=(co[0]//40)
                        y=(co[1]-100)//40
                        if factory_layout[y][x]==0:                      
                            if [x,y] not in selected_pos:
                                if selection=='place':
                                    selected_pos.append([x,y])
                                    new_GreenSquare=GreenSquare(x*40,y*40)
                                    green_square_group.add(new_GreenSquare)
                        
                            else:
                                if selection=='delete':
                                    selected_pos.remove([x,y])  
                                    green_square_group.update(selected_pos)
                        print(selected_pos)            
                        #green_square_group.update(selected_pos)
                        grid_surface_copy= grid_surface.copy()
                        screen.blit(grid_surface_copy,(0,100))
                        green_square_group.draw(grid_surface_copy)
                                                 
                elif game_state=='edit':
                        if transparent_grid_button.rect.collidepoint(co):

                            x=(co[0]//40)
                            y=(co[1]-100)//40
                            co =[x*40,y*40]
                            decimal_co=str(co[0])+'.'+str(co[1])
                            if factory_layout[y][x]==1:
                                if selection=='select':
                                    if decimal_co in producer_cos:
                                        if co not in selected_producers:
                                            selected_producers.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                            arrows_group.add(new_arrow)

                                    elif decimal_co in crafter_cos:
                                        if co not in selected_crafters:
                                            selected_crafters.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                            arrows_group.add(new_arrow)

                                    elif decimal_co in conveyor_cos:
                                        if co not in selected_conveyors:
                                            selected_conveyors.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                            arrows_group.add(new_arrow)

                                    elif decimal_co in seller_cos:
                                        if co not in selected_sellers:
                                            selected_sellers.append(co)
                                            selected_machines.append(co)
                                            new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
                                            arrows_group.add(new_arrow)


                                elif selection =='remove':
                                    if co in selected_machines:
                                        if decimal_co in producer_cos:
                                            if co in selected_producers:
                                                selected_producers.remove(co)
                                                selected_machines.remove(co)
                                                arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)

                                        elif decimal_co in crafter_cos:
                                            if co in selected_producers:
                                                selected_crafters.remove(co)
                                                selected_machines.remove(co)
                                                arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)


                                        elif decimal_co in conveyor_cos:
                                            if co in selected_producers:
                                                selected_conveyors.remove(co)   
                                                selected_machines.remove(co)  
                                                arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)

                                        elif decimal_co in seller_cos:
                                            if co in selected_sellers:
                                                selected_sellers.remove(co)   
                                                selected_machines.remove(co)  
                                                arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)


                                        grid_surface_copy= grid_surface.copy()
                                        screen.blit(grid_surface_copy,(0,100))
                                        rotate_button.draw()
                                        delete_button.draw()
                                        confirm_button.draw()
                                        cancel_button.draw()
                                        producer_group.draw(grid_surface_copy)
                                        crafter_group.draw(grid_surface_copy)
                                        conveyor_group.draw(grid_surface_copy)
                                        item_group.draw(grid_surface_copy) 
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
        for material in material_group:
            maybe_money = material.update(seller_lv,seller_upgrades,conveyor_lv,conveyor_upgrades,producer_info,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,smelter_group,blueprints_value,money)
            maybe_money=float(maybe_money)
            if maybe_money.is_integer():
                revenue+=(maybe_money-money)
                money=maybe_money
        
        for item in item_group:
            maybe_money=item.update(seller_lv,seller_upgrades,conveyor_lv,conveyor_upgrades,crafter_info,conveyor_group,conveyor_info,crafter_group,seller_group,money)
            if maybe_money.is_integer():
                revenue+=(maybe_money-money)
                money=maybe_money



       
        screen.fill((52,78,91))
        #buttons
        settings_mini_button.draw()
        stats_button.draw()
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
        item_group.draw(grid_surface_copy)


        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)

        screen.blit(grid_surface_copy,(0,100))
        #copy screen
        play_grid_bg=grid_surface_copy.copy()
        play_bg=screen.copy()

    elif game_state=='producer_popup':
        screen.blit(grid_surface_copy,(0,100))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)


        screen.blit(producer_popup_surface,selected_co)
        transparent_producer_popup.draw()
        draw_text('Current Output: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+10,screen)
        draw_text(str(producer_info[decimal_co][2]),font_24,(0,0,0),selected_co[0]+135,selected_co[1]+50,screen)

        draw_text('Select New Output: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+80,screen)



        selected_material_button.draw()
        copper_button.draw()
        iron_button.draw()
        gold_button.draw()
        aluminium_button.draw()
        coal_button.draw()
        lead_button.draw()
    
    elif game_state=='crafter_popup':
        screen.blit(grid_surface_copy,(0,100))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)

        screen.blit(producer_popup_surface,selected_co)
        transparent_crafter_popup.draw()

        draw_text('Inventory: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+10,screen)
        draw_text('Selected Blueprint: ',font_24,(0,0,0),selected_co[0]+10,selected_co[1]+110,screen)
        draw_text(crafter_info[decimal_co][1],font_24,(0,0,0),selected_co[0]+10,selected_co[1]+125,screen)


        draw_text(crafter_inv_quantities[0],font,(0,0,0),selected_co[0]+40,selected_co[1]+50,screen)
        draw_text(crafter_inv_quantities[1],font,(0,0,0),selected_co[0]+80,selected_co[1]+50,screen)
        draw_text(crafter_inv_quantities[2],font,(0,0,0),selected_co[0]+120,selected_co[1]+50,screen)
        draw_text(crafter_inv_quantities[3],font,(0,0,0),selected_co[0]+40,selected_co[1]+90,screen)
        draw_text(crafter_inv_quantities[4],font,(0,0,0),selected_co[0]+80,selected_co[1]+90,screen)
        draw_text(crafter_inv_quantities[5],font,(0,0,0),selected_co[0]+120,selected_co[1]+90,screen)

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

        draw_text(bp_item_quantities[0],font,(0,0,0),selected_co[0]+40,selected_co[1]+160,screen)
        draw_text(bp_item_quantities[1],font,(0,0,0),selected_co[0]+80,selected_co[1]+160,screen)
        draw_text(bp_item_quantities[2],font,(0,0,0),selected_co[0]+120,selected_co[1]+160,screen)
        draw_text(bp_item_quantities[3],font,(0,0,0),selected_co[0]+40,selected_co[1]+200,screen)
        draw_text(bp_item_quantities[4],font,(0,0,0),selected_co[0]+80,selected_co[1]+200,screen)
        draw_text(bp_item_quantities[5],font,(0,0,0),selected_co[0]+120,selected_co[1]+200,screen)

    elif game_state=='shop machines':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)
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

        draw_text('Buy Producer',font_32,(0,0,0),245,320,screen)
        draw_text('Outputs Materials',font_32,(0,0,0),245,350,screen)
        draw_text('Price: 100 each',font_32,(0,0,0),245,380,screen)

        draw_text('Buy Crafter',font_32,(0,0,0),550,320,screen)
        draw_text('Crafts Items',font_32,(0,0,0),550,350,screen)
        draw_text('Price: 100 each',font_32,(0,0,0),550,380,screen)

        draw_text('Buy Conveyor',font_32,(0,0,0),245,450,screen)
        draw_text('Moves Items',font_32,(0,0,0),245,480,screen)
        draw_text('Price: 50 each',font_32,(0,0,0),245,510,screen)

        draw_text('Buy Seller',font_32,(0,0,0),550,450,screen)
        draw_text('Sells Items',font_32,(0,0,0),550,480,screen)
        draw_text('Price: 100 each',font_32,(0,0,0),550,510,screen)                

    elif game_state=='shop upgrades':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)
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


        draw_text('Producer',font_32,(0,0,0),245,320,screen)
        draw_text(('Output '+str(producer_upgrades[producer_lv+1][2])+' Materials'),font_32,(0,0,0),245,350,screen)
        draw_text(('Price: '+str(producer_upgrades[producer_lv+1][0])+producer_upgrades[producer_lv+1][1]),font_32,(0,0,0),245,380,screen)
        draw_text('Buy Upgrade',font_36,(0,0,0),245,405,screen)

        draw_text('Crafter',font_32,(0,0,0),550,320,screen)
        draw_text(('Craft '+str(crafter_upgrades[crafter_lv+1][2])+' at once'),font_32,(0,0,0),550,350,screen)
        draw_text(('Price: '+str(crafter_upgrades[crafter_lv+1][0])+crafter_upgrades[crafter_lv+1][1]),font_32,(0,0,0),550,380,screen)
        draw_text('Buy Upgrade',font_36,(0,0,0),550,405,screen)

        draw_text('Conveyor',font_32,(0,0,0),245,450,screen)
        draw_text(('Move Items +'+str(round((conveyor_upgrades[conveyor_lv+1][2]-1)*100))+'%'),font_32,(0,0,0),245,480,screen)
        draw_text(('Price: '+str(conveyor_upgrades[conveyor_lv+1][0])+conveyor_upgrades[conveyor_lv+1][1]),font_32,(0,0,0),245,510,screen)
        draw_text('Buy Upgrade',font_36,(0,0,0),245,535,screen)

        draw_text('Seller',font_32,(0,0,0),550,450,screen)
        draw_text(('Sell Items for +'+str(round(((seller_upgrades[seller_lv+1][2])-1)*100))+'%'),font_32,(0,0,0),550,480,screen)
        draw_text(('Price: '+str(seller_upgrades[seller_lv+1][0])+seller_upgrades[seller_lv+1][1]),font_32,(0,0,0),550,510,screen) 
        draw_text('Buy Upgrade',font_36,(0,0,0),550,535,screen)  

        scrollbar_button.draw()
        slider_button.draw()

    elif game_state=='shop supply':
        producer_group.update(producer_info)
        for material in material_group:
            maybe_money = material.update(seller_lv,seller_upgrades,conveyor_lv,conveyor_upgrades,producer_info,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,smelter_group,blueprints_value,money)
            maybe_money=float(maybe_money)
            if maybe_money.is_integer():
                money=maybe_money
        
        for item in item_group:
            maybe_money=item.update(seller_lv,seller_upgrades,conveyor_lv,conveyor_upgrades,crafter_info,conveyor_group,conveyor_info,crafter_group,seller_group,money)
            if maybe_money.is_integer():
                money=maybe_money


        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)
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

        #left side text
        copper_lable1=font_32.render(('Copper remaining:'),False,(0,0,0))
        copper_lable2=font_50.render(str(materials_supply['copper']),False,(0,0,0)) 
        copper_lable2_rect=copper_lable2.get_rect(center=(210,350))
        screen.blit(copper_lable2,copper_lable2_rect)
        screen.blit(copper_lable1,(130,305))

        iron_lable1=font_32.render(('Iron remaining:'),False,(0,0,0))
        iron_lable2=font_50.render(str(materials_supply['iron']),False,(0,0,0)) 
        iron_lable2_rect=iron_lable2.get_rect(center=(210,440))
        screen.blit(iron_lable2,iron_lable2_rect)
        screen.blit(iron_lable1,(140,395))

        gold_lable1=font_32.render(('Gold remaining:'),False,(0,0,0))
        gold_lable2=font_50.render(str(materials_supply['gold']),False,(0,0,0)) 
        gold_lable2_rect=gold_lable2.get_rect(center=(210,530))
        screen.blit(gold_lable2,gold_lable2_rect)
        screen.blit(gold_lable1,(140,485))        

        aluminium_lable1=font_32.render(('Aluminium remaining:'),False,(0,0,0))
        aluminium_lable2=font_50.render(str(materials_supply['aluminium']),False,(0,0,0)) 
        aluminium_lable2_rect=aluminium_lable2.get_rect(center=(210,620))
        screen.blit(aluminium_lable2,aluminium_lable2_rect)
        screen.blit(aluminium_lable1,(124,575))        

        lead_lable1=font_32.render(('Lead remaining:'),False,(0,0,0))
        lead_lable2=font_50.render(str(materials_supply['lead']),False,(0,0,0)) 
        lead_lable2_rect=lead_lable2.get_rect(center=(210,720))
        screen.blit(lead_lable2,lead_lable2_rect)
        screen.blit(lead_lable1,(140,675))

        coal_lable1=font_32.render(('Coal remaining:'),False,(0,0,0))
        coal_lable2=font_50.render(str(materials_supply['coal']),False,(0,0,0)) 
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
        screen.blit(buy1_lable2,(615,330)) 

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







        scrollbar_button.draw()
        slider_button.draw()

    elif game_state=='blueprints':
        shop_bg_copy=shop_bg.copy()
        
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)


        blueprints_group.draw(shop_bg_copy)

        
        screen.blit(shop_bg_copy,(0,0))
        transparent_popup_button.draw()
        scrollbar_button.draw()
        slider_button.draw()
        blueprints_group.update(screen,item_imgs)

    elif game_state=='shop confirm':
        grid_surface_copy=grid_surface.copy()
        
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)
        machines_price_button=Buttons(800,500,gui_flat_img,0.5,1)
        machines_price_button.draw()

        machine_price_lable1=font_24.render(('Price:'),False,(0,0,0))
        machine_price_lable2=font_24.render(str(len(selected_pos)*prices[selected_machine]),False,(0,0,0))
        screen.blit(machine_price_lable1,(805,505))
        screen.blit(machine_price_lable2,(805,525))

        transparent_grid_button.draw()
        #machine stuff
        producer_group.draw(grid_surface_copy)
        crafter_group.draw(grid_surface_copy)
        conveyor_group.draw(grid_surface_copy)
        seller_group.draw(grid_surface_copy)
        #materials
        material_group.draw(grid_surface_copy)        
        item_group.draw(grid_surface_copy)
        
        confirm_button.draw()
        cancel_button.draw()
        green_square_group.update(selected_pos)
        green_square_group.draw(grid_surface_copy)
        screen.blit(grid_surface_copy,(0,100))
        
    elif game_state=='edit':
        screen.blit(grid_surface_copy,(0,100))
        stats_button.draw()
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)
        rotate_button.draw()
        delete_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
        arrows_group.draw(grid_surface_copy)
        if have_producer: 
            producer_group.update(producer_info)

    elif game_state=='edit paste':
        grid_surface_copy2=grid_surface_copy.copy()
        stats_button.draw()
        draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24)
        green_square_group.draw(grid_surface_copy2)
        producer_group.draw(grid_surface_copy2)
        crafter_group.draw(grid_surface_copy2)
        conveyor_group.draw(grid_surface_copy2)
        seller_group.draw(grid_surface_copy2)
        screen.blit(grid_surface_copy2,(0,100))

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
 
    elif game_state=='temp shop':
        screen.blit(play_bg,(0,0))
        screen.blit(blueprint_surface,(100,150))
        shop_bg=screen.copy()
        for blueprint in blueprints_group:
            blueprint.kill()

        for y in range(0,8):
            bptitles2[y]=bp_ordered_list[y]
            new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
            blueprints_group.add(new_bp)
        game_state='blueprints'

    elif game_state=='stats':
        screen.blit(grid_surface_copy,(0,100))
        stats_surface.draw()
        current_time=pygame.time.get_ticks()
        current_time =current_time//1000
        total_m =current_time//60
        total_h =current_time//3600
        total_d =current_time//(3600*24)
        current_d=total_d
        current_h=(current_time-((current_time//(3600*24))*3600*24))//3600
        current_m=(current_time-((current_time//(3600))*3600))//60
        current_s=(current_time-((current_time//(60))*60))


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

        draw_text('Statistics',font_60,(0,0,0),310,230,screen)
        draw_text('Revenue: '+ str(round(revenue/(1000**(counter)),1))+str(abbreviation[counter]),font_40,(255,255,255),210,300,screen)
        draw_text('Total play time: '+str(current_d)+'d '+str(current_h)+'h '+str(current_m)+'m '+str(current_s)+'s',font_40,(255,255,255),210,350,screen)
        draw_text('Skill level: Trash ',font_40,(255,255,255),210,400,screen)
        
    pygame.display.update()
    clock.tick(60)