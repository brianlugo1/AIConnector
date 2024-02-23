import readline

from Constants import (
    STD_CMDS,
    DTS,
    STD_FLGS
)

from utilities import split_cmds



class MyCompleter(object):
    def __init__(self, options):
        self.options=sorted(options)

    def complete(self, text, state):
        if state==0:
            line=readline.get_line_buffer()

            cmds=split_cmds(line)

            tokens=cmds[-1].strip().split(" ")

            cmd=tokens[0].strip().lower()

            if len(tokens)==1:
                self.matches=[s for s in STD_CMDS if s and s.startswith(cmd)]

            elif len(tokens)==2:
                if cmd != DTS and cmd != "d":
                    return None

                flag=tokens[1].strip().lower()

                self.matches=[s for s in STD_FLGS if s and s.startswith(flag)]

            if not text:
                self.matches=self.options[:]

        try:
            return self.matches[state]

        except IndexError:
            return None