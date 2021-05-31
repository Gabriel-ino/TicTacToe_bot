import telebot
from time import sleep
import os
import sys

table = [' ' for c in range(9)]
token = 'YOUR TOKEN HERE'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """ Hi, I'm a robot who can play tic tac toe with you, type /play to begin the game or \
    /cancel to cancel\n To choose your letter position, the coordinates are: \n\nTop: 0-2\nMiddle: 3-5\nBottom: 6-8 """)


@bot.message_handler(commands=['play'])
def init_game(message):
    game_table = print_table(table)
    bot.reply_to(message, """\
    Ok, the game will init
    """)
    bot.reply_to(message, game_table)


@bot.message_handler(func=lambda message: True)
def playing(message):
    options = [str(x) for x in range(9)]
    if message.text not in options:
        bot.reply_to(message, """\
        Please, choose a valid option
        """)
    else:
        run(int(message.text))
        game_table = print_table(table)
        bot.send_message(message.chat.id, game_table)

    if check_win():
        game_table = print_table(table)
        message_ = run(None) + '\n' + game_table
        bot.send_message(message.chat.id, message_)
        os.execl(sys.executable, sys.executable, *sys.argv)


def print_table(table_):
    message = '\n'
    for pos in range(2, len(table_), 3):
        message += f'{table_[pos - 2]} | {table_[pos - 1]}\t|{table_[pos]}\n -+-+-\n'
    print(message)
    return message


def space_free(position: int):
    if table[position] == ' ':
        return True
    else:
        return False


def check_draw():
    for pos in range(len(table)):
        if table[pos] == ' ':
            return False
    return True


def check_win():
    if table[0] == table[1] and table[0] == table[2] and table[0] != ' ':
        return True
    elif table[0] == table[3] and table[0] == table[6] and table[0] != ' ':
        return True
    elif table[0] == table[4] and table[0] == table[8] and table[0] != ' ':
        return True
    elif table[1] == table[4] and table[1] == table[7] and table[1] != ' ':
        return True
    elif table[2] == table[5] and table[2] == table[8] and table[2] != ' ':
        return True
    elif table[2] == table[4] and table[2] == table[6] and table[2] != ' ':
        return True
    elif table[3] == table[4] and table[3] == table[5] and table[3] != ' ':
        return True
    elif table[6] == table[7] and table[6] == table[8] and table[6] != ' ':
        return True
    else:
        return False


def check_mark(mark):
    if table[0] == table[1] and table[0] == table[2] and table[0] == mark:
        return True
    elif table[0] == table[3] and table[0] == table[6] and table[0] == mark:
        return True
    elif table[0] == table[4] and table[0] == table[8] and table[0] == mark:
        return True
    elif table[1] == table[4] and table[1] == table[7] and table[1] == mark:
        return True
    elif table[2] == table[5] and table[2] == table[8] and table[2] == mark:
        return True
    elif table[2] == table[4] and table[2] == table[6] and table[2] == mark:
        return True
    elif table[3] == table[4] and table[3] == table[5] and table[3] == mark:
        return True
    elif table[6] == table[7] and table[6] == table[8] and table[6] == mark:
        return True
    else:
        return False


def put_letter(letter, position: int):
    if not space_free(position):
        return False
    else:
        table[position] = letter
        print_table(table)
        if check_draw():
            print('Draw')
            exit()

        if check_win():
            print('okwin')
            if letter == 'X':
                return False
            else:
                return True

        return True


player_letter = 'O'
bot_letter = 'X'


def player_move(move):
    pos = move
    ok = put_letter(player_letter, pos)
    return ok


def minimax(table_, depth, is_maximizing):
    if check_mark(bot_letter):
        return 1
    elif check_mark(player_letter):
        return -1
    elif check_draw():
        return 0

    if is_maximizing:
        best_score = -1000
        for val in range(len(table_)):
            if table_[val] == ' ':
                table_[val] = bot_letter
                score = minimax(table_, 0, False)
                table_[val] = ' '
                if score > best_score:
                    best_score = score
    else:
        best_score = 800
        for val in range(len(table_)):
            if table_[val] == ' ':
                table_[val] = bot_letter
                score = minimax(table_, depth + 1, True)
                table_[val] = ' '
                if score < best_score:
                    best_score = score
    return best_score


def bot_move(play):
    if play:
        best_score = -1000
        best_move = 0
        for val in range(len(table)):
            if table[val] == ' ':
                table[val] = bot_letter
                score = minimax(table, 0, False)
                table[val] = ' '
                if score > best_score:
                    best_score = score
                    best_move = val
        put_letter(bot_letter, best_move)
    else:
        pass


def winner(win):
    if win:
        return 'The player wins!!! To play again type /start and then /play'
    else:
        return 'The bot wins!!! To play again type /start and then /play'


def run(move):
    global table
    the_winner = check_win()
    if not check_win():
        bot_play = player_move(move)
        sleep(1.3)
        bot_move(bot_play)
    message = winner(the_winner)
    return message


def main():
    bot.polling()


if __name__ == '__main__':
    main()
