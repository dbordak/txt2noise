#!/usr/bin/python3

import sys
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from PIL import ImageFont, ImageDraw, Image

font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf", 12)

sentence = sys.argv[1]
instrument_high = 8
instrument_low = 0
instrument_secondary = 9

image = Image.new("L", (800,12))
draw = ImageDraw.Draw(image)
draw.text((0, -1), sentence, font=font, fill="white")
image.save("test.bmp")

image2 = Image.new("L", (800,12))
draw2 = ImageDraw.Draw(image2)
draw2.text((0, -1), sentence, font=font, fill="white")

noping = 2
backup_list = []
for x in range(0,800):
    backup = []
    for y in range(0,12):
        vol = int(image2.getpixel((x, y))/2)
        if vol and vol != 127:
            backup.append(Note(y, 4, 1/16, int(vol*.7)))
    if len(backup):
        noping = 0
        backup_list.append(backup)
    else:
        noping += 1
        if noping == 2:
            backup_list.append(None)

notes_list_high = []
notes_list_low = []
notes_list_backup = []
backup_running = -1
for x in range(0,800):
    notes = []
    backup = []
    for y in range(0,12):
        vol = int(image.getpixel((x, y))/2)
        if vol and vol != 127:
            notes.append(Note(y, 5, 1/16, vol))
    if len(notes):
        seq = NoteSeq(notes)
        notes_list_high.append(NoteSeq(notes[0].harmonize(seq)))
        if len(notes) > 1:
            notes_list_low.append(NoteSeq(notes[len(notes)-1].harmonize(seq)))
        else:
            notes_list_low.append(Rest(1/16))
        if backup_running <= 1:
            notes_list_backup.append(Rest(1*(backup_running + 1)/16))
            backup_running = 0
    else:
        backup_running += 1
        notes_list_high.append(Rest(1/16))
        notes_list_low.append(Rest(1/16))
    if backup_running > 1:
        backup_running = 2
        if len(backup_list) and backup_list[0]:
            bnote = NoteSeq(backup_list[0][len(backup_list[0]) - 1].harmonize(NoteSeq(backup_list[0])))
            notes_list_backup.append(bnote)
        else:
            backup_running = 0
            notes_list_backup.append(Rest(1/16))
        backup_list = backup_list[1:]

midi = Midi(tempo=90, instrument=instrument_high)
midi.seq_chords(notes_list_high)
midi.write("test-high.mid")

midi = Midi(tempo=90, instrument=instrument_low)
midi.seq_chords(notes_list_low)
midi.write("test-low.mid")

midi = Midi(tempo=90, instrument=instrument_secondary)
midi.seq_chords(notes_list_backup)
midi.write("test-backup.mid")
