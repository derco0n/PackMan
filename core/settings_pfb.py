# PackMan (https://github.com/derco0n/PackMan):
# Config-component: Subsettings for pifaceboards

class settings_pifaceboards:
    def __init__(self):
        # Initialize with default values
        self.boardcount = 1
        self.inputsperboard = 8
        self.inputmode = "switch"  # Possible values are button (if you want to connect push-buttons to the inputs) and switch (if you want to connect switches)

    def all_input_count(self):
        return self.inputperboard * self.boardcount