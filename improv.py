"""
"""

from mingus.core import progressions, intervals, chords
from mingus.core.scales import ionian, aeolian, locrian, whole_note, mixolydian
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time, sys
from random import random

choose_scale = {'M' : ionian,
				'm' : aeolian,
				'o' : locrian,
				'+' : whole_note,
				'7' : mixolydian,
				'm7': aeolian,
				'M7': ionian}

def generate_scale(chord_name):
	return choose_scale[chord_name[1:]](chord_name[:1])