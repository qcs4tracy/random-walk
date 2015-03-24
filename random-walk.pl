use strict;

#simulate the distribution P(X) = 0.25, where X:[left, right, down, up].
use constant {
	#directions
	LEFT => 0,
	RIGHT => 1,
	UP => 2,
	DOWN => 3,
	#state of a cell in the grid: clean or contaminant
	CLEAN => 0,
	CONM => 1,
	#state of a random walker after a run: infected or healthy
	HEALTHY => 0,
	INFECTED => 1,
	#command line parameters
	PARAM_NGRID => "ngrid", # # of rows or columns for the grid
	PARAM_NSTEP => "nstep", # # of moves to take for a random walk run
	PARAM_NCONM => "nconm", # # of contaminant cells in the grid
	PARAM_NITR => "nitr",   # # of iterations to run in order to get the probability
};

my $ngrid = 100;
my $nstep = 100;
my $nconm = 50;
my $nitr = 200;

#command line arguments processing: determine grid size, # of moves to take, and # of contaiminated cells
if ($#ARGV > 0) {
	foreach (@ARGV) {
		if (m/(\w+)=([1-9][0-9]*)/i) {
			#size of the grid
			if ($1 eq PARAM_NGRID) {
				$ngrid = int($2);
			}
			#number of moves to take 
			if ($1 eq PARAM_NSTEP) {
				$nstep = int($2);
			}
			#number of contaminants within the grid 
			if ($1 eq PARAM_NCONM) {
				$nconm = int($2);
			}

			if ($1 eq PARAM_NITR) {
			    $nitr = int($2);
			}
		}
	}
}

#wrapper of rand() psuedo random generator
#if no argument is given, it return a floating number from [0,1]
#if a integer number is given, if return a integer from [0, arg]
sub rand_g (;$) {
	if ($#_ < 0) {
		return rand();
	}
	my ($range, ) = @_;
	return int(rand($range));
}

#randomly determine where the next moves
sub next_move {
	#this is a little bit tricky, for it depends on the special values for LEFT, RIGHT, UP, DOWN
	return  int(4 * rand_g());
	# given($ret) {
	# 	when($_ >= 0 and $_ < 0.25) { return LEFT; }
	# 	when($_ >= 0.25 and $_ < 0.5) { return RIGHT; }
	# 	when($_ >= 0.5 and $_ < 0.75) { return UP; }
	# 	when($_ >= 0.75 and $_ <= 1) { return DOWN; }
	# 	default { return LEFT; }
	# }
}

#initialization of the grid map
#takes arguments: 
#			$size: size of the grid (# of row or column)
#			$nc: number of cells contaminated randomly
sub init_grid ($$) {
	#only care about the first parameters
	my ($size, $nc) = @_;
	my @grid = ();
	
	for (my $k = 0; $k < $size; $k++) {
		$grid[$k] = [];
		for (my $i = 0; $i < $size; $i++) {
			$grid[$k]->[$i] = CLEAN;
		}
	}

	my ($x, $y);
	#randomly make $nc cells being contaminated 
	for (my $j = 0; $j < $nc; $j++) {
		#prevent $ngrid from being generated, which is out of bound for the array index, or
		#position ($x, $y) is already contaminated
		do {
			($x, $y) = rand_2d($ngrid);
		} while ($grid[$x]->[$y] == CONM);
		$grid[$x]->[$y] = CONM;
	}

	return @grid;
}

#randomly generated a 2d-point (x, y)
sub rand_2d($) {
	my ($size, ) = @_;
	my ($x, $y);
	do {
		$x = rand_g($size);
		$y = rand_g($size);
	} while ($x >= $size || $y >= $size);
	return ($x, $y);
}

#dump the grid map to standard output
sub dump_grid (@) {
	foreach (@_) {
		my $row = $_;
		for (my $i = 0; $i < $ngrid; $i++) {
			print "$row->[$i] ";
		}
		print "\n";
	}
}

#random walk on the grid:
#arguments:
#	 $nmove: the number of moves to take
#	 @grid_map: the grid map to walk on
sub random_walk($@) {

	my ($nmove, @grid_map) = @_;
	my ($x, $y) = rand_2d($ngrid); # the initial position of the walker
	my $move_cnt = 0; # counter of moves
	my $direction; # direction: LEFT, RIGHT, UP, DOWN

	#the initial position is contaiminated
	if ($grid_map[$x]->[$y] == CONM) {
	 	return INFECTED;
	} 

	#move $nmove steps randomly
	until ($move_cnt++ >= $nstep) {
		#the direction of next move
		$direction = next_move;
		#this could use switch or given/when statement, but in case of version compatibility 
		#problems, simply use if-else here...
		if ($direction == LEFT) {
			if ($x-1 < 0) {#out of bounds of the grid map
				$move_cnt--;
				next;
			}
			$x--;
		} elsif ($direction == RIGHT) {
			if ($x+1 > $#grid_map) {
				$move_cnt--;
				next;
			}
			$x++;
		} elsif ($direction == UP) {
			if ($y-1 < 0) {
				$move_cnt--;
				next;
			}
			$y--;
		} else {
			if ($y+1 > $#grid_map) {
				$move_cnt--;
				next;
			}
			$y++;
		}
		#check if the cell moved in is contaminated
		if ($grid_map[$x]->[$y] == CONM) {
		 	return INFECTED;
		 } 
	};

	return HEALTHY;
}


#top level statements:
my @gm = init_grid($ngrid, $nconm);
my $state;
my $ninfected = 0;
my ($ratio_infect, $ratio_healthy);

#run $nitr iterations and calculate the ratio of both infected and healthy times
for (my $itr = 0; $itr < $nitr; $itr++) 
{
	$state = random_walk($nstep, @gm);
	if ($state == INFECTED) {
		$ninfected++;
	}
}

$ratio_infect = $ninfected / $nitr;
$ratio_healthy = 1 - $ratio_infect;
print "infected 	healthy\n";
print "$ratio_infect 		$ratio_healthy";

