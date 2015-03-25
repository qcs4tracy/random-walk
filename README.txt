#This is the README file for Computational Epidemiology assignment#2
#Author: Chusheng Qiu

-About files in this folder:
	1. random-walk.pl: perl implemented random walk model. 
		*It takes 4 command line arguments:
			1) ngrid: # of rows or columns for the grid, default is 100.
			2) nstep: # of moves to take for a random walk run, default is 100.
			3) nconm: # of contaminant cells in the grid, default is 50.
			4) nitr: # of trials or iterations, default is 200.
		*You can run the script like this:
			perl -w random-walk.pl (all default arguments are used)
			perl -w random-walk.pl ngrid=200 nstep=150 nconm=100 nitr=400 (each iteration/trial takes 150 moves on a 200*200 grid with 150 contaminants, and run 400 iterations to obtain the estimated probability)
		*The result of script output looks like(infected probability is 0.21):
			infected 	healthy
			0.21 		0.79

	2. plot.py: the python script that executes random-walk.pl and plots the resulting figures for the experiments
		*It takes only 1 arguments:
			1) nitr: # of trials or iterations, default is 200.
		*To run the script:
			1) Make sure these modules are installed in your python:
					numpy matplotlib
			2) The command to run:
					python plot.py [nitr=400] (the nitr is optional, default is 200)
		*Two figures will be plotted:
				-Infected & Healthy probabilty with different # of contaminants (both line chart and bar chart)
				-Infected & Healthy probabilty with different # of moves (both line chart and bar chart, and # of contaminants is set to 50)

-Something to note:
	The source files are well documented and both figures will be plotted sequentially, so if you see the first figure and want the second, just
	close the window and the second figure will appear in the next window.




