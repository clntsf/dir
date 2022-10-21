bwv = midi.PrettyMIDI('bach_846.mid')
downbeats = bwv.get_downbeats()

def getMelodyEvents():
	melody = bwv.instruments[0]
	notes = melody.notes
	measures = []
	
	for i in range(1,len(downbeats)):
		
		greaterThan = [(([note.start for note in notes]>=downbeats[i-1]) & ([note.start for note in notes]<downbeats[i]))]
		thisMeasure = [notes[i].pitch for i in range(len(notes)) if greaterThan[0][i] and notes[i].pitch not in [notes[j].pitch for j in range(i) if greaterThan[0][j]]]
		if len(thisMeasure) > 0: measures.append([item % 12 for item in thisMeasure])
		
	return measures