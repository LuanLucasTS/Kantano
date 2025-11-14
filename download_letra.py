from vagalume import lyrics

artist_name = 'k/da'
song_name = 'more'

result = lyrics.find(artist_name, song_name)

if result.is_not_found():
    print('Song not sound')
else:
    print(result.song.name)
    print(result.artist.name)
    print(result.song.lyric)


translation = result.get_translation_to('pt-br')
if not translation:
    print('Translation not found')
else:
    print(translation.name)
    print(translation.lyric)