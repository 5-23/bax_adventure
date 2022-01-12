# import os

# def install(package):
#     os.system(f"pip install {package}")
# try:
#     install("random")
#     from random import randint, random
# except:
#     install("random --upgrade")

# try:
#     install("ursina --upgrade")
#     from ursina import *
# except:
#     install("ursina")
#     from ursina import *

# try:
#     install("asyncio --upgrade")
#     import asyncio
# except:
#     install("asyncio")
#     import asyncio


from random import randint, random
from ursina import *
# from panda3d import *
# from panda3d_tools import *
# from pandas import *

from ursina import texture
from ursina import audio
from ursina import collider
from ursina import entity
from ursina import text

app = Ursina()
app.texture_on = True
app.set_background_color(color.rgb(10,200,50))

held_time_w = 0
held_time_s = 0
held_time_a = 0
held_time_d = 0
hp = 100
stm = 100
scl = 0
gun = 0
ba_count = 0
coin_count = 0
apple_count = 0
tree_count = 0

grass_entity = 0
sn_entity = 0
zombie_entity = 0
ba_entity = 0

all_entity = grass_entity + sn_entity

player = Entity(
    name = "bax1",
    model = "cube",
    scale = (1,1,0.01),
    texture = load_texture("i_bax_down"),
    te = "i_bax_down",
    collider = "box",
    )

class grass(Entity):
    def __init__(self):
        global grass_entity
        if grass_entity < 10:
            grass_entity += 1
            super().__init__(
                model = "cube",
                x = camera.x + randint(-15,15),
                y = camera.y + randint(-7,7),
                texture = load_texture(f"i_grass{randint(1,3)}.png"),
                scale = (1,1,0.000000001)
            )
        else:
            pass
    
    def update(self):
        global grass_entity
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            grass_entity -= 1
            destroy(self)
class sn(Entity):
    def __init__(self):
        global sn_entity
        self.te = "i_sn_right.png"
        self.ti = 0
        self.set_ti = randint(0,4)
        if sn_entity < 10:
            sn_entity += 1
            super().__init__(
                model = "cube",
                x = camera.x + randint(-15,15),
                y = camera.y + randint(-7,7),
                texture = load_texture(self.te),
                scale = (1,1,0.0001)
            )
        else:
            pass
    def update(self):
        self.spd = 0.01
        self.ti += 1/60
        global sn_entity
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            sn_entity -= 1
            destroy(self)
            return
        if self.set_ti < self.ti:
            a = randint(1,5)
            self.set_ti = randint(0,5)
            self.ti = 0
            if a == 1:
                self.te = "i_sn_right.png"
            elif a == 2:
                self.te = "i_sn_left.png"
            elif a == 3:
                self.te = "i_sn_up.png"
            elif a == 4:
                self.te = "i_sn_down.png"
            else:
                self.te = "i_sn_event.png"
        
        if self.te == "i_sn_right.png":
            self.x += self.spd
        if self.te == "i_sn_left.png":
            self.x -= self.spd
        if self.te == "i_sn_up.png":
            self.y += self.spd
        if self.te == "i_sn_down.png":
            self.y -= self.spd
        self.texture = self.te
        
class dbg_bax(Entity):
    def __init__(self):
        global all_entity
        super().__init__(
            model = "cube",
            text = str(all_entity),
            rotation = (0,0,0),
            scale = (2.5,1,0.01),
        )
    def update(self):
        global all_entity
        self.text = str(all_entity)
        self.x = camera.x-5.9
        self.y = camera.y+3.5
        self.alpha = 80
        self.z = -0.2

class dbg_hp(Entity):
    def __init__(self):
        global hp
        super().__init__(
            model = "cube",
            color = color.rgb(255,0,0),
        )
    def update(self):
        self.x = camera.x+(hp/100)-6.8
        self.y = camera.y+3.8
        self.scale = (hp/50,0.2,0.1)
        self.z = -0.2
