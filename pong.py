import py5

# Variables globales
paddle1_y = paddle2_y = 0
paddle_width = paddle_height = 0
paddle_speed = ball_size = 0
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
game_time = 0  # Reloj de juego
last_time = 0  # Almacenará el tiempo del cuadro anterior
color_cycle_time = 0  # Tiempo para ciclo de colores
trail = []  # Lista para almacenar la estela de la pelota

# Estado de las teclas presionadas
keys = set()

def setup():
    py5.size(800, 400)
    global paddle_width, paddle_height, paddle_speed, ball_size
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle1_y, paddle2_y, player1_score, player2_score, game_time, last_time
    paddle_width = 20
    paddle_height = 100
    paddle_speed = 7
    ball_size = 20
    reset_game()
    last_time = py5.millis()  # Inicializar el tiempo

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y, player1_score, player2_score, game_time
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5  # Velocidad reducida de la pelota
    ball_dy = 3
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0
    game_time = 0

def draw():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score, game_time, last_time, color_cycle_time, trail

    # Fondo negro para limpiar la pantalla en cada cuadro
    py5.background(0)

    # Calcular el tiempo transcurrido en segundos
    current_time = py5.millis()
    delta_time = (current_time - last_time) / 1000.0
    game_time += delta_time
    last_time = current_time

    # Dibujar las paletas
    py5.fill(255, 0, 0)  # Color rojo para la paleta izquierda
    py5.rect(30, paddle1_y, paddle_width, paddle_height)
    py5.fill(0, 0, 255)  # Color azul para la paleta derecha
    py5.rect(py5.width - 30 - paddle_width, paddle2_y, paddle_width, paddle_height)

    # Actualizar el color de la pelota en un ciclo de degradado
    color_cycle_time += delta_time * 0.5  # Ajuste de velocidad del cambio de color
    t = (py5.sin(color_cycle_time) + 1) / 2  # Oscilar entre 0 y 1 para el ciclo
    green = py5.color(0, 255, 100)  # Verde
    cyan = py5.color(100, 255, 255)  # Celeste
    ball_color = py5.lerp_color(green, cyan, t)  # Mezcla de colores

    # Dibujar la estela de la pelota
    trail.append((ball_x, ball_y, ball_color))
    if len(trail) > 20:  # Limitar el tamaño de la estela
        trail.pop(0)

    for i, (x, y, color) in enumerate(trail):
        alpha = int(255 * (1 - (i / len(trail))))  # Desvanecer el color
        py5.fill(py5.red(color), py5.green(color), py5.blue(color), alpha)
        py5.ellipse(x, y, ball_size, ball_size)

    # Dibujar la pelota con el color en degradado
    py5.fill(ball_color)
    py5.ellipse(ball_x, ball_y, ball_size, ball_size)

    # Dibujar el marcador
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.fill(255)
    py5.text(f"{player1_score} - {player2_score}", py5.width / 2, 40)

    # Dibujar el reloj en la esquina superior derecha
    py5.text_size(24)
    minutes = int(game_time // 60)
    seconds = int(game_time % 60)
    py5.text(f"{minutes:02}:{seconds:02}", py5.width - 60, 40)

    # Actualizar posición de la pelota
    ball_x += ball_dx
    ball_y += ball_dy

    # Rebote de la pelota en la parte superior e inferior
    if ball_y <= ball_size / 2 or ball_y >= py5.height - ball_size / 2:
        ball_dy *= -1

    # Verificar colisiones con las paletas
    if ball_x - ball_size / 2 <= 30 + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1  # Sin incremento de velocidad
            ball_x = 30 + paddle_width + ball_size / 2

    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1  # Sin incremento de velocidad
            ball_x = py5.width - 30 - paddle_width - ball_size / 2

    # Si la pelota sale por la izquierda
    if ball_x < 0:
        player2_score += 1
        reset_ball()

    # Si la pelota sale por la derecha
    if ball_x > py5.width:
        player1_score += 1
        reset_ball()

    # Limitar el movimiento de las paletas
    if 'w' in keys and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if 's' in keys and paddle1_y < py5.height - paddle_height:
        paddle1_y += paddle_speed
    if 'o' in keys and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if 'l' in keys and paddle2_y < py5.height - paddle_height:
        paddle2_y += paddle_speed

def key_pressed():
    global keys
    keys.add(py5.key)

def key_released():
    global keys
    keys.discard(py5.key)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5  # Velocidad original
    ball_dy = py5.random(-3, 3)

if __name__ == "__main__":
    py5.run_sketch()
