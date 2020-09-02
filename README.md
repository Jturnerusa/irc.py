# irc.py
A simple tiny wrapper around the IRC protocol

Example:

    import irc
    
    irc = Irc("example.com", 6667, ssl=False)
    irc.connect()
    irc.user("username")
    irc.nick("username")
    irc.password("password")
    
    for message in irc:
        if message.type == "PING":
            irc.pong(message.suffix)
        if message.type == "PRIVMSG":
            print(f"{message.sender} said {message.suffix}")
            
Different IRC servers have different initial authentication routines, some might need you to respond to a ping at first for example. It can take a little bit of experimenting to figure it out.
