import numpy as np
import pandas as pd
from math import ceil
import tkinter as tk; from tkinter import filedialog
root = tk.Tk(); root.withdraw()

noteLetters = {'C': 1, 'C#': 2, 'D': 3, 'D#': 4, 'E': 5, 'F': 6, 'F#': 7, 'G': 8, 'G#': 9, 'A': 10, 'A#': 11, 'B': 12}


def readParams():

	filepath = filedialog.askopenfilename()
	df = pd.read_excel(filepath)
	
	formants = int(df.columns[0])
	rowLen = len(df.index)
	
	freqCols = {i: list(df[df.columns[2*i+1]]) for i in range(formants)}
	ampCols = {i: [ceil(item) for item in list(df[df.columns[2*i+2]])] for i in range(formants)}
	freqAmpCross = [freqCols[i] * ampCols[i]
	
	
readParams()
	