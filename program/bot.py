from telegram.ext import Updater, CommandHandler
from uuid import uuid4

from program.person import Person
from program.drinks import drink_dict

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Create a Person class for the user if one doesn't already exist
def add_person(bot, update, args, user_data):
    # Check if the user already exists and that rest of the command was legal
    if user_data:
        update.message.reply_text('Olet jo Humalabotin käyttäjä!')
        return

    if len(args) != 2:
        update.message.reply_text('Väärä määrä argumentteja! Käytä näin: \n/aloita {sukupuolesi (M tai N)} {painosi}')
        return

    gender = args[0].upper()
    weight = args[1]

    if not (gender == 'N' or gender == 'M'):
        update.message.reply_text('Sukupuolen tulee olla N tai M!')
        return

    try:
        weight = int(weight)
    except ValueError:
        update.message.reply_text('Painon tulee olla numero!')
        return

    # Create a user id and a Person class for the user and save them to user_data dict
    key = str(uuid4())
    new_person = Person(gender, weight)
    user_data[key] = new_person

    update.message.reply_text('Onneksi olkoon, voit nyt käyttää Humalabottia!')


# Check if the command was legal and call Person classes methods to add the drink
def drink_booze(bot, update, args, user_data):
    # Check if the user already exists or the command was not legal
    if not user_data:
        update.message.reply_text('Et ole vielä käyttäjä! Käytä komentoa: \n/aloita {sukupuolesi (M tai N)} {painosi}')
        return
    elif len(args) == 0:
        update.message.reply_text('Mitä joit? Käytä näin: \n/juo {juoman nimi} tai /juo {juoman nimi} {määrä}')
        return
    elif len(args) > 2:
        update.message.reply_text('Liikaa argumentteja! Käytä näin: \n/juo {juoman nimi} tai /juo {juoman nimi} '
                                  '{määrä}')
        return

    # Check if the given drink exists
    drink = args[0].lower()
    if drink not in drink_dict:
        update.message.reply_text('Valitettavasti en tunne juomaa {}!\nKomennolla /juomalista näet tuntemani '
                                  'juomat.'.format(drink))
        return

    if len(args) == 1:
        amount = 1
    else:
        # Make sure that the given drink-amount was a number
        try:
            amount = int(args[1])
        except ValueError:
            update.message.reply_text('Juomien määrän tulee olla numeromuodossa!')
            return

    # Check if the given amount of alcohol is more than in one bottle of 40% 0.5l Kossu
    if drink_dict[drink] * amount > 158:
        update.message.reply_text('Valitettavasti en usko, että joit {} annosta juomaa {}!'.format(amount, drink))
        return

    # Call the necessary methods for the Person class in user_data
    for x in user_data.values():
        x.burn_alcohol()
        x.add_drink(drink, amount)
        break

    update.message.reply_text('Juomat lisätty onnistuneesti!')


# Show the current permille amount of the user
def show_permilles(bot, update, user_data):
    # Check if the user exists
    if not user_data:
        update.message.reply_text('Et ole vielä käyttäjä! Käytä komentoa: \n/aloita {sukupuolesi (M tai N)} {painosi}')
        return

    # Get the current permille amount from user_data's Person class
    for x in user_data.values():
        x.burn_alcohol()
        permilles = x.return_permilles()
        update.message.reply_text("Promillesi: {:.2f}".format(permilles))
        break


# Show all the drinks in the drink_dict
def list_drinks(bot, update):
    message = 'Käytettävissä olevat juomat:\n'
    for drink_name in sorted(drink_dict):
        message += " - {}\n".format(drink_name)
    message += 'Huom: Joillekin juomille on useita eri nimityksiä; tilavuudet ja vahvuudet ovat pääteltävissä nimistä.'
    update.message.reply_text(message)


# Show the highest permille amount of the user
def show_highest(bot, update, user_data):
    if not user_data:
        update.message.reply_text('Et ole vielä käyttäjä! Käytä komentoa: \n/aloita {sukupuolesi (M tai N)} {painosi}')
        return

    for x in user_data.values():
        x.burn_alcohol()
        permilles = x.return_highest()
        update.message.reply_text('Historian suurin promillemääräsi: {:.2f}'.format(permilles))
        break


# Setup the bot
def main():
    try:
        # Read the token from the file
        file = open('token.txt', 'r')
        token = file.read()
        # Create the EventHandler and pass the token to it
        updater = Updater(token)
        dp = updater.dispatcher
    except:
        return

    # Get the dispatcher to register handlers

    # Register the handlers
    dp.add_handler(CommandHandler("juo", drink_booze, pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler("aloita", add_person, pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler("promillet", show_permilles, pass_user_data=True))
    dp.add_handler(CommandHandler("maksimit", show_highest, pass_user_data=True))
    dp.add_handler(CommandHandler("juomalista", list_drinks))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
