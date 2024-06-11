import os           # Import the os module to use relative paths to link our files
import pygame       # Import pygame to program our game menu
import time         # Import time to control the speed of our character animation
import subprocess   # Import subprocess to run a new script from this menu
import sys          # Import sys to access passed arguments
import sqlite3

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
        self.vel = 8
        self.isJump = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.jumpCount = 5
        self.standing = True
        self.direction = None # New attribute for keeping track of the last direction
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
    NoticeBoard(385, 382, "basics", notice_board_sprite, single_notice_sprite1),
    NoticeBoard(900, 382, "logical-operators", notice_board_sprite, single_notice_sprite2),
    NoticeBoard(1375, 311, "encryption", notice_board_sprite, single_notice_sprite3),
    NoticeBoard(480, 864, "decorators", notice_board_sprite, single_notice_sprite4),
    NoticeBoard(925, 760, "recursive-functions", notice_board_sprite, single_notice_sprite5)
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

        # Check if the character is overlapping with the board
        if (char_center >= board_left and char_center <= board_right and
            char_bottom_side >= board_top and char_top_side <= board_bottom):
            return board

    return None


def char_facing_exit():
    '''Check if the character is facing one of the exit roads'''
    # Calculate the coordinates of the exit zones
    exit_1 = (126, 0, 330, 0)
    exit_2 = (408, 990, 749, 1000)
    # Check if the character is within either exit_1 or exit_2
    if (char_center >= exit_1[0] and char_center <= exit_1[2] and (char_top_side - 38) <= exit_1[3]):
        return "top_exit"
    if (char_center >= exit_2[0] and char_center <= exit_2[2] and char_bottom_side >= exit_2[1]):
        return "bottom_exit"
    return None


def text_box(message, x, y):
    '''Create a text box giving instructions to user, here to press SPACE to start the challenge'''
    font = pygame.font.Font("level-menu-img/Berenika-Bold.ttf", 20)  # Set the font and size
    lines = message.split('\n')  # Split message into lines
    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]  # Render each line
    max_width = max(text_surface.get_width() for text_surface in text_surfaces)  # Find the max width
    total_height = sum(text_surface.get_height() for text_surface in text_surfaces)  # Find the total height

    # Set the position of the text box with a margin
    txtbx_margin = 12
    x = max(min(x, win.get_width() - max_width - txtbx_margin), txtbx_margin)
    y = max(min(y, win.get_height() - total_height - txtbx_margin), txtbx_margin)

    # Draw the rectangle background for the text box
    pygame.draw.rect(win, (40, 40, 40), (x - txtbx_margin, y - txtbx_margin, max_width + txtbx_margin * 2, total_height + txtbx_margin * 2))

    # Blit each line of text onto the screen
    offset_y = y
    for text_surface in text_surfaces:
        win.blit(text_surface, (x, offset_y))
        offset_y += text_surface.get_height()

def get_highscores(db_name):
    '''Fetch high scores from the specified database and return as a formatted string'''
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT username, highscore FROM highscore ORDER BY highscore DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        highscore_text = "\nHighscores:\n"
        for row in rows:
            highscore_text += f"{row[0]}: {row[1]}\n"
        return highscore_text
    except Exception as e:
        return f"\nError fetching highscores: {e}"

def redrawGameWindow():
    '''Draw the game window with all the elements on it'''
    win.blit(bg, (0, 0))  # Draw the background    
    for board in notice_boards:  # Draw each notice board
        board.draw(win)
    
    # Display a message if the character is facing a notice board
    board = char_facing_board()
    if board is not None:
        if board.level == "basics":
            highscores = get_highscores("highscore_basics.db")
            text_box(f'Press SPACE to start Level 1!\nComplete the first challenge.{highscores}', board.x + 125, board.y)
        elif board.level == "logical-operators":
            highscores = get_highscores("highscore_logical-operators.db")
            text_box(f'Press SPACE to start Level 2!\nGet ready for logical operators.{highscores}', board.x + 125, board.y)
        elif board.level == "encryption":
            highscores = get_highscores("highscore_encryption.db")
            text_box(f'Press SPACE to start Level 3!\nEncryption awaits you.{highscores}', board.x - 340, board.y)
        elif board.level == "decorators":
            highscores = get_highscores("highscore_decorators.db")
            text_box(f'Press SPACE to learn about Decorators!\nUnderstand the concept of decorators in Python.{highscores}', board.x + 125, board.y)
        elif board.level == "recursive-functions":
            highscores = get_highscores("highscore_recursive-functions.db")
            text_box(f'Press SPACE to learn about Recursive Functions!\nDive into recursive functions.{highscores}', board.x - 540, board.y)
        else:
            text_box('Press SPACE to start this challenge', board.x + 125, board.y)
    facing_exit = char_facing_exit()
    if facing_exit == "top_exit":
        text_box('Press SPACE to exit the program', 240, 100)
    if facing_exit == "bottom_exit":
        text_box('Press SPACE to exit the program', 800, 892)

    character.draw(win)  # Draw the character
    pygame.display.update()  # Update the display



#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
character = player(676, 470, 48, 60)     # Starting position and size of player
run = True                               # Initialize the 'run' variable to True to keep the game running
while run:
    clock.tick(27)                      # Set the frame rate of the game. Should be a multiple of 9
    
    for event in pygame.event.get():    # Check for events
        if event.type == pygame.QUIT:   # Check if the user wants to quit the game
            run = False    

    # Calculate the coordinates of the corners of the character
    char_left_side = character.x
    char_right_side = character.x + character.width
    char_center = character.x + character.width/2
    char_top_side = character.y + 38
    char_bottom_side = character.y + character.height

    keys = pygame.key.get_pressed()     # Get the keys that are pressed

    # Calculate the player's new position
    new_x = character.x
    new_y = character.y
    # Check if the left key is pressed and the player is not at the left edge of the screen
    if keys[pygame.K_LEFT] and character.x > character.vel:
        new_x -= character.vel                              # Subtract the character's velocity from its current x position to move it to the left
        character.left = True                               # Set the character's 'left' attribute to True to indicate it's moving left
        character.right = False
        character.standing = False
    # Check if the right key is pressed and the player is not at the right edge of the screen
    elif keys[pygame.K_RIGHT] and character.x < 1536 - character.width - character.vel:
        new_x += character.vel
        character.right = True
        character.left = False
        character.standing = False
    # Check if the right key is pressed and the player is not at the right edge of the screen
    else:
        character.left = False
        character.right = False

    # Check if the up key is pressed and the player is not at the top edge of the screen
    if keys[pygame.K_UP] and character.y > 0:
        new_y -= character.vel
        character.up = True
        character.down = False
        character.standing = False
    # Check if the down key is pressed and the player is not at the bottom edge of the screen
    elif keys[pygame.K_DOWN] and character.y + character.height + character.vel < 1000:
        new_y += character.vel
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
            if board is not None:           # If character is facing a board
                # Run a new Python script
                subprocess.Popen(["python3", "quizz_app.py" , username, board.level])    # Open the quiz script with the selected level in a new window
                time.sleep(0.3)
                pygame.quit()       # Close current window
                run = False         # Stop the game loop

            facing_exit = char_facing_exit()    # get whether the character is facing one of the game exits
            if facing_exit != None: # If yes
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

    if run:        
        redrawGameWindow()      # Redraw the game window = update the screen at every frame