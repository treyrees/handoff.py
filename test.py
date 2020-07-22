import sys
import json
import csv
import discord
from discord.ext import commands
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

#auth stuff
PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'id'
SPOTIPY_CLIENT_SECRET = 'secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
#relevant stuff
SCOPE = 'user-top-read'
CACHE = '.spotipyoauthcache'
ranges = ['short_term', 'medium_term', 'long_term']
sp = spotipy.Spotify(auth_manager=SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE ))

#functions
def get_spotify_username(discord_id):
    with open('usernames.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if int(row[0]) == discord_id:
                print('Successfully returned spotify username'+str(row[1]))
                return row[1]

def change_user(discord_id):
    print(discord_id)
    username = get_spotify_username(discord_id)
    print(username)
    token = util.prompt_for_user_token(username, show_dialog=True)
    print(token)
    sp = spotipy.Spotify(token)
    print(sp.me())

#this is where the fun begins
client = commands.Bot(command_prefix="!")

#on login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#on commands
@client.command()
async def handoff(ctx, *args):
    results = sp.search(q='jpegmafia', limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])
    change_user(ctx.author.id)

@client.command()
async def register(ctx, arg):
    discord_id = ctx.author.id
    spotify_username = arg
    already_registered = 0
    with open('usernames.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] == spotify_username:
                await ctx.send('You have already registered!')
                already_registered = 1
    with open('usernames.txt', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if already_registered == 0:
            csv_writer.writerow([discord_id, spotify_username])
            await ctx.send('You have successfully registered!')

client.run('bot-token')