# Source:
https://www.geekslop.com/old-school/2020/the-logic-and-programming-behind-pac-man-all-the-crazy-cool-stuff-you-ever-wanted-to-know-about-how-the-classic-pac-man-game-works-under-the-hood#cmtoc_anchor_id_0 


### The anatomy of the board
There are 244 dots in the Pac-Man maze, each worth 10 points. The flashing dots, known as “energizers,” are worth 50 points each. This yields a total of 2,600 points, or clearing the entire board.

### The size of the Pac-Man screen
The Pac-Man game screen is 224 by 288 pixels. The screen is divided into tiles, 28 horizontally and 36 vertically. Each tile in the game is 8 pixels square.

### The four ghosts
The four ghosts are known as Blinky (red), Pinky (pink), Inky (blue), and Clyde (orange). Each has its own “personality” and gameplay techniques.

### Ghost modes
The ghosts have three modes they can operate in – chase mode, where they find and capture Pac-Man, scatter mode, where they head for their respective corners, and frightened mode, where they run away from Pac-Man after he eats one of the four energizers.

### Ghosts cannot reverse their direction of travel
The ghosts are prohibited from reversing their direction of travel. They can only travel in the direction they are facing to take the next intersection. The ghosts only change direction when the mode changes from chase-to-scatter, chase-to-frightened, scatter-to-chase, and scatter-to-frightened.

### The chase period
The first two chase periods last for 20 seconds. The duration of the third chase period depends on the level. The third chase period is 20 seconds on level one, then 1,033 seconds (more than 17 minutes) for levels 2-4, and 1,037 seconds for all levels afterward.

### Frightened ghost turns at intersections
Frightened ghosts turn blue and appear to wander around aimlessly while avoiding Pac-Man. In truth, a random number is generated and used to determine which direction the ghost should move at each approaching intersection. If a wall blocks the chosen direction, the ghosts attempt the following directions in this order: up, left, down, and right.

### Pac-man speed
Pac-Man moves at 80% of his maximum speed until level 5, when he moves at full speed until level 21, at which point he reduces his speed to 90% for the remainder of the game.

### Ghost speed
Ghosts move at a slightly slower speed than Pac-Man until the 21st level, at which point they begin moving faster than Pac-man.

### When Blinky becomes Elroy
When a level begins, all ghosts move at the same speed. However, Blinky moves twice as fast each round based on the number of dots remaining. When Blinky is in this accelerated state, he is known as “Cruise Elroy.” When in Elroy mode, Blinky always chases Pac-Man and refuses to go into scatter mode with the other ghosts.

### Eating dots slows Pac-Man down
Each dot Pac-Man eats causes him to stop moving for one frame or 1/60th of a second.

### Eating energizes and slows Pac-Man down even more than dots
Each energizer Pac-Man eats causes him to stop moving for three frames or 3/60th of a second.

### Eating ghosts
Pac-Man can eat ghosts without harm after eating one of the four energizers. The first ghost eaten yields 200 points, the second 400 points, the third 800 points, and the fourth and final ghost 1,600 points.

### Ghosts cannot be eaten after level 19
The ghosts’ “blue time” decreases with each level. By level 19, the ghosts stop turning blue altogether and can no longer be eaten by Pac-Man.

### Eating fruit
Fruits appear randomly during the game and are worth between 100 and 5,000 points. The amount of time a fruit stays visible is always between 9 and 10 seconds.

### Pac-Man turns
Pac-Man navigates the turns faster than the ghosts because he does not have to wait until the middle of the turn to change direction as the ghosts do. This is why good players push the joystick before getting to an intersection (called “pre-turns”). Turns are how Pac-Man puts distance between himself and the ghosts.

### The ghost house or monster pen
The area in the middle where ghosts begin their lives (and Pac-Man cannot enter) is called the ghost house or monster pen. Blinky always begins above the ghost house, with Inky, Pinky, and Clyde beginning inside the house in that order.

### Blinky in the ghost house
Blinky (red) always starts outside the ghost house when a level begins. The only time Blinky gets inside the ghost house is after Pac-Man eats him. He then immediately exits the ghost house when revived.

### The order ghosts leave the ghost house
Besides Blinky, who leaves the ghost house immediately, a ghost determines when to leave the ghost house by counting the number of dots Pac-man has eaten. Pinky (pink) leaves first. Inky (blue) leaves after 30 dots are eaten. Clyde (orange) leaves after 60 dots have been eaten. Each character’s counter begins when the prior character leaves the ghost house. However, there is a timer limit, too. A ghost will always leave within 4 seconds during levels 1-4 and 5 seconds starting with level 5, no matter how many dots Pac-Man has eaten.

