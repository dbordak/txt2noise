#!/bin/sh
rm *.mid *.wav mixed.ogg;
python3 txt2noise-double.py "cake pie cake pie cake pie" "cake pie cake pie cake pie"&&
for f in *.mid; do fluidsynth -nli -r 48000 -o synth.cpu-cores=2 -T wav -F ${f%.mid}.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 $f; done &&
sox -m *.wav mixed.ogg
