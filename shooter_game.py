
from pygame import *
from time import sleep
from random import randint

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
game = True
finish = False

clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

count_alive = 0
count_die = 0
goal = 10
sound_fire = mixer.Sound('fire.ogg')

font.init()
font = font.SysFont("Arial",40)

text_win = font.render('Убито:' + str(count_die), 1, (255, 255, 255))
text_lose = font.render('Пропущено:' + str(count_alive), 1, (255, 255, 255))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y,size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 437:
            self.rect.y += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",5,self.rect.centerx,self.rect.top,15,20)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        global count_alive
        
        if self.rect.y <= 500:
            self.rect.y += self.speed
        if self.rect.y >= 500:
            count_alive += 1
            self.rect.x = randint(100,600)
            self.rect.y = 0
            
class Asteroid(GameSprite):
    def update(self):
        global count_alive
        
        if self.rect.y <= 500:
            self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(100,600)
            self.rect.y = 0




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png",randint(1,3),randint(100,600),0,80,50)
    monsters.add(monster)
asters = sprite.Group()

for i in range(1,3):
    aster = Asteroid("asteroid.png",2,randint(100,600),0,80,50)
    asters.add(aster)




bullets = sprite.Group()

sprite1 = Player("rocket.png",5,5,350,60,60)
while game:
    
    for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    sound_fire.play()
                    sprite1.fire()


    if not finish:
        window.blit(background,(0,0))
        sprite1.update()
        monsters.update()
        bullets.update()
        asters.update()

        sprite1.reset()  
        monsters.draw(window)
        bullets.draw(window)
        asters.draw(window)
         


        u_win = font.render('Ты победил', 1, (255, 255, 255))
        u_lose = font.render('Ты проиграл', 1, (255, 255, 255))
    
        

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            count_die += 1
            monster = Enemy("ufo.png",randint(1,3),randint(100,600),0,80,50)
            monsters.add(monster)

        if sprite.spritecollide(sprite1 ,monsters ,False) or sprite.spritecollide(sprite1 ,asters ,False) or count_alive >= 3:
            finish = True
            window.blit(u_lose,(280,250))
            
            
            
        if count_die >= goal:
            finish = True
            
            window.blit(u_win,(280,250))
            

        text_win = font.render('Убито:' + str(count_die), 1, (255, 255, 255))
        text_lose = font.render('Пропущено:' + str(count_alive), 1, (255, 255, 255))

        window.blit(text_win,(15,30))
        window.blit(text_lose,(15,65))
        
        display.update()    
        if finish:
            finish = False
            count_alive = 0
            count_die = 0
            for b in bullets:
                b.kill()
            for m in monsters:
                m.kill()
            for a in asters:
                a.kill()
            time.delay(3000)
            for i in range(1,6):
                monster = Enemy("ufo.png",randint(1,3),randint(100,600),0,80,50)
                monsters.add(monster)
            for i in range(1,3):
                aster = Asteroid("asteroid.png",2,randint(100,600),0,80,50)
                asters.add(aster)

        time.delay(13)
        
    # clock.tick(FPS)
    
    
