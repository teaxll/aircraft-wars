# 引入
import codecs
import random

import pygame

from pygame.locals import *

from sys import exit

SCREEN_WIDTH=480
SCREEN_HEIGHT=800


#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,bullet_img,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.midbottom=init_pos
        self.speed=10
    def move(self):
        self.rect.top -=self.speed

#玩家飞机
class Player(pygame.sprite.Sprite):
    def __init__(self,plane_img,player_rect,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=[]
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect=player_rect[0]
        self.rect.topleft=init_pos
        self.speed=8
        self.bullets=pygame.sprite.Group()
        self.image_index=0
        self.is_hit=False
    #飞机发射子弹
    def shoot(self,bullet_img,):
        bullet=Bullet(bullet_img,self.rect.midtop)
        self.bullets.add(bullet)

    #向上移动
    def Moveup(self):
        if self.rect.top<=0:
            self.rect.top=0
        else:
            self.rect.top -=self.speed
    #向下移动
    def MoveDown(self):
        if self.rect.top>= SCREEN_HEIGHT-self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top +=self.speed
    #向左移动
    def MoveLeft(self):
        if self.rect.left<=0:
            self.rect.left=0
        else:
            self.rect.left -=self.speed
    #向右移动
    def MoveRight(self):
        if self.rect.left>=SCREEN_WIDTH-self.rect.width:
            self.rect.left=SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed
#敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_img,enemy_down_img,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=enemy_img
        self.rect=self.image.get_rect()
        self.rect.topleft=init_pos
        self.down_imgs=enemy_down_img
        self.speed=2
        self.down_index=0
    def move(self):
        self.rect.top +=self.speed

#写入score文件排行榜数据
def write_txt(context,srtim,path):
    f=codecs.open(path,srtim,'utf8')
    f.write(str(context))
    f.close()


#读取score。txt的内容【‘0mr0mr’】
def read_txt(path):
    with open(path,'r',encoding='utf8') as f:
        lines = f.readlines()
    return lines
#初始化pygame
pygame.init()
#设置窗体大小
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#设置名称
pygame.display.set_caption('飞机大战')
#设置图标
me1=pygame.image.load('b/image/me1.png').convert_alpha()
pygame.display.set_icon(me1)
background=pygame.image.load('b/image/background.png')
#游戏结束
game_over=pygame.image.load('b/image/gameover.png')
#玩家，飞机，敌机
plane_img=pygame.image.load('b/image/shoot.png')

def startGame():
    player_rect=[]
    #正常飞机图片
    player_rect.append(pygame.Rect(0,99,100,120))
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    #碰撞后飞机图片
    player_rect.append(pygame.Rect(165, 234, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos=[200,600]
    player=Player(plane_img,player_rect,player_pos)
    bullet_rect=pygame.Rect(1005,987,10,21)
    bullet_img=plane_img.subsurface(bullet_rect)
    enemy1_rect=pygame.Rect(530,612,57,43)
    enemy1_img=plane_img.subsurface(enemy1_rect)
    enemy1_down_ims=[]      #飞机被销毁后的图片
    enemy1_down_ims.append(plane_img.subsurface(pygame.Rect(267,347,57,43)))
    enemy1_down_ims.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_ims.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_ims.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
    shoot_frequency=0
    enemy_frequency=0
    player_down_index=16
    #显示分数
    score=0
    clock=pygame.time.Clock()

    enemies1=pygame.sprite.Group()
    enemies_down=pygame.sprite.Group()



    #游戏主循环
    running=True
    while running:
        screen.fill(0)
        screen.blit(background,(0,0))
        clock.tick(60)
        #生成子弹
        if not player.is_hit:
            if shoot_frequency%15==0:
                player.shoot(bullet_img)
            shoot_frequency+=1
            if shoot_frequency>=15:
                shoot_frequency=0
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom<0:
                player.bullets.remove(bullet)
        player.bullets.draw(screen)
        #创建敌机
        if enemy_frequency%50==0:
            enemy1_pos=[random.randint(0,SCREEN_WIDTH-enemy1_rect.width),0]   #敌机生成的地方，屏幕减去敌机大小
            enemy1=Enemy(enemy1_img,enemy1_down_ims,enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency+=1
        if enemy_frequency>=100:
            enemy_frequency=0
        for enemy in enemies1:
            enemy.move()
            if enemy.rect.top<0:
                enemies1.remove(enemy)

            #检测pygame中两个精灵是否碰撞，玩家飞机和敌机是否碰撞
            if pygame.sprite.collide_circle(enemy,player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit=True
                break

                # 判断玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.image_index], player.rect)
            player.image_index = shoot_frequency // 8
        else:
            player.image_index=player_down_index//8  #玩家飞机销毁以后得知
            #screen.blit(player.image[player.image_index],player_rect)
            player_down_index+=1
        #绘制玩家飞机碰撞时的图片，
            if player_down_index>47:

                running=False

                #  key,veul
        #检测子弹是否与敌机有碰撞（pygame中两个精灵是否碰撞）
        enemiesl_down=pygame.sprite.groupcollide(enemies1,player.bullets,True,True)    #true和1都可以
        for enemy_down in enemiesl_down:
            enemies_down.add(enemiesl_down)   #将发生碰撞的敌机放入字典中
        #绘制敌机爆炸时的图片，播放图片
        for enemy_down in enemies_down:
            if enemy_down.down_index>7:
                enemies_down.remove(enemy_down)
                #击败一架敌机得分1分
                score+=1
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index//2],enemy_down.rect)
            enemy_down.down_index+=1
        enemies1.draw(screen)
        #绘制游戏得分，一家敌机1分
        score_font=pygame.font.Font(None,36)   #设置得分的字号大小
        score_text=score_font.render(str(score),True,(128,128,128))
        text_rect=score_text.get_rect()
        screen.blit(score_text,text_rect)




        #判断玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.image_index],player.rect)
            player.image_index=shoot_frequency//8       #显示动态尾焰，有疑问
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        key_pressed=pygame.key.get_pressed()
    #向上
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.Moveup()

    #向下
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.MoveDown()

    #向左
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.MoveLeft()
    #向右
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.MoveRight()
    #显示最终得分
    screen.blit(game_over,(0,0))
    font=pygame.font.Font(None,48)
    text=font.render('Score:'+str(score),True,(255,0,0))
    text_rect=text.get_rect()
    text_rect.centerx=screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery+4
    screen.blit(text,text_rect)
    #重新开始按钮
    xtfont=pygame.font.SysFont('SimHei',30)#设置中文字体
    textstart=xtfont.render('重新开始',True,(255,0,0))
    text_rect=textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen.blit(textstart, text_rect)
    #制作人信息
    xtfont = pygame.font.SysFont('SimHei', 30)  # 设置中文字体
    textstart = xtfont.render('制作人：李浩恺', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 180
    screen.blit(textstart, text_rect)

    if score>10:
        xtfont = pygame.font.SysFont('SimHei', 30)  # 设置中文字体
        textstart = xtfont.render('勉强有我一半厉害', True, (255, 0, 0))
        text_rect = textstart.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 220
        screen.blit(textstart, text_rect)

    else:
        xtfont = pygame.font.SysFont('SimHei', 30)  # 设置中文字体
        textstart = xtfont.render('就这？你个废物', True, (255, 0, 0))
        text_rect = textstart.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 220
        screen.blit(textstart, text_rect)


    #['0','0','0',...]
        j=0
        arrayscore=read_txt(r'score.txt')[0].split('mr')
        for i in range(0,len(arrayscore)):
            #判断是否是当前获取的分数以及是否大于排行榜上的分数
            if score>int(arrayscore[i]):
                j=arrayscore[i]
                arrayscore[i]=str(score)
                score=0
            if int(j)>int(arrayscore[i]):
                k=arrayscore[i]
                arrayscore[i]=str(j)
                j=k
        for i in range(0,len(arrayscore)):
            if i==0:
                write_txt(arrayscore[i]+'mr','w',r'score.txt')
            else:
                if(i==9):
                    write_txt(arrayscore[i],'a',r'score.txt')
                else:
                    write_txt(arrayscore[i]+'mr','a',r'score.txt')



startGame()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if screen.get_rect().centerx-70<=event.pos[0] and event.pos[0]<=screen.get_rect().centerx+50 and screen.get_rect().centerx+100<=event.pos[1] and event.pos[1]<=screen.get_rect().centery+140:
                startGame()
            if screen.get_rect().centerx - 70 <= event.pos[0] and event.pos[
                0] <= screen.get_rect().centerx - 50 and screen.get_rect().centerx + 160 <= event.pos[1] and event.pos[
                1] <= screen.get_rect().centery+200:
                startGame()


    pygame.display.update()