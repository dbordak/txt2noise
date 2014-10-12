#!/usr/bin/python3

import sys
import random
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from PIL import ImageFont, ImageDraw, Image

font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf", 12)

sentences = sys.argv[1:]
instruments = (70,1,25,50,80)

random.seed(sentences[0])
for track, sentence in enumerate(sentences):
    # if seed_per_sentence:
    #     random.seed(sentence)
    midi = Midi(tempo=90, instrument=instruments[track])
    image = Image.new("L", (800,12), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((0, -1), sentence, font=font)

    notes_list = []
    for x in range(0,800):
        notes = []
        for y in range(0,12):
            vol = int((255 - image.getpixel((x, y)))/2)
            if vol:
                notes.append(Note(y, 5, 1/16, vol))
        if len(notes):
            notes_list.append(NoteSeq(random.choice(notes).harmonize(NoteSeq(notes))))
            # notes_list.append(NoteSeq(notes))
        else:
            notes_list.append(Rest(1/16))
    midi.seq_chords(notes_list)
    midi.write("test" + str(track) + ".mid")



#image.show()

# test for number of notes per frame
# for x in range(0,800):
#     #(y,5,1/16,255-pix/2)
#     #print(' '.join((str(255 - image.getpixel((x,y))) for y in range(0,12))))
#     val = len(list(filter(None,(255-image.getpixel((x,y)) for y in range(0,12)))))
#     if val > 8:
#         print(val)

# First method
# midi = Midi(number_tracks=12, tempo=120, instrument=50)
# for y in range(0,12):
#     seq = []
#     for x in range(0,800):
#         vol = int((255 - image.getpixel((x,y)))/2)
#         if vol:
#             seq.append(Note(y, 5, 1/16, vol))
#         else:
#             seq.append(Rest(1/16))
#     midi.seq_notes(NoteSeq(seq),track=y)
