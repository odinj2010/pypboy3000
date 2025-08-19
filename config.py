import pygame
import os # <-- Added for path handling

try: # Try to initialize pygame mixer for sound
    pygame.mixer.init(44100, -16, 2, 2048) # Initialize mixer with frequency, size, channels, and buffer
    SOUND_ENABLED = True # Set sound enabled flag to True
except Exception as e: # Catch any exceptions during initialization
    print(f"Warning: pygame.mixer.init() failed: {e}") # Print a warning message
    SOUND_ENABLED = False # Set sound enabled flag to False

# Now, load the sounds
SOUNDS = {} # Initialize an empty dictionary to store sounds
if SOUND_ENABLED: # If sound is enabled
    try: # Try to load sound files
        # A dictionary mapping sound names to their file paths
        sound_files = {
            "changemode": "sounds/changemode.ogg", # Path for changemode sound
            "dial_move": "sounds/dial_move.ogg" # Path for dial_move sound
        }
        for name, path in sound_files.items(): # Iterate through sound files
            SOUNDS[name] = pygame.mixer.Sound(path) # Load each sound and store it in the dictionary
    except Exception as e: # Catch any exceptions during sound loading
        print(f"Warning: Could not load sounds: {e}") # Print a warning message
        # Disable sound if loading fails, but keep the program running
        SOUND_ENABLED = False # Set sound enabled flag to False

PLAYERNAME = "NfgOdin" # Player's name
PLAYERLEVEL = 10 # Player's level

WIDTH = 1920 # Screen width
HEIGHT = 1080 # Screen height

# --- NEW: Define the directory for AI models ---
MODELS_DIR = "models" # Directory where AI models are stored

minSwipe = 50 # Minimum distance for a swipe gesture
maxClick = 15 # Maximum distance for a click gesture
longPressTime = 200 # Duration for a long press gesture
touchScale = 1 # Scaling factor for touch input
invertPosition = False # Flag to invert touch position
GPIO_AVAILABLE = True # Flag indicating if GPIO is available
RADIO_PLAYING = True # Flag indicating if radio is playing
QUICKLOAD = False # Flag for quick load functionality
LOAD_CACHED_MAP = True # Flag to load cached map
# Main

TINTCOLOUR = pygame.Color(26, 255, 128) # Green tint color
# TINTCOLOUR = pygame.Color (46, 207, 255) # Blue tint color
# TINTCOLOUR = pygame.Color (255, 182, 66) # Amber tint color
# TINTCOLOUR = pygame.Color (192, 255, 255) # White tint color


#MAP_FOCUS = (-5.9347681, 54.5889076) # Example map focus coordinates
#MAP_FOCUS = (-102.3016145, 21.8841274) # Old Default map focus coordinates
#MAP_FOCUS = (-118.5723894,34.3917171)#CodeNinjasValencia map focus coordinates
#MAP_FOCUS = (32.7157, 117.1611) # Example map focus coordinates
MAP_FOCUS = (-92.1943197, 38.5653437) # Current map focus coordinates

WORLD_MAP_FOCUS = 0.07 # Needed to handle the 50k node limit from OSM

LOAD_CACHED_MAP = True # Flag to load cached map
SOUND_ENABLED = True # Flag indicating if sound is enabled


EVENTS = {
    'SONG_END': pygame.USEREVENT + 1 # Custom event for song end
}

MODULES = {
    0: "home", # Home module
    1: "stats", # Stats module
    2: "items", # Items module
    3: "data", # Data module
    4: "ai", # AI module
    5: "gpio" # GPIO module
}

ACTIONS = {
    pygame.K_F1: "module_home", # F1 key maps to home module
    pygame.K_F2: "module_stats", # F2 key maps to stats module
    pygame.K_F3: "module_items", # F3 key maps to items module
    pygame.K_F4: "module_data", # F4 key maps to data module
    pygame.K_F5: "module_ai", # F5 key maps to AI module
    pygame.K_F6: "module_gpio", # F6 key maps to GPIO module
    pygame.K_1:	"knob_1", # 1 key maps to knob_1 action
    pygame.K_2: "knob_2", # 2 key maps to knob_2 action
    pygame.K_3: "knob_3", # 3 key maps to knob_3 action
    pygame.K_4: "knob_4", # 4 key maps to knob_4 action
    pygame.K_5: "knob_5", # 5 key maps to knob_5 action
    pygame.K_UP: "dial_up", # Up arrow key maps to dial_up action
    pygame.K_DOWN: "dial_down", # Down arrow key maps to dial_down action
    pygame.K_PLUS: "zoom_in", # Plus key maps to zoom_in action
    pygame.K_MINUS: "zoom_out", # Minus key maps to zoom_out action
    pygame.K_KP_PLUS: "zoom_in", # Numpad plus key maps to zoom_in action
    pygame.K_KP_MINUS: "zoom_out" # Numpad minus key maps to zoom_out action
}

