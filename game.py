#imports
from math import floor
import pygame,sys
from fighter import Fighter
from bars import Bar
from random import randint
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from button import Button
from superbase import getHighscores, signUpOrLogin,getCharacterCoins, addCoins, setHighscores, getUserDetails, getOwnedCharacters,buyCharacter, getCharacters


#initialization 
pygame.init()

#create game window
SCREEN_WIDTH = 1400;
SCREEN_HEIGHT = 788;

#AUTH
AUTH = None

#screen info
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

#Background images
BG = pygame.image.load("assets/images/background/background_menu_2.png")
bgEasy = pygame.image.load("assets/images/background/easyBG.png");
bgEasy = pygame.transform.scale(bgEasy, (int(SCREEN_WIDTH/3),SCREEN_HEIGHT))
bgNormal = pygame.image.load("assets/images/background/normalBG.png");
bgNormal = pygame.transform.scale(bgNormal, (int(SCREEN_WIDTH/3),SCREEN_HEIGHT))
bgHard = pygame.image.load("assets/images/background/hardBG.png");
bgHard = pygame.transform.scale(bgHard, (int(SCREEN_WIDTH/3 +2) ,SCREEN_HEIGHT))

#Gets the font and size 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/fonts/The Bomb Sound Italic.ttf", size)


#Character select screen
def chooseFighter(AUTH):
    #load assets
    SWORD = pygame.image.load("assets/sword.png")
    SWORD = pygame.transform.scale(SWORD, (28 ,30))
    HEART = pygame.image.load("assets/heart.png")
    HEART = pygame.transform.scale(HEART, (30 ,30))

    #info array
    damages = [10,15,15,20,20,20,30,30,30]          
    healths = [75,90,100,110,130,150,170,180,200]

    #sorting the characters
    characters = getOwnedCharacters(AUTH.id)
    owned_arr = characters.split(',')
    for x in range(len(owned_arr)):
        owned_arr[x] = int(owned_arr[x])
    owned_arr = sorted(owned_arr)

    while True :
        MOUSE_POS = pygame.mouse.get_pos()
        scaled_bg = pygame.transform.scale(BG, (SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(scaled_bg,(0,0))
        player_positions = [[300,50], [600 ,50], [900,50], [300,300], [600,300], [900,300], [300,550], [600,550], [900,550]]
        sword_positions =[[450,100],[750,100],[1050,100],[450,350],[750,350],[1050,350],[450,600],[750,600],[1050,600]]
        heart_positions =[[450,150],[750,150],[1050,150],[450,400],[750,400],[1050,400],[450,650],[750,650],[1050,650]]
        buttons = {}

        #Back Button
        CHAR_SELECT_BACK = Button(image=None, pos=(80,40), 
                            text_input="<- BACK", font=get_font(30), base_color=(255,255,255), hovering_color=(240,119,0))
        CHAR_SELECT_BACK.changeColor(MOUSE_POS)
        CHAR_SELECT_BACK.update(screen)


        for x in range(len(owned_arr)):
            PLAYER = pygame.image.load("assets/images/shopImages/Player"+str(owned_arr[x])+".png")
            PLAYER = pygame.transform.scale(PLAYER, (141,200))
            screen.blit(SWORD, (sword_positions[x][0], sword_positions[x][1]))
            screen.blit(HEART, (heart_positions[x][0], heart_positions[x][1]))
            screen.blit(get_font(30).render(str(damages[owned_arr[x]-1]), True, (255,255,255)), (sword_positions[x][0] + 35, sword_positions[x][1]))
            screen.blit(get_font(30).render(str(healths[owned_arr[x]-1]), True, (255,255,255)), (heart_positions[x][0] + 35, heart_positions[x][1]))
            screen.blit(PLAYER,(player_positions[x][0],player_positions[x][1]))
            BUTTON_SELECT = Button(image=pygame.image.load("assets/selectButton.png"), pos=(player_positions[x][0], player_positions[x][1]), text_input="Select", font=get_font(25), base_color=(255, 255, 255), hovering_color=(240,119,0))
            buttons["BUTTON_SELECT_{0}".format(x)] = BUTTON_SELECT
            BUTTON_SELECT.changeColor(MOUSE_POS)
            BUTTON_SELECT.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(len(buttons)):
                    if buttons['BUTTON_SELECT_'+str(x)].checkForInput(MOUSE_POS):
                        play(AUTH,owned_arr[x])
                if CHAR_SELECT_BACK.checkForInput(MOUSE_POS):
                    main_menu(AUTH) 

        pygame.display.update()

#Difficulty select screen
def play(AUTH,characterId):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill((255,255,255))

        DIFFICULTY_TEXT = get_font(38).render("Choose your difficulty", True, (255,255,255))
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(SCREEN_WIDTH/2,100))

        screen.blit(bgEasy,(0,0))
        screen.blit(bgNormal,(SCREEN_WIDTH/3,0))
        screen.blit(bgHard,(SCREEN_WIDTH/3 *2 -1 ,0))
        pygame.draw.rect(screen, (20,20,20), pygame.Rect(SCREEN_WIDTH/3 -1 , 218, 2, 900))
        pygame.draw.rect(screen, (20,20,20), pygame.Rect(SCREEN_WIDTH/3 *2 -1 , 178, 2, 900))
        screen.blit(DIFFICULTY_TEXT,DIFFICULTY_RECT)

        
        PLAY_BACK = Button(image=None, pos=(80,40), 
                            text_input="<- BACK", font=get_font(30), base_color=(255,255,255), hovering_color=(240,119,0))
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)



        DIFFICULTY_EASY_BUTTON = Button(image=pygame.image.load("assets/paint_button2.png"), pos=(SCREEN_WIDTH/3 - 230, SCREEN_HEIGHT -150), 
                            text_input="EASY", font=get_font(60), base_color=(215, 252, 212), hovering_color=(240,119,0))
        DIFFICULTY_NORMAL_BUTTON = Button(image=pygame.image.load("assets/paint_button2.png"), pos=(((SCREEN_WIDTH/3) *2) -230, SCREEN_HEIGHT -150), 
                            text_input="NORMAL", font=get_font(60), base_color=(215, 252, 212), hovering_color=(240,119,0))
        DIFFICULTY_HARD_BUTTON = Button(image=pygame.image.load("assets/paint_button2.png"), pos=(SCREEN_WIDTH -230, SCREEN_HEIGHT -150), 
                            text_input="HARD", font=get_font(60), base_color=(215, 252, 212), hovering_color=(240,119,0))

        DIFFICULTY_EASY_BUTTON.changeColor(PLAY_MOUSE_POS)
        DIFFICULTY_EASY_BUTTON.update(screen)
        DIFFICULTY_NORMAL_BUTTON.changeColor(PLAY_MOUSE_POS)
        DIFFICULTY_NORMAL_BUTTON.update(screen)
        DIFFICULTY_HARD_BUTTON.changeColor(PLAY_MOUSE_POS)
        DIFFICULTY_HARD_BUTTON.update(screen)

        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if DIFFICULTY_EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                            game("easy", AUTH, characterId)
                        elif DIFFICULTY_NORMAL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                            game("normal", AUTH, characterId)
                        elif DIFFICULTY_HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                            game("hard", AUTH, characterId)
                        elif PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                            main_menu(AUTH)

        pygame.display.update()


