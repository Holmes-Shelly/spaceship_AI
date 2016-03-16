# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
UNI = [WIDTH, HEIGHT]
missiles = set()
rocks = set()
broken_rocks = set()
broken_miss = set()
#ship_rock = False
#miss_rock = False
ship_pos = [WIDTH / 2, HEIGHT / 2]
ROTA = 3.14 / 60
rotation = 0
thr = False
mis = False
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = float('inf'), animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        self.lifespan = lifespan
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_brown.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.miss_pos = [45, 0]
        self.miss_vel = [0, 0]
        self.thrust = False
        self.missile = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def __str__(self):
        return "Ship"
        
    def get_center(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            self.image_center[0] = 135
        else:
            self.image_center[0] = 45
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle) 
        
    def shoot(self):
        if not self.missile:
            return
        for n in range(2):
            self.miss_pos[n] = self.pos[n] + angle_to_vector(self.angle)[n] * self.radius
            self.miss_vel[n] = self.vel[n] + angle_to_vector(self.angle)[n] * 10
        missiles.add(Sprite(self.miss_pos, self.miss_vel, 0, 0, missile_image, missile_info, missile_sound, 1))
        
    def update(self):
        self.angle += rotation
        for n in range(2):
            self.pos[n] += self.vel[n]
            self.pos[n] = self.pos[n] % UNI[n]
            self.vel[n] -= self.vel[n] * 0.02
        if self.thrust:
            ship_thrust_sound.play()
            for n in range(2):
                self.vel[n] += 0.2 * angle_to_vector(self.angle)[n]
        else:
            ship_thrust_sound.pause()
        

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, age = float('inf')):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = age
        self.live = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def __str__(self):
        return "Sprite"
            
    def get_center(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
            
    def collide(self, SM):
        global lives, score
        min_dis = self.get_radius() + SM.get_radius()
        dis = dist(self.get_center(), SM.get_center())
        if dis < min_dis:
            broken_rocks.add(self)
            if str(SM) == "Ship":
                lives -= 1
            else:
                score += 1
                broken_miss.add(SM)
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.live += 0.02
        if self.live > self.age:
            broken_miss.add(self)
        self.angle += self.angle_vel 
        for n in range(2):
            self.pos[n] += self.vel[n]
            self.pos[n] = self.pos[n] % UNI[n]
        
  
def draw(canvas):
    global time
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    SL = {0.1 : "SCORE:", 0.7 : "LIVES:", 0.3 : score, 0.9 : lives}
    for x in SL:
        canvas.draw_text(str(SL[x]), [WIDTH * x, HEIGHT * 0.1], 36, "Yellow")

    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    for rock in rocks:
        rock.draw(canvas)
        rock.update()
        rock.collide(my_ship) 
        for miss in missiles:
            rock.collide(miss)
    rocks.difference_update(broken_rocks)
    
    
    for miss in missiles:
        miss.draw(canvas)
        miss.update()
    missiles.difference_update(broken_miss)
    

# timer handler that spawns a rock    
def rock_spawner():
    if len(rocks) >= 12:
        return
    rocks.add(Sprite([WIDTH * random.random(), HEIGHT * random.random()], 
                    [random.random() * random.randint(-1, 1),  
                    random.random() * random.randint(-1, 1)], 0, 
                    ROTA * random.random() * random.randint(-1, 1),
                    asteroid_image, asteroid_info))
        
def key_down(key):
    global rotation, thr, mis
    LR = {-1 : 'left', 1 : 'right'}
    for dir in LR:
        if key == simplegui.KEY_MAP[LR[dir]]:
            rotation += ROTA * dir
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    if key == simplegui.KEY_MAP['space']:
        my_ship.missile = True
        my_ship.shoot()
                    
def key_up(key):
    global rotation, thr, mis
    LR = {-1 : 'left', 1 : 'right'}
    for dir in LR:
        if key == simplegui.KEY_MAP[LR[dir]]:
            rotation -= ROTA * dir
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    if key == simplegui.KEY_MAP['space']:
        my_ship.missile = False
  
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship(ship_pos, [0, 0], 0, ship_image, ship_info)
rock_spawner()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

timer_rock = simplegui.create_timer(1000.0, rock_spawner)
timer_shoot = simplegui.create_timer(200.0, my_ship.shoot)

# get things rolling
timer_rock.start()
timer_shoot.start()
frame.start()