class dbg_hp_box(Entity):
    def __init__(self):
        global hp
        super().__init__(
            model = "cube",
            color = color.rgb(255,50,0),
        )
    def update(self):
        self.x = camera.x-7
        self.y = camera.y+3.8
        self.scale = (0.2,0.2,0.1)
        self.z = -0.2

class dbg_stm(Entity):
    def __init__(self):
        global stm
        super().__init__(
            model = "cube",
            color = color.rgb(255,150,0),
        )
    def update(self):
        global stm
        self.x = camera.x+(stm/100)-6.8
        self.y = camera.y+3.5
        self.scale = (stm/50,0.2,0.1)
        self.z = -0.2
class dbg_stm_box(Entity):
    def __init__(self):
        global stm
        super().__init__(
            model = "cube",
            color = color.rgb(255,150,0),
        )
    def update(self):
        global stm
        self.x = camera.x-7
        self.y = camera.y+3.5
        self.scale = (0.2,0.2,0.1)
        self.z = -0.2

class zombie(Entity):
    def __init__(self):
        global zombie_entity
        self.hp = 10
        if zombie_entity < 3:
            zombie_entity += 1
            a = randint(1,4)
            if a == 1:
                tex = "i_bax_left"
            elif a == 2:
                tex = "i_bax_right"
            elif a == 3:
                tex = "i_bax_up"
            else:
                tex = "i_bax_down"
            super().__init__(
                model = "cube",
                x = camera.x + randint(-15,15),
                y = camera.y + randint(-7,7),
                color = color.rgb(50,255,50),
                texture = load_texture(tex),
                collider = "box",
                scale = (1,1,0.001),
                )
        else:
            pass
    def update(self):
        global player
        global hp
        global zombie_entity
        a = 3
        if (self.x < player.x+a and self.x > player.x-a and self.y < player.y+a and self.y > player.y-a):
            if self.x > player.x: 
                self.x-=0.05 
                self.texture = load_texture("i_bax_left")
            
            if self.x < player.x: 
                self.x+=0.05 
                self.texture = load_texture("i_bax_right")
            
            if self.y > player.y: 
                self.y-=0.05 
                self.texture = load_texture("i_bax_down")
            
            if self.y < player.y: 
                self.y+=0.05 
                self.texture = load_texture("i_bax_up")
        if "render/scene/bax1" in str(self.intersects().entities):
            hp -= 1
            Audio("s_hit.mp3",autoplay=False).play()
        if "render/scene/ba1" in str(self.intersects().entities):
            self.hp -=1
            Audio("s_zmb_dmg.mp3",autoplay=False).play()
        if self.hp <= 0:
            coin(x=self.x,y=self.y)
            destroy(self)
            zombie_entity -=1
            return
            
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            zombie_entity -= 1
            destroy(self)
            return

class gun_(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            # color = color.rgb(0,0,0),
            scale = (0.2,0.2,0.01),
        )
    def update(self):
        global player
        global scl
        if gun == 1:
            if scl == 1:
                if player.te == "i_bax_right":
                    self.x = player.x+0.5
                    self.y = player.y-0.1
                    self.scale = (0.5,0.5,0.1)
                    self.texture = load_texture("i_gun_right")
                if player.te == "i_bax_left":
                    self.x = player.x-0.5
                    self.y = player.y-0.1
                    self.scale = (0.5,0.5,0.01)
                    self.texture = load_texture("i_gun_left")
                if player.te == "i_bax_down":
                    self.x = player.x-0.3
                    self.y = player.y-0.2
                    self.scale = (0.3,0.3,0.1)
                    self.texture = load_texture("i_gun_down")
                if player.te == "i_bax_up":
                    self.alpha = 0
                else:
                    self.alpha = 255
            else:
                self.alpha = 0
        else:
            self.alpha = 0
    def input(self,key):
        global ba_count
        if scl == 1:
            if key == "a":
                if ba_count > 0:
                    ba_count -= 1
                    ba()
                    Audio("s_ba.mp3").play()
                else:
                    Audio("s_error.mp3").play()
            
