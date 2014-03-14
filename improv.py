"""
"""

from mingus.core import progressions, intervals, chords
from mingus.core.scales import ionian, aeolian, locrian, whole_note, mixolydian
from mingus.containers import NoteContainer, Note, Bar, Track, Composition
from mingus.midi import fluidsynth
import time, sys
import random
import math

solo_sound_font = "soundfont.sf2"

if not fluidsynth.init(solo_sound_font):
	print "Couldn't load soundfont", solo_sound_font
	sys.exit(1)

choose_scale = {'M' : ionian,
				'm' : aeolian,
				'dim' : locrian,
				'+' : whole_note,
				'7' : mixolydian,
				'm7': aeolian,
				'M7': ionian}

def generate_scale(chord_name):
	i = 1
	while chord_name[i] == 'b' or chord_name[i] == '#':
		i += 1
	return choose_scale[chord_name[i:]](chord_name[:i])


def random_bar(chord_name):
	scale = generate_scale(chord_name)
	bar = Bar()
	beat = 0
	while beat < 1:
		duration = random.choice([4, 8, 16])
		note = random.choice(scale)
		bar.place_notes(note, duration)
		beat = bar.current_beat
	return bar

def solo_bar(chord_name):
	scale = generate_scale(chord_name)
	# note = random.choice(chords.from_shorthand(chord_name))
	# note_index = scale.index(note)
	note_index = random.randrange(len(scale))
	note = scale[note_index]
	beat = 0
	duration = 1
	bar = Bar()
	while beat < 1:
		if beat % .25 == 0:
			duration = random.choice([4, 8, 16])
		stepwise = random.randrange(5) != 0
		rest = random.randrange(10) < 3
		if rest:
			bar.place_notes(None, duration)
		else:
			if stepwise:
				interval = random.choice([-1, 1])
			else:
				interval = random.randrange(len(scale))
			note_index = ((note_index+interval)+len(scale))%len(scale)
			note = scale[note_index]
			bar.place_notes(note, duration)
			print(note)
		beat = bar.current_beat
	print("---")
	return bar


def play_solo_bar_with_chord(chord_name):
	chord = NoteContainer(chords.from_shorthand(chord_name))
	solo = solo_bar(chord_name)
	fluidsynth.play_NoteContainer(chord, 13)
	fluidsynth.play_Bar(solo, 10)
	fluidsynth.stop_NoteContainer(chord, 13)

def play_example(key):
	progression = ["I", "vi", "ii", "iii7",
	       "I7", "viidom7", "iii7", "V7"]

	# key = 'C'
	
	chord_list = progressions.to_chords(progression, key)

	fluidsynth.set_instrument(13, 45)
	fluidsynth.set_instrument(10, 24)

	while True:
		for chord in chord_list:
			play_solo_bar_with_chord(chords.determine(chord, shorthand=True)[0])

# play_example('C')


def generate_solo(chord_list):
	notes = []
	bars = []
	note = random.choice(chords.from_shorthand(chord_list[0]))
	note = Note(note)
	syncopate = random.randrange(1) == 0
	bar = Bar()
	duration = random.choice([4, 8, 16])
	if syncopate:
		bar.place_notes(None, duration)
	bar.place_notes(note, duration)
	notes.append(note)
	first = True
	for chord_name in chord_list:
		if first:
			beat = bar.current_beat
			first = False
		else:
			bar = Bar()
			beat = 0
		scale = generate_scale(chord_name)
		while beat < 1:
			if beat % .25 == 0:
				duration = random.choice([4, 8, 16])
			elif beat % .125 == 0:
				duration = random.choice([8, 16])
			rest = random.randrange(10) == 0 # 1/10
			if rest:
				bar.place_notes(None, duration)
			else:
				beginning = beat == 0
				stepwise = random.randrange(5) != 0 # 4/5
				leap = random.randrange(2) == 0 # 1/2
				if len(notes) >= 2:
					prev_motion = measure_motion(notes[-2], notes[-1], scale)
				else:
					prev_motion = random.choice([-1, 1])
				direction = int(math.copysign(1, prev_motion))
				resolve = False
				
				if abs(prev_motion) == 2:
					if len(notes) >= 3:
						prev2_motion = measure_motion(notes[-3], notes[-2], 
								scale)
					else:
						prev2_motion = 0
					if prev2_motion == 2:
						if random.randrange(2) == 0:
							stepwise, leap = False, False
					else:
						stepwise, leap = False, False
				elif abs(prev_motion) > 2:
					stepwise, resolve = True, True
				
				if beginning:
					chord_tones = chords.from_shorthand(chord_name)
					note = closest_note(notes[-1], chord_tones)
				elif stepwise:
					if resolve:
						interval = -direction
					else:
						interval = random.choice([direction, direction, 
								-direction])
					# 2/3 probability to continue in same direction
					if notes[-1].octave <= 3:
						interval = 1
					elif notes[-1].octave >= 5:
						interval = -1
					note = note_at_interval(notes[-1], interval, scale)
				elif leap: # (1 - 4/5) * 1/2 = 1/10
					interval = random.choice([-1, 1]) \
							* random.choice(range(3, len(scale)))
					note = note_at_interval(notes[-1], interval, scale)
				else: # outlining a chord
					interval = 2 * direction
					note = note_at_interval(notes[-1], interval, scale)
				bar.place_notes(note, duration)
				notes.append(note)
			beat = bar.current_beat
		bars.append(bar)
		print(notes)
	return bars


