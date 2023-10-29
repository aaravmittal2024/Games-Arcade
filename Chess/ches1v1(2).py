import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions and square size
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Set up the screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')

# Fonts
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

# Timer and FPS
timer = pygame.time.Clock()
fps = 60

# Game variables: piece types and initial locations
pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook', 'pawn',
          'rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook', 'pawn']
white_locations = [(x, 0) for x in range(8)] + [(x, 1) for x in range(8)]
black_locations = [(x, 7) for x in range(8)] + [(x, 6) for x in range(8)]

# Lists to track captured pieces
captured_pieces_white = []
captured_pieces_black = []

# Turn and selection variables
turn_step = 0  # 0: white's turn (no selection), 1: white's turn (piece selected), 2: black's turn (no selection), 3: black's turn (piece selected)
selection = 100
valid_moves = []

# Game state variables
counter = 0
winner = ''
game_over = False


def draw_board():
    # Draw the chessboard
    for i in range(32):
        column = i % 4
        row = i // 4
        
        # Draw alternating light gray squares for the chessboard
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
    
    # Draw the bottom gray bar
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    
    # Draw gold borders for the bottom bar and right side panel
    pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
    
    # Display the status text based on the current turn and step
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                   'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
    
    # Draw the grid lines for the chessboard
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
    
    # Display the "FORFEIT" text on the right side panel
    screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))


def draw_piece(color, letter, position):
    pygame.draw.circle(screen, color, position, 40)  # Draw the circle
    font = pygame.font.SysFont(None, 50)
    text = font.render(letter, True, WHITE if color == BLACK else BLACK)
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)

