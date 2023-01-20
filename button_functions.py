

def confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_lv,producer_upgrades,crafter_lv,crafter_upgrades,conveyor_lv,conveyor_upgrades,seller_lv,seller_upgrades,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout,money):
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
                producer_info[decimal_co]=['n','copper',producer_upgrades[producer_lv][2],'none']
                new_producer=Producer(x,y,producer_img,producer_info)
                producer_group.add(new_producer)
                factory_layout[co[1]][co[0]]=1
            elif selected_machine=='crafter':
                crafter_info[decimal_co]=['n','circuit',{},'none']
                new_crafter=Crafter(x,y,crafter_img)
                crafter_group.add(new_crafter)
                factory_layout[co[1]][co[0]]=1
            elif selected_machine=='conveyor':
                conveyor_info[decimal_co]=['n','','','none']
                new_conveyor=Conveyor(x,y,conveyor_img)
                conveyor_group.add(new_conveyor)
                factory_layout[co[1]][co[0]]=1
            elif selected_machine=='seller':
                seller_info[decimal_co]=['n','','','none']
                new_seller=Seller(x,y,seller_img)
                seller_group.add(new_seller)
                factory_layout[co[1]][co[0]]=1

    selected_pos=[]
    return money

def rotate(crafter_upgrades,crafter_lv,blueprints,selected_producers,selected_machines,arrows_group,material_group,item_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy):
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
        
        if conveyor_info[decimal_co][0]=='n':
            conveyor_info[decimal_co][0]='e'
        elif conveyor_info[decimal_co][0]=='e':
            conveyor_info[decimal_co][0]='s'
        elif conveyor_info[decimal_co][0]=='s':
            conveyor_info[decimal_co][0]='w'
        elif conveyor_info[decimal_co][0]=='w':
            conveyor_info[decimal_co][0]='n'

    for pos in selected_sellers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        
        if seller_info[decimal_co][0]=='n':
            seller_info[decimal_co][0]='e'
        elif seller_info[decimal_co][0]=='e':
            seller_info[decimal_co][0]='s'
        elif seller_info[decimal_co][0]=='s':
            seller_info[decimal_co][0]='w'
        elif seller_info[decimal_co][0]=='w':
            seller_info[decimal_co][0]='n'


    #redraw rotated machines
    producer_group.update(producer_info)
    crafter_group.update(crafter_info,blueprints,crafter_upgrades,crafter_lv)
    conveyor_group.update(conveyor_info)
    arrows_group.update(selected_machines,producer_info,crafter_info,conveyor_info,seller_info)
    seller_group.update(seller_info)
    producer_group.draw(grid_surface_copy)
    crafter_group.draw(grid_surface_copy)
    conveyor_group.draw(grid_surface_copy)
    seller_group.draw(grid_surface_copy)
    material_group.draw(grid_surface_copy)
    item_group.draw(grid_surface_copy)
    arrows_group.draw(grid_surface_copy)

def move(direction,selected_producers,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,selected_machines,factory_layout,arrows_group,Arrow):
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
        producer_info[decimal_co][3] =direction
    for pos in selected_crafters:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        crafter_info[decimal_co][3] =direction
    for pos in selected_conveyors:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        conveyor_info[decimal_co][3] =direction
    for pos in selected_sellers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        seller_info[decimal_co][3] =direction

  

    #check if move is possible
    for pos in selected_machines:
        decimal_co=str(pos[0]+movements[direction][0])+'.'+str(pos[1]+movements[direction][1])
        if pos[0]+movements[direction][0]<0 or pos[0]+movements[direction][0]>760:
            cancel_move=True
        if pos[1]+movements[direction][1]<0 or pos[1]+movements[direction][1]>760:
            cancel_move=True              
        if decimal_co in producer_info:
            if producer_info[decimal_co][3] != direction:
                cancel_move =True
        elif decimal_co in crafter_info:
            if crafter_info[decimal_co][3] != direction:
                cancel_move =True
        elif decimal_co in conveyor_info:
            if conveyor_info[decimal_co][3] != direction:
                cancel_move =True
        elif decimal_co in seller_info:
            if seller_info[decimal_co][3] != direction:
                cancel_move =True
            
    #if machine that is not moving with the others is in the way this will not run

    if cancel_move==False:
        for producer in producer_group:
            combined_info=producer.move(producer_info,temp_info)
            if len(combined_info[0])==len(selected_producers):
                producer_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        for crafter in crafter_group:
            combined_info=crafter.move(crafter_info,temp_info)
            if len(combined_info[0])==len(selected_crafters):
                crafter_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        for conveyor in conveyor_group:
            combined_info=conveyor.move(conveyor_info,temp_info)
            if len(combined_info[0])==len(selected_conveyors):
                conveyor_info.update(combined_info[0])
                temp_info={}
                combined_info={}

        for seller in seller_group:
            combined_info=seller.move(seller_info,temp_info)
            if len(combined_info[0])==len(selected_sellers):
                seller_info.update(combined_info[0])
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
            factory_layout[pos[1]//40][pos[0]//40]=0
        for pos in selected_machines:
            factory_layout[(pos[1]+movements[direction][1])//40][(pos[0]+movements[direction][0])//40]=1

        for i in range(len(selected_machines)):
            pos=selected_machines[i]
            selected_machines[i]=[pos[0]+movements[direction][0],pos[1]+movements[direction][1]]
    else:
        for pos in selected_machines:
            decimal_co=str(pos[0])+'.'+str(pos[1])
            if decimal_co in producer_info:
                producer_info[decimal_co][3]='none'
            elif decimal_co in crafter_info:
                crafter_info[decimal_co][3]='none'
            elif decimal_co in conveyor_info:
                conveyor_info[decimal_co][3]='none'
            elif decimal_co in seller_info:
                seller_info[decimal_co][3]='none' 
        cancel_move=False                             

    for arrow in arrows_group:
        arrow.kill()

    for co in selected_machines:
        new_arrow = Arrow(int(co[0]),int(co[1]),producer_info,crafter_info,conveyor_info,seller_info)
        arrows_group.add(new_arrow)

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
