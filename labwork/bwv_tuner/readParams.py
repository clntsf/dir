import numpy as np
import pandas as pd
import tkinter as tk; from tkinter import filedialog
root = tk.Tk(); root.withdraw()

noteLetters = {'C': 1, 'C#': 2, 'D': 3, 'D#': 4, 'E': 5, 'F': 6, 'F#': 7, 'G': 8, 'G#': 9, 'A': 10, 'A#': 11, 'B': 12}


def readParams():

	filepath = filedialog.askopenfilename()
	df = pd.read_excel(filepath, header=None).replace(np.nan, '')
	convertData =  type(df.iloc[0][0]) == str
	return [[noteLetters[item.upper()] if convertData else int(item) for item in list(df.loc[i]) if item != ''] for i in df.index]
	
print(readParams())
