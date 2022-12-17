# /ctsf1/dir
_Directory/Portfolio of past projects_

A landing page of sorts, with a directory and overview portfolio-style of the projects I've uploaded to github (and beyond)

---

### Table of Contents

 1. [Lab work: the _spl_widgets_ package](#lab-work-the-splwidgets-package)

    1. [Initial Specifications and Context](#initial-specifications-and-context)
    2. [Early Development](#early-development)
    3. [Packaging](#packaging)
        1. [tuner](#tuner)
        2. [stk-swx](#stk-swx)
        3. [gorilla-clean](#gorilla-clean)
        4. [jukemake]()

 2. [Snake Five (and counting) Ways](#snake-five-and-counting-ways)

    1. [Python (with Pygame)](#python-with-pygame)
    2. [C++ (with ncurses)](#c-with-ncurses)
    3. [Rust (with Glutin, Piston2d and OpenGL)](#rust-with-glutin-piston2d-and-opengl)
    4. [HTML/CSS/JS (with JS Canvas)](#htmlcssjs-with-js-canvas)
    5. [Java (with AWT and Swing)](#java-with-awt-and-swing)

 3. [School Python Projects](#school-python-projects)

    1. [ALT4: Hardware Interfacing](#alt4-hardware-interfacing)
    2. [ALT2: Data Visualisation and analysis](#alt2-data-visualisation-and-analysis)
    3. [ALT3: Modelling and Simulation](#alt3-modelling-and-simulation)

---

## Projects

These are arranged categorically, not in chronological order. I have tried, however, to sort items within a category by the order in which I completed them where I can

### Lab work: the [*spl_widgets*](https://pypi.org/project/spl-widgets/) package

Since the summer of 2019 I have been working at the Barnard Speech Perception Laboratory in various capacities, most recently in developing a series of in-house tools to enable (or streamline) the use of a variety of common lab tasks as well as experimental transformations required for the testing of research hypotheses. A summary of these modules and a brief timeline of the work I have done is as follows:

 - #### Initial specifications and context

    In the fall of 2020 I reapplied for a work placement at the lab for that November, and as part the work I would do that week I was asked to implement a mathematical transformation for files containing a type of synthesised speech.

    The specifics of the transformation are as such - Given an input of a series of notes from the user and an averaging slice size, average the frequencies in the file in blocks of the given size and then "tune" these averaged frequencies to the closest note in that set on an 88-key keyboard.

    This transformation had been created in concept by Professor Remez, who wanted to use it to create samples that could be simultaneously perceived as speech and music to explore the nature of a perceptual phenomenon known as auditory bistability, but the project had been shelved due to the impracticality (over an hour for a single three-second file) of applying it manually at the scale needed. As such, I was asked to create a mock-up of a process implementing it algorithmically to explore the feasibility of the experiment and potentially continue developing it given positive results.

 - #### Early Development

    In the beginning, the specifics of what was required were not yet established as the transformation I was developing was a new one (It would have been almost impossible to apply by hand and so no tests had ever been run with it) so development began with small, individual scripts.
    
    First among these was the script [musicosity.py](labwork/oldest_tuner/musicosity.py) which was created during my work placement week in November as a proof-of-concept for a feasible way to apply the transformation at scale. This script performed the transformation on an inputted .xlsx file and outputted it to a new one, plotting also the adjusted frequencies using the matplotlib.pyplot module.

    With the positive results yielded by this proof-of-concept I continued working even after the end of my placement week, and by the end of November I had created a basic UI using wxPython that allowed a user to input their .xlsx file, tuning interval and desired notes and opened the tuned file at the press of a button.

    In 2021 I continued work on tuner, making a [demo](labwork/bwv_tuner) (mostly as a showpiece to sell the viability of the project) to tune a file to the notes of each arpeggio in Bach's _The Well-Tempered Clavier_. I also designed more processes to streamline or automate tedious tasks in the production of these samples, such as implementing a [file conversion process](labwork/stk_swx/stk_swx.py) (now _spl_widgets.stk_swx.py_) which previously had to be done by hand and making a [script](https://github.com/ctsf1/gorilla) (now _spl_widgets.gorilla_clean.py_) to parse and clean survey data returned from the online subject testing service Gorilla (used due to pandemic restrictions on live testing).

- #### Packaging

    By late 2021 the various scripts I had developed had become cumbersome to continuously update and maintain remotely, and the slapdash shell scripts I had written to remedy this were too unwieldy to be a permanent solution, so I began to look into packaging python modules. I created the first version of the [spl_widgets](https://pypi.org/project/spl-widgets/) package in November of 2021, and as I grew more comfortable using and updating packages I updated a [github repository](https://github.com/ctsf1/spl_widgets) with its contents in parallel, and continued to add functionality, as long as any scripts I developed for use in the lab.

    The scripts currently included in *spl_widgets* are as follows:

    - #### Tuner
    
        My original project in the lab, now two years on. It now has an improved, feature-complete UI, along with a companion script [*batch_tune.py*](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/batch_tune.py) which allows for rapid bulk-volume tuning using parameter configuration files.

        (Multiple files make up the entirety of Tuner: [_tuner.py_](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/tuner.py) contains the user interface, [_tune_freq.py_](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/tune_freq.py) contains the main body of the tuning transformation, and [_misc_util.py_](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/misc_util.py) contains various helper functions for both)

    - #### [stk-swx](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/stk_swx.py)

        The file conversion process I wrote to eliminate the need to manually convert .stk files (outputted by SynthWorks) to tunable .swx files to be played in MATLAB.

    - #### [gorilla-clean](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/gorilla_clean.py)

        A script to parse and clean subject data from the Gorilla online subject testing service (returned as a .zip archive of multiple excel files). Updated to allow for the creation and modification of a configuration file so a user can adapt the parser for the data returned by the specific task without having to edit the source.

    - #### [jukemake](https://github.com/ctsf1/spl_widgets/tree/master/src/spl_widgets/jukemake.py)

        A helper script to take a series of timings and a directory of .wav files specified by the user and convert it to a parameter file able to be interpreted by the MATLAB routine Jukebox, used for the preparation of a testing condition of a set of samples.

---

### Snake Five (and counting) Ways
   
It's become somewhat of a ritual for me to write a Snake game in languages I pick up as a first 'big project'. The relatively simple implementation of game rules and low graphical requirements make for an ideal beginner project, especially given that in doing so I learn about the language's approach to user input, rendering a simple window (or printing graphics to a terminal), constructing a working game loop and implementing more complex  logic, skills that are foundational to most other intermediate/advanced techniques in CS. This series of incarnations mostly encapsulates my journey through CS, and through each I gained a rewarding understanding of new concepts and techniques.

- #### [Python](/snake_5_ways/Python) (with Pygame)
    - My first major project in Computer Science, undertaken in winter 2020. Before this I'd never dabbled in graphics in any language, so the Pygame module was a massive help in making the process beginner-friendly. There are definitely some sharp corners, but it carries a lot of nostalgia for me and I'm quite proud of it, especially considering it was the first of its kind. (November 2020)

- #### [C++](/snake_5_ways/cpp) (with ncurses)
    - After getting comfortable with basic CS concepts in Python, I took the leap of exploring lower-level languages. While C was a bit too daunting for me at the time, C++ had a lot more beginner-friendly documentation and tutorials on sites like stackoverflow so I worked my way up to a text-based version of the game, using the ncurses Window class and its methods to print colored text to the terminal to display the game window. (September 2021)

        (_as a warning to any potential downloaders, a mistake exists in the source (in the creation of a local file to save user highscore) which creates a new file in the user's CWD when the script is called instead of finding the one in a directory relative to the script. this doesn't affect the performance of the game in any way, but creates annoying clutter_)

- #### [Rust](https://github.com/ctsf1/rust-snake) (with Glutin, Piston2d and OpenGL)
    - A while passed before I picked up any more new languages, mainly because I was busy with the beginnings of developing what would become [spl_widgets](). At this stage, I had become acquainted with Github, so most of my large projects were uploaded there, this one included. Learning rust was a very new experience given its unique nature (namely, its use of a borrow-checker) but a very rewarding one as well, as I was forced to seriously consider my actions in a way even beyond what I was used to in C++. The amount of documentation (cargo's built-in docs feature, specifically) was a massive help, though, and with it I made my most polished version yet using Piston2d, Glutin and OpenGL to display the window. (May 2022)

- #### [HTML/CSS/JS](https://github.com/ctsf1/canvas_games) (with JS Canvas)
    - I had been experimenting with HTML and CSS for a while, and had written little curiosities in JS (like one to generate and style a Minesweeper grid), but had never really combined the two. JS's tools for drawing to HTML Canvas Elements are quite well-documented, and given the much more lax nature of JS (comparatively), building Snake was a much more relaxed experience. Looking for a greater challenge I also tried to implement a version of the popular web game 2048, the logic for which is quite involved and provided a good stimulus for me to improve my grasp of control flow. (June and July 2022)

        _I've created a Github Pages site for this repository to allow for easy access without downloads. Snake can be played [here](https://ctsf1.github.io/canvas_games/snake/snake.html), and 2048 [here](https://ctsf1.github.io/canvas_games/2048/2048.html)_

- #### [Java](/snake_5_ways//Java) (with AWT and Swing)
    - More recently I've been experimenting with Java, partly in an attempt to fill in some OOP concepts I missed out on in Python and C++. The Object Oriented style was foreign to me initially, having come from at least partially functional programming languages, but I completed a series of learning exercises covering different concepts and developed the confidence to tackle the project of making Snake. With the assistance of the (thankfully) well-documented modules Swing and AWT to render the screen, and implementing the KeyListener class to process user input, this version is arguably the most refined so far.
    (June, September 2022)

        _The linked folder contains a subfolder 'cls' with .class files able to be executed (after download) with "cd cls && java Snake"_

---

### School Python Projects
Throughout my time in Leaving Cert Computer Science I have completed several projects (called Applied Learning Tasks, or ALTs) in Python, both individually and collaboratively, each with a different focus. As most* of these have a comprehensive README along with them I won't explain them in redundant detail, but a brief summary of each is attached along with a link (click the title) to its repository.

The complexity of these projects started low as the class is intended to be introductory, but later projects were quite demanding in terms of the technical requirements attached and provided for a good challenge.

<small><i>*alt3_lotto and alt3_coinflip do not have README files as the project brief only requested one of the three tasks be completed, and I did the other two mostly for some practice. I will describe these along with alt3_diceroll (the project I chose)</i></small>

- #### [ALT4](https://github.com/ctsf1/halloween_lights): Hardware interfacing
    - I worked in a group of three to interface with a BBC MicroBit using Python and the MicroPython module and design a halloween-themed artefact - Our group chose to program a sound/proximity-activated strip of lights that fluctuated between shades of orange

- #### [ALT2](https://github.com/ctsf1/data_sci): Data Visualisation and Analysis
    - We were tasked to analyse a given dataset on road safety test data on a metric of our choice. We had to strip and clean data from a set of excel sheets, visualise it in a chosen graphical format, and analyse the graph by giving insights/inferences into what each part of it signified.

- #### [ALT3](https://github.com/ctsf1/alt3_diceroll): Modelling and Simulation
    - We were posed a set of three simulation problems, of which to choose one:
        - Simulate the odds of a given combination arising in a fair _n_-coin toss
        ([alt3_coinflip](https://github.com/ctsf1/alt3_coinflip))

        - Simulate the odds of rolling a given sum with _x_ fair _n_-sided dice
        ([alt3_diceroll](https://github.com/ctsf1/alt3_diceroll)) 
        <small>_(same link as title)_</small>

        - Simulate the odds of "winning" a ball-and-drum style lottery given the size of the drum and number of balls on a lottery ticket
        ([alt3_lotto](https://github.com/ctsf1/alt3_lotto))