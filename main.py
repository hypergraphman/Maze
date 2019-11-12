# Сам лабиринт, чтобы выводился на экран - сделано
# Кол-во шагов? - сделано
# Вход в лабиринт и точка старта у входа - сделано
# Выход из лабиринта - финиш - сделано
# уровни сложности - размер полей - сделано
#   1 - маленькая карта, шагов больше чем нужно в максимальном пути
#   2 - средняя карта, шагов столько же сколько в максимальном пути
#   3 - большая карта, шагов ровно сколько в минимальном пути
# Сообщение об окончании игры - сделано
# Возможность сохранять - сделано

# Создать поле, вывод поля на экран, и возможность ходить по этому полю
import copy
import random

lvl = [4, 7, 10]
width = 4
height = 4
player = (0, 1)
finish = (3, 0)
rest_step = 15
field = [[' ', ' ', ' ', '#'],
         ['#', '#', ' ', ' '],
         [' ', '#', ' ', '#'],
         [' ', ' ', ' ', '#']]


def print_field():
    global field, rest_step
    temp_field = copy.deepcopy(field)
    temp_field[player[0]][player[1]] = 'P'
    temp_field[finish[0]][finish[1]] = 'F'

    for i in range(height):
        for j in range(width):
            print(temp_field[i][j], end='')
        print()
    print('оставшееся кол-во шагов:', rest_step)


def step(cmd):
    global player, field, rest_step
    if cmd == 'r' and player[1] < width - 1 and field[player[0]][player[1] + 1] == ' ':
        player = (player[0], player[1] + 1)
    elif cmd == 'l' and player[1] > 0 and field[player[0]][player[1] - 1] == ' ':
        player = (player[0], player[1] - 1)
    elif cmd == 'u' and player[0] > 0 and field[player[0] - 1][player[1]] == ' ':
        player = (player[0] - 1, player[1])
    elif cmd == 'd' and player[0] < height - 1 and field[player[0] + 1][player[1]] == ' ':
        player = (player[0] + 1, player[1])
    rest_step -= 1


def save():
    global player, field, rest_step, finish, width, height
    with open('save.txt', 'w', encoding='utf-8') as save_file:
        print(*player, file=save_file)
        print(*finish, file=save_file)
        print(rest_step, file=save_file)
        print(width, height, file=save_file)
        for i in range(height):
            for j in range(width):
                print(field[i][j], end='', file=save_file)


def load():
    global player, field, rest_step, finish, width, height
    with open('save.txt', 'r', encoding='utf-8') as load_file:
        line = load_file.readline().split()
        player = (int(line[0]), int(line[1]))
        line = load_file.readline().split()
        finish = (int(line[0]), int(line[1]))
        rest_step = int(load_file.readline())
        line = load_file.readline().split()
        width = int(line[0])
        height = int(line[1])
        line = load_file.readline()
        for i in range(height):
            for j in range(width):
                field[i][j] = line[height * i + j]


def run_cmd(cmd):
    if cmd in 'rlud':
        step(cmd)
    elif cmd == 's':
        save()
    elif cmd == 'z':
        load()


def is_finish():
    global player, finish, rest_step
    return player == finish or rest_step < 1


# Вспомогательная функция для поиска пути, нужна только для того чтобы повысить читабельность кода
# сама эта функция вызывает основную функцию и ищет путь для 4х точек вокруг текущей
def find_path_nswe(temp_field, current_pos, current_step):
    if current_pos[0] + 1 < height:
        find_path(temp_field, (current_pos[0] + 1, current_pos[1]), current_step + 1)
    if current_pos[1] + 1 < width:
        find_path(temp_field, (current_pos[0], current_pos[1] + 1), current_step + 1)
    if current_pos[1] - 1 >= 0:
        find_path(temp_field, (current_pos[0], current_pos[1] - 1), current_step + 1)
    if current_pos[0] - 1 >= 0:
        find_path(temp_field, (current_pos[0] - 1, current_pos[1]), current_step + 1)


# волновой поиск пути мне показался слишком тяжелым в реализации,
# поэтому я решила придумать свой на основе полученного опыта при разборе
# волнового поиска
def find_path(temp_field, current_pos, current_step):
    global finish, height, width
    if temp_field[current_pos[0]][current_pos[1]] == ' ' or \
            isinstance(temp_field[current_pos[0]][current_pos[1]], int) and \
            int(temp_field[current_pos[0]][current_pos[1]]) > current_step:
        temp_field[current_pos[0]][current_pos[1]] = current_step
        find_path_nswe(temp_field, current_pos, current_step)

    if temp_field[finish[0]][finish[1]] == ' ':
        return 0
    else:
        return temp_field[finish[0]][finish[1]]


def generate_field():
    global player, finish, rest_step, field, height, width, lvl
    # создаем случайное поле
    field = []
    for i in range(height):
        row = []
        for j in range(width):
            if j % 2 == 0:
                row.append(['#', ' '][random.randint(0, 10) < 2])
            else:
                row.append(' ')
        field.append(row)
    for j in range(width):
        for i in range(height):
            if i % 2 == 1 and field[i][j] == random.choice(['#', ' ', '#', '# ']):
                field[i][j] = ['#', ' '][random.randint(0, 10) < 1]
    # создаем точки старта и финиша
    if ' ' in field[0] and ' ' in field[height - 1]:
        # точку старта ставим с левого края первой строки карты
        player = (0, field[0].index(' '))
        # точку финиша ставим с правого края последней строки карты
        finish = (height - 1, width - field[height - 1][::-1].index(' ') - 1)
        # точку финиша ставим с левого края последней строки карты
        # finish = (height - 1, field[height - 1].index(' '))
    else:
        # если точки старта и финиша создать не удалось, тогда говорим что карта не сгенерировалась
        return False

    # Ищем путь
    x = find_path(copy.deepcopy(field), player, 0)
    if x == 0:
        # если найти не удалось то говорим, что карта не сгенерировалась
        return False
    # в зависимости от уровня сложности задаем кол-во возможных шагов
    if lvl.index(height) == 0:
        rest_step = x * 2
    elif lvl.index(height) == 1:
        rest_step = int(x * 1.5)
    else:
        rest_step = x
    return True


def init():
    global height, width, lvl
    lvl_cmd = input('Выберите уровень сложности: 1, 2, 3\n')
    while not lvl_cmd.isdigit() and 1 <= int(lvl_cmd) <= 3:
        lvl_cmd = input('Наберите цифрой 1, 2 или 3\n')

    height = width = lvl[int(lvl_cmd) - 1]

    # генерируем поле пока не будет создано такое, которое можно пройти
    while not generate_field():
        pass


def game():
    while not is_finish():
        print_field()
        cmd = input('введите команду:\n'
                    'r - вправо, l - влево, u - вверх, d - вниз,\n'
                    's - сохранить, z - загрузить\n')
        run_cmd(cmd)

    print_field()
    if rest_step > 0:
        print('Лабиринт пройден, вы вышли из лабиринта')
    else:
        print('Вы не успели пройти лабиринт')


# выбираем уровень сложности и генерируем карту
# если закоментировать init() будет работать без генарации карт с картой по умолчанию,
# которая в самом начале кода
init()
# запускаем игру
game()