#login screen
def login():
    usernameInput = ""
    passwordInput = ""
    passwordProtected = ""
    whichInput = 0
    color_error = (0,0,0)
    height_arrow = 280
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill((0,0,0))

        LOGIN_TEXT = get_font(45).render("Login", True, (255,255,255))
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(SCREEN_WIDTH/2,100))
        screen.blit(LOGIN_TEXT,LOGIN_RECT)

        LOGIN_TEXT = get_font(25).render("Username", True, (255,255,255))
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(SCREEN_WIDTH/2,220))
        screen.blit(LOGIN_TEXT,LOGIN_RECT)

        LOGIN_USERNAME_INPUT = Button(image=pygame.image.load("assets/paint_button3.png"), pos=(SCREEN_WIDTH/2 , SCREEN_HEIGHT /2 -70), 
                            text_input=usernameInput, font=get_font(45), base_color=(215, 252, 212), hovering_color=(215, 252, 212))

        LOGIN_TEXT = get_font(25).render("Password", True, (255,255,255))
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(SCREEN_WIDTH/2,500))
        screen.blit(LOGIN_TEXT,LOGIN_RECT)

        LOGIN_PASSWORD_INPUT = Button(image=pygame.image.load("assets/paint_button3.png"), pos=(SCREEN_WIDTH/2 , SCREEN_HEIGHT /2 + 200), 
                            text_input=passwordProtected, font=get_font(45), base_color=(215, 252, 212), hovering_color=(215, 252, 212))

        LOGIN_ARROW = pygame.image.load("assets/arrow.png")
        LOGIN_ARROW = pygame.transform.scale(LOGIN_ARROW, (200 ,100))
        screen.blit(LOGIN_ARROW,(160 ,height_arrow))


        LOGIN_USERNAME_INPUT.changeColor(PLAY_MOUSE_POS)
        LOGIN_USERNAME_INPUT.update(screen)

        LOGIN_PASSWORD_INPUT.changeColor(PLAY_MOUSE_POS)
        LOGIN_PASSWORD_INPUT.update(screen)


        ERROR_TEXT = get_font(20).render("The username and password must exceed 5 characters.", True, color_error)
        ERROR_RECT = ERROR_TEXT.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT -50))
        screen.blit(ERROR_TEXT,ERROR_RECT)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    height_arrow = 280
                    whichInput = 0
                elif event.key == pygame.K_DOWN:
                    height_arrow = 550
                    whichInput = 1

            if event.type == pygame.KEYDOWN:
                if whichInput == 0:
                    if event.key == pygame.K_BACKSPACE:
                        usernameInput = usernameInput[:-1]
                    else:
                        usernameInput += event.unicode
                elif whichInput == 1:
                    if event.key == pygame.K_BACKSPACE:
                        passwordInput = passwordInput[:-1]
                        passwordProtected = passwordProtected[:-1]
                    else:
                        if event.key != pygame.K_RETURN and event.key != pygame.K_UP and event.key != pygame.K_DOWN:
                            passwordInput += event.unicode
                            passwordProtected += '*'

                

                if event.key == pygame.K_RETURN:
                    if(len(usernameInput) < 2 or len(passwordInput) < 5) :
                        color_error = (255,255,255)
                    else:
                        AUTH = signUpOrLogin(usernameInput,passwordInput)
                        main_menu(AUTH)
                        

        pygame.display.update()

