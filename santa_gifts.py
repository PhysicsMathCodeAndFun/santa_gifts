import pygame
import sys
import random
import math


# https://www.gameart2d.com/santa-claus-free-sprites.html
# https://www.pngitem.com/download/iombmmb_christmas-gift-sprite-hd-png-download/


pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()


delta_time = 0.0
dt = 0.001
t = 0


class Gifts:
    def __init__(self):
        self.rect = pygame.Rect(0,0, 64, 64)
        self.rect.centerx = random.randint(64, w - 64)
        self.rect.centery = random.randint(64, h - 64)
        self.color = (255, 0, 0)
        self.velocity = [0,0]
        self.santa_id = -1
        img = pygame.image.load('gift.png').convert_alpha()
        img = pygame.transform.scale(img, (50, 50))  
        self.image = img
 
    def draw(self, screen):
        if self.santa_id != -1:
            self.rect.centerx += self.velocity[0]
            self.rect.centery += self.velocity[1]

        screen.blit(self.image, self.rect)
        
    def move(self, rect_2):
        d = [rect_2.centerx - self.rect.centerx, rect_2.centery - self.rect.centery]
        m = math.sqrt(d[0]**2 + d[1]**2)

        if m >= 30 and m != 0.0:
            self.velocity = [3 * d[0] / m, 3 * d[1] / m] 
        
gifts = []

for l in range(200):
    gifts.append(Gifts())


class Santa(pygame.sprite.Sprite):
    def __init__(self, pos, santa_id):
        super().__init__()

        self.dead_imgs = []
        self.run_imgs = []
        
        for i in range(1, 18):  
            img = pygame.image.load(f'dead/Dead ({i}).png').convert_alpha()
            img = pygame.transform.scale(img, (280, 192))  
            self.dead_imgs.append(img)
            
        for i in range(1, 12):  
            img = pygame.image.load(f'run/Run ({i}).png').convert_alpha()
            img = pygame.transform.scale(img, (280, 192))  
            self.run_imgs.append(img)
        
        self.rect = self.run_imgs[0].get_rect(center=pos)
        self.collid_rect = pygame.Rect(self.rect.x, self.rect.y, 70, 180)
        
        self.id = 0
        self.santa_id = santa_id
        
        self.dead = False
        self.count = 0
        
        v0 = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
        m = math.sqrt(v0[0]**2 + v0[1]**2)
        self.velocity = [3.0 * v0[0] / m, 3.0 * v0[1] / m]
        
        if self.velocity[0] < 0:
            self.flipX()
            
        self.time_change_pos = 0
        self.gifts_ids = []
        
    def draw(self, screen):
        global gifts
        
        if self.count >= 10:
            if not self.dead:
                self.id += 1
                self.count = 0
        if not self.dead and self.id >= 11:
            self.id = 0

        #pygame.draw.rect(screen, (255,0,0), self.collid_rect, width=0, border_radius=2)
        
        if self.dead:
            screen.blit(self.dead_imgs[self.id], self.rect)
        else:
            screen.blit(self.run_imgs[self.id], self.rect)
        
        if not self.dead:
            self.count += 1
            
            # movement
            last_pos = [self.rect.centerx, self.rect.centery]
            self.rect.centerx += self.velocity[0]
            self.rect.centery += self.velocity[1]
            
            if self.rect.centerx + 70 >= w or self.rect.centerx - 70 <= 0:
                self.rect.centerx = last_pos[0]
                self.velocity[0] = -self.velocity[0]
                self.flipX()
                
            if self.rect.centery + 48 >= h or self.rect.centery - 48 <= 0:
                self.rect.centery = last_pos[1]
                self.velocity[1] = -self.velocity[1]
            
            if self.time_change_pos >= 100:            
                v0 = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
                m = math.sqrt(v0[0]**2 + v0[1]**2)
                new = [3.0 * v0[0] / m, 3.0 * v0[1] / m]
                if new[0] == 0:
                    new[0] = 1.0
                    
                if new[0] / abs(new[0]) != self.velocity[0] / abs(self.velocity[0]):
                    self.velocity = new
                    self.flipX()
                self.time_change_pos = 0
            self.time_change_pos += 1
            self.collid_rect.centerx = self.rect.centerx
            self.collid_rect.centery = self.rect.centery
            # ---
            
            # gifts
            if len(self.gifts_ids) != 0:
                gifts[self.gifts_ids[0]].move(self.collid_rect)
                for i in range(1, len(self.gifts_ids)):
                    gifts[self.gifts_ids[i]].move(gifts[self.gifts_ids[i-1]].rect)           
            # ---
            
    def flipX(self):
        for i in range(len(self.run_imgs)):
            self.run_imgs[i] = pygame.transform.flip(self.run_imgs[i], True, False)
    def flipY(self):
        for i in range(len(self.run_imgs)):
            self.run_imgs[i] = pygame.transform.flip(self.run_imgs[i], False, True)
            
    def collide(self):
        global gifts
        
        for i in range(len(gifts)):
            if self.collid_rect.colliderect(gifts[i].rect) and gifts[i].santa_id == -1:
                gifts[i].santa_id = self.santa_id
                if self.santa_id == 0:
                    gifts[i].color = (0, 100, 0)
                elif self.santa_id == 1:
                    gifts[i].color = (100, 100, 0)
                else:
                    gifts[i].color = (0, 100, 100)
                
                self.gifts_ids.append(i)
                beep.play()

santa = []
santa.append(Santa((random.randint(280, w - 280), random.randint(192, h - 192)), 0))
santa.append(Santa((random.randint(280, w - 280), random.randint(192, h - 192)), 1))
#santa.append(Santa((random.randint(140, w - 140), random.randint(96, h - 96)), 2))


def Update(screen):
    global delta_time
    global dt
    global t
    global h,w
    global santa, gifts
       
    
    for n in gifts:
        n.draw(screen)
     
    for s in santa:
        s.draw(screen)
        s.collide()
    
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    t += 1
    
    
isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
            
    screen.fill((0,0,0))       
    Update(screen)
    
pygame.quit()
sys.exit()
