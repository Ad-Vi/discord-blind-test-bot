# Blind test Bot Discord

Discord Bot to play blind tests on Discord. This bot was initially developed for a student Association.

## Installation

1. Add the bot to your discord server
2. Add a text channel named `blindtest` (or change the ``channel_name`` in the code)
3. Add a voice channel named `blindtest` (or change the ``channel_name`` in the code)  
4. Install the requirements with the command ``pip3 install -r requirements.txt``
5. Run the bot with the command ``python3 bot.py``


## Commands

- ``$newmusic link title author playlist`` Add new music to the database.  
``link``: link to the music on YouTube,  
``title``: title of the music to be saved in the database,  
``author``: author of the music to be saved in the database,  
`playlist`: a playlist of the music to be saved in the database (optional)  

- ``$import_musics_from_yt_playlist link``  
Import all the musics from a youtube playlist.  
``link``: link to the youtube playlist  

- ``$vuvuzela``  
Play a vuvuzela sound in the voice channel.

- ``$blindtest playlist_name nb_music duration``  
Play a blind test in the ``channel_name`` voice channel. The command has to be sent in the ``channel_name`` text channel.  
``playlist_name``: name of the playlist to play(optional, default: All music will be played),  
``nb_music``: number of music to play (optional, default: 10),  
``duration``: duration of the music in seconds (optional, default: 30s)  
To answer, send a message in the ``user_id-channel_name`` thread channel with the title of the music or the author. Points are attributed with regard to how close the answer is to the real answer.  

- ``$fin_blindtest``  
End the blind test. The command has to be sent in the ``channel_name`` text channel.

- ``$shuffle playlist_name nb_music`` Shuffle the music of a playlist in the ``channel_name`` voice channel.  
``playlist_name``: name of the playlist to shuffle (optional, default: All music will be shuffled),  
``nb_music``: number of music to shuffle (optional, default: All music will be played)  

- ``$next``  
Play the next music on the shuffle list. The command has to be sent in the ``channel_name`` text channel.

- ``$fin_shuffle``  
End the shuffle. The command has to be sent in the ``channel_name`` text channel.

- ``$see_musics``  
See the number of music in the database.  

- ``$see_playlists``  
See the playlists in the database.  

- ``$delete_music title author`` Delete a music from the database.  
``title``: title of the music to be deleted,  
``author``: author of the music to be deleted