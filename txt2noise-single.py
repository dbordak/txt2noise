#!/usr/bin/python3

import sys
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from PIL import ImageFont, ImageDraw, Image

font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf", 12)

sentence = sys.argv[1]
instrument_high = 25
instrument_low = 1

image = Image.new("L", (800,12))
draw = ImageDraw.Draw(image)
draw.text((0, -1), sentence, font=font, fill="white")

notes_list_high = []
notes_list_low = []
for x in range(0,800):
    notes = []
    for y in range(0,12):
        vol = int(image.getpixel((x, y))/2)
        if vol == 127:
            continue
        if vol:
            notes.append(Note(y, 5, 1/16, vol))
    if len(notes):
        seq = NoteSeq(notes)
        notes_list_high.append(NoteSeq(notes[0].harmonize(seq)))
        if len(notes) > 1:
            notes_list_low.append(NoteSeq(notes[len(notes)-1].harmonize(seq)))
        else:
            notes_list_low.append(Rest(1/16))
    else:
        notes_list_high.append(Rest(1/16))
        notes_list_low.append(Rest(1/16))

midi = Midi(tempo=90, instrument=instrument_high)
midi.seq_chords(notes_list_high)
midi.write("test-high.mid")

midi = Midi(tempo=90, instrument=instrument_low)
midi.seq_chords(notes_list_low)
midi.write("test-low.mid")

