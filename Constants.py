EXT="exit"
HLP="help"
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

STD_CMDS=[
    EXT,
    HLP,
    CLR,
    GPT,
    PER,
    DTS,
    LMA
]

STD_FLGS=[
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

AI="ai"
FLE="file"
PRB="probable"

width=13

ID="ID".center(width, ' ')
TIME="Times Asked".center(width, ' ')
DATE="Date Asked".center(width, ' ')
TIMEWAITED="Time Waited".center(width, ' ')
AI="AI".center(width, ' ')