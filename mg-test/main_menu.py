import os       # Import the os module to use relative paths to link our files
import pygame   # Import pygame to program our game menu

sourceFileDir = os.path.dirname(os.path.abspath(__file__)) # changes the current working directory of the Python script to the directory where the script is located
os.chdir(sourceFileDir)

pygame.init()

win = pygame.display.set_mode((1280,1000))

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

characters = SpriteSheet('characters.png')

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
bg = pygame.image.load('bg.png')
# Get the current size of the image
bg_width, bg_height = bg.get_size()
# Halve the size of the image
char = sprites[24]

clock = pygame.time.Clock()

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

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
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.velY = 2  # New variable for vertical velocity
        self.frameCounter = 0  # New variable for frame counter
        self.defaultSprite = char # Default sprite for player
        self.rect = pygame.Rect(x, y, width, height)  # create and assign a rect object to player

    def draw(self, win):
        self.frameCounter += 1  # Increment frame counter in every frame
        self.rect.topleft = (self.x, self.y)  # Update the rect position

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount % len(walkLeft)], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount % len(walkRight)], (self.x,self.y))
                self.walkCount += 1

            if self.walkCount >= len(walkLeft):  # Reset walkCount when it reaches the end of the list
                self.walkCount = 0
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(self.defaultSprite, (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

class House(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

# Create some houses
houses = [
    House(387, 66, 616, 243), # We add 9px to starting x and substract 18px to rectangle width to make it look good with player sprite
    House(537, 359, 318, 49)        # We substract 48px from height to show player except feet in front of it at the bottom
]

def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)

    # Draw the player's rectangle for debugging
    pygame.draw.rect(win, (255, 0, 0), (man.x, man.y, man.width, man.height), 1)
    
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(576, 470, 48, 60)          # Starting position and size of player
shootLoop = 0
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Calculate the player's new position
    new_x = man.x
    new_y = man.y
    if keys[pygame.K_LEFT] and man.x > man.vel:
        new_x -= man.vel
    elif keys[pygame.K_RIGHT] and man.x < 1280 - man.width - man.vel:
        new_x += man.vel
    if keys[pygame.K_UP] and man.y > man.velY:
        new_y -= man.velY
    elif keys[pygame.K_DOWN] and man.y + man.height + man.velY < 1000:
        new_y += man.velY

    # Check if the new position would collide with a house
    player_rect = pygame.Rect(new_x, new_y, man.width, man.height)
    if not any(player_rect.colliderect(house.rect) for house in houses):
        # If not colliding with any house, update the player's position
        man.x = new_x
        man.y = new_y

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 1280 - man.width - man.vel:
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not(man.standing):
        man.walkCount += 1
            
    redrawGameWindow()

pygame.quit()