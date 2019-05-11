import os
import pygame
pygame.init()

Screen_Size = display_width, display_height = 720, 480
BACKGROUND_COLOR = pygame.Color('black')
FPS = 60

gameDisplay = pygame.display.set_mode(Screen_Size)
clock = pygame.time.Clock()


def load_images(path):
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images, center):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()


        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.

        self.image_rect = self.image.get_rect()
        size = (self.image_rect[2], self.image_rect[3])  # This should match the size of the images.

        if center == True:
            position = (x-self.image_rect[2]/2, y-self.image_rect[3]/2)
        self.rect = pygame.Rect(position, size)
        
        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self, dt):
        """
        This is the method that's being called when 'all_sprites.update(dt)' is called.
        """
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
        # self.update_frame_dependent()
        
    def button_image(x, y, event, action=None):
        """
        Calls the function Selection when clicking oh the image
        """
        mouse = pygame.mouse.get_pos()  
        button = player.image.convert()
        button_rect = button.get_rect(topleft=(x,y))

        if player.rect.collidepoint(mouse):
            gameDisplay.blit(player.image, player.rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if action != None:
                    action()
                    
def Animated_Sprite(Sprite_Path, x, y, center, action):
    global player
    images = load_images(path=Sprite_Path)  # Make sure to provide the relative or full path to the images directory.
    player = AnimatedSprite(position=(x, y), images=images, center=center)
    all_sprites = pygame.sprite.Group(player)  # Creates a sprite group and adds 'player' to it.
    running = True
    while running:

        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Button
            if callable(action) == True:    # Check if action is an Function
                AnimatedSprite.button_image(x, y, event, action)
            
        all_sprites.update(dt)  # Calls the 'update' method on all sprites in the list (currently just the player).

        all_sprites.draw(gameDisplay)
        pygame.display.update()
        yield

# Debug
def Action_Test():
    print("Click!")

def Test():
    for _ in Animated_Sprite(Sprite_Path, x, y, True, Action_Test):
        gameDisplay.fill(BACKGROUND_COLOR)
        print('Loop 1')

Sprite_Path = "Data\Sprite_Button\Sprite_Button_Traning"
x = display_width/2
y = display_height/2

if __name__ == '__main__':
    Test()