### After level 2, all ghosts leave the ghost house immediately
Ghosts normally leave the house depending on how many dots Pac-Man has eaten. However, beginning at level three, all ghosts leave the ghost house immediately after being revived.

### The direction a ghost takes when leaving the ghost house is usually left
Ghosts move left when leaving the ghost house unless the game has changed modes (from chase-to-scatter, chase-to-frightened, scatter-to-chase, or scatter-to-frightened) while the ghost is inside the ghost house. If the game changes modes while a ghost is in the house, the ghost will move to the right when leaving the house.

### Ghosts cannot move upward through the intersections above the ghost house
The two upward paths above the ghost house door cannot be taken by any ghosts. Ghosts are forbidden to move upward in this zone. They can only travel from right-to-left of from left-to-right when above the ghost house.

### There is a second area where ghosts cannot move upward
There is a T-shaped wall at the bottom-center of the screen. In the area directly above the T, ghosts are forbidden from turning upward at the intersection. Only Pac-Man can travel upward through these tunnel entrances.

### You can pass through a ghost unharmed
Pac-Man can pass right through a ghost without being harmed. This happens when Pac-Man and an approaching ghost enter the tile at the exact same time. The window of opportunity is so small (1/60th of a second) that it rarely happens.

### Ghosts prefer to move in specific directions
Ghosts prefer to move in this order: up, left, down, right. However, “target tiles” override these choices.

### Ghosts always travel towards a “target tile”
Ghosts do not wander around aimlessly. A ghost is always trying to reach a specific tile somewhere on or off the screen. Each ghost calculates its target tile in a different manner. In chase mode, the target tile is usually related to Pac-Man’s current tile. In scatter mode, the target tile is a fixed tile located in the character’s home corner. Thus, the only difference between chase mode and scatter mode is where the ghost’s target tile is located.

### Blinky’s target tile
Blinky’s target tile is always Pac-Man’s current tile. This is why Blinky always chases Pac-Man with reckless abandon.

### Pinky’s target tile
Pinky does not target Pac-Man’s current tile directly. Instead, his target tile in chase mode is a tile offset four tiles away from Pac-Man in the direction Pac-Man is currently moving. This is why Pinky seems to often move ahead and “block” Pac-Man.

### Pinky sometimes seems to run away from Pac-Man
Pinky’s target tile is four tiles away from Pac-Man in the direction Pac-Man is travelling. If the target tile calculated by Pinky falls behind Pac-Man, Pinky will turn right before he reaches Pac-Man in an attempt to get behind him. For this reason, when Pinky approaches Pac-man, a player can jiggle the control back and forth, a technique known as head faking, to make Pinky turn away.

### Inky’s target tile
Inky’s tile-targeting scheme is more complex than that of the other ghosts. It takes into account Pac-Man and Blinky’s current tiles, which is why Inky’s behavior is more unpredictable.

### Clyde’s target tile
Clyde’s tile-targeting scheme is more complex than Blink and Pinky’s but less complex than Inky’s. If Pac-Man is more than 8 tiles away, Clyde’s target tile will be Pac-Man’s current tile. If Clyde is closer than 8 tiles to Pac-Man, he will switch to scatter-mode targeting and head for his own corner of the board until he is far enough away to target Pac-Man again. It is for this reason that, in special circumstances, Pac-Man can park in a corner and force Clyde into an endless circle pattern.

### The random fruits
Random objects appear during the game that can be eaten for extra points. They are cherries, strawberries, peaches, apples, grapes, Galaxian, bell, and a key. All objects are food except for three. The Galaxian was a tribute to the Galaxian game, which was being developed by Midway at the same time as Pac-Man. Nobody knows why the bell and key were included in the selection of fruits.

### The game ends at level 256 and enters a split-screen
It is impossible to proceed past level 256 (as with many of the early video games, the developers never foresaw any player getting that far). The reason is a bug in the game that causes the board to go into “split screen,” with the left side of the screen playing normally but the right side of the screen drawing a bizarre series of seemingly random shapes. Hidden behind the shape are nine dots that can be eaten by a player if they can blindly find them.

### A perfect score
A perfect score would be 3,333,360 points and is achieved when the player eats every dot, energize, fruit, and blue ghost through level 256. Some players have achieved this score.

### Pac-Man Intermissions (aka Pac-Man Commercials)
There are three intermissions in Pac-Man, humorous animations that appear between levels. The first appears after round 2 and shows a larger “super” version of Pac-Man chasing Blinky. The second appears after round 5 and shows Blinky getting caught on a nail. The third is seen after rounds 9, 13, and 17 and shows Blinky disrobed.