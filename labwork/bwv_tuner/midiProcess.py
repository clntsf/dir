import pretty_midi as midi
import tkinter as tk; from tkinter import filedialog
import numpy as np; import pandas as pd
from math import ceil, floor, log

def toLetter(n):
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; out=''
    for i in range(floor(log(n,26)),-1,-1):out+=alphabet[floor(n/26**i)];n%=26**i
    return out

def toFreq(note): return 27.5*(2**((note-1)/12))

def adjust_freq(freq,scale):
	
    fkey=round(log(freq/27.5,2**(1/12)),0); octKey = int(fkey-(fkey-3)%12)
    below, octave, above = [toFreq(octKey-12+note) for note in scale], [toFreq(octKey+note) for note in scale], [toFreq(octKey+12+note) for note in scale]
    
    closest2 = [max([0]+[item for item in below+octave if 27.5<=item<=freq]), min([0]+[item for item in octave+above if freq<=item<=4187])]
    freqDist = [abs(freq - noteFreq) for noteFreq in closest2]
    
    return closest2[freqDist.index(min(freqDist))]

def tuneSheet(scale, filepath=None):
    
    interval = 15
	
    df = pd.read_excel(filepath); out_df = pd.DataFrame()
    df_first = df[df.columns[0]]; modlen=int(len(df_first)%interval)
    reps = int((len(df_first)-modlen)/interval+1); out_df['Time (ms)'] = df_first
    
    for formant in range(1,int((len(df.columns)-1)/2)+1):
        freq_col = df[df.columns[2*formant-1]]; amp_col = df[df.columns[2*formant]]
        out_column_1 = []; out_column_2 = []
        
        for i in range(reps):   
        	if i+1 < reps: out_column_1 += [freq_col[interval*i+j] * ceil(amp_col[interval*i+j]) for j in range(interval)]
        	else: out_column_1 += [freq_col[interval*i+j] * ceil(amp_col[interval*i+j]) for j in range(modlen)] + [0]*(interval-modlen)
        	nz=len(np.nonzero(out_column_1[interval*i:])[0]); adj_freq=0.0
        	if nz > 0: adj_freq = adjust_freq(sum(out_column_1[interval*i:])/nz, scale)
        	{out_column_2.append(item) for item in np.where(np.array(out_column_1[interval*i:])!=0, adj_freq, 0)}
            
        out_df[f'F{formant}'] = out_column_2[:len(df_first)]
        out_df[f'A{formant}'] = amp_col
        
    return out_df
   
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

def main():

	root=tk.Tk(); root.withdraw()
	filepath = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
	writer = pd.ExcelWriter('output.xlsx')
	
	for measure in getMelodyEvents():
		tuned = tuneSheet(measure, filepath)
		tuned.to_excel(writer, sheet_name=' '.join([str(item) for item in measure]), index=False)
	writer.save()
	
if __name__ == '__main__': main()