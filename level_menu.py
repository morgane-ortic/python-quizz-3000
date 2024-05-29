import os           # Import the os module to use relative paths to link our files
import pygame       # Import pygame to program our game menu
import time         # Import time to control the speed of our character animation
import subprocess   # Import subprocess to run a new script from this menu
import sys          # Import sys to access passed arguments

start_frame = time.time()   # get the current time when we start the program in order to calculate frame index for sprite animations
noi = 3                     # number of images for each of our animations
frames_per_second = 9       # frames per second of animation
space_pressed = False       # sets that space key is not pressed = it will wait for user to press it to perform corresponding code

try:
    username = sys.argv[1]  # Import username from the arguments passed from login file
except IndexError:
    username = "Guest"      # Defines username as "Guest" in case it has not been passed

print(f"Current user is {username}")


sourceFileDir = os.path.dirname(os.path.abspath(__file__)) # changes the current working directory of the Python script to the directory where the script is located
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
        image = pygame.transform.scale(image, (width * 3, height * 3))  # Scale if needed
        return image

characters = SpriteSheet('level-menu-img/characters.png')

sprite_width = 16
sprite_height = 20
sprites = []

for k in range(3):  # For each section
    for j in range(4):  # For each row
        for i in range(3):  # For each column
            x = (i + k*3) * sprite_width
            y = j * sprite_height
            print(f"Getting sprite at x={x}, y={y}")
            image = characters.get_image(x, y, sprite_width, sprite_height)
            sprites.append(image)

walkRight = [sprites[i] for i in range(30, 33)]
walkLeft = [sprites[i] for i in range(27, 30)]
walkUp = [sprites[i] for i in range(33, 36)]
walkDown = [sprites[i] for i in range(24, 27)]
bg = pygame.image.load('level-menu-img/bg.png')    # import background image
notice_board_sprite = pygame.image.load('level-menu-img/notice-board.png')    # import notice board image
single_notice_sprite1 = pygame.image.load('level-menu-img/single_notice1.png')    # import single_notice images
single_notice_sprite2 = pygame.image.load('level-menu-img/single_notice2.png')    
single_notice_sprite3 = pygame.image.load('level-menu-img/single_notice3.png')
single_notice_sprite4 = pygame.image.load('level-menu-img/single_notice4.png')
single_notice_sprite5 = pygame.image.load('level-menu-img/single_notice5.png')   

char = sprites[24]

clock = pygame.time.Clock()

# music = pygame.mixer.music.load('music.mp3')
# pygame.mixer.music.play(-1)

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
        self.direction = None # New attribute for keeping track of the last direction
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.velY = 5  # New variable for vertical velocity
        self.frameCounter = 0  # New variable for frame counter
        self.defaultSprite = char # Default sprite for player
        self.rect = pygame.Rect(x, y, width, height)  # create and assign a rect object to player

    def draw(self, win):
        self.frameCounter += 1  # Increment frame counter in every frame
        self.rect.topleft = (self.x, self.y)  # Update the rect position

        self.walkCount = int((time.time() - start_frame) * frames_per_second % noi) # Calculate the frame index for animations

        direction_map = {'left': walkLeft, 'right': walkRight, 'up': walkUp, 'down': walkDown}
        # Determine the direction
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

# Create some houses
houses = [                 
    # Inn
    House(380, 66, 629, 291),
    House(531, 359, 331, 97),

    # shop
    House(234, 551, 346, 243),
    House(234, 841, 194, 79),
    House(484, 841, 96, 79),
    House(234, 794, 14, 48),
    House(521, 794, 59, 48),
    House(252, 758, 171, 47),

    # stables
    House(1150, 286, 142, 167),

    # small house
    House(770, 575, 238, 217),
    House(926, 792, 82, 30),

    # fence
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

# Add 
notice_boards = [
    NoticeBoard(385, 382, "lvl1", notice_board_sprite, single_notice_sprite1, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(900, 382, "lvl2", notice_board_sprite, single_notice_sprite2, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(1375, 311, "lvl3", notice_board_sprite, single_notice_sprite3, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(480, 864, "lvl4", notice_board_sprite, single_notice_sprite4, ".level-menu-img/quizz-mg.py"),
    NoticeBoard(925, 760, "lvl5", notice_board_sprite, single_notice_sprite5, ".level-menu-img/quizz-mg.py")
]

notice_board_positions = [(board.x, board.y) for board in notice_boards]

# Add rect. for collision to notice boards
for pos in notice_board_positions:
    houses.append(House(pos[0], pos[1], notice_board_sprite.get_width(), notice_board_sprite.get_height()))

def redrawGameWindow():
    win.blit(bg, (0,0))                         # Draw the background    
    for board in notice_boards:                 # Draw each notice board
        board.draw(win)
    character.draw(win)                         # Draw the character

    # Draw the player's rectangle for debugging
    # pygame.draw.rect(win, (255, 0, 0), (character.x, character.y, character.width, character.height), 1)

    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
character = player(676, 470, 48, 60)          # Starting position and size of player
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

    # Calculate the player's new position
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

    # Check if the new position would collide with a house
    player_rect = pygame.Rect(new_x, new_y + 42, character.width, character.height - 42)
    if not any(player_rect.colliderect(house.rect) for house in houses):
        # If not colliding with any house, update the player's position
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

        # Check if the space key is pressed
    if keys[pygame.K_SPACE]:

        if not space_pressed:       # Run this code only if space key is not alread pressed = only once per press
            for board in notice_boards:
                # Calculate the coordinates of the corners of the board
                board_left = board.x
                board_right = board.x + 113
                board_top = board.y
                board_bottom = board.y + 71

                # Calculate the coordinates of the corners of the character
                character_left = character.x
                character_right = character.x + character.width
                character_center = character.x + character.width/2
                character_top = character.y + 38
                character_bottom = character.y + character.height

                # Check if the character is overlapping with the board
                if (character_center >= board_left and character_center <= board_right and
                    character_bottom >= board_top and character_top <= board_bottom):
                    # Run a new Python script
                    subprocess.Popen(["python3", "sunny_customtk_2.py" , username, board.level])

            space_pressed = True  # Set the flag to True when space is pressed
        else:
            space_pressed = False  # Reset the flag when space is released

    if not character.left and not character.right and not character.up and not character.down:
        character.standing = True
        character.walkCount = 0

    if not(character.standing):
        character.walkCount += 1
            
    redrawGameWindow()

pygame.quit()