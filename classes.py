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

    def move(self,machine_info,temp_info):
        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1])

        self.left_decimal_co=str(self.current_co[0]-40)+'.'+str(self.current_co[1])
        self.up_decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1]-40)
        self.right_decimal_co=str(self.current_co[0]+40)+'.'+str(self.current_co[1])
        self.down_decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1]+40)


        if machine_info[self.decimal_co][3] == 'left':
            temp_info[self.left_decimal_co] = machine_info[self.decimal_co]
            del machine_info[self.decimal_co]
            self.rect=self.image.get_rect(topleft=(self.current_co[0]-40,self.current_co[1]))
            temp_info[self.left_decimal_co][3] ='none'

        elif machine_info[self.decimal_co][3] == 'up':
            temp_info[self.up_decimal_co] = machine_info[self.decimal_co]
            del machine_info[self.decimal_co]
            self.rect=self.image.get_rect(topleft=(self.current_co[0],self.current_co[1]-40))
            temp_info[self.up_decimal_co][3] ='none'

        elif machine_info[self.decimal_co][3] == 'right':
            temp_info[self.right_decimal_co] = machine_info[self.decimal_co]
            del machine_info[self.decimal_co]
            self.rect=self.image.get_rect(topleft=(self.current_co[0]+40,self.current_co[1]))
            temp_info[self.right_decimal_co][3] ='none'

        elif machine_info[self.decimal_co][3] == 'down':
            temp_info[self.down_decimal_co] = machine_info[self.decimal_co]
            del machine_info[self.decimal_co]
            self.rect=self.image.get_rect(topleft=(self.current_co[0],self.current_co[1]+40))
            temp_info[self.down_decimal_co][3] ='none'

        combined_info=[temp_info,machine_info]
        return combined_info

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
        self.post_conveyor_thrust=False
        self.worth=20
   
    def update(self,seller_lv,seller_upgrades,conveyor_lv,conveyor_upgrades,producer_info,conveyor_info,conveyor_group,crafter_info,crafter_group,seller_group,smelter_group,blueprints_value,money):
        self.this_producer_info=producer_info.get(self.decimal_co)
        self.co=self.decimal_co.split('.')
        self.co[0]=int(self.co[0])
        self.co[1]=int(self.co[1])

        self.conveyor_speed=5*conveyor_upgrades[conveyor_lv][2]
        self.ticks_per_conveyor=40//self.conveyor_speed
        self.r_ticks_per_conveyor=40%self.conveyor_speed



        if self.conveyor_thrust==False and self.producer_thrust==False:

            if pygame.sprite.spritecollideany(self,conveyor_group,pygame.sprite.collide_rect_ratio(1)):
                self.x= ((self.rect.x)//40)*40
                self.y= (((self.rect.y))//40)*40
                self.decimal_co=str(self.x)+'.'+str(self.y)
                if self.decimal_co!=self.previous_conveyor_pos:
                    self.conveyor_direction=conveyor_info[self.decimal_co][0]
                    self.conveyor_thrust=True
                    self.producer_thrust=False
                    self.count=0
                    self.previous_conveyor_pos=self.decimal_co

        #conveyor movement.
        if self.count<self.ticks_per_conveyor+(self.r_ticks_per_conveyor//self.conveyor_speed)+1 and self.conveyor_thrust==True:
            if self.conveyor_direction=='n':
                self.rect.y-=self.conveyor_speed
            elif self.conveyor_direction=='e':
                self.rect.x+=self.conveyor_speed
            elif self.conveyor_direction=='s':
                self.rect.y+=self.conveyor_speed
            elif self.conveyor_direction=='w':
                self.rect.x-=self.conveyor_speed
            self.count+=1

        elif self.count==self.ticks_per_conveyor+1 and self.conveyor_thrust:
            if self.conveyor_direction=='n':
                self.rect.y-=self.r_ticks_per_conveyor
            elif self.conveyor_direction=='e':
                self.rect.x+=self.r_ticks_per_conveyor
            elif self.conveyor_direction=='s':
                self.rect.y+=self.r_ticks_per_conveyor
            elif self.conveyor_direction=='w':
                self.rect.x-=self.r_ticks_per_conveyor
            self.conveyor_thrust=False
            self.count=0

        #initial producer thrust
        if self.count<7 and self.producer_thrust:
            print(self.rect.y)
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
            self.count+=1
        else:
            self.producer_thrust=False

        
        self.conveyor_collision=pygame.sprite.spritecollideany(self,conveyor_group,pygame.sprite.collide_rect_ratio(1))

        #if self.conveyor_thrust==True:
        #    if self.conveyor_direction=='n':
        #        self.rect.y-=5*conveyor_upgrades[conveyor_lv][2]
        #    elif self.conveyor_direction=='e':
        #        self.rect.x+=5*conveyor_upgrades[conveyor_lv][2]
        #    elif self.conveyor_direction=='s':
        #        self.rect.y+=5*conveyor_upgrades[conveyor_lv][2]
        #    elif self.conveyor_direction=='w':
        #        self.rect.x-=5*conveyor_upgrades[conveyor_lv][2]
        #    if pygame.sprite.spritecollideany(self,conveyor_group,pygame.sprite.collide_rect_ratio(1))==False:
        #        self.conveyor_thrust=False
        #        self.post_conveyor_thrust=True
        ##
        #if self.post_conveyor_thrust==True:
        #    if self.conveyor_direction=='n':
        #        self.rect.y-=20
        #    elif self.conveyor_direction=='e':
        #        self.rect.x+=20
        #    elif self.conveyor_direction=='s':
        #        self.rect.y+=20
        #    elif self.conveyor_direction=='w':
        #        self.rect.x-=20
        #    self.post_conveyor_thrust=False

        #if self.count<16 and self.conveyor_thrust==True:
        #    if self.conveyor_direction=='n':
        #        self.rect.y-=5*conveyor_upgrades[conveyor_lv][2]
        #    elif self.conveyor_direction=='e':
        #        self.rect.x+=5*conveyor_upgrades[conveyor_lv][2]
        #    elif self.conveyor_direction=='s':
        #        self.rect.y+=5*conveyor_upgrades[conveyor_lv][2]
        #    elif self.conveyor_direction=='w':
        #        self.rect.x-=5*conveyor_upgrades[conveyor_lv][2]
        #    self.count+=1
        #else:
        #    self.conveyor_thrust=False

        if pygame.sprite.spritecollideany(self,crafter_group,pygame.sprite.collide_rect_ratio(1)) and self.producer_thrust==False and self.conveyor_thrust==False:
            self.x= ((self.rect.x)//40)*40
            self.y= (((self.rect.y))//40)*40
            self.decimal_co=str(self.x)+'.'+str(self.y)
            self.kill()
            if self.type in crafter_info[self.decimal_co][2]:
                self.stored_amount=crafter_info[self.decimal_co][2][self.type]
                crafter_info[self.decimal_co][2].update({self.type:self.stored_amount+self.amount})
            else:
                crafter_info[self.decimal_co][2].update({self.type:self.amount})


        if self.rect.x>800:
            self.kill()
        elif self.rect.x<0:
            self.kill()
        elif self.rect.y>800:
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
            money+=(self.worth)*seller_upgrades[seller_lv][2]*self.amount
        return money

class Items(pygame.sprite.Sprite):
    def __init__(self,co,item,blueprints_value,item_imgs,amount):
        super().__init__()
        self.type=item
        self.image=item_imgs[self.type]        
        self.spawn_co=co
        self.image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect(center=(self.spawn_co[0]+20,self.spawn_co[1]+20))
        self.amount= amount
        self.count=0
        self.crafter_thrust=True
        self.conveyor_thrust=False
        self.previous_conveyor_pos=''
        self.decimal_co=str(co[0])+'.'+str(co[1])
        self.worth=blueprints_value[self.type]

    def update(self,seller_lv,seller_upgrades,conveyor_lv,conveyor_upgrades,crafter_info,conveyor_group,conveyor_info,crafter_group,seller_group,money):
        self.this_crafter_info=crafter_info.get(self.decimal_co)
        if self.conveyor_thrust==False and self.crafter_thrust==False:
            if pygame.sprite.spritecollideany(self,conveyor_group,pygame.sprite.collide_rect_ratio(1)):
                self.x= ((self.rect.x)//40)*40
                self.y= (((self.rect.y))//40)*40
                self.decimal_co=str(self.x)+'.'+str(self.y)
                if self.decimal_co!=self.previous_conveyor_pos:
                    self.conveyor_direction=conveyor_info[self.decimal_co][0]
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
                self.rect.y-=5*conveyor_upgrades[conveyor_lv][2]
            elif self.conveyor_direction=='e':
                self.rect.x+=5*conveyor_upgrades[conveyor_lv][2]
            elif self.conveyor_direction=='s':
                self.rect.y+=5*conveyor_upgrades[conveyor_lv][2]
            elif self.conveyor_direction=='w':
                self.rect.x-=5*conveyor_upgrades[conveyor_lv][2]
            self.count+=1
        else:
            self.conveyor_thrust=False

        if pygame.sprite.spritecollideany(self,crafter_group,pygame.sprite.collide_rect_ratio(1)) and self.crafter_thrust==False and self.conveyor_thrust==False:
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
            money+=(self.worth)*seller_upgrades[seller_lv][2]*self.amount
        return money

class Crafter(Machine):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)

    def update(self,crafter_info,blueprints,crafter_upgrades,crafter_lv):
        
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
            self.starting_item= self.item_bp[0]

            self.item_bp_components=len(self.item_bp)
            self.components_fulfilled=0
            self.craft=False

            self.crafts_possible=0
            for x in self.item_bp:
                if crafter_info[self.decimal_co][2].get(x)is not None:
                    if crafter_info[self.decimal_co][2].get(x)>=blueprints[self.item][x]:
                        self.crafts_possible_temp=crafter_info[self.decimal_co][2].get(x)//blueprints[self.item][x]
                        if x == self.starting_item:
                            self.crafts_possible=self.crafts_possible_temp
                        elif self.crafts_possible<=self.crafts_possible_temp:
                            self.crafts_possible=self.crafts_possible_temp
                        self.components_fulfilled +=1
                else:
                    self.components_fulfilled=0
                    
            if self.components_fulfilled==self.item_bp_components:
                self.craft=True
            else:
                return False
 
            if self.craft==True:
                if self.crafts_possible>=crafter_upgrades[crafter_lv][2]:
                    self.crafts_multiple=crafter_upgrades[crafter_lv][2]
                else:
                    self.crafts_multiple=self.crafts_possible
                for x in self.item_bp:
                    crafter_info[self.decimal_co][2][x]-=blueprints[self.item][x]*self.crafts_multiple
                    self.co=self.decimal_co.split('.')
                    self.co[0]=int(self.co[0])
                    self.co[1]=int(self.co[1])
                self.craft=False
                print('crafted')
                return self.crafts_multiple
            else:
                return False

    def create_item(self,blueprints_value,item_imgs,amount):
        return Items(self.co,self.item,blueprints_value,item_imgs,amount)

class Smelter(Machine):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)

    def create_item(self,co,item,blueprints_value):
        return Items(co,item,blueprints_value)

class Blueprints(pygame.sprite.Sprite):
    def  __init__(self,title_position,y,blueprints_value,empty_slot_img,bp_ordered_list,blueprints,item_imgs,font_24,font_20,font):
        super().__init__()
        blueprint_position={0:[20,145],1:[330,145],2:[20,280],3:[330,280],4:[20,415],5:[330,415],6:[20,550 ],7:[330,550]}
        blueprint_title_position={0:[140,310],1:[450,310],2:[140,445],3:[450,445],4:[140,580],5:[450,580],6:[140,715 ],7:[450,715]}

        self.bp_item_images={0:empty_slot_img,1:empty_slot_img,2:empty_slot_img,3:empty_slot_img,4:empty_slot_img,5:empty_slot_img}
        self.bp_component_quantities=['','','','','','']
        self.position=y

        self.image=pygame.image.load('images/gui_flat.png').convert_alpha()
        self.image=pygame.transform.scale(self.image,(320,135))
        self.title_pos=blueprint_title_position[y]
        self.rect=self.image.get_rect(topleft=(self.title_pos[0]-30,self.title_pos[1]-20))

        if title_position==-1:
            self.bp_title='nothing'
        else:
            self.bp_title = bp_ordered_list[title_position]
            self.bp_items=blueprints[self.bp_title].keys()
            self.count=0

            for item in self.bp_items:
                self.bp_item_images[self.count]=item_imgs[item]
                self.bp_component_quantities[self.count]=blueprints[self.bp_title][item]
                self.count+=1

        self.title=font_24.render(str(self.bp_title),False,(0,0,0))

        self.amount1=font.render(str(self.bp_component_quantities[0]),False,(0,0,0))
        self.amount2=font.render(str(self.bp_component_quantities[1]),False,(0,0,0))
        self.amount3=font.render(str(self.bp_component_quantities[2]),False,(0,0,0))
        self.amount4=font.render(str(self.bp_component_quantities[3]),False,(0,0,0))
        self.amount5=font.render(str(self.bp_component_quantities[4]),False,(0,0,0))
        self.amount6=font.render(str(self.bp_component_quantities[5]),False,(0,0,0))

        self.price_lable1=font_20.render('Sell Price:',False,(0,0,0))
        self.price_lable2=font_20.render(str(blueprints_value[self.bp_title]),False,(0,0,0))

       
    def update(self,screen,item_imgs):
        blueprint_position={0:[20,145],1:[330,145],2:[20,280],3:[330,280],4:[20,415],5:[330,415],6:[20,550 ],7:[330,550]}
        blueprint_title_position={0:[140,310],1:[450,310],2:[140,445],3:[450,445],4:[140,580],5:[450,580],6:[140,715 ],7:[450,715]}
        self.pos = blueprint_title_position[self.position]

        #bp title
        screen.blit(self.title,blueprint_title_position[self.position])
        #bp main item img
        screen.blit(item_imgs[self.bp_title],(self.pos[0]+200,self.pos[1]+30))

        #bp component images
        screen.blit(self.bp_item_images[0],(self.pos[0],self.pos[1]+20))
        screen.blit(self.bp_item_images[1],(self.pos[0]+40,self.pos[1]+20))
        screen.blit(self.bp_item_images[2],(self.pos[0]+80,self.pos[1]+20))
        screen.blit(self.bp_item_images[3],(self.pos[0],self.pos[1]+60))
        screen.blit(self.bp_item_images[4],(self.pos[0]+40,self.pos[1]+60))
        screen.blit(self.bp_item_images[5],(self.pos[0]+80,self.pos[1]+60))

        #bp component quantitiy 
        screen.blit(self.amount1,(self.pos[0]+40,self.pos[1]+60))
        screen.blit(self.amount2,(self.pos[0]+80,self.pos[1]+60))
        screen.blit(self.amount3,(self.pos[0]+120,self.pos[1]+60))
        screen.blit(self.amount4,(self.pos[0]+40,self.pos[1]+100))
        screen.blit(self.amount5,(self.pos[0]+80,self.pos[1]+100))
        screen.blit(self.amount6,(self.pos[0]+120,self.pos[1]+100))

        #bp price text
        screen.blit(self.price_lable1,(self.pos[0]+200,self.pos[1]+80))
        screen.blit(self.price_lable2,(self.pos[0]+200,self.pos[1]+90))


class Arrow(pygame.sprite.Sprite):
    def __init__(self,x,y,producer_info,crafter_info,conveyor_info,seller_info):
        super().__init__()
        self.image=pygame.image.load('images/arrow.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.image=pygame.transform.rotate(self.image,90)
        self.image_N=self.image
        self.image_E=pygame.transform.rotate(self.image,270)
        self.image_S=pygame.transform.rotate(self.image,180)
        self.image_W=pygame.transform.rotate(self.image,90)

        self.decimal_co=str(x)+'.'+str(y) 

        if self.decimal_co in producer_info:
            if producer_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif producer_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif producer_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif producer_info[self.decimal_co][0]=='w':
                self.image=self.image_W

        elif self.decimal_co in crafter_info:
            if crafter_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif crafter_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif crafter_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif crafter_info[self.decimal_co][0]=='w':
                self.image=self.image_W

        elif self.decimal_co in conveyor_info:
            if conveyor_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif conveyor_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif conveyor_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif conveyor_info[self.decimal_co][0]=='w':
                self.image=self.image_W
        
        elif self.decimal_co in seller_info:
            if seller_info[self.decimal_co][0]=='n':
                self.image=self.image_N
            elif seller_info[self.decimal_co][0]=='e':
                self.image=self.image_E
            elif seller_info[self.decimal_co][0]=='s':
                self.image=self.image_S
            elif seller_info[self.decimal_co][0]=='w':
                self.image=self.image_W

        self.rect=self.image.get_rect(topleft=(x,y))

        self.current_co=self.rect.topleft
        self.decimal_co=str(self.current_co[0])+'.'+str(self.current_co[1]) 
    
    def update(self,selected_machines,producer_info,crafter_info,conveyor_info,seller_info):
        self.current_co=self.rect.topleft
        self.layout_x=self.current_co[0]//40
        self.layout_y=self.current_co[1]//40
        self.co=[self.layout_x*40,self.layout_y*40]
        self.decimal_co=str(self.layout_x*40)+'.'+str(self.layout_y*40)

        if self.co not in selected_machines:
            self.kill()
        else:
            if self.decimal_co in producer_info:
                if producer_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif producer_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif producer_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif producer_info[self.decimal_co][0]=='w':
                    self.image=self.image_W

            elif self.decimal_co in crafter_info:
                if crafter_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif crafter_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif crafter_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif crafter_info[self.decimal_co][0]=='w':
                    self.image=self.image_W

            elif self.decimal_co in conveyor_info:
                if conveyor_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif conveyor_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif conveyor_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif conveyor_info[self.decimal_co][0]=='w':
                    self.image=self.image_W

            elif self.decimal_co in seller_info:
                if seller_info[self.decimal_co][0]=='n':
                    self.image=self.image_N
                elif seller_info[self.decimal_co][0]=='e':
                    self.image=self.image_E
                elif seller_info[self.decimal_co][0]=='s':
                    self.image=self.image_S
                elif seller_info[self.decimal_co][0]=='w':
                    self.image=self.image_W 

class GreenSquare(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('images/green_square.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (40, 40))
        self.rect=self.image.get_rect(topleft=(x,y))
    
    def update(self,selected_pos):
        self.current_co=self.rect.topleft
        self.layout_x=self.current_co[0]//40
        self.layout_y=self.current_co[1]//40
        if [self.layout_x,self.layout_y] not in selected_pos:
            self.kill()   
