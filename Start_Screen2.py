import pygame as pg
import sys
import subprocess

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((600, 400))
pg.display.set_caption("LEVEL 1")
icon = pg.image.load('joystick.png')
pg.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 215)

#Fonts
font = pg.font.SysFont(None, 40)
header_font = pg.font.SysFont(None, 30) 

#Text wrapping 
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

#Button Class
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.color = GRAY
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pg.mouse.get_pos()
        self.color = DARK_GRAY if self.rect.collidepoint(mouse_pos) else GRAY
        pg.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        surface.blit(text_surface, (
            self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        ))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

#Button actions
def start_game():
    subprocess.Popen([sys.executable, "level_2.py"]) 

def open_options():
    print("Opening options...")

def quit_game():
    pg.quit()
    sys.exit()

#Create buttons
buttons = [
    Button("Start", 200, 150, 200, 50, start_game),
    Button("Options", 200, 220, 200, 50, open_options),
    Button("Quit", 200, 290, 200, 50, quit_game),
]

#Header text
header_text = ("Welcome level 2,\n"
               "in this level you will learn some basic levelling concepts,\n "
               "calculations and steps performed in Spatial science and"
               "and some of the quipment used to collect data and do some measurements"
               "used in Geospatial science.")

#Main loop
running = True
while running:
    screen.fill(BLUE)

    #Draw wrapped header
    draw_wrapped_text(screen, header_text, header_font, WHITE, pg.Rect(20, 10, 560, 100))

    #Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    #Draw buttons
    for button in buttons:
        button.draw(screen)

    pg.display.flip()

pg.quit()
