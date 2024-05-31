import os           # Import the os module to use relative paths to link our files
import pygame       # Import pygame to program our game menu
import time         # Import time to control the speed of our character animation
import subprocess   # Import subprocess to run a new script from this menu
import sys          # Import sys to access passed arguments

start_frame = time.time()   # get the current time when we start the program in order to calculate frame index for sprite animations
anim_noi = 3                # number of images for each of our animations
anim_fps = 9                # frames per second of animation. Should be a multiple of 3
space_pressed = False       # sets that space key is not pressed = it will wait for user to press it to perform corresponding code

try:
    username = sys.argv[1]  # Import username from the arguments passed from login file
except IndexError:
    username = "Guest"      # Defines username as "Guest" in case it has not been passed


sourceFileDir = os.path.dirname(os.path.abspath(__file__)) # changes the current working directory of the Python script to the directory where the script is located
os.chdir(sourceFileDir)

pygame.init()   # Initialize pygame

win = pygame.display.set_mode((1536,1000))  # Set the window size

pygame.display.set_caption("Python Quest")    # Set the window title

class SpriteSheet:
    '''Create class to extract images from sprite sheet'''
    def __init__(self, filename):
        '''Initialize the sprite sheet object with the provided file name'''
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width * 3, height * 3))  # Scale if needed
        return image

# Load the sprite sheet and divide it to extract individual character sprites
characters = SpriteSheet('level-menu-img/characters.png')
sprite_width = 16
sprite_height = 20
sprites = []    # Create list to store all the character sprites

for k in range(3):  # For each section
    for j in range(4):  # For each row
        for i in range(3):  # For each column
            x = (i + k*3) * sprite_width
            y = j * sprite_height
            print(f"Getting sprite at x={x}, y={y}")
            image = characters.get_image(x, y, sprite_width, sprite_height)
            sprites.append(image)   # Add the sprite to the list

# Define the animations = which sprites to use for each direction
walkRight = [sprites[i] for i in range(30, 33)]
walkLeft = [sprites[i] for i in range(27, 30)]
walkUp = [sprites[i] for i in range(33, 36)]
walkDown = [sprites[i] for i in range(24, 27)]
bg = pygame.image.load('level-menu-img/bg.png')    # import background image
notice_board_sprite = pygame.image.load('level-menu-img/notice-board.png')          # import notice board image
single_notice_sprite1 = pygame.image.load('level-menu-img/single_notice1.png')      # import notice images with each level name
single_notice_sprite2 = pygame.image.load('level-menu-img/single_notice2.png')    
single_notice_sprite3 = pygame.image.load('level-menu-img/single_notice3.png')
single_notice_sprite4 = pygame.image.load('level-menu-img/single_notice4.png')
single_notice_sprite5 = pygame.image.load('level-menu-img/single_notice5.png')   

char = sprites[24]

clock = pygame.time.Clock()

# music = pygame.mixer.music.load('music.mp3')
# pygame.mixer.music.play(-1)

class player(object):
    '''Create a player class to represent the character in the game'''
    def __init__(self,x,y,width,height):
        '''Initialize the player object with its attributes'''
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
        '''Draw the player on the screen'''
        self.frameCounter += 1      # Increment frame counter in every frame
        self.rect.topleft = (self.x, self.y)    # Update the rect position
        self.walkCount = int((time.time() - start_frame) * anim_fps % anim_noi)     # Calculate the frame index for animations

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
    '''Create a house class to represent the buildings and obstacles in the game'''
    def __init__(self, x, y, width, height):
        '''Initialize the house object with its attributes'''
        self.rect = pygame.Rect(x, y, width, height)    # Create a rect object for the house to deal with collisions

