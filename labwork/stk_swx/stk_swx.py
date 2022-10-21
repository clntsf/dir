#! /usr/bin/env python3
import pandas as pd
import numpy as np
from io import StringIO
import tkinter as tk
from tkinter import filedialog
import sys; from subprocess import run

# --- Config --- #
formants = 4
desired_cols=['f0','f1','a1f','f2','a2f','f3','a3f','f4','a4f']
amp_cols = ['a1f','a2f','a3f','a4f']
multipliers = [.7,.4,.2,.1]

def tuneFile(filepath, cleanFilepath):
	global formants, desired_cols, amp_cols, multipliers

	# --- Read .stk file, and take the info to a dataframe --- #
	with open(filepath, 'r') as reader:
		file_content = ''.join(reader.readlines()[8:])
		df = pd.read_csv(StringIO(file_content), sep='\t')[desired_cols]

	# --- Tune amplitude vals --- #
	amp_max = [max(df[col]) for col in amp_cols]
	for i in range(formants):
		ampcol = amp_cols[i]
		df[amp_cols[i]] = np.where(df[amp_cols[i]] > 30, multipliers[i]/df[amp_cols[i]]*amp_max[i], 0)

	# --- Format df column names and timestamp column --- #
	df.columns = [formants]+['']*8
	df[formants] = [10*i for i in range(len(df.index))]

	# --- Get filepath to write to and sanitized filepath for terminal --- #
	outFilepath = filepath[:filepath.rfind(".")]

	# --- Write to .tsv, then manually convert to .swx --- #
	df.to_csv(f'{outFilepath}.tsv', index=False, sep='\t')
	run(['mv', f'{cleanFilepath}.tsv', f'{cleanFilepath}.swx'], capture_output=False)

	return outFilepath

def sanitizeFilepath(filepath):
	temp = filepath
	for n in ['\\',"'",' ','"']: temp = temp.replace(n, f'\{n}')
	return temp

def convertSingle():
		filepath=filedialog.askopenfilename(filetypes=[('','.stk')])
		cleanFilepath = sanitizeFilepath(filepath)[:-4]

		outFilepath = tuneFile(filepath, cleanFilepath)
		print('\n'+f'File written to {outFilepath}.swx.')
		cleanFilepath+='.swx'

def main():
	# --- Get filepath to .stk file --- #
	root = tk.Tk(); root.withdraw()
	if 'folder' in sys.argv:
		filepath = filedialog.askdirectory()
		cleanFilepath = sanitizeFilepath(filepath)

		filesInDir = str(run(['ls', cleanFilepath], capture_output=True).stdout)[2:-1].split('\\n')[:-1]
		operableFiles = [file for file in filesInDir if '.stk' in file]

		for file in operableFiles:
			fileClean = sanitizeFilepath(file)
			tuneFile(f'{filepath}/{file}', f'{cleanFilepath}/{fileClean[:-4]}')

		print('\nCompatible files have been successfully converted')

	else:
		convertSingle()


	# --- Display completion message, open .swx file/dir if user chooses --- #
	if input('Open Output? (y/n): ').lower() == 'y':
		run(['open', cleanFilepath], capture_output=False)

if __name__ == '__main__': main()