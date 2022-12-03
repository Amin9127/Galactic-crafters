import pygame 
from sys import exit
import time
from button_functions import *
from classes import *
from variables import *
pygame.init()
pygame.font.init()

global money
money=1000





def draw_text(text,font,text_colour,x,y):
    img=font.render(text,True,text_colour)
    screen.blit(img,(x,y))






#output factory layout
'''
for x in factory_layout:
    for y in x:
        print(y,end='')
    print()
'''


#timers
change_event=pygame.USEREVENT
pygame.time.set_timer(change_event,1000)
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
        if event.type ==change_event:
            if game_state=='play':
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
                if crafter.update(crafter_info,blueprints)==True:
                    item_group.add(crafter.create_item(blueprints_value,item_imgs))

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
            
            elif game_state == 'shop confirm':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'shop'
                elif event.key == pygame.K_RETURN:
                    print('enter')
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout,money)
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
                    rotate(blueprints,selected_producers,selected_machines,arrows_group,material_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy)
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
                    crafter_group.update(crafter_info,blueprints)
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
                    crafter_group.update(crafter_info,blueprints)
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
                    crafter_group.update(crafter_info,blueprints)
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
                    crafter_group.update(crafter_info,blueprints)
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
                    crafter_group.update(crafter_info,blueprints)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
                    producer_group.draw(grid_surface_copy)
                    crafter_group.draw(grid_surface_copy)
                    conveyor_group.draw(grid_surface_copy)
                    material_group.draw(grid_surface_copy)
                    seller_group.draw(grid_surface_copy)
                    arrows_group.draw(grid_surface_copy)        
            
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
                    game_state='shop machines'
                elif edit_button.rect.collidepoint(co):
                    game_state='edit'
                elif blueprints_button.rect.collidepoint(co):
                    game_state='temp shop'

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

                            item_button=Buttons(co[0]+140,co[1]+30,item_imgs[crafter_info[decimal_co][1]],0.15,0.15)

                            co = [x+40,y+100]
                            selected_co=co
                            transparent_crafter_popup=Buttons(co[0],co[1],transparent_producer_popup_surface,1,2.25)
                            last_selected_crafter = decimal_co
                            
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
                elif item_button.rect.collidepoint(co):
                    game_state='temp shop'

                    for y in range(0,8):
                        bptitles2[y]=bp_ordered_list[y]
                        new_bp= Blueprints((y),y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font)
                        blueprints_group.add(new_bp)

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
                if producer_button.rect.collidepoint(co):
                    game_state='shop confirm'
                    selected_machine='producer'
                elif upgrades_button.rect.collidepoint(co):
                    game_state = 'shop upgrades'
                elif supply_button.rect.collidepoint(co):
                    game_state = 'shop supply'
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
                        
            elif game_state=='shop upgrades':
                if machines_button.rect.collidepoint(co):
                    game_state = 'shop machines'
                elif supply_button.rect.collidepoint(co):
                    game_state = 'shop supply'
                elif transparent_popup.rect.collidepoint(co) == False:
                    game_state ='play'

            elif game_state=='shop supply':
                if machines_button.rect.collidepoint(co):
                    game_state = 'shop machines'
                elif upgrades_button.rect.collidepoint(co):
                    game_state = 'shop upgrades'
                elif transparent_popup.rect.collidepoint(co) == False:
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
                if transparent_popup.rect.collidepoint(co) == False:
                    game_state ='play'
                elif slider_button.rect.collidepoint(co):
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
                    choose_bp=False
                    print(crafter_info)
                            
            elif game_state=='shop confirm':
                if transparent_grid_button.rect.collidepoint(co):
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
                    money = confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout,money)
                    selected_pos=[]
                    print(crafter_info)
                    game_state = 'play'
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
                        material_group.draw(grid_surface_copy) 
                        arrows_group.draw(grid_surface_copy)
                    
                elif rotate_button.rect.collidepoint(co):
                    rotate(blueprints,selected_producers,selected_machines,arrows_group,material_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy)
      
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
                    crafter_group.update(crafter_info,blueprints)
                    conveyor_group.update(conveyor_info)
                    seller_group.update(seller_info)
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
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
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info) 

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
                    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)

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
            maybe_money = material.update(producer_info,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,smelter_group,blueprints_value,money)
            maybe_money=float(maybe_money)
            if maybe_money.is_integer():
                money=maybe_money
        
        for item in item_group:
            maybe_money=item.update(crafter_info,conveyor_group,conveyor_info,crafter_group,seller_group,money)
            if maybe_money.is_integer():
                money=maybe_money



       
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
        item_group.draw(grid_surface_copy)


        draw_money(money,screen,money_panel_img,font_50)

        screen.blit(grid_surface_copy,(0,100))
        #copy screen
        play_grid_bg=grid_surface_copy.copy()
        play_bg=screen.copy()

    elif game_state=='producer_popup':
        screen.blit(grid_surface_copy,(0,100))
        draw_money(money,screen,money_panel_img,font_50)


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
        draw_money(money,screen,money_panel_img,font_50)

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
        item_button.draw()

    elif game_state=='shop machines':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50)
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

        producer_button.draw()
        crafter_button.draw()
        conveyor_button.draw()
        seller_button.draw()

    elif game_state=='shop upgrades':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50)
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

    elif game_state=='shop supply':
        screen.blit(play_bg,(0,0))
        draw_money(money,screen,money_panel_img,font_50)
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
        
        draw_money(money,screen,money_panel_img,font_50)
        transparent_popup.draw()

        blueprints_group.draw(shop_bg_copy)

        
        screen.blit(shop_bg_copy,(0,0))
        scrollbar_button.draw()
        slider_button.draw()
        blueprints_group.update(screen,item_imgs)

    elif game_state=='shop confirm':
        grid_surface_copy=grid_surface.copy()
        
        draw_money(money,screen,money_panel_img,font_50)
        machines_price_button=Buttons(800,500,gui_flat_img,0.5,1)
        machines_price_button.draw()

        machine_price_lable1=font_24.render(('Price:'),False,(0,0,0))
        machine_price_lable2=font_24.render(str(len(selected_pos)*100),False,(0,0,0))
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
        draw_money(money,screen,money_panel_img,font_50)

        screen.blit(grid_surface_copy,(0,100))
        rotate_button.draw()
        delete_button.draw()
        confirm_button.draw()
        cancel_button.draw()
        arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
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
 
    elif game_state=='temp shop':
        screen.blit(play_bg,(0,0))
        screen.blit(blueprint_surface,(100,150))
        shop_bg=screen.copy()
        game_state='blueprints'

    pygame.display.update()
    clock.tick(60)

