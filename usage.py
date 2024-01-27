def usage(m, ai = ""):
    if m=="h":
        print()

        print("Usage: [options]")

        print()

        print("Options:")
        print("    h,    help: display this message")
        print("         clear: clear the console")
        print("          exit: exit OpenAIConnector")

        print()

        print("       chatgpt: ask chatgpt a question")
        print("       perplexity: ask perplexity a question")
        print("       details: view details about existing conversations")

        print()
    elif m=="o":
        print()

        print(f"Usage: {ai} [question]")

        print()
    elif m=="d":
        print()

        print("Usage: details [options]")

        print()

        print("Options:")
        print("    t,       today: display a report for today's conversations")
        print("    y,   yesterday: display a report for yesterday's conversations")
        print("    a,         all: display a report for all conversations")
        print("    m,        most: display a report for the most asked conversation")
        print("    l,     longest: display a report for the conversation that took the longest")
        print("    s,    shortest: display a report for the conversation that took the shortest")
        print("              [id]: display the report for the conversation with the given id")
        print("       date [date]: display the report for the conversation with the given date")
        print("                     (expected format: YYYY-MM-DD)")

        print()
    elif m=="dd":
        print("Usage: details date [YYYY-DD-MM]")

        print()
