import random
import tkinter as tk
import keyboard
import threading

root = tk.Tk()
root.geometry('600x700')
root.title('Sudoku')

canvas = tk.Canvas(root, width=600, height=800, bg='bisque')
canvas.create_rectangle(20, 9, 40, 32, fill='white')

canvas.pack()
dictionary = {}

"""Here you can add Sudoku grids (It must be in LIST and it goes from LEFT to RIGHT from TOP to BOTTOM, Empty have value 0);"""
grids = [
        [6, 0, 2, 7, 1, 8, 9, 0, 4, 3, 4, 0, 0, 2, 9, 1, 6, 0, 1, 9, 8, 3, 0, 6, 2, 5, 7, 2, 6, 9, 0, 3, 0, 8, 7, 0, 0, 7, 1, 9, 0, 5, 0, 4, 0, 4, 0, 5, 8, 7, 2, 6, 0, 1, 0, 8, 6, 2, 5, 3, 4, 1, 9, 0, 1, 4, 6, 8, 0, 5, 2, 3, 0, 0, 0, 4, 0, 0, 7, 0, 6],
        [7, 8, 0, 4, 0, 0, 1, 2, 0, 6, 0, 0, 0, 7, 5, 0, 0, 9, 0, 0, 0, 6, 0, 1, 0, 7, 8, 0, 0, 7, 0, 4, 0, 2, 6, 0, 0, 0, 1, 0, 5, 0, 9, 3, 0, 9, 0, 4, 0, 6, 0, 0, 0, 5, 0, 7, 0, 3, 0, 0, 0, 1, 2, 1, 2, 0, 0, 0, 7, 4, 0, 0, 0, 4, 9, 2, 0, 6, 0, 0, 7],
        [8, 1, 0, 0, 3, 0, 0, 2, 7, 0, 6, 2, 0, 5, 0, 0, 9, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 6, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 8, 0, 0, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 2, 0, 0, 1, 0, 7, 5, 0, 3, 8, 0, 0, 7, 0, 0, 4, 2],
        [4, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 8, 3, 0, 0, 0, 8, 2, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 0, 9, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6, 7, 0, 0, 5, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 2, 0, 0, 9, 0, 7, 6, 4, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 9, 7, 2, 1, 3, 8, 6, 8, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 9, 0, 7, 0, 4, 4, 0, 0, 0, 3, 0, 0, 0, 9, 6, 0, 0, 4, 0, 2, 0, 0, 7, 3, 0, 0, 0, 8, 0, 0, 0, 5, 7, 0, 3, 0, 4, 0, 6, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 8, 9, 8, 4, 1, 6, 5, 2, 0, 0],
        ]

grid = random.choice(grids)
grid_original = grid.copy()


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


class HoverButton(tk.Button):
    def __init__(self, master, **kwargs):
        global number_button, last_created, counter, button_list
        tk.Button.__init__(self, master=master, **kwargs)

        self.width = kwargs.get('padx', None)
        self.height = kwargs.get('pady', None)

        self.defaultBackground = self["background"]

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        if grid[counter] == 0:
            dictionary[str(self)] = [self, 'open', '  ']
        else:
            dictionary[str(self)] = [self, 'closed', grid[counter]]
        counter += 1

        button_list.append(self)

    def on_enter(self, e):
        global last_button, pressed_index

        # We keep track of last button here (It was last button which mouse hovered on)
        last_button = self

        # Make button with mouse hovered on it little darker and displays active number if it is valid
        if self not in pressed_index and dictionary[str(self)][1] == 'open':
            self.config(text=number, fg='gray', activeforeground='gray', font=('Arial', 11, 'bold'), bg='gray90')

    def on_leave(self, e):
        global button_pressed

        # Change button color and number to original which was displayed before hovering
        if not button_pressed and self not in pressed_index and dictionary[str(self)][1] == 'open':
            self.config(text=dictionary[str(last_button)][2], fg='black', font=('Arial', 11, 'bold'), bg='gray93')

        button_pressed = False


old_number = 0
counter = 0


