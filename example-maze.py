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
- . represents a pellet
- o represents an energizer pellet

- | represents a SINGLE wall (in the middle of the tile)
- = represents a DOUBLE wall (one line in the middle and one on the border) used for borders
- _ represents the WALL for the GHOSTS (which cannot be passed through by pacman but can be passed through by ghosts)

- L represents a SINGLE ELBOW
- j represents a DOUBLE ELBOW (with a dot in the corner (used for ghost cage))

- C represents a BORDER ELBOW which has TWO lines
- P represents a BORDER "BLIP" which has an ELBOW and a HORIZONTAL LINE ABOVE
- H represents a BORDER BLIP with an ELBOW and a VERTICAL LINE to the RIGHT of it  
NOTE since the "blips" are a line and a circle, they create a sparse edge case

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
    "H|L.||.LL.L||||||L.LL.||.L|H"
    "H|L.LL.||.L||LL||L.||.LL.L|H"
    "=......||....||....||......="
    "=.L||||LL||L.||.L||LL||||L.="
    "=..........................="
    "C==========================C"
    "############################"
    "############################"
)


"""
This is this layout for the ORIENTATION of each tile:
WALLS are drawn PARALLEL to the X AXIS
Corners are drawn in the first quadrant using the xy axis as the bounds like this:

|
|
|+++
|  +
|__+_______


KEY:
- T represents a 90 degree rotation (used for walls) CLOCKWISE 
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
    "T......TT....TT....TT......T"
    "zxxxx0.Tz000#TT#y00xT.yxxxxx"
    "#####T.Ty00x#zx#zTT0T.T#####"
    "#####T.TT##########TT.T#####"
    "#####T.TT#y0000000#TT.T#####"
    "00000x.zx#T######T#zx.z00000"
    "######.###T######T###.######"
    "xxxxx0.y0#T######T#y0.yxxxxx"
    "#####T.TT#z000000x#TT.T#####"
    "#####T.TT##########TT.T#####"
    "#####T.TT#y0000000#TT.T#####"
    "y0000x.zx#z000y00x#zx.z00000"
    "T............TT............T"
    "T.y000.y0000.TT.y0000.y000.T"
    "T.z00T.z000x.zy.z000y.Ty0x.T"
    "To..TT.......##.......TT..oT"
    "z00.TT.y0.y0000000.y0.TT.y0x"
    "y0x.zx.TT.z000y00x.TT.zx.z00"
    "T......TT....TT....TT......T"
    "T.y0000xz000.TT.y00xz00000.T"
    "T.z00000000x.zx.z00000000x.T"
    "T..........................T"
    "z==========================x"
    "############################"
    "############################"
)