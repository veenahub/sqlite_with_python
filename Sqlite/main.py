from app import  run,get
from data import artists_data,albums_data,songs_data

# creating artits table
run('''
  CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name STRING NOT NULL,
    description STRING NOT NULL
  )
''')

# creating albums table
run('''
    CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING NOT NULL,
    description STRING NOT NULL,
    year_released INTEGER,
    artist_id INTEGER NOT NULL,
    FOREIGN KEY(artist_id) REFERENCES artists(id)
    ON DELETE CASCADE
  )
''')
# creating songs table
run('''
    CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_name STRING NOT NULL,
    duration REAL NOT NULL,
    album_id INTEGER NOT NULL,
    FOREIGN KEY(album_id) REFERENCES album(id)
    ON DELETE CASCADE
  )
''')


for artist in artists_data:
   run('INSERT INTO artists VALUES(NULL, :artist_name, :description)', artist)


for album in albums_data:
   run('INSERT INTO albums VALUES(NULL, :title, :description,:year_released,:artist_id)', album)

for song in songs_data:
   run('INSERT INTO songs VALUES(NULL, :song_name, :duration, :album_id)', song)


# Print the names of all the artists
artists = get(''' SELECT * FROM artists ''') 
for artist in artists:
  #print(artist.keys())
  print(artist['artist_name'],)


#Print the oldest album
oldest_album = get('''SELECT * FROM albums
                WHERE  year_released = ( SELECT min(year_released)
                                           FROM albums );''')
for album in oldest_album:            
  # print(album.keys())
    print(album['id'],album['title'],album['description'],album['year_released'],album['artist_id'])


#Print the album with length of playing time  
albums = get(''' SELECT albums.title,sum(songs.duration) AS "length_of_playingtime"
                 FROM albums JOIN songs
                 ON songs.id = albums.id
                ''')
for album in albums:
  print(album['title'],album['length_of_playingtime'])


#Update the album that is missing year_released by a year
run('''  UPDATE albums 
         SET year_released = 2012 
         WHERE id = 2; ''')
                  
#Add artist via input
artist_name = input("Please define a 'artist_name':")
description = input("Please define a 'description':")
run('''INSERT INTO artists(artist_name,description) VALUES ('{}','{}'); '''.format(artist_name,description))

#Add album via input
title = input("Please define a 'title':")
description = input("Please define a 'description':")
year_released = input("Please define a 'year_released':")
artist_id = input("Please define a 'artist_id':")
run('''INSERT INTO albums(title,description,year_released,artist_id) VALUES ('{}','{}','{}','{}'); '''.format(title,description,year_released,artist_id))


                
#Add songs via input
song_name = input("Please define a 'song_name':")
duration = input("Please define a 'duration':")
album_id = input("Please define a 'album_id':")
run('''INSERT INTO songs(song_name,duration,album_id) VALUES ('{}','{}','{}'); '''.format(song_name,duration,album_id))


#Be able to delete an artist, album or song via input
run('''  DELETE FROM artists 
          WHERE id = 1; ''')

#Print the average length of a song in an album
albums = get(''' SELECT albums.title,avg(songs.duration) AS "avg_length_of_playingtime"
                 FROM albums JOIN songs
                 ON songs.id = albums.id
                ''')
for album in albums:
  print(album['title'],album['avg_length_of_playingtime'])

#View the longest song from each album
longest_songs = get(''' SELECT id,album_id,song_name,MAX(duration)
                       FROM songs
                       GROUP BY album_id''')
for longest_song in longest_songs:
  print(longest_song['id'],longest_song['album_id'],longest_song['song_name'],longest_song['MAX(duration)'])

#View the number of songs each artist has
artists_songs = get(''' SELECT artists.id,artists.artist_name,COUNT(songs.song_name) AS no_of_songs
                 FROM songs  JOIN albums
                 ON albums.id = songs.album_id
                 JOIN artists
                 ON artists.id = albums.artist_id
                 GROUP BY artist_name 
                 ''')
for artist_song in artists_songs:
  print(artist_song['id'],artist_song['artist_name'],artist_song['no_of_songs'])
#Be able to search for artists via input

search_artist = input("Please write a 'artist_name':")
artist = get(''' SELECT * FROM artists
                 WHERE  artist_name LIKE :search ''', 
                  { 'search': f'%{search_artist}%' })
for name in artist:
  print(name['id'],name['artist_name'],name['description'])

#Be able to search for songs via input
search_song = input("Please write a 'song_name':")
song = get(''' SELECT * FROM songs
                 WHERE  song_name LIKE :search ''', 
                  { 'search': f'%{search_song}%' })
for name in song:
  print(name['id'],name['song_name'],name['duration'],name['album_id'])

#Be able to show details about an artist where you also see the artist's all albums
artist = get('''SELECT artist_name,*from albums
                 JOIN
                 artists  on artists.id=albums.artist_id WHERE artist_name='Thaman'; ''')
for name in artist:
   print(name['artist_name'],name['title'],name['description'],name['year_released'],name['artist_id'])

#Be able to show details about an album where you also see the album's songs
album = get('''SELECT title,*from songs
                 JOIN
                 albums  on albums.id=songs.album_id WHERE title='Kick'; ''')
for name in album:
   print(name['title'],name['song_name'],name['duration'],name['album_id'])
