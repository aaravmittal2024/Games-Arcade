import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')

# Fonts
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

# Timer and FPS
timer = pygame.time.Clock()
fps = 60

# Game variables
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

# Turn variables: 
# 0 - whites turn no selection
# 1 - whites turn piece selected
# 2 - black turn no selection
# 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

# Load game piece images for both black and white pieces
# Black pieces
black_queen = pygame.image.load('chessImages/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_king = pygame.image.load('chessImages/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_rook = pygame.image.load('chessImages/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_bishop = pygame.image.load('chessImages/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_knight = pygame.image.load('chessImages/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_pawn = pygame.image.load('chessImages/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

# White pieces
white_queen = pygame.image.load('chessImages/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_king = pygame.image.load('chessImages/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_rook = pygame.image.load('chessImages/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_bishop = pygame.image.load('chessImages/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_knight = pygame.image.load('chessImages/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_pawn = pygame.image.load('chessImages/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

# Image lists
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# Check variables and game over flag
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



def draw_pieces():
    # Draw white pieces on the board
    for i in range(len(white_pieces)):
        # Get the index of the current piece in the piece_list
        index = piece_list.index(white_pieces[i])
        
        # Draw the pawn pieces with a specific offset for better positioning
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        # Draw other white pieces
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        
        # Highlight the selected white piece with a red rectangle during white's turn
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    # Draw black pieces on the board
    for i in range(len(black_pieces)):
        # Get the index of the current piece in the piece_list
        index = piece_list.index(black_pieces[i])
        
        # Draw the pawn pieces with a specific offset for better positioning
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        # Draw other black pieces
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        
        # Highlight the selected black piece with a blue rectangle during black's turn
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)



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
    """
    Draw the captured pieces on the side of the screen.
    """
    
    # Draw captured white pieces
    for i, captured_piece in enumerate(captured_pieces_white):
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    
    # Draw captured black pieces
    for i, captured_piece in enumerate(captured_pieces_black):
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))



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
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

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