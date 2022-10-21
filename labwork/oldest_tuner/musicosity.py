import pandas as pd
from pandas import ExcelWriter
import numpy as np; import openpyxl                             # Imports
from math import ceil, floor, log
import matplotlib.pyplot as plt

fig,ax=plt.subplots()

notes_dict = {                                                  # Dictionary which matches notes on the chromatic scale to their number in order.
            'C':1, 'C#':2, 'D':3, 'D#':4, 'E':5, 'F':6,
            'F#':7, 'G':8, 'G#':9, 'A':10, 'A#':11, 'B':12
            }
scales_dict = {                                                 # Dictionary which outlines scales based on the notes they contain, numbered.
            'C Major':[1,3,5,6,8,10,12],'D Major':[2,3,5,7,8,10,12],'E Major':[2,4,5,7,9,10,12], # Can be easily modified to add new scales.
            'F Major':[1,3,5,6,8,10,11],'G Major':[8, 10, 12, 1, 3, 5, 6],
            'A Major':[10, 12, 1, 3, 5, 6, 8], 'B Major':[12, 1, 3, 5, 6, 8, 10],'Black Notes Only':[2,4,7,9,11]
            }

def add_custom_scale(notes):                                    # Creates a custom entry into the dictionary of scales, containing a list of notes.
    scales_dict['Custom Scale'] = list(notes)                   # Used in conjunction with the Note Selection mode of the tuner app, in order to
    return 'Custom Scale'                                       # tune the inputted spreadsheet to a custom 'scale' of only selected notes.
                                                                
def number_to_letter(number):                                   # Miscellaneous function used to convert numbered excel rows/columns to letters,
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'                      # as openpyxl's sheet.column_dimensions does not support number-form columns.
    outStr = ''
    while number > 0:
        i = 0
        while 26**(i+1) < number:
            i+= 1
        outStr += (letters[floor(number/(26**i))-1])
        number -= floor(number/(26**i))*26**i
    return(outStr)

def adjust_freq(freq,scale):                                    # Function that rounds the input frequency to the nearest piano note, and then to the
    number = round(log(freq/27.5,2**(1/12)),0)                  # nearest note in the scale by passing it through an equation which is documented elsewhere.
    note = (number-2)%12
    scale_notes_freq = [27.5*((2**(1/12))**(number-note-item)) for item in scales_dict[scale] if 0 <= number-note-item <= 87][::-1] + [27.5*((2**(1/12))**(number-note+item)) for item in scales_dict[scale]  if 0 <= number-note+item <= 87]
    comp_freq_and_notes = [abs(freq - item) for item in scale_notes_freq]
    return scale_notes_freq[comp_freq_and_notes.index(min(comp_freq_and_notes))]

def return_edited_column_by_formant_interval_scale(df,out_df,formant,interval,scale):   # The largest function in this program. This takes input dataframe
    df_first = df[[column for column in df][0]]; out_df['Time (ms)'] = df_first         # and fully adjusts it to the selected scale. Fully documented elsewhere. 
    out_column_1 = []; out_column_2 = []; interval_avg = 0
    freq_col = df['F'+str(formant)]; amp_col = df['A'+str(formant)]
    
    for i in range(0,int(round(len(df_first)/interval,0))):     # Averages and adjusts the frequencies in the spreadsheet dataframe where relevant, and then puts
        for j in range(0,interval):                             # the values back into their places, returning zero if the entire interval is zero (error is raised
            if i*interval+j < len(df_first):                    # due to how the program processes the frequencies and amplitudes).
                out_column_1.append(freq_col[i*interval+j] * ceil(amp_col[i*interval+j]))
        try:
            interval_avg = sum([item for item in out_column_1[i*interval:] if item != 0]) / len([item for item in out_column_1[i*interval:] if item != 0])
            adjusted_freq = adjust_freq(interval_avg,scale)
        except ZeroDivisionError:
            interval_avg = adjusted_freq = 0.0
        for item in np.where(np.array(out_column_1[i*interval:])!=0,adjusted_freq,freq_col[i*interval:(i+1)*interval]):
            out_column_2.append(item)
        color = f"{['b','g','r','y'][formant-1]}-"
        ax.plot([i*interval+k for k in range(len(out_column_1[i*interval:])) if amp_col[i*interval+k] != 0], [adjusted_freq for k in range(len(out_column_1[i*interval:])) if amp_col[i*interval+k] != 0],color)
            
    out_df['Note-Adjusted '+str(formant)+ 'Values'] = out_column_2  # Completely formats the newly-created column, copies the old dataframe's amplitude values,
    out_df['A'+str(formant)] = df['A'+str(formant)]                 # and returns both columns as a dataframe to be added to the new spreadsheet.
    return out_df

def handle_filetype(file):                                      # Shell function for filetype handling. Not yet instrumented.
    pass

def main(file='',scale='',interval=0):                          # The code's main function. Takes user input if run directly, reads the excel sheet with pandas,
    if file=='' and scale=='' and interval == 0:                # runs the necessary functions and then writes the values to an output sheet.
        scale = input('Scale (Ex. "C", Only non-sharp/flat Maj. scales supported at the moment): ')
        interval = int(input('Interval (in 10s of ms (i.e. 10 -> 100ms interval)): '))
        file = input('Filepath: ')
    if type(scale)==list:
        scale = add_custom_scale(scale)
    df = pd.read_excel(file)
    out_df = pd.DataFrame()
    
    for i in range(1,[column for column in df][0]+1):
        out_df = return_edited_column_by_formant_interval_scale(df,out_df,i,interval,scale)
    
    with ExcelWriter('output_sheet.xlsx',engine='xlsxwriter') as writer:
        out_df.to_excel(writer, sheet_name='output')

    workbook = openpyxl.load_workbook('output_sheet.xlsx')
    sheet = workbook.active
    for i in range(1,len([column for column in out_df])+1):
        sheet.column_dimensions[number_to_letter(i+1)].width = 20
    workbook.save('output_sheet.xlsx')
    plt.show()

if __name__ == '__main__':                                      # Self-explanatory, runs the main function on startup if the file is called directly.
    main()                                                      # Otherwise, it waits, and allows it to be called manually by the tuner app.