# Create some houses
houses = [                 
    # Inn
    House(380, 66, 629, 291),   # Create a house object with it coordinates on the screen and its size
    House(531, 359, 331, 97),   # Numbers are, starting from top-left corner: x, y, width, height

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
    '''Create a notice board class to represent the notice boards in the game'''
    def __init__(self, x, y, level, board_sprite, notice_sprite):
        '''Initialize the notice board object with its attributes'''
        self.x = x
        self.y = y
        self.level = level
        self.board_sprite = board_sprite
        self.single_notice_sprite = notice_sprite

    def draw(self, win):
        '''Draw the notice board on the screen'''
        win.blit(self.board_sprite, (self.x, self.y))
        win.blit(self.single_notice_sprite, (self.x, self.y))


# Add notice boards
notice_boards = [
    NoticeBoard(385, 382, "lvl1", notice_board_sprite, single_notice_sprite1),
    NoticeBoard(900, 382, "lvl2", notice_board_sprite, single_notice_sprite2),
    NoticeBoard(1375, 311, "lvl3", notice_board_sprite, single_notice_sprite3),
    NoticeBoard(480, 864, "lvl4", notice_board_sprite, single_notice_sprite4),
    NoticeBoard(925, 760, "lvl5", notice_board_sprite, single_notice_sprite5)
]

notice_board_positions = [(board.x, board.y) for board in notice_boards]    # Get the positions of each notice board

# Add rect. for collision to notice boards
for pos in notice_board_positions:
    houses.append(House(pos[0], pos[1], notice_board_sprite.get_width(), notice_board_sprite.get_height()))

def char_facing_board():
    '''Check if the character is facing a notice board'''
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
            return board

    return None


def text_box(message, x, y):
    '''Create a text box giving instructions to user, here to press SPACE to start the challenge'''
    font = pygame.font.Font("level-menu-img/Berenika-Bold.ttf", 20)           # Set the font and size
    text = font.render(message, 1, (255,255,255))     # Create the text
    text_rect = text.get_rect(center=(x, y))    # Set the position of the text

    # Ensure the text box is within the window boundaries + add a margin between text box and window edge
    txtbx_margin = 12
    text_rect.x = max(min(text_rect.x, win.get_width() - text_rect.width - txtbx_margin), txtbx_margin)
    text_rect.y = max(min(text_rect.y, win.get_height() - text_rect.height - txtbx_margin), txtbx_margin)

    pygame.draw.rect(win, (40, 40, 40), text_rect.inflate(12, 12))   # Draw a rectangle around the text
    win.blit(text, text_rect)                   # Display the text on the screen



def redrawGameWindow():
    '''Draw the game window with all the elements on it'''
    win.blit(bg, (0,0))                         # Draw the background    
    for board in notice_boards:                 # Draw each notice board
        board.draw(win)
    # Display a message if the character is facing a notice board
    board = char_facing_board()
    if board is not None:
        text_box('Press SPACE to start this challenge', board.x + 56, board.y - 25)

    character.draw(win)                         # Draw the character

    # Draw the player's rectangle for debugging
    # pygame.draw.rect(win, (255, 0, 0), (character.x, character.y, character.width, character.height), 1)

    pygame.display.update()                    # Update the display


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
character = player(676, 470, 48, 60)     # Starting position and size of player
run = True                               # Initialize the 'run' variable to True to keep the game running
while run:
    clock.tick(27)                      # Set the frame rate of the game. Should be a multiple of 9
    
    for event in pygame.event.get():    # Check for events
        if event.type == pygame.QUIT:   # Check if the user wants to quit the game
            run = False

    keys = pygame.key.get_pressed()     # Get the keys that are pressed

    # Calculate the player's new position
    new_x = character.x
    new_y = character.y
    # Check if the left key is pressed and the player is not at the left edge of the screen
    if keys[pygame.K_LEFT] and character.x > character.vel:
        new_x -= character.vel  # Update the new x position
        character.left = True   
        character.right = False
        character.standing = False
    # Check if the right key is pressed and the player is not at the right edge of the screen
    elif keys[pygame.K_RIGHT] and character.x < 1536 - character.width - character.vel:
        new_x += character.vel
        character.right = True
        character.left = False
        character.standing = False
    else:
        character.left = False
        character.right = False

    # Check if the up key is pressed and the player is not at the top edge of the screen
    if keys[pygame.K_UP] and character.y > character.velY:
        new_y -= character.velY
        character.up = True
        character.down = False
        character.standing = False
    # Check if the down key is pressed and the player is not at the bottom edge of the screen
    elif keys[pygame.K_DOWN] and character.y + character.height + character.velY < 1000:
        new_y += character.velY
        character.down = True
        character.up = False
        character.standing = False
    else:
        character.up = False
        character.down = False

    # Check if the new position would collide with a house
    player_rect = pygame.Rect(new_x, new_y + 42, character.width, character.height - 42)
    if not any(player_rect.colliderect(house.rect) for house in houses):
        # If not colliding with any house, update the player's position
        character.x = new_x
        character.y = new_y

    # Check if the space key is pressed
    if keys[pygame.K_SPACE]:

        if not space_pressed:               # Run this code only if space key is not alread pressed = only once per press
            board = char_facing_board()     # Get the board that the character is facing
            if board is not None:
                # Run a new Python script
                subprocess.Popen(["python3", "quizz_app.py" , username, board.level])    # Open the quiz script with the selected level in a new window
                time.sleep(0.3)
                pygame.quit()       # Close current window
                run = False         # Stop the game loop

            space_pressed = True    # Set the flag to True when space is pressed
            time.sleep(0.2)         # Add a small delay to prevent multiple script executions on a single space key press
        elif space_pressed:         # Check if the space key is released
            space_pressed = False   # Reset the flag when space is released

    if not character.left and not character.right and not character.up and not character.down:  # Define when character is standing
        character.standing = True
        character.walkCount = 0

    if not(character.standing):     # Define when character is walking
        character.walkCount += 1    # Increment the walk count
            
    redrawGameWindow()      # Redraw the game window = update the screen at every frame