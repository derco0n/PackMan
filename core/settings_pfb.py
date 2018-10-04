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

    def linear_input_number(self, boardnumber, inputnumber):
        # returns a linear number over all Inputs
        # Board 0, Input 0 = 0
        # Board 1, Input 0 = 8
        # Board 2, Input 2 = 18 ...
        if inputnumber > self.inputsperboard:
            # Impossible. inputnumber must be smaller than inputsperboard
            return -1
        else:
            linearnumber = boardnumber * self.inputsperboard + inputnumber  # TODO: Verify this calculation is correct
            return linearnumber