## CONSTANT DEFINITION

# Time history generation modes
LOADTH = 1          # Generate a series of steady points driving only Load Request
SPEEDTH = 2         # Generate a series of steady points driving only Speed limiter
SPEEDLOADTH = 3     # Generate a table of steady points driving Speed, Load Requests: series of Loads at constant speed
LOADSPEEDTH = 4     # Generate a table of steady points driving Speed, Load Requests: series of Speeds at constant Load

UPWARDS = 1         # Direction of the movement in the time history generation
DOWNWARDS = 2       # Direction of the movement in the time history generation
DEFAULTDIR = UPWARDS

# Steady Times boundaries for safe operations
STEADYMINTIME = 20      # seconds
STEADYMAXTIME = 600     # seconds
DEFAULTSTEADYTIME = 60  #

DEFAULTTRNTIME = 20     # default transition time between steady points

TRN_D_TIME = 0.1        # DELTA TIME (time resolution) for developing transient among steady points
