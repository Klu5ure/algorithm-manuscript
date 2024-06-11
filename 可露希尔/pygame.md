精灵、精灵组、rect、direction

```python
# 精灵和精灵组
class A(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 		# 继承自父类
        self.image = 一张图片
        self.rect = self.image.get_rect()
    def update(self):
        pass
group = pygame.sprite.Group()
a = A()
group.draw(screen) # 将所有精灵绘制到窗口
group.update() # 调用所有精灵的update方法


# 除了用add，还可以用下面这种方式将精灵加到精灵组
class A(pygame.sprite.Sprite):
    def __init__(self,g):
        super().__init__(g)
    def update(self):
        pass
 
group = pygame.sprite.Group()
a = A(group)


# self.rect
self.rect.x：精灵左上角的x坐标
self.rect.y：精灵左上角的y坐标
self.rect.centerx：精灵中心点的x坐标
self.rect.centery：精灵中心点的y坐标
self.rect.center：精灵中心点的坐标
self.rect.width：精灵的宽度
self.rect.height：精灵的高度
self.rect = self.image.get_rect(center = (100,100)) # 这样可以将图片中心放在100,100
```

```python
# player.py
import pygame
from settings import *
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
       super().__init__(group)
       # general setup
       #创建一个矩形来代表玩家
       #这里的变量名一定要叫image，这是它的父类Sprite的规定
       self.image = pygame.Surface((32,64))
       self.image.fill('green')
       #设置坐标
       #返回值有很多，既包含了距离也包含了大小
       #大概有x,y,centerx,centery,width,height这六个返回值
       #参数如果不写，默认为(0,0)，也就是把他的位置设为左上角
       #这里参数为center = pos，也就是把他的中心放在了pos位置上
       #这里的变量一定要取名为rect，这是它的父类Sprite的规定
       #只有这样，才能正确调用 draw函数
       self.rect = self.image.get_rect(center = pos)
       # movement attributes
       self.direction = pygame.math.Vector2()
       self.pos = pygame.math.Vector2(self.rect.center)
       self.speed = 200
 
    def input(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_UP]:
          self.direction.y = -1
       elif keys[pygame.K_DOWN]:
          self.direction.y = 1
       else:
          self.direction.y = 0
       if keys[pygame.K_RIGHT]:
          self.direction.x = 1
       elif keys[pygame.K_LEFT]:
          self.direction.x = -1
       else:
          self.direction.x = 0
 
    def move(self,dt):
       # normalizing a vector
       #向量归一化，pygame提供了一个便捷的API
       if self.direction.magnitude() > 0:#只有按下按钮移动的时候才能调用，不然会报错
          #magnitude是返回向量的欧几里得距离
          #向量的存储格式是[x,y],归一化的作用是让x**2 + y**2 = 1 
          #但是没有按下按钮的时候，【0，0】会使数学计算发生错误
          self.direction = self.direction.normalize()
       # horizontal movement 
       #变化的位移 = 方向 * 速度 * 变化的时间
       #如果不*dt，就是一秒变化的距离，但实际上每一帧都在调用move函数，因此需要乘上一帧所用的时间，才是真正的位移
       self.pos.x += self.direction.x * self.speed * dt
       #rect.centerx 是中心点的x坐标，如果是rect.x就是左上角的x坐标
       self.rect.centerx = self.pos.x
       # vertical movement
       self.pos.y += self.direction.y * self.speed * dt
       self.rect.centery = self.pos.y
 
    def update(self, dt):
       self.input()
       self.move(dt)
        

        
'''
main.py while里面调用level.run，每一帧都调用这个方法
level.run 调用
    self.all_sprites.draw(self.display_surface)
    self.all_sprites.update(dt)
update实际上调用的是player.py里的update，也就是input和move
'''
```

导入图片资源

```python
class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)

		self.import_assets()
		self.status = 'left_water'
		self.frame_index = 0

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 200

	def import_assets(self):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        # 经过这一步之后，self.animations = {'up': [图片一，图片二，图片三，图片四],...}
		for animation in self.animations.keys():
			full_path = './s3 - import/s3 - import/graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

            
def import_folder(path):
	surface_list = []
	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list

'''
./s3 - import/s3 - import/graphics/character/这下面有很多文件夹，例如up，down，left等，每一个文件夹都有对应的几张图片
Player的方法import_assets会遍历这些图片，全部转为pygame的图片格式，然后导入到self.animations这个结构中
'''
```

