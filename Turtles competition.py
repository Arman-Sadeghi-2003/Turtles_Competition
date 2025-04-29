import turtle as t
import random as r

# Constants
SCREEN_SIZE = 1.0
ROAD_WIDTH = 100
START_X = 350
START_Y = 325
ROAD_LENGTH = 700
ROAD_DECREMENT = 150
MIN_STEP = 5
MAX_STEP = 20
BOOST_STEP = 30
FONT = ("Tahoma", 30, "normal")
SMALL_FONT = ("Tahoma", 20, "normal")

def setup_screen():
    """Initialize the screen settings."""
    screen = t.Screen()
    screen.setup(SCREEN_SIZE, SCREEN_SIZE)
    screen.bgcolor("Green")
    screen.title("Turtle Competition")
    return screen

def draw_track(num_laps):
    """Draw the rectangular track with decreasing size."""
    pen = t.Turtle()
    pen.pensize(ROAD_WIDTH)
    pen.color("Brown")
    pen.speed(0)
    pen.up()
    pen.goto(START_X, START_Y)
    pen.setheading(-90)
    pen.down()
    
    road_lengths = []
    current_length = ROAD_LENGTH
    for _ in range(num_laps):
        for _ in range(2):
            pen.forward(current_length)
            pen.right(90)
            road_lengths.append(current_length)
        current_length -= ROAD_DECREMENT
    
    return road_lengths, pen

def create_player(color, x_offset):
    """Create and position a player turtle."""
    player = t.Turtle()
    player.shape("turtle")
    player.setheading(-90)
    player.color(color)
    player.up()
    player.goto(START_X + x_offset, START_Y)
    player.down()
    return player

def draw_start_screen(screen, start_callback, lap_selector_callback):
    """Draw the start screen with buttons."""
    screen.clearscreen()
    screen.bgcolor("Green")
    
    title = t.Turtle()
    title.hideturtle()
    title.color("White")
    title.up()
    title.goto(0, 100)
    title.write("Turtle Competition", align="center", font=FONT)
    
    start_button = t.Turtle()
    start_button.shape("square")
    start_button.color("Yellow")
    start_button.shapesize(stretch_wid=2, stretch_len=8)
    start_button.up()
    start_button.goto(0, 0)
    start_button.write("Start Race", align="center", font=SMALL_FONT)
    
    lap_options = [2, 4, 6]
    lap_buttons = []
    for i, laps in enumerate(lap_options):
        btn = t.Turtle()
        btn.shape("square")
        btn.color("LightBlue")
        btn.shapesize(stretch_wid=1, stretch_len=4)
        btn.up()
        btn.goto(0, -50 - i * 50)
        btn.write(f"Laps: {laps}", align="center", font=SMALL_FONT)
        lap_buttons.append((btn, laps))
    
    def on_click(x, y):
        if abs(x) < 80 and 0 < y < 40:
            start_callback()
        for btn, laps in lap_buttons:
            btn_y = btn.ycor()
            if abs(x) < 40 and btn_y - 20 < y < btn_y + 20:
                lap_selector_callback(laps)
                for b, _ in lap_buttons:
                    b.color("LightBlue")
                btn.color("Blue")
    
    screen.onscreenclick(on_click)

def display_lap_number(lap_writer, current_lap, total_laps):
    """Display the current lap number."""
    lap_writer.clear()
    lap_writer.write(f"Lap {current_lap + 1}/{total_laps}", align="center", font=SMALL_FONT)

def main():
    """Main game loop with enhanced features."""
    screen = setup_screen()
    selected_laps = 4  # Default value
    
    # Game state
    game_state = {"racing": False, "num_laps": selected_laps, "boosts": [False] * 4}
    
    def start_race():
        game_state["racing"] = True
        screen.onscreenclick(None)  # Disable start screen clicks
        screen.clearscreen()
        screen.bgcolor("Green")
        
        # Draw track and create players
        road_lengths, finish_pen = draw_track(game_state["num_laps"])
        players = [
            create_player("Red", -15),
            create_player("Blue", -5),
            create_player("Yellow", 5),
            create_player("Purple", 15)
        ]
        
        # Setup lap display
        lap_writer = t.Turtle()
        lap_writer.hideturtle()
        lap_writer.color("White")
        lap_writer.up()
        lap_writer.goto(0, 0)
        
        # Setup boost keys
        boost_keys = ["r", "b", "y", "p"]
        for i, key in enumerate(boost_keys):
            def make_boost(idx=i):
                return lambda: set_boost(idx)
            screen.onkey(make_boost(i), key)
        screen.listen()
        
        def set_boost(player_idx):
            game_state["boosts"][player_idx] = True
            screen.ontimer(lambda: reset_boost(player_idx), 1000)
        
        def reset_boost(player_idx):
            game_state["boosts"][player_idx] = False
        
        # Game loop
        player_distances = [0] * len(players)
        current_segment = 0
        players_at_corner = 0
        total_laps = game_state["num_laps"]
        
        while game_state["racing"]:
            display_lap_number(lap_writer, current_segment // 2, total_laps)
            
            for i, player in enumerate(players):
                # Move player
                step = r.randint(MIN_STEP, MAX_STEP)
                if game_state["boosts"][i]:
                    step = BOOST_STEP
                player.forward(step)
                player_distances[i] += step
                
                # Check for corner
                if (player_distances[i] >= road_lengths[current_segment] and 
                    current_segment < len(road_lengths) - 1):
                    player.right(90)
                    player_distances[i] = 0
                    players_at_corner += 1
                    
                # Check for finish
                elif (player.pos()[0] >= finish_pen.pos()[0] and 
                      current_segment == len(road_lengths) - 1):
                    player.write("I won!", font=FONT)
                    game_state["racing"] = False
                    
                    # Add restart option
                    restart_button = t.Turtle()
                    restart_button.shape("square")
                    restart_button.color("Yellow")
                    restart_button.shapesize(stretch_wid=2, stretch_len=8)
                    restart_button.up()
                    restart_button.goto(0, -50)
                    restart_button.write("Restart", align="center", font=SMALL_FONT)
                    
                    def on_restart_click(x, y):
                        if abs(x) < 80 and -70 < y < -30:
                            screen.onscreenclick(None)
                            main()  # Restart the game
                    
                    screen.onscreenclick(on_restart_click)
                    break
            
            # Update segment when all players turn
            if players_at_corner == len(players):
                current_segment += 1
                players_at_corner = 0
    
    def set_laps(laps):
        game_state["num_laps"] = laps
    
    # Show start screen
    draw_start_screen(screen, start_race, set_laps)

if __name__ == "__main__":
    main()
    t.done()