def measure_motion(note1, note2, scale):
	interval = note1.measure(note2)
	direction = int(math.copysign(1, interval))
	if direction == 0:
		return 0
	if note1.name in scale and note2.name in scale:
		index1, index2 = scale.index(note1.name), scale.index(note2.name)
	else:
		index1, index2 = int(note1), int(note2)
	motion = index2 - index1
	while motion * direction < 0:
		motion += len(scale) * direction
	while interval * direction >= 12:
		motion += len(scale) * direction
		interval -= 12 * direction
	return motion

def note_at_interval(note1, interval, scale):
	if interval == 0:
		return Note(note1.name, note1.octave)
	direction = int(math.copysign(1, interval))
	if note1.name in scale:
		index2 = scale.index(note1.name) + interval
	else:
		index2 = 0
	octave_diff = 0
	
	while index2 < 0:
		octave_diff -= 1
		index2 += len(scale)
	while index2 >= len(scale):
		octave_diff += 1
		index2 -= len(scale)
	note2 = Note(scale[index2], note1.octave + octave_diff)
	# check = Note('C', max(note1.octave, note2.octave))
	# if check.measure(note1) >  0 and check.measure(note1) > 0:
	# 	note2.octave_up()
	# elif check.measure(note1) <  0 and check.measure(note1) < 0:
	# 	note2.octave_down()
	return note2

def closest_note(note1, chord):
	min_dist = 12
	note2 = None
	for tone in chord:
		tone = Note(tone, note1.octave)
		dist = abs(note1.measure(tone))
		if dist < min_dist: 
			min_dist = dist
			note2 = tone
	return note2


def play_smart_solo_over_chords(chord_list):
	fluidsynth.set_instrument(13, 45)
	fluidsynth.set_instrument(10, 108)

	fluidsynth.main_volume(13, 75)
	fluidsynth.main_volume(10, 100)
	
	solo = Track()

	bars = generate_solo(chord_list)
	for i in range(len(bars)):
		chord = NoteContainer(chords.from_shorthand(chord_list[i]))
		bar = bars[i]
		fluidsynth.play_NoteContainer(chord, 13)
		fluidsynth.play_Bar(bar, 10)
		fluidsynth.stop_NoteContainer(chord, 13)
		solo.add_bar(bar)
	return solo

def play_smart_example():
	progression = ["I", "vi", "ii", "iii7",
	       "I7", "viidom7", "iii7", "V7"]

	key = 'C'

	chord_list = progressions.to_chords(progression, key)
	for i in range(len(chord_list)):
		chord_list[i] = chords.determine(chord_list[i], shorthand=True)[0]
		# print(chord_list[i])
	while True:
		play_smart_solo_over_chords(chord_list)

# play_smart_example()

def test_instruments():
	for i in range(150):
		fluidsynth.set_instrument(13, 45)
		fluidsynth.set_instrument(10, i)
		print("Instrument number: {0}".format(i))
		play_smart_solo_over_chords(['Cm'])

# test_instruments()
