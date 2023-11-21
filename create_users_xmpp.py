from sleekxmpp import ClientXMPP

class XMPPUserRegistration(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

if __name__ == "__main__":
    server = "localhost"

    user_details = [
        ("Drone1@" + server, "password"),
        ("Drone2@" + server, "password"),
        ("Drone3@" + server, "password"),
        ("Drone4@" + server, "password"),
        ("Drone5@" + server, "password"),
        ("Drone6@" + server, "password"),
        ("Drone7@" + server, "password"),
        ("Drone8@" + server, "password"),
        ("Drone9@" + server, "password"),
        ("HubH@" + server, "password"),
    ]

    for jid, password in user_details:
        xmpp = XMPPUserRegistration(jid, password)
        xmpp.register_plugin("xep_0077")

        print("Before connecting")
        try:
            if xmpp.connect((server, 5222)):
                print("Connected successfully")
                xmpp.process(block=True)
                print("User registered successfully")
            else:
                print("Unable to connect to the XMPP server")
        except Exception as e:
            print(f"Error {str(e)}")

    print("All users registered.")