class ba(Entity):
    def __init__(self):
        global player
        super().__init__(
            model = "cube",
            texture = "i_ba",
            collider = "box",
            name = "ba1",
            position = player.position,
            scale = (0.6,0.5,0.3),
        )
        self.te = player.te
        self.audio = 0
    def update(self):
        a = self.te
        if self.audio == 0:
            Audio("s_ba.mp3").play()
            self.audio = 1
        if a == "i_bax_left":
            self.x -= 0.4
            self.rotation_z = 180
        if a == "i_bax_right":
            self.x += 0.4
        if a == "i_bax_up":
            self.y += 0.4
            self.rotation_z = -90
        if a == "i_bax_down":
            self.y -= 0.4
            self.rotation_z = 90
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            destroy(self)
            return

class entity_gun(Entity):
    def __init__(self):
        super().__init__(
            name = "gun_entity1",
            model = "cube",
            texture = load_texture("i_gun_right"),
            scale = (0.5,0.5,0.0001),
            collider = "box",
            position = (player.x + randint(-5,5),player.y + randint(-5,5)),
        )
    def update(self):
        global gun
        if hp <= 0:
            self.position = (player.x + randint(-10,10),player.y + randint(-10,10))
        self.rotation_z += 5
        if "render/scene/bax1" in str(self.intersects().entities):
            gun = 1
            destroy(self)
            Audio("s_item.mp3").play()
            return
        if gun == 0:
            self.alpha = 255
        else:
            self.alpha = -100 

class b_count(Entity):
    def __init__(self):
        global player
        global ba_entity
        if ba_entity < 1:
            ba_entity += 1
            super().__init__(
                model = "cube",
                texture = "i_ba",
                collider = "box",
                name = "ba_entity2",
                scale = (0.6,0.5,0.0001),
                x = camera.x + randint(-15,15),
                y = camera.y + randint(-7,7),
            )
        else:
            pass
    def update(self):
        global ba_count
        global ba_entity
        if "render/scene/bax1" in str(self.intersects().entities):
            ba_count += 1
            ba_entity -= 1
            destroy(self)
            Audio("s_item.mp3").play()
            return
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            destroy(self)
            ba_entity -= 1
            return

class item_box(Entity):
    def __init__(self):
        super().__init__(
            alpha = 50,
            model = "cube",
            scale = (6.3,0.71,0.1)
        )
    def update(self):
        self.y = camera.y - 3.6
        self.x = camera.x
        self.z = -0.2

class out_line(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            scale = (0.7,0.7,0.1),
            texture = load_texture("i_out_line")
        )
    def update(self):
        self.z = -0.2
        self.y = camera.y - 3.6
        if scl == 1:
            self.x = camera.x - 2.8
        if scl == 2:
            self.x = camera.x - 2.1
        if scl == 3:
            self.x = camera.x - 1.4
        if scl == 4:
            self.x = camera.x - 0.7
        if scl == 5:
            self.x = camera.x - 0
        if scl == 6:
            self.x = camera.x + 0.7
        if scl == 7:
            self.x = camera.x + 1.4
        if scl == 8:
            self.x = camera.x + 2.1
        if scl == 9:
            self.x = camera.x + 2.8
        if scl == 0:
            self.x = camera.x + 1000000000000

class item_gun(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            scale = (0.6,0.6,0.00001),
            texture = load_texture("i_gun_right")
        )
    def update(self):
        self.x = camera.x - 2.8
        self.y = camera.y - 3.6
        self.rotation_z = -35
        if gun == 1:
            self.alpha = 255
        else:
            self.alpha = 0

class coin(Entity):
    def __init__(self,x = 0,y = 0):
        super().__init__(
            name = "coin",
            model = "cube",
            texture = load_texture("i_coin"),
            position = (x,y),
            collider = "box"
        )
    def update(self):
        global coin_count
        self.scale = (1,1,0.0001)
        self.rotation_y += 3
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            destroy(self)
            return
        if "render/scene/bax1" in str(self.intersects().entities):
            coin_count += 1
            Audio("s_coin.mp3").play()
            destroy(self)
            return

