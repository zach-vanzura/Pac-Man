"""
preliminary design for the maze,

the entire pacman screen is 28 tiles wide and 36 tiles tall

the PLAYABLE maze is 28 x 31

thus, each character in the following string represents a tile

I am using this steam link as a reference:
https://images.steamusercontent.com/ugc/367408356169798800/55F56BDFA947A6CE6E187876C62BFE76362D6320/
"""
"""
This is the layout for the POSITION of each tile
KEY:
- # represents an empty tile
- | represents a SINGLE wall (in the middle of the tile)
- = represents a DOUBLE wall (one line in the middle and one on the border) used for borders
- L represents a SINGLE ELBOW
- j represents a DOUBLE ELBOW (with a dot in the corner (used for ghost cage))
- _ represents the wall for the ghosts (which cannot be passed through by pacman but can be passed through by ghosts)
- C represents a BORDER elbow which has two lines
- P represents a BORDER "BLIP" which has an ELBOW and a LINE
- . represents a pellet
- o represents an energizer pellet
"""

positions = (
    "############################"
    "############################"
    "############################"
    "C============PP============C"
    "=............||............="
    "=.L||L.L|||L.||.L|||L.L||L.="
    "=o|##|.|###|.||.|###|.|##|o="
    "=.L||L.L|||L.LL.L|||L.L||L.="
    "=..........................="
    "=.L||L.LL.L||||||L.LL.L||L.="
    "=.L||L.||.L||LL||L.||.L||L.="
    "=......||....||....||......="
    "C====L.|L||L#||#L||L|.L====C"
    "#####=.|L||L#LL#L||L|.=#####"
    "#####=.||##########||.=#####"
    "#####=.||#j==__==j#||.=#####"
    "=====L.LL#=######=#LL.L====="
    "######.###=######=###.######"
    "=====L.LL#=######=#LL.L====="
    "#####=.||#j======j#||.=#####"
    "#####=.||##########||.=#####"
    "#####=.||#L||||||L#||.=#####"
    "C====L.LL#L||LL||L#LL.L====C"
    "=............||............="
    "=.L||L.L|||L.||.L|||L.L||L.="
    "=.L|L|.L|||L.LL.L|||L.L||L.="
    "=o..||.......##.......||..o="
    "P|L.||.LL.L||||||L.LL.||.L|P"
    "P|L.LL.||.L||LL||L.||.LL.L|P"
    "=......||....||....||......="
    "=.L||||LL||L.||.L||LL||||L.="
    "=..........................="
    "C==========================C"
    "############################"
    "############################"
)

"""
This is this layout for the ORIENTATION of each tile:
WALLS are drawn parallel to the X AXIS
Corners are drawn in the first quadrant using the xy axis as the bounds like this:

|
|
|+++
|  +
|__+_______


KEY:
- T represents a 90 degree rotation (used for walls)
- x represents a reflection about the X AXIS
- y represents a reflection about the Y AXIS
- z represents a reflection about the X and Y axes
- 0 represents no change to the original orientation
- # represents a blank space still
- . represents a pellet still 
- o represents an energizer still 
"""

orientations = (
    "############################"
    "############################"
    "############################"
    "y============0y============0"
    "T............TT............T"
    "T.y000.y0000.TT.y0000.y000.T"
    "ToT##T.T###T.TT.T###T.T##ToT"
    "T.z00x.z000x.zx.z000x.z00x.T"
    "T..........................T"
    "T.y000.y0.y0000000.y0.y000.T"
    "T.z00x.TT.z000y00x.TT.z00x.T"
    # where I stopped
    "T......||....||....||......="
    "z====L.|L||L#||#L||L|.L====C"
    "#####=.|L||L#LL#L||L|.=#####"
    "#####=.||##########||.=#####"
    "#####=.||#j==__==j#||.=#####"
    "=====L.LL#=######=#LL.L====="
    "######.###=######=###.######"
    "=====L.LL#=######=#LL.L====="
    "#####=.||#j======j#||.=#####"
    "#####=.||##########||.=#####"
    "#####=.||#L||||||L#||.=#####"
    "C====L.LL#L||LL||L#LL.L====C"
    "=............||............="
    "=.L||L.L|||L.||.L|||L.L||L.="
    "=.L|L|.L|||L.LL.L|||L.L||L.="
    "=o..||.......##.......||..o="
    "P|L.||.LL.L||||||L.LL.||.L|P"
    "P|L.LL.||.L||LL||L.||.LL.L|P"
    "=......||....||....||......="
    "=.L||||LL||L.||.L||LL||||L.="
    "=..........................="
    "C==========================C"
    "############################"
    "############################"
)