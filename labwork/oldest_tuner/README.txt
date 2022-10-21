
IMPORTANT: For use of the program, place this file 
and its enclosing package on your Desktop

1. Open a new terminal window

2. Look at the top of your window. There sits your shell type:
zsh, sh, bash, etc. If your profile type is not zsh, copy and paste the following into your terminal window:

chsh -s /bin/zsh

3. Copy the following lines 1 by 1 into your terminal window:

nano ~/.zprofile

4. Move the cursor down to a free space in the text that
appears, and paste the following:

alias tuner="python3 Desktop/Sinewave\ Tuner/tuner.py"

5. Hit CTRL+X, then y, then enter

6. Close and reopen your terminal window

7. If done correctly, these actions should allow you to type the word 'tuner' into the command line at any time and open the Musicalization App.

8. If the app does not work, chances are that wxPython, a non-native module of python, is not installed on your device. If you have PIP installed, enter the following:

pip install wxPython

or, for pip3 (if pip is installed but terminal does not recognize 'pip' command);

pip3 install wxPython

