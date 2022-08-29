import pygame

class Fighter():
    def __init__(self,player, x, y,flip,data,sprite_sheet,animation_steps,health):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack #4:hit 
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = health
        self.alive = True
        self.speed = 10
        self.bar = 5



    def load_images(self,sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y,animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size[0],y * self.size[1],self.size[0],self.size[1])
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size[0] * self.image_scale, self.size[1] * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    
    def move(self,screen_width, screen_height, surface,target,round_over,attackEnemy,attackTimer,attackAmountPlayer,attackAmountEnemy):
        dx = 0
        self.attack_type = 0
        #get keypresses
        key  = pygame.key.get_pressed()
        #can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #check player 1 controls
            if self.player == 1:
                #attack
                if attackEnemy == True:
                    self.attack(surface,target,attackAmountPlayer,attackAmountEnemy)
                    #determine which attack type
                    self.attack_type = 1
                  

            if self.player == 2:
                #attack
                if attackTimer == 0:
                    self.attack(surface,target,attackAmountPlayer,attackAmountEnemy)
                    self.attack_type = 1
                  

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #update player position
        self.rect.x += dx


    #handle animation updates
    def update(self):

        #check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(2)
        #hit
        elif self.hit == True:
            self.update_action(3)

        #attack 1 & 2
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(1)
            elif self.attack_type == 2:
                self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70
        #update image 
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1 
            self.update_time = pygame.time.get_ticks()

        #check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0 
                #check if attack was executed
                if self.action == 1 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 50
                #check if damage was taken
                if self.action == 3:
                    self.hit = False
                    #if the player was in the middle of an attack , then the attack is stopped
                    self.attacking = False

    def attack(self,surface,target,attackAmountPlayer,attackAmountEnemy):
        if self.attack_cooldown == 0:
            #execute attack
            self.attacking = True
            if self.player == 2:
                target.health -= attackAmountEnemy
                target.hit = True
            else:
                target.health -= attackAmountPlayer
                target.hit = True
            # pygame.draw.rect(surface, (0,255,0), attacking_rect)


    def update_action(self,new_action):
        #check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255,0,25), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - - (self.offset[1] * self.image_scale)))
        