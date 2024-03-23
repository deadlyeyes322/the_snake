from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        self.body_color = (0, 0, 0)
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def draw(self):
        """Метод определяющий, как объект будет отрисовываться."""
        pass


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку."""

    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def draw(self):
        """Метод отрисовывающий змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод изменяющий положение змейки на экране."""
        head = self.get_head_position()
        head = (head[0] + self.direction[0] * GRID_SIZE, head[1] + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, (head[0] % SCREEN_WIDTH, head[1] % SCREEN_HEIGHT))
        last = self.positions.pop()
        
        if self.length > 2 and head in self.positions[2::]:
            self.reset()
        
        if self.length != len(self.positions):
            self.positions.append(last)
        
        self.last = self.positions[-1] * (self.length > 1)

    def get_head_position(self):
        """Функция для получения координат головы змеи."""
        return self.positions[0]
    
    def reset(self):
        """Метод сбрасывающая все параметры."""
        self.__init__()
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко."""

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = randint(0, GRID_WIDTH) * GRID_SIZE, \
            randint(0, GRID_HEIGHT) * GRID_SIZE

    def draw(self):
        """Метод отрисовывающий яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
    def randomize_position(self):
        """Метод устанавливающий случайное положение яблока"""
        new_apple_coordinates = randint(0, GRID_WIDTH) * GRID_SIZE, \
            randint(0, GRID_HEIGHT) * GRID_SIZE

        if new_apple_coordinates != self.position:
            self.position = new_apple_coordinates
        else:
            self.randomize_position()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция приложения."""
    snake = Snake()
    apple = Apple()
    snake.draw()
    apple.randomize_position()
    apple.draw()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()

        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        
        pygame.display.flip()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
