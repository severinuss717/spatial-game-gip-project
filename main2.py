import pygame as pg
import sys
import subprocess
import asyncio


# Initialize Pygame
pg.init()
screen = pg.display.set_mode((600, 400))
pg.display.set_caption("Geospatial Gaming")
icon = pg.image.load('joystick.png')
pg.display.set_icon(icon)

# Load background image
background_image = pg.image.load("op.png")  
background_image = pg.transform.scale(background_image, (600, 400))

# Colors
WHITE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fonts
font = pg.font.SysFont(None, 40)
header_font = pg.font.SysFont(None, 30)

# Text wrapping helper
def draw_wrapped_text(surface, text, font, color, rect, line_spacing=5):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= rect.width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (rect.left, y))
        y += font.get_height() + line_spacing

# Button Class
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pg.mouse.get_pos()
        color = DARK_GRAY if self.rect.collidepoint(mouse_pos) else GRAY
        pg.draw.rect(surface, color, self.rect, border_radius=8)
        text_surface = font.render(self.text, True, WHITE)
        surface.blit(text_surface, (
            self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        ))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# Button actions
def start_game():
    subprocess.Popen([sys.executable, "Start_Screen1.py"]) 
    pg.quit()
    sys.exit()

def quit_game():
    pg.quit()
    sys.exit()

#Create buttons
buttons = [
    Button("Start", 200, 200, 200, 50, start_game),
    Button("Quit", 200, 270, 200, 50, quit_game),
]

#Header text
header_text = ("Welcome to the geospatial gaming app, where you learn through gaming! "
               "Geospatial science is a broad study "
               "In this game you learn and get a basic insight of geospatial science "
               "Where you interact with icons that relates to geospatial science "
               "This icons will give basic information needed to complete a quisz at the end of every level "
               "You may start your journey of learning through gaming. ")

#Main loop
running = True
while running:
    screen.blit(background_image, (0, 0)) 

    draw_wrapped_text(screen, header_text, header_font, WHITE, pg.Rect(20, 20, 560, 100))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    for button in buttons:
        button.draw(screen)

    pg.display.flip()

pg.quit()
