from random import choice, randint

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        self.body_color = BOARD_BACKGROUND_COLOR
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def draw(self):
        """Метод определяющий, как объект будет отрисовываться."""
        raise NotImplementedError(
            f'В классе {self.__class__.__name__}'
            f'метод draw не переопределен.')

    def get_rect(self, pos):
        """Функция для получения pg.Rect."""
        return pg.Rect(pos, (GRID_SIZE, GRID_SIZE))


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку."""

    def __init__(self):
        self.reset()
        self.direction = RIGHT

    def draw(self):
        """Метод отрисовывающий змейку на экране."""
        for position in self.positions[:-1]:
            rect = (self.get_rect(position))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = self.get_rect(self.positions[0])
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод изменяющий положение змейки на экране."""
        head_x, head_y = self.get_head_position()
        head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(
            0, (head[0], head[1]))
        last = self.positions.pop()

        if self.length != len(self.positions):
            self.positions.append(last)

        self.last = self.positions[-1] * (self.length > 1)

    def get_head_position(self):
        """Функция для получения координат головы змеи."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывающая все параметры."""
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко."""

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Метод отрисовывающий яблоко"""
        rect = self.get_rect(self.position)
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод устанавливающий случайное положение яблока"""
        new_apple_coordinates = (randint(0, GRID_WIDTH) * GRID_SIZE,
                                 randint(0, GRID_HEIGHT) * GRID_SIZE)

        if new_apple_coordinates != self.position:
            self.position = new_apple_coordinates
        else:
            self.randomize_position()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция приложения."""
    # Инициализация PyGame:
    pg.init()

    snake = Snake()
    apple = Apple()
  
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()

        if all(
                (snake.length > 2),
                (snake.get_head_position() in snake.positions[2::])):
            snake.reset()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        pg.display.flip()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
