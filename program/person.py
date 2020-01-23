from program.drinks import drink_dict

import datetime


# Class that is made for each user, keeps track of the permilles, time and alcohol burning
class Person:
    # Constructor
    def __init__(self, gender, weight):
        # Set the body liquid based on the user's gender and weight
        if gender == 'M':
            gmp = 0.75
        else:
            gmp = 0.66
        self.body_liquid = gmp * weight * 1000

        self.permilles = 0.0
        self.last_burn = datetime.datetime.now()
        self.burn_rate = weight / 10
        self.high_score = 0.0

    # Add permilles according to the given drink and its amount
    def add_drink(self, drink, amount):
        self.permilles += self.calc_permilles(drink, amount)
        if self.permilles > self.high_score:
            self.high_score = self.permilles

    # Calculate the exact permilles of amount of the given drink
    def calc_permilles(self, drink, amount):
        return (drink_dict[drink] * amount * 1000) / self.body_liquid

    def return_permilles(self):
        return self.permilles

    def return_highest(self):
        return self.high_score

    # Calculate the current amount of permilles based on the time passed
    def burn_alcohol(self):
        if self.permilles == 0:
            return
        now = datetime.datetime.now()
        difference = now - self.last_burn
        hours = difference / datetime.timedelta(hours=1)

        burned_grams = self.burn_rate * hours
        burned_permilles = (burned_grams * 1000) / self.body_liquid
        temp_permilles = self.permilles - burned_permilles

        if temp_permilles <= 0:
            self.permilles = 0.0
        else:
            self.permilles = temp_permilles
        self.last_burn = now
