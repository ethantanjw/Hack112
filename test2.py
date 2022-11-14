from songGenerator import *

sg = SongGenerator()
sg.assignSongs()

print(sg.getSong("happy")['name'])