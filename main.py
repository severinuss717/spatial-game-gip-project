import random
import math
import pygame as pg
import tkinter as tk
import threading
import subprocess

# Initialize pygame
pg.init()

# Create a screen
screen = pg.display.set_mode((1000, 800))
pg.display.set_caption("Geospatial Gaming")
icon = pg.image.load('joystick.png')
pg.display.set_icon(icon)

# Load images
playerImg = pg.image.load('muted.png')
enemyImg = pg.image.load('satellite.png')
dataImg = pg.image.load('geographical.png')
gpsImg = pg.image.load('gps.png')
coordinateImg = pg.image.load('coordination.png')
mapImg = pg.image.load('map.png')
kingImg = pg.image.load('sejong-the-great.png')

# Object states
enemy_active = True
data_active = True
gps_active = True
coordinate_active = True
map_active = True
king_active = True
king_denied_shown = False
quiz_started = False

# Prevent multiple popups at once
popup_lock = threading.Lock()

# Ensure non-overlapping object placement
positions = []

def get_non_overlapping_position(existing_positions, min_distance=50):
    while True:
        x = random.randint(0, 736)
        y = random.randint(0, 536)
        if all(math.hypot(x - px, y - py) >= min_distance for px, py in existing_positions):
            existing_positions.append((x, y))
            return x, y

# Set player starting position at bottom center and avoid overlap with other objects
playerX, playerY = 368, 700  # Positioned near bottom of screen
playerX_change = 0
playerY_change = 0
positions.append((playerX, playerY))

# Generate non-overlapping positions for other game elements
enemyX, enemyY = get_non_overlapping_position(positions)
dataX, dataY = get_non_overlapping_position(positions)
gpsX, gpsY = get_non_overlapping_position(positions)
coordinateX, coordinateY = get_non_overlapping_position(positions)
mapX, mapY = get_non_overlapping_position(positions)
kingX, kingY = get_non_overlapping_position(positions)

# Drawing functions
def player(x, y): screen.blit(playerImg, (x, y))
def enemy(x, y): screen.blit(enemyImg, (x, y))
def data(x, y): screen.blit(dataImg, (x, y))
def gps(x, y): screen.blit(gpsImg, (x, y))
def coordinate(x, y): screen.blit(coordinateImg, (x, y))
def map_icon(x, y): screen.blit(mapImg, (x, y))
def king_icon(x, y): screen.blit(kingImg, (x, y))

# Collision detection
def is_collision(x1, y1, x2, y2, threshold=27):
    return math.hypot(x1 - x2, y1 - y2) < threshold

# Popup display
def show_popup(message, title="Info", button_text=None, button_command=None):
    def popup():
        with popup_lock:
            root = tk.Tk()
            root.title(title)
            root.geometry("800x500")
            label = tk.Label(root, text=message, font=("Arial", 10), wraplength=700, justify="left")
            label.pack(pady=10, padx=10)

            if button_text and button_command:
                button = tk.Button(root, text=button_text, command=lambda: [root.destroy(), button_command()])
                button.pack(pady=5)
            else:
                close_button = tk.Button(root, text="Close", command=root.destroy)
                close_button.pack(pady=5)

            root.mainloop()

    threading.Thread(target=popup).start()

# Quiz launcher
def start_quiz():
    subprocess.Popen(["python", "quiz1.py"])

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -0.5
            if event.key == pg.K_RIGHT:
                playerX_change = 0.5
            if event.key == pg.K_UP:
                playerY_change = -0.5
            if event.key == pg.K_DOWN:
                playerY_change = 0.5

        if event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                playerX_change = 0
            if event.key in [pg.K_UP, pg.K_DOWN]:
                playerY_change = 0

    # Update player position
    playerX += playerX_change
    playerY += playerY_change
    playerX = max(0, min(playerX, 736))
    playerY = max(0, min(playerY, 736))

    # Collision handling
    if enemy_active and is_collision(enemyX, enemyY, playerX, playerY):
        show_popup(
            "Geospatial Science consists of various components such as:\n"
            "- GIS: Geographic Information Systems\n"
            "- Remote Sensing: Collecting data from a distance\n"
            "- GPS: Global Positioning Systems\n\n"
            "Next, find the Data icon."
        )
        enemy_active = False

    if data_active and is_collision(dataX, dataY, playerX, playerY):
        show_popup(
            "GIS (Geographic Information Systems) is a technology using computer-based tools to map and analyze "
            "data linked to specific geographic locations.\n\nGIS includes:\n"
            "- Data Collection\n- Data Analysis\n- Data Interpretation\n- Data Presentation\n\n"
            "Applications include Urban Planning, Weather Forecasting, Climate Change, Agriculture.\n\n"
            "Next, find the GPS icon."
        )
        data_active = False

    if gps_active and is_collision(gpsX, gpsY, playerX, playerY):
        show_popup(
            "GIS Data Collection:\n"
            "- Primary Data: collected for the current GIS project\n"
            "- Secondary Data: existing datasets adapted for GIS use\n\n"
            "Tools: Satellite Imagery, GPS\n"
            "Formats:\n- Raster: Grids/Images\n- Vector: Points, Lines, Polygons\n\n"
            "Next, find the Coordinate icon."
        )
        gps_active = False

    if coordinate_active and is_collision(coordinateX, coordinateY, playerX, playerY):
        show_popup(
            "Presentation of GIS Data:\n"
            "- Cartography: The art of making maps\n"
            "- Tools: ArcMap, ArcGIS Pro, QGIS\n"
            "- Other forms: Reports, Story Maps\n\n"
            "Next, find the Map icon."
        )
        coordinate_active = False

    if map_active and is_collision(mapX, mapY, playerX, playerY):
        show_popup(
            "Maps - Basic Data Presentation:\n"
            "- Reference Maps: e.g., Topographic, Political Maps\n"
            "- Thematic Maps: e.g., Choropleth, Heat Maps, Dot-Density\n\n"
            "Maps should include Title, Legend, Date, Cartographer, and Scale.\n\n"
            "Next, find the King icon."
        )
        map_active = False

    # Allow access to the King only after all others are collected
    if not (enemy_active or data_active or gps_active or coordinate_active or map_active):
        king_denied_shown = False

    if king_active and is_collision(kingX, kingY, playerX, playerY):
        if not (enemy_active or data_active or gps_active or coordinate_active or map_active):
            if not quiz_started:
                show_popup(
                    "Congratulations! You've completed all your tasks. Please complete the quiz to continue.",
                    title="Master of the Level",
                    button_text="Start Quiz",
                    button_command=start_quiz
                )
                quiz_started = True
                king_active = False
        elif not king_denied_shown:
            show_popup("You need to collect all other geospatial elements before meeting the King.", "Access Denied")
            king_denied_shown = True

    # Draw active objects
    if enemy_active: enemy(enemyX, enemyY)
    if data_active: data(dataX, dataY)
    if gps_active: gps(gpsX, gpsY)
    if coordinate_active: coordinate(coordinateX, coordinateY)
    if map_active: map_icon(mapX, mapY)
    if king_active: king_icon(kingX, kingY)

    player(playerX, playerY)
    pg.display.update()

# Exit pygame
pg.quit()