def track_keyboard():
    global number, old_number
    while True:
        try:  # used try so that if user pressed other than the given key error will not be shown

            if keyboard.is_pressed('1'):
                number = 1

            elif keyboard.is_pressed('2'):
                number = 2

            elif keyboard.is_pressed('3'):
                number = 3

            elif keyboard.is_pressed('4'):
                number = 4

            elif keyboard.is_pressed('5'):
                number = 5

            elif keyboard.is_pressed('7'):
                number = 7

            elif keyboard.is_pressed('8'):
                number = 8

            elif keyboard.is_pressed('9'):
                number = 9

            elif keyboard.is_pressed('6'):
                number = 6

            # To avoid refreshing active number every frame
            # Only refreshes if user pressed different number
            if old_number != number:

                for el in dictionary.values():
                    # Highlights spaces with value of active number
                    if el[2] == number:
                        el[0].config(bg='peach puff')

                    else:
                        el[0].config(bg='gray93')

            # Rewrite active number in top left corner
            if old_number != number:
                old_number = number
                canvas.delete('active_number')
                canvas.create_text(30, 20, text=number, font=('Arial', 18), tag='active_number')

        except:
            continue


s, m, h = 0, 0, 0
s_zero, m_zero, h_zero = 0, 0, 0


def clock():
    global s, m, h, s_zero, m_zero, h_zero

    # Delete old time
    canvas.delete('timer')
    # Create new time
    canvas.create_text(
        290, 28, text="%s%s:%s%s" % (m_zero, m, s_zero, s), tag='timer', font=('Arial', 20))

    s += 1
    if s == 60:
        m += 1
        s = 0
    elif m == 60:
        h += 1
        m = 0

    if s >= 10:
        s_zero = ''
    else:
        s_zero = 0

    if m >= 10:
        m_zero = ''
    else:
        m_zero = 0

    # After 1 second, call Run again (start an infinite recursive loop)
    root.after(1000, clock)


button_pressed = False


def update_button():
    global button_pressed

    # Updates only if we click valid button (open)
    if dictionary[str(last_button)][1] == 'open':
        button_pressed = True
        last_button.config(text=number, fg='black', font=('Arial', 11, 'bold'))
        pressed_index.append(button_list.index(last_button))

        grid[pressed_index[len(pressed_index) - 1]] = number

        dictionary[str(last_button)][2] = number


def check_win():
    solut = solution()
    if grid == solut:
        print('Correct')
    else:
        for el in dictionary.values():
            if el[2] != solut[[i for i in dictionary.values()].index(el)]:
                el[0].config(bg='OrangeRed2')


def solution():
    global grid, grid_original
    grid_solved = []
    board = []
    count = 0
    while count != 9:
        board.append([el for el in grid_original[count * 9:count * 9 + 9]])
        count += 1
    solve(board)

    for el in board:
        for i in el:
            grid_solved.append(i)

    return grid_solved


def show_solution():
    s = solution()
    for el in dictionary.values():
        el[0].config(text=s[[i for i in dictionary.values()].index(el)])
        el[2] = s[[i for i in dictionary.values()].index(el)]
    root.update()


pressed_index = []
button_list = []

last_button = 0
number = 0
button_x = 20
button_y = -30

# Start side thread for tracking keyboard
thread = threading.Thread(target=track_keyboard)
thread.start()

for i in range(81):
    # Every 3 buttons adds a gap on x
    if i % 3 == int():
        button_x += 14

        # Every 27 buttons adds a gap on y
        if i % 27 == int():
            button_y += 14

        # Every 9 buttons goes in the next line
        if i % 9 == int():
            button_y += 66
            button_x = 13

    HoverButton(root, padx=20, pady=18, command=update_button, font=('Arial', 11, 'bold'), bg='gray93').place(
        x=button_x,
        y=button_y)
    button_x += 60

for el in dictionary.values():
    el[0].config(text=el[2])

    if el[2] != '  ':
        el[0].config(state='disabled')

tk.Button(root, bg='green', height=1, width=2, command=check_win).place(x=520, y=15)
tk.Button(root, bg='gray83', height=1, width=8, command=show_solution, text='SOLUTION').place(x= 450, y= 15)

clock()
root.mainloop()
