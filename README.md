# MatplotlibPizza
The terrible script I wrote for the pizza talk on Matplotlib features. 

Because some people were interested: here is the pizza talk on matplotlib. Before I get into the details of the slides: Other people have done a better job at making nice examples than I have in the presentation. So, please have a look at the Matplotlib gallery (at https://matplotlib.org/stable/gallery/index.html) and the book written by Nicolas P. Rougier (available on https://github.com/rougier/scientific-visualization-book). The gallery has more examples than you could possibly dream of, and the book shows off some cool (and possibly unnecessary) features as well as some explanations. Some of the figures featured here are taken from there. 


The code is very poorly written and very rushed. Do not use this as an example. It is trash and probably very broken. For good information on how things work and clear examples, the internet and the matplotlib documentation is your friend, check out the gallery and such.


On to the slides. It is a python script and not actual slides, so they are not as portable. The code is very poorly written and very rushed. Do not use this as an example. It is trash and probably very broken.


**There are some complications:**

- It requires at least matplotlib version 3.4.0, but newer is better.

- It also requires numpy and scipy, but I don't think it is very version dependent for those.

- It is designed with latex text rendering in mind. But it has an option to not use it (which is the default now. It will look a bit funky because of that.) See below as well.

- The way it displays depends on the screen you show it on. (And possibly python/matplotlib versions)

- You need an interactive backend installed. I think most people will have this already, but if not you can install pyqt or other equivalents. Note: It is not really compatible with the "ipympl" backend of Jupyter notebooks.


**Instructions for use:**

If everything works the slides will open automatically when you run the_talk.py (just **python the_talk.py**). If that does not work check the dependencies above. The latex text rendering can be switched on and off using the LATEX=False variable at the top of the_talk.py. Setting it to True will turn on latex rendering. To use it you require latex to be installed on your computer and matplotlib needs to know where to find it.

The script will refuse to run if the matplotlib version is too old.


You can move between slides by using the arrow keys. "right arrow" goes to the next slide, "left arrow" to the previous slide. On some slides there are some additional things that can change using space. These "steps" are one way only, and can only be reset by going to a different slide and back. I could not be bothered to include a previous step button. Bugs and problems can occur if you move through the slides too quickly.


There are several other buttons that do things:

- "e" switches between latex and non-latex rendering (if allowed by LATEX) (note: pretty jank)

- "w" switches between serif and sans-serif fonts (note: pretty jank)

- "r" redraws the current slide. (Can also be pretty jank, can also reset the latex rendering and serif fonts, depending on the slide, probably not very functional anymore.)

- "z" add the ruler background to the slide. (takes a second)

- "d" switch to dark mode. (a little jank, some weird things might happen)


Next to that there are the standard built in keys shortcuts: "q" closes the figure, "p" allows panning, "o" switches to selecting boxes to zoom into, "f" switches to full screen. These might be backend dependent, I don't know.


**Instructions per slide:**

0. "Title slide" N-body simulation/animation. You can left click in the figure to add extra bodies. The bodies have a small random velocity. 

1. "Figure basis" Just the names of parts of a figure. Press space bar to make them appear in steps.

2. "Figure size" Just some text

3. "Making subplots" The unorthodox way, the ruler remains, so it appears like the text just disappears. You can drag rectangles by left clicking and dragging. It might be a bit slow, don't move the mouse around too wildly. A random subplot will appear each time.

4. "Make subplots 2" The more orthodox way, just some text

5. "Sliders and buttons" you can move the sliders around and the subplots will change. Pressing one of the buttons will select all available values of a slider.

6. "Some generic tips" Just some text

7. "Histogram example" A random example. Hit space to reveal the next step.

8. "Vector vs raster" Stuff about saving figures. Note the example script for saving is included as well (raster_vs_vector.py).