#shop screen
def shop(AUTH):
    SWORD = pygame.image.load("assets/sword.png")
    SWORD = pygame.transform.scale(SWORD, (28 ,30))
    HEART = pygame.image.load("assets/heart.png")
    HEART = pygame.transform.scale(HEART, (30 ,30))
    COINS = pygame.image.load("assets/coins.png")
    COINS = pygame.transform.scale(COINS, (30 ,30))

    characters = getOwnedCharacters(AUTH.id)
    all_characters = [1,2,3,4,5,6,7,8,9]

    damages = [10,15,15,20,20,20,30,30,30]          # 
    healths = [75,90,100,110,130,150,170,180,200]
    costs = [0,500,1000,3000,5000,7000,10000,15000,20000]

    owned_arr = characters.split(',')
    for x in range(len(owned_arr)):
        owned_arr[x] = int(owned_arr[x])
        all_characters.remove(owned_arr[x])
    owned_arr = sorted(owned_arr)
    text_error = ""

    while True :
        MOUSE_POS = pygame.mouse.get_pos()
        scaled_bg = pygame.transform.scale(BG, (SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(scaled_bg,(0,0))
        player_positions = [[300,50], [600 ,50], [900,50], [300,300], [600,300], [900,300], [300,550], [600,550], [900,550]]
        sword_positions =[[450,100],[750,100],[1050,100],[450,350],[750,350],[1050,350],[450,600],[750,600],[1050,600]]
        heart_positions =[[450,150],[750,150],[1050,150],[450,400],[750,400],[1050,400],[450,650],[750,650],[1050,650]]
        coins_positions =[[450,200],[750,200],[1050,200],[450,450],[750,450],[1050,450],[450,700],[750,700],[1050,700]]
        buttons = {}


        CHAR_SELECT_BACK = Button(image=None, pos=(80,40), 
                            text_input="<- BACK", font=get_font(30), base_color=(255,255,255), hovering_color=(240,119,0))
        CHAR_SELECT_BACK.changeColor(MOUSE_POS)
        CHAR_SELECT_BACK.update(screen)

        COINS_TEXT = get_font(35).render(str(getCharacterCoins(AUTH.id)), True, (255,255,255)) # !!!! CHANGE TO USER COINS !!!!
        screen.blit(COINS_TEXT,(110,90))
        
        COINS2 = pygame.image.load("assets/coins.png")
        COINS2 = pygame.transform.scale(COINS2, (70 ,70))
        screen.blit(COINS2,(30 ,70))

        for x in range(len(all_characters)):
            PLAYER = pygame.image.load("assets/images/shopImages/Player"+str(all_characters[x])+".png")
            PLAYER = pygame.transform.scale(PLAYER, (141,200))
            screen.blit(PLAYER,(player_positions[x][0],player_positions[x][1]))
            screen.blit(SWORD, (sword_positions[x][0], sword_positions[x][1]))
            screen.blit(HEART, (heart_positions[x][0], heart_positions[x][1]))
            screen.blit(COINS, (coins_positions[x][0], coins_positions[x][1]))
            screen.blit(get_font(30).render(str(damages[all_characters[x]-1]), True, (255,255,255)), (sword_positions[x][0] + 35, sword_positions[x][1]))
            screen.blit(get_font(30).render(str(healths[all_characters[x]-1]), True, (255,255,255)), (heart_positions[x][0] + 35, heart_positions[x][1]))
            screen.blit(get_font(30).render(str(costs[all_characters[x]-1]), True, (255,255,255)), (coins_positions[x][0] + 35, coins_positions[x][1]))
            screen.blit(get_font(30).render(text_error, True, (255,255,255)), (SCREEN_WIDTH/2 + 220, SCREEN_HEIGHT - 100))
            BUTTON_SELECT = Button(image=pygame.image.load("assets/selectButton3.png"), pos=(player_positions[x][0], player_positions[x][1]), text_input="Buy", font=get_font(25), base_color=(255, 255, 255), hovering_color=(240,119,0))
            buttons["BUTTON_SELECT_{0}".format(x)] = BUTTON_SELECT
            BUTTON_SELECT.changeColor(MOUSE_POS)
            BUTTON_SELECT.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(len(buttons)):
                    if buttons['BUTTON_SELECT_'+str(x)].checkForInput(MOUSE_POS):
                        if buyCharacter(all_characters[x],AUTH.id) == "":
                            shop(AUTH)
                        else:
                            text_error = "You do not have enough coins"
                if CHAR_SELECT_BACK.checkForInput(MOUSE_POS):
                    main_menu(AUTH) 
    
        pygame.display.update()

#highscores screen
def highscores(AUTH):
    while True:
        AllScores = getHighscores()
        HIGHSCORES_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill((0,0,0))

        HIGHSCORES_TEXT = get_font(38).render("Highscores", True, (255,255,255))
        HIGHSCORES_RECT = HIGHSCORES_TEXT.get_rect(center=(SCREEN_WIDTH/2, 100))
        screen.blit(HIGHSCORES_TEXT, HIGHSCORES_RECT)

        HIGHSCORES_BACK = Button(image=None, pos=(80,40), 
                            text_input="<- BACK", font=get_font(30), base_color=(255,255,255), hovering_color=(240,119,0))
        HIGHSCORES_BACK.changeColor(HIGHSCORES_MOUSE_POS)
        HIGHSCORES_BACK.update(screen)

        HIGHSCORES_TABLE_USER_TEXT = get_font(30).render("USER", True, (255,255,255))
        HIGHSCORES_TABLE_USER_RECT = HIGHSCORES_TABLE_USER_TEXT.get_rect(center=((SCREEN_WIDTH/2) - 200,175))
        screen.blit(HIGHSCORES_TABLE_USER_TEXT,HIGHSCORES_TABLE_USER_RECT)

        HIGHSCORES_TABLE_FLOOR_TEXT = get_font(30).render("FLOOR", True, (255,255,255))
        HIGHSCORES_TABLE_FLOOR_RECT = HIGHSCORES_TABLE_FLOOR_TEXT.get_rect(center=((SCREEN_WIDTH/2),175))
        screen.blit(HIGHSCORES_TABLE_FLOOR_TEXT,HIGHSCORES_TABLE_FLOOR_RECT)

        HIGHSCORES_TABLE_ENEMY_TEXT = get_font(30).render("ENEMY", True, (255,255,255))
        HIGHSCORES_TABLE_ENEMY_RECT = HIGHSCORES_TABLE_ENEMY_TEXT.get_rect(center=((SCREEN_WIDTH/2)+200,175))
        screen.blit(HIGHSCORES_TABLE_ENEMY_TEXT,HIGHSCORES_TABLE_ENEMY_RECT)

        pygame.draw.rect(screen, (240,240,240), pygame.Rect(SCREEN_WIDTH/2 - 300 , 200, 600,4))

        POSITION = 250

        for s in AllScores:
            HIGHSCORE_USER_SCORE = get_font(30).render(s['username'], True, (255,255,255))
            HIGHSCORES_USER_RECT = HIGHSCORE_USER_SCORE.get_rect(center=((SCREEN_WIDTH/2) - 200,POSITION))
            screen.blit(HIGHSCORE_USER_SCORE,HIGHSCORES_USER_RECT)

            HIGHSCORE_USER_SCORE = get_font(30).render(str(s['floor']), True, (255,255,255))
            HIGHSCORES_USER_RECT = HIGHSCORE_USER_SCORE.get_rect(center=((SCREEN_WIDTH/2),POSITION))
            screen.blit(HIGHSCORE_USER_SCORE,HIGHSCORES_USER_RECT)

            HIGHSCORE_USER_SCORE = get_font(30).render(str(s['enemy']), True, (255,255,255))
            HIGHSCORES_USER_RECT = HIGHSCORE_USER_SCORE.get_rect(center=((SCREEN_WIDTH/2) + 200,POSITION))
            screen.blit(HIGHSCORE_USER_SCORE,HIGHSCORES_USER_RECT)
            POSITION += 50
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HIGHSCORES_BACK.checkForInput(HIGHSCORES_MOUSE_POS):
                    main_menu(AUTH)

        pygame.display.update()

#THE GAME
def game(difficulty, AUTH, characterId):
    #sensors
    sensor = GroveUltrasonicRanger(16) # pin12, slot D12
    sensor2 = GroveUltrasonicRanger(5) 
    
    pygame.display.set_caption("FightSense")

    characters = getCharacters()
    #set framerate
    clock = pygame.time.Clock()
    FPS = 60

    #Define colors
    RED = (255,0,0)
    YELLOW = (255,165,0)
    WHITE = (255,255,255)
    BLACK = (30,30,30)
    BLUE = (30,144,255)

    #define Font
    base_font = pygame.font.Font("assets/fonts/OdibeeSans-Regular.ttf", 40)
    small_font = pygame.font.Font("assets/fonts/OdibeeSans-Regular.ttf", 30)
    count_font = pygame.font.Font("assets/fonts/OdibeeSans-Regular.ttf", 80)
    floor_font = pygame.font.Font("assets/fonts/OdibeeSans-Regular.ttf", 30)
    enemy_count_font = pygame.font.Font("assets/fonts/OdibeeSans-Regular.ttf", 30)
  

    #Define game variables
    user = getUserDetails(AUTH.id)
  
    #coins
    coins = 0
    #Counter before game starts
    intro_count = 3 

    #timer variables + coin multiplier
    last_count_update = pygame.time.get_ticks()
    last_timer_update = pygame.time.get_ticks()
    last_attack_update =  pygame.time.get_ticks()
    timer = 1
    if difficulty == "easy":
        coinMultiplier = 1
        attackTimer = 10
    elif difficulty == "normal":
        coinMultiplier = 2
        attackTimer = 8
    elif difficulty == "hard":
        coinMultiplier = 3
        attackTimer = 6

    #counters
    enemy_count = 1
    floor_count = 1

    #logical variables
    round_over = False
    game_over = False
    ROUND_OVER_COOLDOWN = 2000

    selectedCharacter = characterId - 1

    #random variables
    randomMove1 = randint(0,6)
    randomMove2 = randint(0,6)
    randomEnemyNumber = randint(0,8)
    randomBackgroundNumber = randint(0,8)
    # randomSensor = randint(0,40)
    # randomSensor2 = randint(0,40)

    #variable to check for attack
    attack1 = False
    attack2 = False
    attackEnemy = False

    #define Player Variables
    PLAYER_SIZE = [[150,150],[150,150],[200,200],[200,200],[94,91],[104,46],[162,161],[231,190],[32,32]]
    PLAYER_SCALE = [4,4,4,4,4,4,4,3,5]
    PLAYER_OFFSET = [[60,-57],[60,-56],[90,-85],[85,-82],[30,-50],[0,-5],[65,-60],[85,-85],[5,0]]
    PLAYER_HEALTH = characters[characterId-1]['health']
    PLAYER_MAX_HEALTH = characters[characterId-1]['health']
    PLAYER_DAMAGE = characters[characterId-1]['attack']
    PLAYER_DATA = [PLAYER_SIZE[selectedCharacter], PLAYER_SCALE[selectedCharacter],PLAYER_OFFSET[selectedCharacter]]

    #ENEMY variables
    ENEMY_SIZE = [[90,90],[150,150],[250,250],[120,80],[50,36],[100,100],[180,180],[155,155],[64,64],[128,127],[194,97]]
    ENEMY_NAMES = ["GuackGuack-3000", "Fire Mage", "Death Mage", "Silver Knight", "Wouter Kabouter", "The Huntress" , "Silver Lancer", "The King", "Skelly","King of Kings","Dwayne The Rock"]
    ENEMY_SCALE = [4,4,3,5,5,5,4,3,4,7,6]
    ENEMY_OFFSET = [[30,-18],[60,-60],[105,-113],[50,-48],[5,-3],[35,-35],[65,-70],[70,-60],[25,-7],[50,-50],[125,-45]]
    ENEMY_HEALTH = 100
    ENEMY_MAX_HEALTH = 100
    ENEMY_DATA = [ENEMY_SIZE[randomEnemyNumber],ENEMY_SCALE[randomEnemyNumber],ENEMY_OFFSET[randomEnemyNumber]]

    #Healing
    NORMAL_ENEMY_HEAL = 15
    BOSS_ENEMY_HEAL = 30

    #Damage by difficulty
    if difficulty == "easy":
        ENEMY_DAMAGE = 3
    elif difficulty == "normal":
        ENEMY_DAMAGE = 5
    elif difficulty == "hard":
        ENEMY_DAMAGE = 8
    #Define Bar variables
    BAR_WIDTH = 40
    BAR_HEIGHT = 20
   
    #load background image
    BACKGROUNDS = ["1.png","2.png","3.png","4.jpg","5.jpg","6.jpg","7.jpg","8.png","9.png"]
    bg_image = pygame.image.load("assets/images/background/game_backgrounds/backgroundArena_" + BACKGROUNDS[randomBackgroundNumber]).convert_alpha()

    #array enemy sprites
    ENEMY_SPRITES = ["1","2","3","4","5","6","7","8","9","10","11"]
    PLAYER_SPRITES = ["1","2","3","4","5","6","7","8","9"]

    #load spritesheets
    player_sheet = pygame.image.load("assets/images/players/Player_" + PLAYER_SPRITES[selectedCharacter] + ".png").convert_alpha()
    enemy_sheet = pygame.image.load("assets/images/enemies/Enemy_" + ENEMY_SPRITES[randomEnemyNumber] + ".png").convert_alpha()
    healing_sheet = pygame.image.load("assets/images/fx/Healing.png").convert_alpha()
    #define number of steps in each animation

       
    # [[8,4,6,4],[6,13,12,3],[6,9,10,3],[8,5,8,3],[4,4,7,3],[8,6,6,4],[10,8,7,3],[6,8,7,4],[6,10,8,5]]

    PLAYER_ANIMATION_STEPS = [[8,4,6,4],[8,5,8,3],[4,4,7,3],[8,6,6,4],[6,13,12,3],[6,9,10,3],[10,8,7,3],[6,8,7,4],[6,10,8,5]]
    ENEMY_ANIMATION_STEPS = [[9,16,8,3],[8,8,5,4],[8,8,7,3],[10,10,10,7],[4,6,7,3],[10,6,10,3],[11,7,11,4],[6,6,11,4],[4,13,13,3],[18,58,37,6],[4,8,4,6]]

    #function to draw text
    def draw_text(text,font,text_color,x,y):
        img = font.render(text,True,text_color)
        screen.blit(img , (x,y))

    #function for drawing background
    def draw_bg(bg_image):
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(scaled_bg,(0,0))

    #function for drawing fighter health bars
    def draw_health_bar(health,x,y,maxHealth):
        ratio = health / maxHealth
        health_bar_image = pygame.image.load("assets/images/background/health_bar.png").convert_alpha()
        screen.blit(health_bar_image, (x,y,500,20))
        pygame.draw.rect(screen,YELLOW, (x,y,500 * ratio,20))
        
        

    #create two instances of fighters (player and enemies)
    fighter_player = Fighter(1,250,SCREEN_HEIGHT/1.7, False,PLAYER_DATA, player_sheet,PLAYER_ANIMATION_STEPS[selectedCharacter], PLAYER_HEALTH)
    fighter_enemy = Fighter(2,950,SCREEN_HEIGHT/1.7, True,ENEMY_DATA,enemy_sheet,ENEMY_ANIMATION_STEPS[randomEnemyNumber],ENEMY_HEALTH)

    #Create bars for attacks
    bar_left = Bar(150, SCREEN_HEIGHT - 120, BAR_WIDTH, BAR_HEIGHT)
    bar_right = Bar(150, SCREEN_HEIGHT - 80, BAR_WIDTH, BAR_HEIGHT)
    bar_left_sensor = Bar(150, SCREEN_HEIGHT - 120, BAR_WIDTH, BAR_HEIGHT)
    bar_right_sensor = Bar(150, SCREEN_HEIGHT - 80, BAR_WIDTH, BAR_HEIGHT)



    #game loop
    run = True
    while run:

        GAME_MOUSE_POS = pygame.mouse.get_pos()
        #60 FPS
        clock.tick(FPS)
        #draw background

        #logic for random movement of attack bars
        if timer <= 0:
            timer = 1
            randomMove1 = randint(0,6)
            randomMove2 = randint(0,6)
            randomSensor = randint(0,10)
            randomSensor2 = randint(0,10)
        else:
            if (pygame.time.get_ticks() - last_timer_update) >= 1000:
                timer -= 1
                last_timer_update = pygame.time.get_ticks()

        #logic for enemy attack after 10 seconds
        if attackTimer <= 0:
            if difficulty == "easy":
                attackTimer = 10
            elif difficulty == "normal":    
                attackTimer = 8
            elif difficulty == "hard":
                attackTimer = 6
        else:
            if (pygame.time.get_ticks() - last_attack_update) >= 1000:
                attackTimer -= 1
                last_attack_update = pygame.time.get_ticks()
    
    
        #check if left sensor is inside the left bar
        if ((bar_left_sensor.rect.x >= (bar_left.rect.left - (bar_left_sensor.rect.width/2))) and (bar_left_sensor.rect.x <= (bar_left.rect.right + (bar_left_sensor.rect.width/2)))):
            attack1 = True
        else:
            attack1 = False

        #check if right sensor is inside the right bar
        if ((bar_right_sensor.rect.x >= bar_right.rect.left) and (bar_right_sensor.rect.x <= (bar_right.rect.right + (bar_right_sensor.rect.width/2)))):
            attack2 = True
        else:
            attack2 = False

        #if both are inside the bars --> Attack the enemy
        if attack1 == True and attack2 == True:
            attackEnemy = True
        else:
            attackEnemy = False

        #draw background and info bar
        draw_bg(bg_image)
            

        pygame.draw.rect(screen,BLACK, (0,0,SCREEN_WIDTH,50))
        

        STOP_BUTTON = Button(image=None, pos=(60,30), 
                            text_input="STOP", font=get_font(30), base_color=(255,255,255), hovering_color=(240,119,0))
        STOP_BUTTON.changeColor(GAME_MOUSE_POS)
        STOP_BUTTON.update(screen)
        draw_text("Floor " + str(floor_count),floor_font, WHITE, (SCREEN_WIDTH /2) - 40 , 10 )
        draw_text("Enemy: "+ str(enemy_count) + "/5", enemy_count_font, WHITE, (SCREEN_WIDTH - 435), 10)
        draw_text("Coins: "+ str(coins), enemy_count_font, WHITE, (SCREEN_WIDTH - 200), 10)
        
        draw_text(str(fighter_player.health) + " / " + str(PLAYER_MAX_HEALTH) ,floor_font, WHITE, 80 , 100 )
        draw_text(str(fighter_enemy.health) + " / " + str(ENEMY_MAX_HEALTH) ,floor_font, WHITE, 820 , 100 )
        #show player healthbar
        draw_health_bar(fighter_player.health, SCREEN_WIDTH/17, SCREEN_HEIGHT/10,PLAYER_MAX_HEALTH)
        draw_health_bar(fighter_enemy.health, SCREEN_WIDTH/1.7, SCREEN_HEIGHT/10, ENEMY_HEALTH)

        #update countdown
        if intro_count <= 0:
            fighter_player.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_enemy,round_over,attackEnemy,attackTimer,PLAYER_DAMAGE,ENEMY_DAMAGE)
            fighter_enemy.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_player,round_over,attackEnemy,attackTimer,PLAYER_DAMAGE,ENEMY_DAMAGE)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
            
        #msensor bars 
        bar_left.move(screen,randomMove1)
        bar_right.move(screen,randomMove2)
        #bars for sensor input (SENSOR INPUT INTO randomMoveSensor variable)
        bar_left_sensor.sensor_move(screen,sensor.get_distance()) # !!!! sensor.get_distance() on raspberry !!!!!
        bar_right_sensor.sensor_move(screen,sensor2.get_distance())

        
        #update fighters
        fighter_player.update()
        fighter_enemy.update()

        #draw fighters
        fighter_player.draw(screen)
        fighter_enemy.draw(screen)
        draw_text(ENEMY_NAMES[randomEnemyNumber], base_font, WHITE, fighter_enemy.rect.x, SCREEN_HEIGHT/2.8)
        pygame.draw.rect(screen,BLUE, (fighter_enemy.rect.x, SCREEN_HEIGHT/2.8 + 50,180 * (attackTimer/10),5))

        #draw bars 
        bar_left.draw(screen,0, (255,60,0))
        bar_right.draw(screen,40, (255,30,0))
        bar_left_sensor.drawSensor(screen, (255,255,0))
        bar_right_sensor.drawSensor(screen, (255,255,0))

        draw_text("Left",small_font,WHITE,80,663)
        draw_text("Right",small_font,WHITE,80,703)
        #check for player defeat
        if round_over == False:
            if fighter_player.alive == False:
                game_over = True
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_enemy.alive == False:
                if enemy_count == 5: # if boss enemy is defeated -> change floor 
                    if difficulty == "easy":
                        attackTimer = 10
                    elif difficulty == "normal":    
                        attackTimer = 8
                    elif difficulty == "hard":
                        attackTimer = 6
                    ENEMY_HEALTH = 100
                    ENEMY_MAX_HEALTH = 100
                    ENEMY_DAMAGE = ENEMY_DAMAGE
                    randomEnemyNumber = randint(0,8)
                    ENEMY_DATA = [ENEMY_SIZE[randomEnemyNumber],ENEMY_SCALE[randomEnemyNumber],ENEMY_OFFSET[randomEnemyNumber]]
                    coins += ((5 * floor_count)*coinMultiplier)
                    enemy_count = 1
                    if not fighter_player.health >= PLAYER_MAX_HEALTH:
                        if fighter_player.health + BOSS_ENEMY_HEAL >= PLAYER_MAX_HEALTH:
                            PLAYER_HEALTH = PLAYER_MAX_HEALTH
                        else:
                            PLAYER_HEALTH = fighter_player.health + BOSS_ENEMY_HEAL
                    if floor_count % 2:
                        randomBackgroundNumber = randint(0,8)
                        bg_image = pygame.image.load("assets/images/background/game_backgrounds/backgroundArena_" + BACKGROUNDS[randomBackgroundNumber]).convert_alpha()
                    floor_count += 1
                elif enemy_count == 4: #if enemy is 4 -> change damage, health and sprite to Boss
                    if difficulty == "easy":
                        attackTimer = 10
                    elif difficulty == "normal":    
                        attackTimer = 8
                    elif difficulty == "hard":
                        attackTimer = 6
                    randomEnemyNumber = randint(9,10)
                    ENEMY_HEALTH *= 2
                    ENEMY_MAX_HEALTH *=2
                    ENEMY_DAMAGE *= 2
                    ENEMY_DATA = [ENEMY_SIZE[randomEnemyNumber],ENEMY_SCALE[randomEnemyNumber],ENEMY_OFFSET[randomEnemyNumber]]
                    enemy_count += 1
                else:
                    if difficulty == "easy":
                        attackTimer = 10
                    elif difficulty == "normal":    
                        attackTimer = 8
                    elif difficulty == "hard":
                        attackTimer = 6
                    randomEnemyNumber = randint(0,8)
                    ENEMY_DATA = [ENEMY_SIZE[randomEnemyNumber],ENEMY_SCALE[randomEnemyNumber],ENEMY_OFFSET[randomEnemyNumber]]
                    coins += ((1 * floor_count)*coinMultiplier)
                    if not fighter_player.health >= PLAYER_MAX_HEALTH:
                        if fighter_player.health + NORMAL_ENEMY_HEAL >= PLAYER_MAX_HEALTH:
                            PLAYER_HEALTH = PLAYER_MAX_HEALTH
                        else:
                            PLAYER_HEALTH = fighter_player.health + NORMAL_ENEMY_HEAL
                    enemy_count += 1
                    
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                if game_over == True:
                    draw_text("GAME OVER",base_font, WHITE, SCREEN_WIDTH /2 , SCREEN_HEIGHT/2 )
                    addCoins(AUTH.id, coins)
                    setHighscores(user[0]['username'],floor_count,enemy_count)
                    main_menu(AUTH)
                enemy_sheet = pygame.image.load("assets/images/enemies/Enemy_" + ENEMY_SPRITES[randomEnemyNumber] + ".png").convert_alpha()
                round_over = False
                intro_count = 3    
                fighter_player = Fighter(1,250,SCREEN_HEIGHT/1.7, False,PLAYER_DATA, player_sheet,PLAYER_ANIMATION_STEPS[selectedCharacter],PLAYER_HEALTH)
                fighter_enemy = Fighter(2,950,SCREEN_HEIGHT/1.7, True,ENEMY_DATA,enemy_sheet,ENEMY_ANIMATION_STEPS[randomEnemyNumber],ENEMY_HEALTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if STOP_BUTTON.checkForInput(GAME_MOUSE_POS):
                    fighter_player.alive = False

        #update display
        pygame.display.update()


def main_menu(AUTH):
    while True:
        scaled_bg = pygame.transform.scale(BG, (SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(scaled_bg,(0,0))

        COINS_TEXT = get_font(35).render(str(getCharacterCoins(AUTH.id)), True, (255,255,255)) # !!!! CHANGE TO USER COINS !!!!
        screen.blit(COINS_TEXT,(110,70))
        
        COINS = pygame.image.load("assets/coins.png")
        COINS = pygame.transform.scale(COINS, (70 ,70))
        screen.blit(COINS,(30 ,50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("FightSense", True, (255,255,255))
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/paint_button2.png"), pos=((SCREEN_WIDTH/2) - 190 , 250), 
                            text_input="PLAY", font=get_font(75), base_color=(255, 255, 255), hovering_color=(240,119,0))
        SHOP_BUTTON = Button(image=pygame.image.load("assets/paint_button2.png"), pos=((SCREEN_WIDTH/2) + 190, 250), 
                            text_input="SHOP", font=get_font(75), base_color=(255, 255, 255), hovering_color=(240,119,0))
        HIGHSCORE_BUTTON = Button(image=pygame.image.load("assets/paint_button3.png"), pos=(SCREEN_WIDTH/2, 400), 
                            text_input="HIGHSCORES", font=get_font(75), base_color=(255, 255, 255), hovering_color=(240,119,0))
        QUIT_BUTTON = Button(image=pygame.image.load("assets/paint_button2.png"), pos=(SCREEN_WIDTH/2, 550), 
                            text_input="QUIT", font=get_font(75), base_color=(255, 255, 255), hovering_color=(240,119,0))



        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SHOP_BUTTON, HIGHSCORE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    chooseFighter(AUTH)
                if SHOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shop(AUTH)
                if HIGHSCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    highscores(AUTH)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login()

        pygame.display.update()

# game("easy")

login()