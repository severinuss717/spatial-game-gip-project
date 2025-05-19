import random
import math
import pygame as pg
import tkinter as tk
import threading
import subprocess
from PIL import Image, ImageTk  # Added for JPG

# Initializing pygame
pg.init()

# Creating the screen
screen = pg.display.set_mode((1000, 800))
pg.display.set_caption("Geospatial Gaming")
icon = pg.image.load('joystick.png')
pg.display.set_icon(icon)

# the player object
playerImg = pg.image.load('muted.png')
playerX = 100
playerY = 100
player_speed = 0.5

# Object assets
enemyImg = pg.image.load('satellite.png')
dataImg = pg.image.load('geographical.png')
gpsImg = pg.image.load('gps.png')
coordinateImg = pg.image.load('coordination.png')
mapImg = pg.image.load('map.png')
kingImg = pg.image.load('sejong-the-great.png')

# States of the objects
enemy_active = True
data_active = True
gps_active = True
coordinate_active = True
map_active = True
king_active = True
king_denied_shown = False
quiz_started = False

# Defining the walls rectangles
walls = [
    pg.Rect(200, 100, 20, 600),
    pg.Rect(400, 0, 20, 500),
    pg.Rect(600, 300, 20, 500),
    pg.Rect(0, 300, 300, 20),
    pg.Rect(700, 100, 200, 20)
]

#Collision detection for walls
def collides_with_wall(x, y, width=64, height=64):
    player_rect = pg.Rect(x, y, width, height)
    return any(player_rect.colliderect(wall) for wall in walls)

#Generate valid positions
positions = []
def get_non_overlapping_position(existing_positions, min_distance=60):
    while True:
        x = random.randint(0, 936)
        y = random.randint(0, 736)
        if all(math.hypot(x - px, y - py) >= min_distance for px, py in existing_positions):
            if not collides_with_wall(x, y):
                existing_positions.append((x, y))
                return x, y

enemyX, enemyY = get_non_overlapping_position(positions)
dataX, dataY = get_non_overlapping_position(positions)
gpsX, gpsY = get_non_overlapping_position(positions)
coordinateX, coordinateY = get_non_overlapping_position(positions)
mapX, mapY = get_non_overlapping_position(positions)
kingX, kingY = get_non_overlapping_position(positions)

#Drawing functions
def player(x, y): screen.blit(playerImg, (x, y))
def enemy(x, y): screen.blit(enemyImg, (x, y))
def data(x, y): screen.blit(dataImg, (x, y))
def gps(x, y): screen.blit(gpsImg, (x, y))
def coordinate(x, y): screen.blit(coordinateImg, (x, y))
def map_icon(x, y): screen.blit(mapImg, (x, y))
def king_icon(x, y): screen.blit(kingImg, (x, y))

def draw_walls():
    for wall in walls:
        pg.draw.rect(screen, (0, 0, 0), wall)

#Collision detection between objects
def is_collision(x1, y1, x2, y2, threshold=27):
    return math.hypot(x1 - x2, y1 - y2) < threshold

#pop with an image
def show_popup(message, title="Info", header=None, image_path=None, button_text=None, button_command=None):
    def popup():
        root = tk.Tk()
        root.title(title)
        root.geometry("800x500")

        if header:
            header_label = tk.Label(root, text=header, font=("Arial", 16, "bold"), pady=10)
            header_label.pack()

        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((500, 200))
                tk_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(root, image=tk_img)
                img_label.image = tk_img 
                img_label.pack(pady=10)
            except Exception as e:
                print(f"Image load failed: {e}")

        message_label = tk.Label(root, text=message, font=("Arial", 11), wraplength=700, justify="left")
        message_label.pack(pady=10)

        if button_text and button_command:
            button = tk.Button(root, text=button_text, command=lambda: [root.destroy(), button_command()])
            button.pack(pady=5)
        else:
            tk.Button(root, text="Close", command=root.destroy).pack(pady=5)

        root.mainloop()

    threading.Thread(target=popup).start()

def start_quiz():
    subprocess.Popen(["python", "quiz2.py"])

playerX_change = 0
playerY_change = 0
running = True

