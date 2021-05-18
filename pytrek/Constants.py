
CONSOLE_HEIGHT:       int = 190

SCREEN_WIDTH:     int = 800
SCREEN_HEIGHT:    int = 640 + CONSOLE_HEIGHT

QUADRANT_GRID_WIDTH:  int = 640
QUADRANT_GRID_HEIGHT: int = 640

STATUS_VIEW_WIDTH: int = SCREEN_WIDTH - QUADRANT_GRID_WIDTH

QUADRANT_PIXEL_HEIGHT: int = 64
QUADRANT_PIXEL_WIDTH:  int = 64

QUADRANT_Y_ADJUSTMENT: int = CONSOLE_HEIGHT

QUADRANT_ROWS:    int = 10
QUADRANT_COLUMNS: int = 10
QUADRANT_MARGIN:  int = 1

GALAXY_ROWS:    int = 10
GALAXY_COLUMNS: int = 10

MINIMUM_COORDINATE: int = 0     # These should match the galaxy/quadrant size
MAXIMUM_COORDINATE: int = 9     # Currently assumed that are the same size


STANDARD_SPRITE_WIDTH:  int = 32
STANDARD_SPRITE_HEIGHT: int = 32

HALF_QUADRANT_PIXEL_WIDTH:  int = QUADRANT_PIXEL_WIDTH // 2
HALF_QUADRANT_PIXEL_HEIGHT: int = QUADRANT_PIXEL_HEIGHT // 2

THE_GREAT_MAC_PLATFORM:  str = 'darwin'
GAME_SETTINGS_FILE_NAME: str = "pytrek.ini"
BACKUP_SUFFIX:           str = '.bak'


SOUND_VOLUME_LOW:    float = 0.1
SOUND_VOLUME_MEDIUM: float = 0.5
SOUND_VOLUME_HIGH:   float = 1.0

MIN_SECTOR_X_COORDINATE = 0
MAX_SECTOR_X_COORDINATE = QUADRANT_COLUMNS - 1
MIN_SECTOR_Y_COORDINATE = 0
MAX_SECTOR_Y_COORDINATE = QUADRANT_ROWS - 1

MIN_QUADRANT_X_COORDINATE = 0
MAX_QUADRANT_X_COORDINATE = GALAXY_COLUMNS - 1
MIN_QUADRANT_Y_COORDINATE = 0
MAX_QUADRANT_Y_COORDINATE = GALAXY_ROWS - 1

FIXED_WIDTH_FONT_NAME:     str = 'UniverseCondensed'
FIXED_WIDTH_FONT_FILENAME: str = f'{FIXED_WIDTH_FONT_NAME}.ttf'

DEFAULT_FULL_SHIELDS = 2500.0
