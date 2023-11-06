import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands
import asyncio
from typing import Optional
from music_acquisition import Music, new_music, playlist, full_discography
import csv

prefix= "/"
intents = discord.Intents.all() 
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
intents.message_content = True
bot=commands.Bot(command_prefix=prefix, intents=intents)
is_blindest_running = False
current_music: Music = None
user_points = {}
user_points_correct_on_this_round = {}
channel = None
# read discord token
token = ""
with open("token.txt", "r") as f:
    token = f.read()

@bot.event
async def on_ready():
    print("Le blind Test est prêt !")
    # send list of command to discord
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.Game(name="Blind Test"))

@bot.tree.command(name='newmusic',description="permet d ajouter des nouveaux sons")
@app_commands.describe(link="le lien",title="le titre", author="l auteur", playlist="la playlist dans laquele le son ira")
async def newmusic(ctx, link:str, title:str, author:str, playlist:str):
    if link == None or len(link) == 0 :
        await ctx.send("You need to pass at least the youtube link of the music \n use : $newmusic <link> <title> <author> <playlist>")
        pass
    new_music(link, title, author, playlist)
    print(link, title, author, playlist)
    await ctx.send(f'Music {title} created', ephemeral=True)
    #await ctx.send(f'Music {title} created')
    
@bot.tree.command(name='test',description="yes")
async def test(ctx, arg: Optional[str] = None):
    print("https://media.discordapp.net/attachments/809139078687490079/1170802163568623758/fb_img_1599284128726-2748822194.jpg")
    await ctx.send(arg)

@bot.tree.command(name='vuvuzela',description="Plays an awful vuvuzela in the voice channel")
async def vuvuzela(ctxt):
    # grab the user who sent the command
    user=ctxt.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    # grab user's voice channel
    channel=voice_channel
    print(('User is in channel: '+ str(channel)))
    if not channel:
        await ctxt.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctxt.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source="./audios/vuvuzela.mp4"))
    await asyncio.sleep(10)  # play for 10 seconds
    if voice.is_playing():
        voice.stop()
    await voice.disconnect()


@bot.tree.command(name='blindtest',description="Launch the blindtest")
@app_commands.describe(playlist_name="le nom de la playlist",nb_music="le nombre de musique", duration="la durée")
async def blindtest(ctxt, playlist_name:str, nb_music:int, duration:int):
    global is_blindest_running, current_music, channel
    # grab the user who sent the command
    user=ctxt.message.author
    voice_channel=user.voice.channel
    channel = ctxt.message.channel
    print(('User is in channel: '+ str(channel)))
    if not voice_channel:
        await ctxt.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctxt.guild)
    if voice and voice.is_connected():
        await voice.move_to(voice_channel)
    else:
        voice = await voice_channel.connect()
    is_blindest_running = True
    await channel.send(f"Let's go for the blind test !  {nb_music} musics will be played for {duration} seconds each !")
    #get playlist
    if playlist_name == None:
        discography = full_discography()
    else:
        discography = playlist(playlist_name)
    
    i = 0
    l = discography.get_length()
    while i < nb_music and i < l:
        # get one random music
        current_music = discography.get_one_music()
        print(current_music.title)
        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=current_music.path))
        await asyncio.sleep(duration)
        if voice.is_playing():
            voice.stop()
        i += 1
        await channel.send(f"It was {current_music.title} by {current_music.author}. Music {i} out of {nb_music}")
        await asyncio.sleep(10)
    is_blindest_running = False
    await voice.disconnect()
    # show points
    await ctxt.send("Fin du blindtest !")
    for user in user_points:
        await ctxt.send(str(user.name) + " : " + str(user_points[user]))
    user_points = {}

