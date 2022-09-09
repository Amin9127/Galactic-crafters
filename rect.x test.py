import pygame

screen=pygame.display.set_mode((10,10))
pygame.display.set_caption('assembly game')
clock=pygame.time.Clock()
game_active = True
surface=pygame.Surface((10,10))
white=(255,255,255)
surface.fill(white)

class Material(pygame.sprite.Sprite):
    def __init__(self,co):
        global producer_info,conveyor_info#,conveyor_group

        super().__init__()
        self.image=pygame.Surface((10,10))
        self.image.fill((255,0,0 ))
        self.rect=self.image.get_rect(center=(0,0))
    def update(self):
        print(self.rect.x,self.rect.y,'xy')
material_group=pygame.sprite.Group()
material1=Material((0,0))
material_group.add(material1)
while 1==1:
    material_group.draw(surface)
    material_group.update()

    pygame.display.update()