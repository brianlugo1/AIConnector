EXT="exit"
HLP="help"
WLC="welcome"
CLR="clear"

GPT="chatgpt"
GPT_LEN=len(GPT)
PER="perplexity"
PER_LEN=len(PER)
LMA="llama"
LMA_LEN=len(LMA)
DTS="details"
DTS_LEN=len(DTS)

TDY="today"
YTD="yesterday"
ALL="all"
MST="most"
LGT="longest"
SRT="shortest"
DTE="date"
AI="ai"

STD_CMDS=[
    EXT,
    HLP,
    WLC,
    CLR,
    GPT,
    PER,
    DTS,
    LMA
]

STD_FLGS=[
    AI,
    TDY,
    YTD,
    ALL,
    MST,
    LGT,
    SRT,
    DTE,
]

STD_FLGS_1ST_CHAR=[
    TDY[0],
    YTD[0],
    ALL[0],
    MST[0],
    LGT[0],
    SRT[0],
    DTE[0],
]

# TODO work on creating a utility for flag/cmd detection!!!
STD_AIS=[
    GPT,
    PER,
    LMA,
]

STD_AIS_1ST_CHAR=[
    GPT[0],
    PER[0],
    LMA[0],
]

AIE="ai_exception"
FLE="file"
LNK="link"
PRB="probable"

COLUMN_WIDTH=13

ID="ID".center(COLUMN_WIDTH, ' ')
TIME="Times Asked".center(COLUMN_WIDTH, ' ')
DATE="Date Asked".center(COLUMN_WIDTH, ' ')
TIMEWAITED="Time Waited".center(COLUMN_WIDTH, ' ')
AIC="AI".center(COLUMN_WIDTH, ' ')

STANDARD_TEXT_WIDTH=70

STANDARD_TIMEOUT=3