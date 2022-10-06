# /ctsf1/dir
_Directory/Portfolio of past projects_

A landing page of sorts, with a directory and overview portfolio-style of the projects I've uploaded to github (and beyond)

## Projects

These are arranged categorically, not in chronological order. I have tried, however, to sort items within a category by the order in which I completed them where I can

- ### Snake five (and counting) ways
    It's become somewhat of a ritual for me to write a Snake game in languages I pick up as a first project. The (relatively) simple implementation of game rules and low (but present) graphical requirements make for an ideal beginner project, especially given that in doing so I learn about the language's approach to user input, rendering a simple window (or printing graphics to a terminal), constructing a working game loop and implementing complex (ish) logic, skills that are foundational to most other intermediate/advanced techniques in CS. This series of incarnations mostly encapsulates my journey through CS, and through each I gained a rewarding understanding of new concepts and techniques.

    - #### [Python](/snake_5_ways/Python) (with Pygame)
        - My first major project in Computer Science, undertaken in winter 2020. Before this I'd never dabbled in graphics in any language, so the Pygame module was a massive help in making the process beginner-friendly. There are definitely some sharp corners, but it carries a lot of nostalgia for me and I'm quite proud of it, especially considering it was the first of its kind. (November 2020)

    - #### [C++](/snake_5_ways/C++) (With ncurses)
        - After getting comfortable with basic CS concepts in Python, I took the leap of exploring lower-level languages. While C was a bit too daunting for me at the time, C++ had a lot more beginner-friendly documentation and tutorials on sites like stackoverflow so I worked my way up to a text-based version of the game, using the ncurses Window class and its methods to print colored text to the terminal to display the game window (September 2021)

            (_as a warning to any potential downloaders, a mistake exists in the source (in the creation of a local file to save user highscore) which creates a new file in the user's CWD when the script is called instead of finding the one in a directory relative to the script. this doesn't affect the performance of the game in any way, but creates annoying clutter_)

    - #### [Rust](https://github.com/ctsf1/rust-snake) (With Glutin, Piston2d and OpenGL)
        - A while passed before I picked up any more new languages, mainly because I was busy with the beginnings of developing what would become [spl_widgets](). At this stage, I had become acquainted with Github, so most of my large projects were uploaded there, this one included. Learning rust was a very new experience given its unique nature (namely, its use of a borrow-checker) but a very rewarding one as well, as I was forced to seriously consider my actions in a way even beyond what I was used to in C++. The amount of documentation (cargo's built-in docs feature, specifically) was a massive help, though, and with it I made my most polished version yet using Piston2d, Glutin and OpenGL to display the window. (May 2022)

    - #### [HTML/CSS/JS](https://github.com/ctsf1/canvas_games) (with JS Canvas)
        - I had been experimenting with HTML and CSS for a while, and had written little curiosities in JS (like one to generate and style a Minesweeper grid), but had never really combined the two. JS's tools for drawing to HTML Canvas Elements are quite well-documented, and given the much more lax nature of JS (comparatively), building Snake was a much more relaxed experience. Looking for a greater challenge I also tried to implement a version of the popular web game 2048, the logic for which is quite involved and provided a good stimulus for me to improve my grasp of control flow. (June/July 2022)

            _I've created a Github Pages for this repository to allow for easy access without downloads. Snake can be played [here](https://ctsf1.github.io/canvas_games/snake/snake.html), and 2048 [here](https://ctsf1.github.io/canvas_games/2048/2048.html)_

    - #### [Java](/Java) (with awt and swing)
        - More recently I've been experimenting with Java, partly in an attempt to fill in some OOP concepts I missed out on in Python and C++. The Object Oriented style was foreign to me initially, having come from at least partially functional programming languages, but I completed a series of learning exercises covering different concepts and developed the confidence to tackle the project of making Snake. With the assistance of the (thankfully) well-documented modules swing and AWT to render the screen, and implementing the KeyListener class to process user input, this version is arguably the most refined so far.
        (June, September 2022)

            _The linked folder contains a subfolder 'cls' with .class files able to be executed (after download) with "cd cls & java Snake"_