# Using GPIO.BCM as mode
#GPIO 23 pin16 reboot # Comment about GPIO 23
#GPIO 25 pin 22 blank screen do not use # Comment about GPIO 25
GPIO_ACTIONS = {
	4: "dial_down", #GPIO 23
	17: "dial_up", #GPIO 24
	22: "knob_down", #GPIO 4
	27: "knob_up", #GPIO 17
}

# LEDs
# pin 18, 23, 24,

MAP_ICONS = {
    "camp": 		pygame.image.load('images/map_icons/camp.png'),
    "factory": 		pygame.image.load('images/map_icons/factory.png'),
    "metro": 		pygame.image.load('images/map_icons/metro.png'),
    "misc": 		pygame.image.load('images/map_icons/misc.png'),
    "monument": 	pygame.image.load('images/map_icons/monument.png'),
    "vault": 		pygame.image.load('images/map_icons/vault.png'),
    "settlement": 	pygame.image.load('images/map_icons/settlement.png'),
    "ruin": 		pygame.image.load('images/map_icons/ruin.png'),
    "cave": 		pygame.image.load('images/map_icons/cave.png'),
    "landmark": 	pygame.image.load('images/map_icons/landmark.png'),
    "city": 		pygame.image.load('images/map_icons/city.png'),
    "office": 		pygame.image.load('images/map_icons/office.png'),
    "sewer": 		pygame.image.load('images/map_icons/sewer.png'),
}

AMENITIES = {
    'pub': 				MAP_ICONS['vault'],
    'nightclub': 		MAP_ICONS['vault'],
    'bar': 				MAP_ICONS['vault'],
    'fast_food': 		MAP_ICONS['settlement'],
	'cafe': 			MAP_ICONS['settlement'],
#	'drinking_water': 	MAP_ICONS['sewer'],
    'restaurant': 		MAP_ICONS['settlement'],
    'cinema': 			MAP_ICONS['office'],
    'pharmacy': 		MAP_ICONS['office'],
    'school': 			MAP_ICONS['office'],
    'bank': 			MAP_ICONS['monument'],
    'townhall': 		MAP_ICONS['monument'],
#	'bicycle_parking': 	MAP_ICONS['misc'],
#	'place_of_worship': MAP_ICONS['misc'],
	'theatre': 			MAP_ICONS['office'],
#	'bus_station': 		MAP_ICONS['misc'],
#	'parking': 			MAP_ICONS['misc'],
#	'fountain': 		MAP_ICONS['misc'],
#	'marketplace': 		MAP_ICONS['misc'],
#	'atm': 				MAP_ICONS['misc'],
    'misc':             MAP_ICONS['misc']
}

INVENTORY_OLD = [
"Ranger Sequoia",
"Anti-Materiel Rifle ",
"Deathclaw Gauntlet",
"Flamer",
"NCR dogtag",
".45-70 Gov't(20)",
".44 Magnum(20)",
"Pulse Grenade (2)"
]

WEAPONS = [
    "10mm Pistol",
    "Combat Knife",
    "Fragmentation Grenade (2)",
    "Laser Pistol",
    "Plasma Mine (3)"
]

ARMOR = [
    "Eyeglasses",
    "Vault 111 Jumpsuit",
    "Wedding Ring"
]

AID = [
    "Purified Water (3)",
    "Rad Away (2)",
    "Stim Pack (2)"
]

MISC = [
    "Pencil",
    "Pre-War Money (250)",
    "Super Glue",
    "Toy Mini-Nuke"
]

AMMO = [
    "10mm Rounds (15)",
    "Fusion Cells (28)"
]

QUESTS = [
    "Cosplacon",
    "Cosplay Royale",
    "Drink n Draw",
    "Queens of Cosplay"
]

SKILLS = [
    "Action Boy",
    "Animal Friend",
    "Awareness",
    "Gunslinger"
    "Hacker",
    "Mysterious Stranger",
    "Rifleman",
    "Science"   
]

PERKS = [
    "Action Boy",
    "Animal Friend",
    "Awareness",
    "Gunslinger"
    "Hacker",
    "Mysterious Stranger",
    "Rifleman",
    "Science"   
]


pygame.font.init()
FONTS = {}
for x in range(10, 28):
    FONTS[x] = pygame.font.Font('monofonto.ttf', x)


kernedFontName = 'fonts/monofonto-kerned.ttf'
monoFontName = 'fonts/monofonto.ttf'

# Scale font-sizes to chosen resolution:
FONT_SML = pygame.font.Font(kernedFontName, int (HEIGHT * (12.0 / 360)))
FONT_MED = pygame.font.Font(kernedFontName, int (HEIGHT * (16.0 / 360.0)))
FONT_LRG = pygame.font.Font(kernedFontName, int (HEIGHT * (18.0 / 360.0)))
MONOFONT = pygame.font.Font(monoFontName, int (HEIGHT * (16.0 / 360.0)))
# Find monofont's character-size:
tempImg = MONOFONT.render("X", True, TINTCOLOUR, (0, 0, 0))
charHeight = tempImg.get_height()
charWidth = tempImg.get_width()
del tempImg