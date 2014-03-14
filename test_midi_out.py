from improv import generate_solo
from mingus.midi import MidiFileOut
from mingus.containers import Bar

bar = generate_solo(["Am7"])[0]
MidiFileOut.write_Bar("test_bar.mid", bar)