class tip_1(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_tip1",
            scale = (2,2,0.001),
            position = (5,3,-0.1),
        )
class tip_2(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_tip1",
            scale = (2,2,0.001),
            position = (8,3,-0.1),
        )
class tip_3(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_tip1",
            scale = (2,2,0.001),
            position = (11,3,-0.1),
        )

class ba_count_box(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_ba",
        )
    def update(self):
        self.z = -0.2
        self.x = camera.x-6.96
        self.y = camera.y+3.23
        self.scale = (0.3,0.3,0.0001)
        self.z = -0.2
        self.rotation_z = -35
        if scl == 1:
            if gun == 1:
                if ba_count > 0:
                    self.alpha = 255
                else:
                    self. alpha = 0
            else:
                self. alpha = 0
        else:
            self.alpha = 0


class apple(Entity):
    def __init__(self,x = 0,y = 0):
        super().__init__(
            name = "apple_entity1",
            model = "cube",
            texture = "i_apple",
            x = x,
            y = y,
            collider = "box",
            scale = (0.5,0.5,0.0001),
        )
    def update(self):
        global apple_count
        if "render/scene/bax" in str(self.intersects().entities):
            apple_count += 1
            Audio("s_item.mp3").play()
            destroy(self)
            return
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            destroy(self)
            return

class item_apple(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_apple",
            scale = (0.5,0.5,0.00001),
        )
    def update(self):
        self.x = camera.x - 2.1
        self.y = camera.y - 3.6
        self.rotation_z = -35
        if apple_count > 0:
            self.alpha = 255
        else:
            self.alpha = 0

class apple_(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_apple",
            scale = (0.2,0.2,0.01),
        )
    def update(self):
        global player
        global apple_count
        if apple_count > 0:
            if scl == 2:
                if player.te == "i_bax_right":
                    self.x = player.x+0.5
                    self.y = player.y-0.1
                    self.scale = (0.3,0.3,0.1)
                    self.texture = load_texture("i_apple")
                if player.te == "i_bax_left":
                    self.x = player.x-0.5
                    self.y = player.y-0.1
                    self.scale = (-0.3,0.3,0.01)
                    self.texture = load_texture("i_apple")
                if player.te == "i_bax_down":
                    self.x = player.x-0.3
                    self.y = player.y-0.2
                    self.scale = (0.3,0.3,0.1)
                    self.texture = load_texture("i_apple")
                if player.te == "i_bax_up":
                    self.alpha = 0
                else:
                    self.alpha = 255
            else:
                self.alpha = 0
        else:
            self.alpha = 0

class apple_count_box(Entity):
    def __init__(self):
        super().__init__(
            model = "cube",
            texture = "i_apple",
        )
    def update(self):
        self.z = -0.2
        self.x = camera.x-6.98
        self.y = camera.y+3.21
        self.scale = (0.25,0.25,0.0001)
        self.z = -0.2
        self.rotation_z = -35
        if scl == 2:
            if apple_count > 0:
                self.alpha = 255
            else:
                self.alpha = 0
        else:
            self.alpha = 0

class tree(Entity):
    def __init__(self):
        global tree_count
        te = randint(1,2)
        t = randint(1,3)
        if tree_count < 2:
            tree_count += 1
            super().__init__(
            model = "cube",
            texture = f"i_tree{te}",
            collider = "box",
            x = camera.x + randint(-15,15),
            y = camera.y + randint(-7,7),
            z = -0.1,
            scale = (t,t,0.0001),
        )
        else:
            pass
       
    def update(self):
        global tree_count
        if "render/scene/ba1" in str(self.intersects().entities):
            for i in range(randint(0,3)): apple(x = self.x + randint(-5,5)/10 , y = self.y + randint(-5,5)/10)
            tree_count -= 1

            destroy(self)
            return
        if self.x > camera.x+16 or self.x < camera.x-16 or self.y > camera.y+8 or self.y < camera.y-8:
            destroy(self)
            tree_count -= 1
            return

