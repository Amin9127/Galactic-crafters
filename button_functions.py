from variables import *

def confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,Producer,Crafter,Conveyor,Seller,money,area):
    game_state='play'
    prices={
        'producer':100,
        'crafter':100,
        'conveyor':50,
        'seller':100,
    }
    screen.blit(grid_surface,(0,100))
    no_of_machines=len(selected_pos)
    if no_of_machines*prices[selected_machine]<=money:
        money-=no_of_machines*prices[selected_machine]
        for co in selected_pos:
            x= co[0]*40
            y= co[1]*40
            
            decimal_co=str(x)+'.'+str(y)
            if selected_machine =='producer':
                area.producer_info[decimal_co]=['n','copper',producer_upgrades[area.producer_lv][2],'none']
                new_producer=Producer(x,y,producer_img,area.producer_info)
                area.producer_group.add(new_producer)
                area.factory_layout[co[1]][co[0]]=1
                print(area.producer_info)
            elif selected_machine=='crafter':
                area.crafter_info[decimal_co]=['n','circuit',{},'none']
                new_crafter=Crafter(x,y,crafter_img)
                area.crafter_group.add(new_crafter)
                area.factory_layout[co[1]][co[0]]=1
            elif selected_machine=='conveyor':
                area.conveyor_info[decimal_co]=['n','','','none']
                new_conveyor=Conveyor(x,y,conveyor_img)
                area.conveyor_group.add(new_conveyor)
                area.factory_layout[co[1]][co[0]]=1
            elif selected_machine=='seller':
                area.seller_info[decimal_co]=['n','','','none']
                new_seller=Seller(x,y,seller_img)
                area.seller_group.add(new_seller)
                area.factory_layout[co[1]][co[0]]=1

    selected_pos=[]
    return money

def rotate(blueprints,selected_producers,selected_machines,selected_crafters,selected_conveyors,selected_sellers,grid_surface_copy,area):
    for pos in selected_producers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        
        if area.producer_info[decimal_co][0]=='n':
            area.producer_info[decimal_co][0]='e'
        elif area.producer_info[decimal_co][0]=='e':
            area.producer_info[decimal_co][0]='s'
        elif area.producer_info[decimal_co][0]=='s':
            area.producer_info[decimal_co][0]='w'
        elif area.producer_info[decimal_co][0]=='w':
            area.producer_info[decimal_co][0]='n'

    for pos in selected_crafters:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        
        if area.crafter_info[decimal_co][0]=='n':
            area.crafter_info[decimal_co][0]='e'
        elif area.crafter_info[decimal_co][0]=='e':
            area.crafter_info[decimal_co][0]='s'
        elif area.crafter_info[decimal_co][0]=='s':
            area.crafter_info[decimal_co][0]='w'
        elif area.crafter_info[decimal_co][0]=='w':
            area.crafter_info[decimal_co][0]='n'

    for pos in selected_conveyors:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        
        if area.conveyor_info[decimal_co][0]=='n':
            area.conveyor_info[decimal_co][0]='e'
        elif area.conveyor_info[decimal_co][0]=='e':
            area.conveyor_info[decimal_co][0]='s'
        elif area.conveyor_info[decimal_co][0]=='s':
            area.conveyor_info[decimal_co][0]='w'
        elif area.conveyor_info[decimal_co][0]=='w':
            area.conveyor_info[decimal_co][0]='n'

    for pos in selected_sellers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        
        if area.seller_info[decimal_co][0]=='n':
            area.seller_info[decimal_co][0]='e'
        elif area.seller_info[decimal_co][0]=='e':
            area.seller_info[decimal_co][0]='s'
        elif area.seller_info[decimal_co][0]=='s':
            area.seller_info[decimal_co][0]='w'
        elif area.seller_info[decimal_co][0]=='w':
            area.seller_info[decimal_co][0]='n'


    #redraw rotated machines
    area.producer_group.update(area.producer_info)
    area.crafter_group.update(area.crafter_info,blueprints,crafter_upgrades,area.crafter_lv)
    area.conveyor_group.update(area.conveyor_info)
    area.arrows_group.update(selected_machines,area.producer_info,area.crafter_info,area.conveyor_info,area.seller_info)
    area.seller_group.update(area.seller_info)
    area.producer_group.draw(grid_surface_copy)
    area.crafter_group.draw(grid_surface_copy)
    area.conveyor_group.draw(grid_surface_copy)
    area.seller_group.draw(grid_surface_copy)
    area.material_group.draw(grid_surface_copy)
    area.item_group.draw(grid_surface_copy)
    area.arrows_group.draw(grid_surface_copy)

