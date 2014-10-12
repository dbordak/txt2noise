#!/bin/sh
rm *.mid mixed.ogg;
python3 txt2noise.py "revan is a butt" "i like pie" "get gud scrub" "i am the pootisman" "i love horses; best of all the animals" &&
for f in *.mid; do timidity $f -Ow; done &&
sox -m *.wav mixed.ogg