@bot.command(
    name='fin_blindtest',
    description='End the blindtest',
    pass_context=True,
)
async def fin_blindtest(ctxt):
    # get the user channel
    user=ctxt.message.author
    channel = user.get_channel()
    # Disconnect the bot from voice channel
    voice = get(bot.voice_clients, guild=ctxt.guild)
    if voice and voice.is_connected():
        if voice.is_playing():
            voice.stop()
    await voice.disconnect()
    # show points
    await ctxt.send("Fin du blindtest !")
    for user in user_points:
        await ctxt.send(user.name + " : " + user_points[user])
    user_points = {}
    
@bot.tree.command(name='see_musics',description="See the musics")
async def see_musics(ctx):
    to_send = ""
    # open the index file
    with open('index.csv', 'r') as f:
        csv.reader(f,delimiter=';')
        for line in f:
            to_send+=line
            print(line)
        print(to_send)
    await ctx.send(to_send)
#        for line in f:
#            to_send += line
#    await ctxt.send(to_send)
        

@bot.tree.command(name='see_playlists',description="See the playlists")
async def see_playlists(ctxt):
    to_send = ""
    send = []
    # open the index file
    with open('index.csv', 'r') as f:
        for line in f:
            if len(line.split(";")) > 2:
                if line.split(";")[2] not in send:
                    to_send += line.split(";")[2] + "\n"
                    send += [line.split(";")[2]]
    await ctxt.send(to_send)

@bot.tree.command(name='delete_music',description="Delete a music")
async def delete_music(ctxt, title:str, author:str):
    if title == None or author == None or len(title) == 0 or len(author) == 0:
        await ctxt.send("You need to pass the title and the author of the music to delete \n use : $delete_music <title><author>")
        return
    # open the index file
    with open('index.csv', 'r') as f:
        lines = f.readlines()
    with open('index.csv', 'w') as f:
        for line in lines:
            if line.split(";")[0] != title and line.split(";")[1] != author:
                f.write(line)
    await ctxt.send(f"Music {title} deleted")    
    

    
@bot.tree.command(name='ping',description='Retourne la latence du bot.')
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(
        title = f'Pong! :ping_pong:',
        description = f'latence = {round(bot.latency * 1000)}ms'
    )
    await interaction.response.send_message(embed=embed,ephemeral=True)
    return

@bot.event
async def on_message(message):
    # 2 channel in parallel ? -> dictionnary ?
    global is_blindest_running, current_music, channel, user_points, user_points_correct_on_this_round
    await bot.process_commands(message)
    print(message.author, message.content, is_blindest_running)
    if message.author == bot.user:
        return
    if message.channel != channel:
        return
    if is_blindest_running:
        title = current_music.title
        author = current_music.author
        print(title, author)
        print(message.author, message.content, (message.content == title), (message.content == author))
        if message.content.lower() == title.lower():
            if message.author in user_points_correct_on_this_round and user_points_correct_on_this_round[message.author][0] ==  True:
                await message.channel.send("Tu avais déjà trouvé le titre !")
                return
            await message.channel.send("Bravo ! Tu as trouvé le titre !")
            if message.author in user_points_correct_on_this_round:
                user_points_correct_on_this_round[message.author][0] = True
            else:
                user_points_correct_on_this_round[message.author] = [True, False]
            # add points to the user
            if message.author in user_points:
                user_points[message.author] += 1
            else:
                user_points[message.author] = 1
        elif message.content.lower() == author.lower():
            if message.author in user_points_correct_on_this_round and user_points_correct_on_this_round[message.author][1] ==  True:
                await message.channel.send("Tu avais déjà trouvé l'artiste !")
                return
            await message.channel.send("Bravo ! Tu as trouvé l'artiste !")
            if message.author in user_points_correct_on_this_round:
                user_points_correct_on_this_round[message.author][1] = True
            else:
                user_points_correct_on_this_round[message.author] = [False, True]
            # add points to the user
            if message.author in user_points:
                user_points[message.author] += 1
            else:
                user_points[message.author] = 1
        else:
            await message.channel.send("Raté !")
    if message.content == "Ping":
        await message.channel.send("Pong")
    print(message.content)

bot.run(token)