def move(direction,selected_producers,selected_crafters,selected_conveyors,selected_sellers,selected_machines,Arrow,area):
    movements={
        'left':[-40,0],
        'up':[0,-40],
        'right':[40,0],
        'down':[0,40],
    }
    temp_info={}
    cancel_move=False
    #change all selected machines move direction to left 
    decimal_co=''
    for pos in selected_producers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        area.producer_info[decimal_co][3] =direction
    for pos in selected_crafters:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        area.crafter_info[decimal_co][3] =direction
    for pos in selected_conveyors:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        area.conveyor_info[decimal_co][3] =direction
    for pos in selected_sellers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        area.seller_info[decimal_co][3] =direction

  

    #check if move is possible
    for pos in selected_machines:
        decimal_co=str(pos[0]+movements[direction][0])+'.'+str(pos[1]+movements[direction][1])
        if pos[0]+movements[direction][0]<0 or pos[0]+movements[direction][0]>760:
            cancel_move=True
        if pos[1]+movements[direction][1]<0 or pos[1]+movements[direction][1]>760:
            cancel_move=True              
        if decimal_co in area.producer_info:
            if area.producer_info[decimal_co][3] != direction:
                cancel_move =True
        elif decimal_co in area.crafter_info:
            if area.crafter_info[decimal_co][3] != direction:
                cancel_move =True
        elif decimal_co in area.conveyor_info:
            if area.conveyor_info[decimal_co][3] != direction:
                cancel_move =True
        elif decimal_co in area.seller_info:
            if area.seller_info[decimal_co][3] != direction:
                cancel_move =True
            
    #if machine that is not moving with the others is in the way this will not run

    if cancel_move==False:
        for producer in area.producer_group:
            combined_info=producer.move(area.producer_info,temp_info)
            if len(combined_info[0])==len(selected_producers):
                area.producer_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        for crafter in area.crafter_group:
            combined_info=crafter.move(area.crafter_info,temp_info)
            if len(combined_info[0])==len(selected_crafters):
                area.crafter_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        for conveyor in area.conveyor_group:
            combined_info=conveyor.move(area.conveyor_info,temp_info)
            if len(combined_info[0])==len(selected_conveyors):
                area.conveyor_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        for seller in area.seller_group:
            combined_info=seller.move(area.seller_info,temp_info)
            if len(combined_info[0])==len(selected_sellers):
                area.seller_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        #change selected machine variable with their new positions.
        for i in range(len(selected_producers)):
            pos=selected_producers[i]
            selected_producers[i]=[pos[0]+movements[direction][0],pos[1]+movements[direction][1]]

        for i in range(len(selected_crafters)):
            pos=selected_crafters[i]
            selected_crafters[i]=[pos[0]+movements[direction][0],pos[1]+movements[direction][1]]

        for i in range(len(selected_conveyors)):
            pos=selected_conveyors[i]
            selected_conveyors[i]=[pos[0]+movements[direction][0],pos[1]+movements[direction][1]]

        for i in range(len(selected_sellers)):
            pos=selected_sellers[i]
            selected_sellers[i]=[pos[0]+movements[direction][0],pos[1]+movements[direction][1]]

        for pos in selected_machines:
            area.factory_layout[pos[1]//40][pos[0]//40]=0
        for pos in selected_machines:
            area.factory_layout[(pos[1]+movements[direction][1])//40][(pos[0]+movements[direction][0])//40]=1

        for i in range(len(selected_machines)):
            pos=selected_machines[i]
            selected_machines[i]=[pos[0]+movements[direction][0],pos[1]+movements[direction][1]]
    else:
        for pos in selected_machines:
            decimal_co=str(pos[0])+'.'+str(pos[1])
            if decimal_co in area.producer_info:
                area.producer_info[decimal_co][3]='none'
            elif decimal_co in area.crafter_info:
                area.crafter_info[decimal_co][3]='none'
            elif decimal_co in area.conveyor_info:
                area.conveyor_info[decimal_co][3]='none'
            elif decimal_co in area.seller_info:
                area.seller_info[decimal_co][3]='none' 
        cancel_move=False                             

    for arrow in area.arrows_group:
        arrow.kill()

    for co in selected_machines:
        new_arrow = Arrow(int(co[0]),int(co[1]),area.producer_info,area.crafter_info,area.conveyor_info,area.seller_info)
        area.arrows_group.add(new_arrow)

def draw_money(money,screen,money_panel_img,font_50,money_per_min,font_24,stats_button):
    screen.blit(money_panel_img,(200,0))
    stats_button.draw()

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

    counter=0
    money_per_min1=money_per_min
    allowed=True
    while allowed:
        money_per_min1=money_per_min1//1000
        if money_per_min1 >=10:
            counter+=1
        else:
            allowed=False

    draw_text('Money/min:',font_24,(0,0,0),800,10,screen,False)
    draw_text((str(round(money_per_min/(1000**(counter)),1))+str(abbreviation[counter])),font_24,(0,0,0),800,25,screen,False)

def draw_text(text,font,text_colour,x,y,screen,center):
    text=font.render(text,True,text_colour)
    if center:
        text_rect=text.get_rect(center=(x,y))
        screen.blit(text,text_rect)
    else:
        screen.blit(text,(x,y))