while running:
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -player_speed
            if event.key == pg.K_RIGHT:
                playerX_change = player_speed
            if event.key == pg.K_UP:
                playerY_change = -player_speed
            if event.key == pg.K_DOWN:
                playerY_change = player_speed
        if event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                playerX_change = 0
            if event.key in [pg.K_UP, pg.K_DOWN]:
                playerY_change = 0

    newX = playerX + playerX_change
    newY = playerY + playerY_change
    if not collides_with_wall(newX, playerY):
        playerX = newX
    if not collides_with_wall(playerX, newY):
        playerY = newY

    playerX = max(0, min(playerX, 936))
    playerY = max(0, min(playerY, 736))

    # Object collisions
    if enemy_active and is_collision(enemyX, enemyY, playerX, playerY):
        show_popup("Lets first define what levelling is:\n"
                   "Levelling - the process of determining and measuring height differences between points on the Earth's surface\n"
                   "Levelling requires some processes such as data collection and calculations\n"
                   "Levelling Instruments:\n"
                   "Dumpy level, Automatic level, Tilting level, Digital level\n"
                   "Levelling Staffs, Tripod and measuring wheels\n"
                   "Next is find")
        enemy_active = False

    if data_active and is_collision(dataX, dataY, playerX, playerY):
        show_popup("In order for one to do some basic levelling calculations one need:\n"
                   "Such as: Back sight, Fore Sight, Intermediate sight and Turning point\n"
                   "Backsight (BS): This is the first reading taken by the observer at every instrument station after setting up the level.\n"
                   "Foresight (FS): This is the last reading taken at every instrument station before moving the level.\n"
                   "Intermediate Sight (IS): This is any reading taken at an instrument station between the backsight and the foresight.\n"
                   "Turning point (TP): This point at which both a foresight and a back sight are taken before moving the staff\n"
                   "Next is find")
        data_active = False

    if gps_active and is_collision(gpsX, gpsY, playerX, playerY):
        show_popup(
            message="In this levelling process one use a staff and a level to take accurate measurements.\n"
            "This activity is carried out by two individuals\n "
            "Always atarting of with your Back sight and Ending with the Fore sight\n",
            title="levelling",
            header="Visualization of the levelling process!",
            image_path=r"E:\project\levelling-in-surveying.jpg"  
        )
        gps_active = False

    if coordinate_active and is_collision(coordinateX, coordinateY, playerX, playerY):
        show_popup("Remote Sensing is one the key components of GIS.\n"
                   "Remote Sensing - the art and science of acquiring data of an object from a distance.\n"
                   "Data is acquired with sensors detecting different wavelengths of the electromagnetic spectrum\n"
                   "Satellites are a primary source of remote sensing data\n"
                   "Aerial photography - process of capturing images from an elevated position using platforms like balloons or airplanes\n"
                   "Aerial photography is also one of the primary sources of remote sensing\n"
                   "in order for one to capture this aerial photographs you have to plan what is called flight\n"
                   "In flight planning you do some calculations such as flight height and dtermining photo scale, determining flight area and number of photographs required\n"
                   "Next is to fin the calculator")
        coordinate_active = False

    if map_active and is_collision(mapX, mapY, playerX, playerY):
        show_popup("Lets get you what you will need for the calculations\n"
                   " s= photoscale, f = focal length, H = flight height, h = height above sea level\n"
                   "To determine photo scale, s = f/(H - h)\n"
                   "To determine flight height the height at which the sensor or camera platform is flying to capture the aerial photograph\n"
                   "H = (f/s) + h\n"
                   "please note down this formulaes as you will need the in the Intection with the king\n"
                   "Next is to find the king!")
        map_active = False

    if not (enemy_active or data_active or gps_active or coordinate_active or map_active):
        king_denied_shown = False

    if king_active and is_collision(kingX, kingY, playerX, playerY):
        if not (enemy_active or data_active or gps_active or coordinate_active or map_active):
            if not quiz_started:
                show_popup(
                    "Congratulations! You've mastered the geospatial elements and found the King!",
                    title="Victory",
                    header="Final Challenge",
                    image_path="sejong-the-great.png",
                    button_text="Start Quiz",
                    button_command=start_quiz
                )
                quiz_started = True
                king_active = False
        elif not king_denied_shown:
            show_popup("You need to collect all other geospatial elements before meeting the King.", "Access Denied")
            king_denied_shown = True

    draw_walls()
    if enemy_active: enemy(enemyX, enemyY)
    if data_active: data(dataX, dataY)
    if gps_active: gps(gpsX, gpsY)
    if coordinate_active: coordinate(coordinateX, coordinateY)
    if map_active: map_icon(mapX, mapY)
    if king_active: king_icon(kingX, kingY)
    player(playerX, playerY)

    pg.display.update()

pg.quit()
