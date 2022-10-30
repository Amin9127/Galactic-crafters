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
   
    def update(self,producer_info,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,money):
        self.this_producer_info=producer_info.get(self.decimal_co)
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
        
        if pygame.sprite.spritecollideany(self,seller_group,pygame.sprite.collide_rect_ratio(1)) and self.producer_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            money+=self.worth
        return money
