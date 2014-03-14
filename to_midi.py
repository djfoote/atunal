from mingus.core import chords, intervals, notes, scales 
from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.containers.Instrument import MidiInstrument
from mingus.midi import MidiFileOut
from improv import generate_solo
from subprocess import call

num_progressions = 4
chords_list = ['CM', 'G7', 'CM7', 'FM7', 'G7', 'Am7', 'G7', 'C#+']
chords_bars = []
for chord in chords_list:
	chord_nc = NoteContainer(chords.from_shorthand(chord))
	bar = Bar()
	bar.place_notes(chord_nc, 1)
	chords_bars.append(bar)
solo_track = Track()
chords_track = Track()
for _ in range(num_progressions):
	for bar in generate_solo(chords_list):
		solo_track.add_bar(bar)
	for bar in chords_bars:
		chords_track.add_bar(bar)

guitar = MidiInstrument()
guitar.instrument_nr = 26
solo_track.instrument = guitar

piano = MidiInstrument()
piano.instrument_nr = 0
chords_track.instrument = piano

song = Composition()
song.add_track(solo_track)
song.add_track(chords_track)

MidiFileOut.write_Composition("test.mid", song)

filename = "test.mid"
call("timidity -Ow {0}".format(filename), shell=True)
# fluidsynth -F test.wav -i -n -T wav soundfont.sf2 test.mid