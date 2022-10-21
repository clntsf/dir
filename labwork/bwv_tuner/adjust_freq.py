from math import ceil, log
import pandas as pd; import numpy as np

def tuneSheet(scale, filepath, musicalize):
	
	interval = 15
	toFreq = lambda note: 27.5*(2**((note-1)/12))											# Equation to convert note number to frequency
	
	df = pd.read_excel(filepath); outDf = pd.DataFrame()								# Gets dataframe from the given filepath and creates the output dataframe
	outDf[df.columns[0]] = df[df.columns[0]]													# Adds the first column of the inputted dataframe (timestamps) to the output df
	dfRowLen, dfColLen = len(df.index), len(df.columns)								# Gets horizontal and vertical length of the inputted dataframe
	
	for formant in range(df.columns[0]):
		
		freqCol = df.columns[2*formant+1]
		ampCol = df.columns[2*formant+2]
		newFreqCol = []
		
		for place in range(0,dfRowLen, interval):
			
			freqList = df[freqCol][place:min([dfRowLen, place+interval])]
			ampCeils = [ceil(item) for item in df[ampCol][place:min([dfRowLen, place+interval])]]
			
			if sum(ampCeils) > 0:
			
				rangeFreq = np.dot(freqList, ampCeils)/sum(ampCeils)
				
				if musicalize:
					
					fkey=round(log(rangeFreq/27.5,2**(1/12)),0)
					octKey = int(fkey-(fkey-3)%12)
					
					lowerOctave = [toFreq(octKey-12+note) for note in scale] 
					octave = [toFreq(octKey+note) for note in scale]
					higherOctave = [toFreq(octKey+note+12) for note in scale]
				
					closestBelow = max([0]+[item for item in lowerOctave + octave if 27.5<=item<=rangeFreq])
					closestAbove = min([4186] + [item for item in octave + higherOctave if rangeFreq<=item<=4187])
					
					rangeFreq = closestBelow if closestAbove - 2 * rangeFreq + closestBelow < 0 else closestAbove
					
				newFreqCol += [rangeFreq]*min([interval, dfRowLen-place])
				
			else: newFreqCol += [0]*min([interval, dfRowLen-place])
		
		outDf[freqCol] = newFreqCol
		outDf[ampCol] = df[ampCol]
			
	return outDf
