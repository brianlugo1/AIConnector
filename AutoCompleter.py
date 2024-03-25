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

    def complete(self, text: str, state: int) -> str | None:
        """
        complete() attempts to parse the current buffer of command
        when the tab button is pressed and appends any matching
        strings to the current target word to autocomplete. If the
        parse target word is a command, then only stored commands
        are compared to return the correct autocomplete command.
        If the parse target word is a flag on a command, then
        only the stored flags are commpared to return the
        correct autocomplete flag. If there is no target word,
        then the array of potential matches is cleared. If the
        array look up of the state index fails, None is returned
        because no matching word exists.

        Paramters:
        self: a reference to this MyCompleter object instance
        text: string (the target word to autocomplete)
        state: integer (the index of the current state)

        Returns:
        self.matches[state]: a string of autocomplete word or None
        """
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