def draw_pieces():
    # Black pieces
    for i in range(8):
        draw_piece(BLACK, 'P', (i*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'R', (0, SQUARE_SIZE//2))
    draw_piece(BLACK, 'N', (SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'B', (2*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'Q', (3*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'K', (4*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'B', (5*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'N', (6*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))
    draw_piece(BLACK, 'R', (7*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE//2))

    # White pieces
    for i in range(8):
        draw_piece(WHITE, 'P', (i*SQUARE_SIZE + SQUARE_SIZE//2, 6*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'R', (0, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'N', (SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'B', (2*SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'Q', (3*SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'K', (4*SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'B', (5*SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'N', (6*SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))
    draw_piece(WHITE, 'R', (7*SQUARE_SIZE + SQUARE_SIZE//2, 7*SQUARE_SIZE + SQUARE_SIZE//2))



def check_options(pieces, locations, turn):
    """
    Check valid moves for all pieces on the board.
    """
    
    all_moves_list = []

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        moves_list = []

        # Check valid moves based on the type of the piece
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)

        # Append the valid moves for the current piece to the overall list
        all_moves_list.append(moves_list)

    return all_moves_list



def check_king(position, color):
    """
    Check valid moves for the king.
    """

    moves_list = []

    # Determine enemy and friend pieces based on the king's color
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Define potential moves for the king (one square in any direction)
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

    # Check each potential move
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])

        # Ensure the move is within the board and not onto a friendly piece
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list



def check_queen(position, color):
    """
    Check valid moves for the queen.
    """
    
    # Get valid moves for the bishop (diagonal moves)
    moves_list = check_bishop(position, color)
    
    # Get valid moves for the rook (horizontal and vertical moves)
    second_list = check_rook(position, color)
    
    # Combine the moves from both lists
    for move in second_list:
        moves_list.append(move)

    return moves_list



def check_bishop(position, color):
    """
    Calculate the valid moves for a bishop from a given position and color.
    """
    
    moves_list = []
    
    # Define the directions for the bishop's movement: up-right, up-left, down-right, down-left
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
    
    # Set the enemy and friend lists based on the bishop's color
    enemies_list = black_locations if color == 'white' else white_locations
    friends_list = white_locations if color == 'white' else black_locations
    
    # Iterate over each direction
    for dx, dy in directions:
        chain = 1
        while True:
            new_x = position[0] + (chain * dx)
            new_y = position[1] + (chain * dy)
            new_position = (new_x, new_y)
            
            # Check if the new position is within the board and not occupied by a friend
            if 0 <= new_x <= 7 and 0 <= new_y <= 7 and new_position not in friends_list:
                moves_list.append(new_position)
                
                # If the new position is occupied by an enemy, stop checking in this direction
                if new_position in enemies_list:
                    break
                chain += 1
            else:
                break
                
    return moves_list



def check_rook(position, color):
    """
    Calculate the valid moves for a rook from a given position and color.
    """
    
    moves_list = []
    
    # Define the directions for the rook's movement: down, up, right, left
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # Set the enemy and friend lists based on the rook's color
    enemies_list = black_locations if color == 'white' else white_locations
    friends_list = white_locations if color == 'white' else black_locations
    
    # Iterate over each direction
    for dx, dy in directions:
        chain = 1
        while True:
            new_x = position[0] + (chain * dx)
            new_y = position[1] + (chain * dy)
            new_position = (new_x, new_y)
            
            # Check if the new position is within the board and not occupied by a friend
            if 0 <= new_x <= 7 and 0 <= new_y <= 7 and new_position not in friends_list:
                moves_list.append(new_position)
                
                # If the new position is occupied by an enemy, stop checking in this direction
                if new_position in enemies_list:
                    break
                chain += 1
            else:
                break
                
    return moves_list



def check_pawn(position, color):
    """
    Calculate the valid moves for a pawn from a given position and color.
    """
    
    moves_list = []
    
    # Check moves for white pawn
    if color == 'white':
        # Forward move by 1 step
        forward_one = (position[0], position[1] + 1)
        if forward_one not in white_locations and forward_one not in black_locations and position[1] < 7:
            moves_list.append(forward_one)
        
        # Forward move by 2 steps (only from starting position)
        forward_two = (position[0], position[1] + 2)
        if forward_two not in white_locations and forward_two not in black_locations and position[1] == 1:
            moves_list.append(forward_two)
        
        # Capture diagonally to the right
        capture_right = (position[0] + 1, position[1] + 1)
        if capture_right in black_locations:
            moves_list.append(capture_right)
        
        # Capture diagonally to the left
        capture_left = (position[0] - 1, position[1] + 1)
        if capture_left in black_locations:
            moves_list.append(capture_left)
    
    # Check moves for black pawn
    else:
        # Forward move by 1 step
        forward_one = (position[0], position[1] - 1)
        if forward_one not in white_locations and forward_one not in black_locations and position[1] > 0:
            moves_list.append(forward_one)
        
        # Forward move by 2 steps (only from starting position)
        forward_two = (position[0], position[1] - 2)
        if forward_two not in white_locations and forward_two not in black_locations and position[1] == 6:
            moves_list.append(forward_two)
        
        # Capture diagonally to the right
        capture_right = (position[0] + 1, position[1] - 1)
        if capture_right in white_locations:
            moves_list.append(capture_right)
        
        # Capture diagonally to the left
        capture_left = (position[0] - 1, position[1] - 1)
        if capture_left in white_locations:
            moves_list.append(capture_left)
                
    return moves_list



def check_knight(position, color):
    """
    Calculate the valid moves for a knight from a given position and color.
    """
    
    moves_list = []
    
    # Set the enemy and friend lists based on the knight's color
    enemies_list = black_locations if color == 'white' else white_locations
    friends_list = white_locations if color == 'white' else black_locations
    
    # Define the possible moves for the knight
    # Knights can move two squares in one direction and one square in the perpendicular direction
    targets = [
        (1, 2), (1, -2), (2, 1), (2, -1),
        (-1, 2), (-1, -2), (-2, 1), (-2, -1)
    ]
    
    # Check each possible move
    for dx, dy in targets:
        new_x = position[0] + dx
        new_y = position[1] + dy
        new_position = (new_x, new_y)
        
        # Check if the new position is within the board and not occupied by a friend
        if 0 <= new_x <= 7 and 0 <= new_y <= 7 and new_position not in friends_list:
            moves_list.append(new_position)
                
    return moves_list



def check_valid_moves():
    """
    Check the valid moves for the currently selected piece based on the current turn step.
    """
    
    # Determine which options list to use based on the current turn step
    options_list = white_options if turn_step < 2 else black_options
    
    # Retrieve the valid moves for the selected piece
    valid_options = options_list[selection]
    
    return valid_options



def draw_valid(moves):
    """
    Draw the valid moves for the selected piece on the screen.
    """
    
    # Determine the color to use for drawing based on the current turn step
    color = 'red' if turn_step < 2 else 'blue'
    
    # Draw each valid move as a circle on the screen
    for move in moves:
        pygame.draw.circle(screen, color, (move[0] * 100 + 50, move[1] * 100 + 50), 5)



def draw_captured():
    circle_radius = 20
    letter_font = pygame.font.Font('freesansbold.ttf', 30)

    # Draw captured white pieces
    for i, piece in enumerate(captured_pieces_white):
        pygame.draw.circle(screen, BLACK, (825, 30 + 50 * i), circle_radius)
        piece_letter = letter_font.render(piece[0].upper(), True, WHITE)
        screen.blit(piece_letter, (825 - piece_letter.get_width() // 2, 30 + 50 * i - piece_letter.get_height() // 2))
    
    # Draw captured black pieces
    for i, piece in enumerate(captured_pieces_black):
        pygame.draw.circle(screen, WHITE, (925, 30 + 50 * i), circle_radius)
        piece_letter = letter_font.render(piece[0].upper(), True, BLACK)
        screen.blit(piece_letter, (925 - piece_letter.get_width() // 2, 30 + 50 * i - piece_letter.get_height() // 2))


def draw_check():
    """
    Draw a flashing square around the king if it's in check.
    """
    
    # Check for white king in check
    if turn_step < 2 and 'king' in white_pieces:
        king_index = white_pieces.index('king')
        king_location = white_locations[king_index]
        
        # Check if any black piece has the white king's location in its valid moves
        for options in black_options:
            if king_location in options and counter < 15:
                pygame.draw.rect(screen, 'dark red', 
                                 [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)
                break  # Exit loop once the king is found in check

    # Check for black king in check
    elif 'king' in black_pieces:
        king_index = black_pieces.index('king')
        king_location = black_locations[king_index]
        
        # Check if any white piece has the black king's location in its valid moves
        for options in white_options:
            if king_location in options and counter < 15:
                pygame.draw.rect(screen, 'dark blue', 
                                 [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)
                break  # Exit loop once the king is found in check



def draw_game_over():
    """
    Draw the game over screen, displaying the winner and a prompt to restart the game.
    """
    
    # Draw a black rectangle as the background for the game over message
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    
    # Display the winner's message
    winner_message = font.render(f'{winner} won the game!', True, 'white')
    screen.blit(winner_message, (210, 210))
    
    # Display the restart prompt
    restart_prompt = font.render(f'Press ENTER to Restart!', True, 'white')
    screen.blit(restart_prompt, (210, 240))


# Mainloop
# Initializing the options for black and white pieces
black_options = check_options(draw_pieces, black_locations, 'black')
white_options = check_options(draw_pieces, white_locations, 'white')

# Main game loop
run = True
while run:
    # Limit the frame rate
    timer.tick(fps)
    
    # Counter logic
    if counter < 30:
        counter += 1
    else:
        counter = 0

    # Fill the screen with a dark gray color
    screen.fill('dark gray')
    
    # Drawing functions
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    
    # If a piece is selected, show its valid moves
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # Event handling loop
    for event in pygame.event.get():
        # Close the game if the close button is clicked
        if event.type == pygame.QUIT:
            run = False
        
        # Handle mouse button down events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # Calculate the board coordinates from the pixel coordinates
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            
            # Logic for white's turn
            if turn_step <= 1:
                # Check for special board positions
                if click_coords in [(8, 8), (9, 8)]:
                    winner = 'black'
                # Selecting a white piece
                elif click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                # Moving a selected white piece
                elif click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            # Logic for black's turn
            elif turn_step > 1:
                # Check for special board positions
                if click_coords in [(8, 8), (9, 8)]:
                    winner = 'white'
                # Selecting a black piece
                elif click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                # Moving a selected black piece
                elif click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []

        # Handle key press events when the game is over
        if event.type == pygame.KEYDOWN and game_over:
            # Restart the game if the Enter key is pressed
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    # Check for game over condition
    if winner:
        game_over = True
        draw_game_over()

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()