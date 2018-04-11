Design overview:

The text file is considered as a list of lines where each line is 
again a list of two elements, the timestamp and the state.

In the solution, one iteration over this list is done to generate 
another list which has each of its element as a collection of 
1. timestamp at which the state of system changes
2. the new state of system
3. duration in seconds before the next state change of system

Each of these collection is appended to the tail of this list which
serves as a queue.

Once the complete input file is processed, we have our final queue 
which is passed to the SVG generator for svg file.

[
	['1429591293', 'True', 130], ['1429591423', 'False', 182],
	['1429591605', 'True', 247], ['1429591852', 'False', 39],
	['1429591891', 'True', 117], ['1429592008', 'False', 26],
	...
]

svgwrite library is used for generating the svg from change_queue

	'pip install svgwrite'

Each member is taken from the head of the queue and a 'rect' sub-element
is added to the root 'svg' element. The width of each 'rect' element 
is calculated based on the duration of the corresponding state.

We have already calculated the number of seconds per pixel from the
input time range and available width of 500 px.

So width of each rect element = duration(in sec)/seconds per pixel

The complete xml tree thus generated is written to the output file 
path provided.  