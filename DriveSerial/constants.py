## CONSTANT DEFINITION

# Steady Times boundaries for safe operations
STEADYMINTIME = 20      # seconds
STEADYMAXTIME = 600     # seconds
DEFAULTSTEADYTIME = 60  #

DEFAULTTRNTIME = 20     # default transition time between steady points

TRN_D_TIME = 0.1        # DELTA TIME (time resolution) for developing transient among steady points


# Time history generation modes
LOADTH = 1          # Generate a series of steady points driving only Load Request
SPEEDTH = 2         # Generate a series of steady points driving only Speed limiter
SPEEDLOADTH = 3     # Generate a table of steady points driving Speed, Load Requests: series of Loads at constant speed
LOADSPEEDTH = 4     # Generate a table of steady points driving Speed, Load Requests: series of Speeds at constant Load
SPEEDSLOPE = 5      # Generate a time history with TRN_D_TIME resolution sloping on engine speed
LOADSLOPE = 6       # Generate a time history with TRN_D_TIME resolution sloping on engine load

# Time history generation modes descriptors
SEQ_TYPES_DESCR = {LOADTH: {'code': 'LOADTH', 'name': 'LOAD Sequence',
                            'description': 'Generate a series of steady points driving only Load Request'}}

SEQ_TYPES_DESCR[SPEEDTH] = {'code': 'SPEEDTH', 'name': 'Engine SPEED Sequence',
                            'description': 'Generate a series of steady points driving only Speed Control of brake'}

SEQ_TYPES_DESCR[SPEEDLOADTH] = {'code': 'SPEEDLOADTH', 'name': 'Engine SPEED and LOAD Sequence',
                'description': 'Table of steady points driving Speed, Load Requests: series of Loads at constant speed'}

SEQ_TYPES_DESCR[LOADSPEEDTH] = {'code': 'LOADSPEEDTH', 'name': 'Engine LOAD and SPEED Sequence',
                'description': 'Table of steady points driving Speed, Load Requests: series of Speeds at constant Load'}

SEQ_TYPES_DESCR[SPEEDSLOPE] = {'code': 'SPEEDSLOPE', 'name': 'Engine SPEED slope',
                'description': 'Time history with {} [s] time resolution sloping on engine speed'.format(TRN_D_TIME)}

SEQ_TYPES_DESCR[LOADSLOPE] = {'code': 'LOADSLOPE', 'name': 'Engine LOAD slope',
                'description': 'Time history with {} [s] time resolution sloping on engine load'.format(TRN_D_TIME)}




UPWARDS = 1         # Direction of the movement in the time history generation
DOWNWARDS = 2       # Direction of the movement in the time history generation
DEFAULTDIR = UPWARDS

