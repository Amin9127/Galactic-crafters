def confirm_place_machinery(screen,grid_surface,selected_pos,selected_machine,producer_info,Producer,producer_group,producer_img,crafter_info,Crafter,crafter_group,crafter_img,conveyor_info,Conveyor,conveyor_group,conveyor_img,seller_info,Seller,seller_group,seller_img,factory_layout):
    game_state='play'
    screen.blit(grid_surface,(0,100))
    for co in selected_pos:
        x= co[0]*40
        y= co[1]*40
        
        decimal_co=str(x)+'.'+str(y)
        str(decimal_co)
        print(decimal_co,'in function')
        if selected_machine =='producer':
            producer_info[decimal_co]=['n','copper',1]
            new_producer=Producer(x,y,producer_img,producer_info)
            producer_group.add(new_producer)
            factory_layout[co[0]][co[1]]=1
            have_producer=True
        elif selected_machine=='crafter':
            crafter_info[decimal_co]=['n','circuit',{}]
            new_crafter=Crafter(x,y,crafter_img)
            crafter_group.add(new_crafter)
            factory_layout[co[0]][co[1]]=1
            have_crafter=True
        elif selected_machine=='conveyor':
            conveyor_info[decimal_co]='n'
            new_conveyor=Conveyor(x,y,conveyor_img)
            conveyor_group.add(new_conveyor)
            factory_layout[co[0]][co[1]]=1
            have_conveyor=True
        elif selected_machine=='seller':
            seller_info[decimal_co]='n'
            new_seller=Seller(x,y,seller_img)
            seller_group.add(new_seller)
            factory_layout[co[0]][co[1]]=1
            have_seller=True

    selected_pos=[]
    return game_state

def rotate(selected_producers,selected_machines,arrows_group,material_group,producer_info,producer_group,selected_crafters,crafter_info,crafter_group,selected_conveyors,conveyor_info,conveyor_group,selected_sellers,seller_info,seller_group,grid_surface_copy):
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

    for pos in selected_sellers:
        decimal_co=str(pos[0])+'.'+str(pos[1])
        
        if seller_info[decimal_co]=='n':
            seller_info[decimal_co]='e'
        elif seller_info[decimal_co]=='e':
            seller_info[decimal_co]='s'
        elif seller_info[decimal_co]=='s':
            seller_info[decimal_co]='w'
        elif seller_info[decimal_co]=='w':
            seller_info[decimal_co]='n'


    #redraw rotated machines
    producer_group.update(producer_info)
    crafter_group.update()
    conveyor_group.update(conveyor_info)
    arrows_group.update(selected_machines)
    producer_group.draw(grid_surface_copy)
    crafter_group.draw(grid_surface_copy)
    conveyor_group.draw(grid_surface_copy)
    seller_group.draw(grid_surface_copy)
    material_group.draw(grid_surface_copy)
    arrows_group.draw(grid_surface_copy)

