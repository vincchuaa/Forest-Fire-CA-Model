# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np


def transition_func(grid, burnTimers, neighbourstates, neighbourcounts):
    #Canyon catches fire from 1 neighbour, burns for short time
    #Chaparral catches fire from 2 neighbour, burns for medium time
    #Forest catches fire from 3 neighbour, burns for long time

    #Neighbour states returns curretn state of the adjacent states
    #Neighbour counts returns boolean array, counting each type of adjacency
    chaparral, burning, burntOut, town, lake, denseForest, canyon = neighbourcounts
    #Set new burning areas (1 time = 12 hours)
    #Can burns for "several hours" = 1 time
    #Chap burns for "several days" = 8 time
    #Forest burns for "one month" = 60 time

    burningCan = (grid == 6) & (burning >= 1)
    burningChap = (grid == 0) & (burning >= 2)
    burningFor = (grid == 5) & (burning >= 3)

    burnTimers[burningCan] = 2
    burnTimers[burningChap] = 9
    burnTimers[burningFor] = 61

    grid[burningCan | burningChap | burningFor] = 1
    fireStop = burnTimers == 1
    grid[fireStop] = 2

    onFire = (burnTimers > 0)
    burnTimers[onFire] = burnTimers[onFire] - 1
    #print(burnTimers)

    

    #print(burningCan)
    #print(burningChap)
    #print(burningFor)

    # dead = state == 0, live = state == 1
    # unpack state counts for state 0 and state 1
    #dead_neighbours, live_neighbours = neighbourcounts
    # create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born
    #birth = (live_neighbours == 3) & (grid == 0)
    # if 2 or 3 live neighbours and is alive -> survives
    #survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # Set all cells to 0 (dead)
    #grid[:, :] = 0        
    # Set cells to 1 where either cell is born or survives
    #grid[birth | survive] = 1
    
    return grid, burnTimers


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6) #chaparral, burning, burnt out, town, lake, dense forest, canyon
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.6,0.6,0),(1,0,0),(0.4,0,0),(0,0,0),(0.2,0.6,1),(0.2,0.4,0),(1,1,0.2)]
    # config.num_generations = 150
    # config.grid_dims = (200,200)
    grid = np.zeros((200,200))

    #Top left is (0,0)
    #Top right is (0,199)
    #Add canyon (6)
    for down in range(20,160,1):
      for right in range(120,130,1):
        grid[down,right] = 6
    #Add upper then lower forest (5)
    for down in range(20,70,1):
      for right in range(60,100,1):
        grid[down,right] = 5
    for down in range(80,140,1):
      for right in range(0,100,1):
        grid[down,right] = 5
    #Add lake (4)
    for down in range(70,80,1):
      for right in range(20,100,1):
        grid[down,right] = 4
    #Add town (3)
    for down in range(175,185,1):
      for right in range(75,85,1):
        grid[down,right] = 3
    #Add power plant fire
    #grid[0,0] = 1
    #grid[0,1] = 1
    #grid[1,0] = 1
    #grid[1,1] = 1
    #Add incinerator fire
    grid[0,199] = 1
    grid[1,199] = 1
    grid[0,198] = 1
    grid[1,198] = 1


    #for y in range(200):
    #    for x in range(200):
    #        if y >= 20 & y < 160 & x >= 120 & x < 130:
    #            grid[y,x] = 6 # canyon
    #        elif y >= 70 & y < 80 & x >= 20 & x < 100:
    #            grid[y,x] = 4 # water from 30-32.5km on y and 5-25km on x
    #        elif y >= 80 & y < 140 & x < 100:
    #            grid[y,x] = 5 # forest block from 15-30km on y and 0-25km on x
    #        elif y >= 20 & y < 70 & x >= 60 & x < 100:
    #            grid[y,x] = 5 # forest block from 32.5-45km on y and 15-25km on x


    config.set_initial_grid(grid)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
