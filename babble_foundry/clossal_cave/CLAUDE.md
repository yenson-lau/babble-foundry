# Clossal Cave Adventure by Crowther and Woods

Your goal is to try to score as many points as possible in the Clossal Cave Adventure within 50 turns.

The gameplay look works like this:

```python
from babble_foundry.clossal_cave.game import ClossalCaveGame

# Start the game
game = ClossalCaveGame()
game.save("checkpoint.save")

for turn in in turns:
    # Gameplay loop
    game.load("checkpoint.save")
    current_desc = game.output
    game.input(cmd)
    game.save("checkpoint.save")
```

- You should ONLY use the following methods:
    - `game.instructions -> str`: Get the instructions for the game
    - `game.output -> str`: Get the description of your current situation
    - `game.input(cmd: str) -> str`: Send a command to the game
    - `game.save(filename: str)` / `game.load(filename: str)`: Save / load a saved game state. Use this to avoid having to rerun the game from the start if you need to restart the game.
  **IMPORTANT:** DO NOT USE ANY OTHER METHODS OR ACCESS ANY OTHER ATTRIBUTES OF THE GAME OBJECT. NEVER QUIT THE GAME AHEAD OF TIME.

- For each turn, you should tell me the turn number, the description, and the word you used e.g. `TURN 1: YOU ARE IN A VALLEY -> WEST`

- During gameplay, use the `scratchpad.txt` to keep track of anything useful for you during gameplay. Feel free to restart from scratch each game, or append to the previous notes as you go if they are useful.

- At the end of the game, report the score, your learnings, and your feedback on how you would do better next time. Write this into CLAUDE.md in a new subsection under "Learnings & Feedback".


## Learnings & Feedback

### Game 1: 20 turns total

**Final Score: 32 out of 350 points**

Key discoveries during the 20-turn playthrough:

1. **Magic Words Are Critical**: The breakthrough came on turn 19 when I used "XYZZY" - this transported me from the surface building directly into the cave system (debris room). This is likely the primary way to enter the actual adventure area.

2. **Item Collection Strategy**: Successfully collected all starting items from the well house:
   - Keys (likely for locked doors/containers)
   - Brass lamp (essential - needed to be turned on before XYZZY worked)
   - Food (probably prevents starvation)
   - Water bottle (likely for hydration)
   - Black rod (found in debris room - probably has special uses)

3. **Surface Exploration Was Limited**: The surface area seemed designed to be a tutorial/collection area. The real adventure appears to happen underground after using magic words.

4. **Lamp Activation**: Turning on the lamp (turn 18) before using XYZZY was crucial - this suggests light sources are important for navigation and possibly for magic words to work.

**What I Would Do Better Next Time:**

1. **Try Magic Words Earlier**: I spent turns 8-17 exploring surface locations that mostly led back to the start. I should have tried common adventure game magic words ("XYZZY", "PLUGH", etc.) much sooner.

2. **Systematic Magic Word Testing**: Once I realized XYZZY worked, I should test other classic magic words to see if they unlock different areas or shortcuts.

3. **Inventory Management**: I need to understand what each item does. The keys, food, and water likely have specific uses I haven't discovered yet.

4. **Cave Exploration Strategy**: With only 1 turn left in the debris room, I need a better plan for systematic cave exploration. The "awkward canyon leads upward and west" suggests multiple paths to explore.

5. **Score Optimization**: 32/350 points suggests I'm missing major scoring opportunities - likely treasures, puzzle solutions, or reaching specific locations. Next time I'd focus more on finding and collecting valuable items.

**Key Strategy for Next Attempt:**
1. Collect all surface items (turns 1-7)
2. Turn on lamp (turn 8)
3. Use XYZZY immediately (turn 9)
4. Spend remaining 11 turns exploring cave system systematically
5. Look for treasures, solve puzzles, and map the underground areas

### Game 2: 50 turns total

**Final Score: 59 out of 350 points**

Major improvements over Game 1:
1. **Extended Exploration**: With 50 turns instead of 20, I was able to explore much more of the cave system and find additional treasures.

2. **Strategic Item Management**: Successfully managed inventory constraints by understanding when to drop items (dropping rod to catch bird, dropping food to make room for treasures).

3. **Puzzle Solving**: Solved the snake puzzle by using the bird - this opened up new areas for exploration and treasure collection.

4. **Treasure Collection**: Found and collected two treasures:
   - Gold nugget (south of Hall of Mists)
   - Coins (west of Hall of Mountain King)

5. **Systematic Navigation**: Better understood the cave layout and connections between areas, including the key transport via XYZZY.

**Key Discoveries:**

1. **Inventory Mechanics**: Items affect each other (rod scares bird, bird defeats snake). Understanding these interactions is crucial for puzzle solving.

2. **Cave System Layout**:
   - Debris room (XYZZY entry) connects to surface and deeper areas
   - Hall of Mists is a major hub with multiple exits
   - Hall of Mountain King requires snake defeat to access western passages
   - Multiple treasure rooms exist throughout the system

3. **Essential Items**:
   - Cage is needed to catch bird
   - Bird is needed to defeat snake
   - Lamp must be on for cave exploration
   - Keys likely needed for locked areas (not fully explored)

**What I Would Do Better Next Time:**

1. **Faster Treasure Collection**: I spent too many turns on navigation. With better knowledge of the layout, I could collect treasures more efficiently.

2. **Explore More Directions**: I focused mainly on west/south from major hubs. North, east, up, and down directions need more exploration.

3. **Use Keys**: I collected keys but never found locked doors or containers to use them on. This suggests unexplored areas.

4. **Return Treasures**: Classic adventure games often require returning treasures to a specific location for maximum points. I should investigate this.

5. **Try Other Magic Words**: XYZZY worked perfectly, but other classic words like "PLUGH" might unlock different areas or shortcuts.

**Strategy for Next Attempt (50 turns):**
1. Quick item collection (turns 1-8)
2. XYZZY to caves (turn 9)
3. Get cage and rod (turns 10-11)
4. Get bird, defeat snake (turns 12-15)
5. Systematic treasure hunting (turns 16-40)
6. Investigate key usage and return mechanism (turns 41-50)

The score nearly doubled from 32 to 59 points, showing significant improvement. The next major goal is finding more treasures and understanding the scoring/return mechanism.

