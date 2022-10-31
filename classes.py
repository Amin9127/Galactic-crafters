from platform import machine
import pygame

class Machine(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        super().__init__()
        self.image=img
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image_N=self.image
        self.image_E=pygame.transform.rotate(self.image,270)
        self.image_S=pygame.transform.rotate(self.image,180)
        self.image_W=pygame.transform.rotate(self.image,90)
        
        self.rect=self.image.get_rect(topleft=(x,y))
        self.decimal_co=str(x)+'.'+str(y)
    
    def update(self,machine_info):
        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1])

        if self.decimal_co not in machine_info.keys():
            self.kill()
        else:
            if machine_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif machine_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif machine_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif machine_info[self.decimal_co][0]=='w':
                self.image=self.image_W


class Conveyor(Machine):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)

class Seller(Machine):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)




class Producer(Machine):
    def __init__(self,x,y,img,producer_info):
        super().__init__(x,y,img)

    def create_material(self,co,producer_info):
        return Material(co,producer_info)

class Material(pygame.sprite.Sprite):
    def __init__(self,co,producer_info):
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
        self.worth=1000
   
    def update(self,producer_info,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,smelter_group,blueprints_value,money):
        self.this_producer_info=producer_info.get(self.decimal_co)
        self.co=self.decimal_co.split('.')
        self.co[0]=int(self.co[0])
        self.co[1]=int(self.co[1])

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

        material_to_liquid={'copper':'liquid copper','iron':'liquid iron','gold':'liquid gold','aluminium':'liquid aluminium','lead':'liquid lead','coal':'liquid coal'}
        if pygame.sprite.spritecollideany(self,smelter_group,pygame.sprite.collide_rect_ratio(1)) and self.producer_thrust==False and self.conveyor_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            self.liquid=material_to_liquid[self.type]
            Smelter.create_item(self.co,self.liquid,blueprints_value)

        if pygame.sprite.spritecollideany(self,seller_group,pygame.sprite.collide_rect_ratio(1)) and self.producer_thrust==False and self.conveyor_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            money+=self.worth+0.5
        return money




class Items(pygame.sprite.Sprite):
    def __init__(self,co,item,blueprints_value):
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

    def update(self,crafter_info,conveyor_group,conveyor_info,crafter_group,seller_group,money):
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

        if pygame.sprite.spritecollideany(self,seller_group,pygame.sprite.collide_rect_ratio(1)) and self.crafter_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            money+=self.worth
        return money

class Crafter(Machine):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)

    def update(self,crafter_info,blueprints):
        print('crafter update')
        
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

    def create_item(self,blueprints_value):
        return Items(self.co,self.item,blueprints_value)

class Smelter(Machine):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)

    def create_item(self,co,item,blueprints_value):
        return Items(co,item,blueprints_value)