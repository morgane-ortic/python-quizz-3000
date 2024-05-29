import os           
import pygame       
import time         
import subprocess   
import sys          

start_frame = time.time()   
noi = 3                     
frames_per_second = 9       
space_pressed = False       

try:
    username = sys.argv[1]  
except IndexError:
    username = "Guest"      

print(f"Current user is {username}")


sourceFileDir = os.path.dirname(os.path.abspath(__file__)) 
os.chdir(sourceFileDir)

pygame.init()

win = pygame.display.set_mode((1536,1000))

pygame.display.set_caption("First Game")

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width * 3, height * 3))  
        return image

characters = SpriteSheet('level-menu-img/characters.png')

sprite_width = 16
sprite_height = 20
sprites = []

for k in range(3):  
    for j in range(4):  
        for i in range(3):  
            x = (i + k*3) * sprite_width
            y = j * sprite_height
            print(f"Getting sprite at x={x}, y={y}")
            image = characters.get_image(x, y, sprite_width, sprite_height)
            sprites.append(image)

walkRight = [sprites[i] for i in range(30, 33)]
walkLeft = [sprites[i] for i in range(27, 30)]
walkUp = [sprites[i] for i in range(33, 36)]
walkDown = [sprites[i] for i in range(24, 27)]
bg = pygame.image.load('level-menu-img/bg.png')    
notice_board_sprite = pygame.image.load('level-menu-img/notice-board.png')    
single_notice_sprite1 = pygame.image.load('level-menu-img/single_notice1.png')    
single_notice_sprite2 = pygame.image.load('level-menu-img/single_notice2.png')    
single_notice_sprite3 = pygame.image.load('level-menu-img/single_notice3.png')
single_notice_sprite4 = pygame.image.load('level-menu-img/single_notice4.png')
single_notice_sprite5 = pygame.image.load('level-menu-img/single_notice5.png')   

char = sprites[24]

clock = pygame.time.Clock()




score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.jumpCount = 5
        self.standing = True
        self.direction = None 
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.velY = 5  
        self.frameCounter = 0  
        self.defaultSprite = char 
        self.rect = pygame.Rect(x, y, width, height)  

    def draw(self, win):
        self.frameCounter += 1  
        self.rect.topleft = (self.x, self.y)  

        self.walkCount = int((time.time() - start_frame) * frames_per_second % noi) 

        direction_map = {'left': walkLeft, 'right': walkRight, 'up': walkUp, 'down': walkDown}
        
        if self.up:
            self.direction = 'up'
        elif self.down:
            self.direction = 'down'
        elif self.left:
            self.direction = 'left'
        elif self.right:
            self.direction = 'right'

        if not self.standing and self.direction:
            win.blit(direction_map[self.direction][self.walkCount], (self.x, self.y))
        else:
            if self.direction:
                win.blit(direction_map[self.direction][0], (self.x, self.y))
            else:
                win.blit(self.defaultSprite, (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

class House(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


houses = [                 
    
    House(380, 66, 629, 291),
    House(531, 359, 331, 97),

    
    House(234, 551, 346, 243),
    House(234, 841, 194, 79),
    House(484, 841, 96, 79),
    House(234, 794, 14, 48),
    House(521, 794, 59, 48),
    House(252, 758, 171, 47),

    
    House(1150, 286, 142, 167),

    
    House(770, 575, 238, 217),
    House(926, 792, 82, 30),

    
    House(1008, 312, 141, 41),
]

class NoticeBoard(object):
    def __init__(self, x, y, level, board_sprite, notice_sprite, file_to_run):
        self.x = x
        self.y = y
        self.level = level
        self.board_sprite = board_sprite
        self.single_notice_sprite = notice_sprite
        self.file_to_run = file_to_run

    def draw(self, win):
        win.blit(self.board_sprite, (self.x, self.y))
        win.blit(self.single_notice_sprite, (self.x, self.y))


notice_boards = [
    NoticeBoard(385, 382, "lvl1", notice_board_sprite, single_notice_sprite1, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(900, 382, "lvl2", notice_board_sprite, single_notice_sprite2, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(1375, 311, "lvl3", notice_board_sprite, single_notice_sprite3, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(480, 864, "lvl4", notice_board_sprite, single_notice_sprite4, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(925, 760, "lvl5", notice_board_sprite, single_notice_sprite5, ".level-menu-img/quizz-mg.py")
]

notice_board_positions = [(board.x, board.y) for board in notice_boards]


for pos in notice_board_positions:
    houses.append(House(pos[0], pos[1], notice_board_sprite.get_width(), notice_board_sprite.get_height()))

def redrawGameWindow():
    win.blit(bg, (0,0))                         
    for board in notice_boards:                 
        board.draw(win)
    character.draw(win)                         

    
    

    pygame.display.update()



font = pygame.font.SysFont('comicsans', 30, True)
character = player(676, 470, 48, 60)          
shootLoop = 0
run = True
while run:
    clock.tick(30)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    
    new_x = character.x
    new_y = character.y
    if keys[pygame.K_LEFT] and character.x > character.vel:
        new_x -= character.vel
    elif keys[pygame.K_RIGHT] and character.x < 1536 - character.width - character.vel:
        new_x += character.vel
    if keys[pygame.K_UP] and character.y > character.velY:
        new_y -= character.velY
    elif keys[pygame.K_DOWN] and character.y + character.height + character.velY < 1000:
        new_y += character.velY

    
    player_rect = pygame.Rect(new_x, new_y + 42, character.width, character.height - 42)
    if not any(player_rect.colliderect(house.rect) for house in houses):
        
        character.x = new_x
        character.y = new_y
    


    if keys[pygame.K_LEFT] and character.x > character.vel:
        character.left = True
        character.right = False
        character.standing = False
    else:
        character.left = False

    if keys[pygame.K_RIGHT] and character.x < 1536 - character.width - character.vel:
        character.right = True
        character.left = False
        character.standing = False
    else:
        character.right = False

    if keys[pygame.K_UP] and character.y > character.velY:
        character.up = True
        character.down = False
        character.standing = False
    else:
        character.up = False

    if keys[pygame.K_DOWN] and character.y + character.height + character.velY < 1000:
        character.down = True
        character.up = False
        character.standing = False
    else:
        character.down = False

        
    if keys[pygame.K_SPACE]:

        space_pressed = True  # Set space_pressed to True when the space key is pressed

        if not space_pressed:       
            for board in notice_boards:
                
                board_left = board.x
                board_right = board.x + 113
                board_top = board.y
                board_bottom = board.y + 71

                
                character_left = character.x
                character_right = character.x + character.width
                character_center = character.x + character.width/2
                character_top = character.y + 38
                character_bottom = character.y + character.height

                
                if (character_center >= board_left and character_center <= board_right and
                    character_bottom >= board_top and character_top <= board_bottom):
                    
                    subprocess.Popen(["python3", "sunny_customtk_2.py" , username, board.level])

            space_pressed = True  
        else:
            space_pressed = False  

    if not character.left and not character.right and not character.up and not character.down:
        character.standing = True
        character.walkCount = 0

    if not(character.standing):
        character.walkCount += 1
            
    redrawGameWindow()

pygame.quit()