import tkinter as tk; from tkinter import filedialog
import numpy as np; import pandas as pd
from math import ceil, log


# READS THE CONTENTS OF THE INPUTTED FILEPATH, AVERAGES THEM IN SLICES, AND TUNES THEM TO THE SPECIFIED SCALE IF DESIRED

def tuneSheet(filepath, interval, musicalize, scale):

	toFreq = lambda note: 27.5*(2**((note-1)/12))																								# Equation to convert note number to frequency
	
	df = pd.read_excel(filepath); outDf = pd.DataFrame()																					# Gets DataFrame from the given filepath and creates the output DataFrame
	dfRowLen, dfColLen = len(df.index), len(df.columns)																					# Gets horizontal and vertical length of the inputted DataFrame
	
	for formant in range(df.columns[0]):																											# Runs program loop for each formant (Number in cell 1 of the sheet)
		
		freqCol = df.columns[2*formant+1]																												# Specifies column for formant frequency values
		ampCol = df.columns[2*formant+2]																												# Specifies column for formant amplitude values
		newFreqCol = []																																			# Makes a new empty list for the altered frequencies
		
		for place in range(0,dfRowLen, interval):																									# Operates on each vertical slice of the formant, length specified by interval variable
			
			freqList = df[freqCol][place:min([dfRowLen, place+interval])]																		# Gets the frequency values in the slice
			ampCeils = [ceil(item) for item in df[ampCol][place:min([dfRowLen, place+interval])]]								# Gets the amplitude values in the slice, then gets the ceiling of each of those
			
			if sum(ampCeils) > 0:																																	# Checks whether any amplitude value in the slice is greater than zero
			
				rangeFreq = np.dot(freqList, ampCeils)/sum(ampCeils)																				# Gets the range frequency by averaging all frequency values with non-zero amplitude values
				
				if musicalize:																																				# Checks if the user wants to tune their results to music or not
					
					fkey=round(log(rangeFreq/27.5,2**(1/12)),0)																								# Gets the 'key' value of the range frequency
					octKey = int(fkey-(fkey-3)%12)																													# Gets the key value of the nearest octave start below that 
					 
					octave = [toFreq(octKey+note) for note in scale]																						# Makes a list of all the valid key values in the range frequency's octave, converted to frequencies
					lowerOctave = [toFreq(octKey-12+note) for note in scale]																			# Does the same for the octave below, in case the range frequency is below those of all valid notes in its octave
					higherOctave = [toFreq(octKey+note+12) for note in scale]																		# Does the same for the octave above, in case the range frequency is above the top of its octave

					closestBelow = max([0]+[item for item in lowerOctave + octave if 27.5<=item<=rangeFreq])					# Gets the closest frequency below the range frequency, or zero if the range frequency is lower than 27.5 (low A)
					closestAbove = min([4186] + [item for item in octave + higherOctave if rangeFreq<=item<=4187])			# Gets the closest frequency above the range frequency, or 4186 (high C) if the frequency is too high to be tuned
					
					rangeFreq = closestBelow if closestAbove - 2 * rangeFreq + closestBelow < 0 else closestAbove			# Sets the range frequency to the closer of the two frequencies found above
				
			else: rangeFreq = 0																																			# If there were no frequency values with non-zero amplitude values for that formant, set the range frequency to zero
		
			newFreqCol += [rangeFreq]*min([interval, dfRowLen-place])																		# Adds the cells tuned to the new range frequency to the new frequency column for that formant
		
		outDf[freqCol] = newFreqCol																														# Adds the altered frequency column to the output DataFrame
		outDf[ampCol] = df[ampCol]																														# Adds the original amplitude column to the output DataFrame
			
	return outDf																																					# Returns the output DataFrame when the process is completed for all formants


# READ TUNING PARAMETERS FROM EXCEL FILE IN NUMBER OR NOTE FORM

noteLetters = {'C': 1, 'C#': 2, 'D': 3, 'D#': 4, 'E': 5, 'F': 6, 'F#': 7, 'G': 8, 'G#': 9, 'A': 10, 'A#': 11, 'B': 12} 							# Dictionary for converting string-form notes to numbers

def readParams():																																							# Reads tuning params from excel sheet, and returns a list of lists
	print('SELECT PARAMETER FILE')
	
	filepath = filedialog.askopenfilename()																															# Gets filepath from tkinter's built-in filepicker
	df = pd.read_excel(filepath, header=None).replace(np.nan, '') 																						# Reads df from filepath and removes empty spaces
	convertData =  type(df.iloc[0][0]) == str																															# Checks whether the file is in string or number form
	return [[noteLetters[item.upper()] if convertData else int(item) for item in list(df.loc[i]) if item != ''] for i in df.index]		# Returns the properly formatted list of lists

def tuneByParams(filepath, params, interval, musicalize, together=True):																						# Tunes a sheet by its parameters
	
	tunedDfs = [tuneSheet(filepath, interval, musicalize, scale) for scale in params]
	
	if together:
		fullDf =  pd.concat(tunedDfs, ignore_index=True)
		return [fullDf], ['output']
	else: 
		sheetNames = [' '.join([str(item) for item in params[i]]) for i in range(len(params))]
		return tunedDfs, sheetNames

def main():

	root=tk.Tk(); root.withdraw()
	print('SELECT FILE TO BE TUNED')
	filepath = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
	
	musicalize = input('Tune frequencies (y/n)? ') == 'y'
	together = input('Output to a single sheet (y/n)? ') == 'y'
	interval = int(input('Sampling Interval (x10ms): '))
	
	params = [lambda: [None], readParams][musicalize]()
		
	dfs, sheetNames = tuneByParams(filepath, params, interval, musicalize, together)
	headers = ['' for item in dfs[0].columns]
	
	with pd.ExcelWriter('output.xlsx') as writer:
		
		for i in range(len(sheetNames)):
			
			timestamps = pd.DataFrame(data={str(int(len(dfs[i].columns)/2)): [10*j for j in range(len(dfs[i]))]})
			headers = [int(timestamps.columns[0])] + headers
			
			outDf = pd.concat([timestamps, dfs[i]], axis=1, ignore_index=True)
			outDf.to_excel(writer, sheet_name = sheetNames[i], index=False, header = headers)

	
if __name__ == '__main__': main()