import discord
import random
from discord.ext import commands

dealercards = []
player_cards = []

dealer_busted = 0
busted = 0

card_value = 0
dealercard_value = 0
cards = [2, 2, 2, 2,
         3, 3, 3, 3,
         4, 4, 4, 4,
         5, 5, 5, 5,
         6, 6, 6, 6,
         7, 7, 7, 7,
         8, 8, 8, 8,
         9, 9, 9, 9,
         10, 10, 10, 10,
         'J', 'J', 'J', 'J',
         'Q', 'Q', 'Q', 'Q',
         'K', 'K', 'K', 'K',
         'A', 'A', 'A', 'A']

def draw_card():
    global card_value
    card = random.choice(cards)
    if not player_cards:
        card_value = 0
    player_cards.append(card)

    if (card == 'J') or (card == 'Q') or (card == 'K') or (card == 'A'):
        card_value += 10
    else:
        card_value += card

    return 'U have {} with {}'.format(card_value, player_cards)

def dealer_draw_card():
    global dealercard_value
    card = random.choice(cards)
    if not dealercards:
        dealercard_value = 0
    dealercards.append(card)

    if (card == 'J') or (card == 'Q') or (card == 'K') or (card == 'A'):
        dealercard_value += 10
    else:
        dealercard_value += card

    if dealercard_value < 17:
        return 'Dealer has {} with {}'.format(dealercard_value, dealercards)
    else:
        return 'Dealer had {} with {}'.format(dealercard_value, dealercards)

def start_game():
    dealercards.clear()
    player_cards.clear()
    dealer_hand = dealer_draw_card()
    player_hand = draw_card()

    return dealer_hand, player_hand

def hit():
    player_hand = draw_card()
    if card_value < 21:
        loss_message = None
        player_hand = 'U have {} with {}'.format(card_value, player_cards)
        return player_hand, loss_message
    if card_value == 21:
        loss_message = None
        player_hand = 'U have {} with {}'.format(card_value, player_cards)
        return player_hand, loss_message
    if card_value > 21:
        player_hand = 'U had {} with {}'.format(card_value, player_cards)
        loss_message = '**U busted!**'
        return player_hand, loss_message

def dealer_hit():
    global player_hand
    while dealercard_value < 17 or dealercard_value < card_value:
        dealer_hand = dealer_draw_card()
        loss_message = None
    if dealercard_value > 21:
        loss_message = '**U won!**'
        player_hand = 'U had {} with {}'.format(card_value, player_cards)
        dealer_hand = 'Dealer had {} with {}'.format(dealercard_value, dealercards)
        return player_hand, dealer_hand, loss_message
    if dealercard_value < 21:
        player_hand = None
        return player_hand, dealer_hand, loss_message
    if dealercard_value == 21:
        player_hand = None
        return player_hand, dealer_hand, loss_message
    if dealercard_value >= 17:
        loss_message = None
        player_hand = None
        dealer_hand = 'Dealer had {} with {}'.format(dealercard_value, dealercards)
        return player_hand, dealer_hand, loss_message

def card_comparison():
    if dealercard_value > card_value:
        return '**U lost**'
    if card_value > dealercard_value:
        return '**U won**'
    if card_value == dealercard_value:
        return "**That's a draw**"

class Casino(commands.Cog): #using class Casino to group game's event and function.
    @commands.command(name='blackjack', help='Under construction')
    async def blackjack(self, ctx: commands.Context):
        embed=discord.Embed(description=":construction: Under construction sry bro :construction_site:", color=0x00bfff)
        await ctx.send(embed=embed)

def setup(morph):
    morph.add_cog(Casino(morph))