ba_count_box()
apple_count_box()

apple_()
item_apple()
apple(y=3)
tip_1()
tip_2()
tip_3()
item_gun()
item_box()
out_line()
gun_()
dbg_bax()
dbg_hp()
dbg_hp_box()
dbg_stm()
dbg_stm_box()
entity_gun()

def update():
    global held_time_w
    global held_time_s
    global held_time_a
    global held_time_d
    global all_entity
    global player
    global hp
    global stm
    global scl
    global gun
    global ba_count
    global apple_count

    camera.x += (player.x-camera.x)/30
    camera.y += (player.y-camera.y)/15

    gr0 = 0.01
    gr1 = 0.005
    if held_keys["shift"]:
        if stm > 0:
            max_spd = 0.2
            stm -= 1
        else:
            max_spd = 0.1
            stm = 0
    else:
        max_spd = 0.1
        if stm < 100:
            stm +=0.5

    if held_keys["up arrow"] == 1:
        held_time_w += gr1
        player.texture = load_texture("i_bax_up")
        player.te = "i_bax_up"
    else:
        held_time_w -= gr0
    if held_time_w < 0:
        held_time_w = 0
    
    if held_keys["down arrow"] == 1:
        held_time_s += gr1
        player.texture = load_texture("i_bax_down")
        player.te = "i_bax_down"
    else:
        held_time_s -= gr0
    if held_time_s < 0:
        held_time_s = 0
    
    if held_keys["left arrow"] == 1:
        held_time_a += gr1
        player.texture = load_texture("i_bax_left")
        player.te = "i_bax_left"
    else:
        held_time_a -= gr0
    if held_time_a < 0:
        held_time_a = 0
    
    if held_keys["right arrow"] == 1:
        held_time_d += gr1
        player.texture = load_texture("i_bax_right")
        player.te = "i_bax_right"
    else:
        held_time_d -= gr0
    
    if held_keys["0"] == 1:
        scl = 0
    if held_keys["1"] == 1:
        scl = 1
    if held_keys["2"] == 1:
        scl = 2
    if held_keys["3"] == 1:
        scl = 3
    if held_keys["4"] == 1:
        scl = 4
    if held_keys["5"] == 1:
        scl = 5
    if held_keys["6"] == 1:
        scl = 6
    if held_keys["7"] == 1:
        scl = 7
    if held_keys["8"] == 1:
        scl = 8
    if held_keys["9"] == 1:
        scl = 9
    
    if held_time_d < 0:
        held_time_d = 0

    if held_time_w > max_spd:
        held_time_w = max_spd
    if held_time_s > max_spd:
        held_time_s = max_spd
    if held_time_a > max_spd:
        held_time_a = max_spd
    if held_time_d > max_spd:
        held_time_d = max_spd
    
    player.x += held_time_d
    player.x -= held_time_a
    player.y += held_time_w
    player.y -= held_time_s
    grass()
    sn()
    zombie()
    b_count()
    tree()
    all_entity = grass_entity + sn_entity
    if hp <= 0:
        Audio("s_oof.mp3").play()
        player.position = (randint(-100,100),randint(-100,100),0)
        hp = 100
        ba_count = 0
        stm = 100
        apple_count = 0
        if gun == 1:
            gun = 0
            entity_gun()
        scl = 0
    if hp > 100:
        hp = 100
    if stm > 100:
        stm = 100
def input(key):
    global hp
    global stm
    global apple_count
    if key == "a":
        if apple_count > 0:
            if scl == 2:
                hp +=10
                stm += 5
                apple_count -=1
                Audio("s_apple_eat.mp3").play()
Audio("s_main.mp3",loop = True).play()
app.run()