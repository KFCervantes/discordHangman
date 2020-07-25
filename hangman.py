import discord
from discord.ext import commands
import nest_asyncio
import game

#generate token later
token = 'NzM1NzYyNTM0OTQxOTgyNzQw.Xxk-WQ.3lNHxnP6F2ki4DfhRQ-m4KDs0qU'

nest_asyncio.apply()

prefix = '^^hangman '
client = commands.Bot(command_prefix = prefix)

#adding variables to client to avoid having to use globals
client.command_prefix = prefix
client.game_channel_id = 733679936878936170
client.game_dict = {}

#for debugging, doesn't affect bot
@client.event
async def on_connect():
    print(f'{client.user.name} is connected to Discord')

#for debugging, doesn't affect bot
@client.event
async def on_disconnect():
    print(f'{client.user.name} disconnected from Discord')

#for debugging, doesn't affect bot
@client.event
async def on_ready():
    print(f'{client.user.name} is logged in')

#will have to add some stuff to allow images in this

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    #this if statement is too long
    #starts by making sure there is no command prefix
    #then checks to see if the person that sent the message has played
    #then checks if that person is currently playing
    #this allows people quitting to make them able to send normal messages
    if (not message.content.startswith(client.command_prefix)) and (message.author in client.game_dict) and client.game_dict[message.author].already_playing:
        s, file_num = client.game_dict[message.author].guess(message.content)
        f = None if file_num < 0 else discord.File(f'assets/hangman{file_num}.png')
        await message.channel.send(s, file = f)

    #this needs to be here in this spot so that the commands will still work
    await client.process_commands(message)

#needed for me to shutdown the bot
@client.command()
@commands.is_owner()
async def shutdown(ctx):
    print('shutting down')
    await client.logout()

@client.command(name = 'start')
async def start_game(ctx):
    #creates game and starts if there is no game running
    if ctx.author not in client.game_dict:
        client.game_dict[ctx.author] = game.Game(ctx.author.mention)
        client.game_dict[ctx.author].start()

    #restarts game otherwise
    else:
        client.game_dict[ctx.author].reset()

    s, file_num = client.game_dict[ctx.author].state()
    f = None if file_num < 0 else discord.File(f'assets/hangman{file_num}.png')
    await ctx.send(s, file = f)

#allows player to quit
@client.command(name = 'quit')
async def quit_game(ctx):
    if ctx.author in client.game_dict:
        client.game_dict[ctx.author].quit()

#allows player to see what state the game is in
@client.command(name = 'state')
async def get_state(ctx):
    if ctx.author in client.game_dict:
        s, file_num = client.game_dict[ctx.author].state()
        f = None if file_num < 0 else discord.File(f'assets/hangman{file_num}.png')
        await ctx.send(s, file = f)

client.run(token)
