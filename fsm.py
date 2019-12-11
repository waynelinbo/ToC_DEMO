from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url
from password import password
from GuessA4B4 import GuessA4B4
import random


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.p = password()
        self.g = GuessA4B4()

    # lobby
    def is_going_to_psw(self, event):
        text = event.message.text
        if text.lower() == "psw" :
            self.p.restart()
            return True
        else:
            return False

    def is_going_to_A4B4(self, event):
        text = event.message.text
        if text.lower() == "a4b4" :
            self.g.generate()
            return True
        else :
            return False

    def is_going_to_lobby_help(self, event):
        text = event.message.text
        return text.lower() == "help"

    def on_enter_lobby(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "You can choose 1 game to play\n1. guess password (0~999) => psw\n2. 4A4B (guess 4 integers) => A4B4\n\n* please input \"psw\" or \"A4B4\"\nif you need help please input \"help\" ")

    # lobby_help
    def on_enter_lobby_help(self, event):
        reply_token = event.reply_token
        #send_image_url(reply_token)
        send_text_message(reply_token, "1. guess password : it's a little game for guessing a password from 0 to 999. Whenever you guess the robot will tell you the range where the password in until you find it\n=> you can input \"psw\" to enter it\n2. 4A4B => it's a game for guessing 4 differents integers consist by 0 ~ 9. Whenever you guess, the robot will tell you how many numbers are in the correct place and how many numbers are in the uncorrect place\n=> you can input \"A4B4\" to enter it\n")
        self.lobby_help_back()

    # psw
    def psw_maintain(self, event):
        text = event.message.text
        num = 0
        try:
            num = int(text)
        except ValueError:
            return False

        c = self.p.compare(num)

        if (c == -2) | (c == 2) | (c == 0):
            return False
        else:
            return True

    def psw_go_back(self, event):
        text = event.message.text
        return text.lower() == "exit"

    def psw_success(self, event):
        text = event.message.text
        num = 0
        try:
            num = int(text)
        except ValueError:
            return False

        c = self.p.compare(num)

        if c == 0:
            return True
        else:
            return False
    
    def is_going_to_psw_help(self, event):
        text = event.message.text
        return text.lower() == "help"
    
    def on_enter_psw(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, str(self.p.down) + " ~ " + str(self.p.up) + " : ")
    
    # psw_help
    def on_enter_psw_help(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "the guess number should be in the range of the robot told, and you only can input a integer")
        # send_text_message(reply_token, str(self.p.down) + " ~ " + str(self.p.up) + " : ")
        self.psw_help_back()

    # psw_done
    def psw_again(self, event):
        text = event.message.text
        if text.lower() == "y" :
            self.p.restart()
            return True
        else :
            return False

    def psw_done_go_back(self, event):
        text = event.message.text
        return (text.lower() == "n") | (text.lower() == "exit")

    def on_enter_psw_done(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Congratulations !\nplay again ? (y/n) : ")

    # A4B4
    def A4B4_maintain(self, event):
        text = event.message.text

        a = self.g.compare(text,0)

        if (a == "2") | (a == "1") | (a == "0") | (a == "-1"):
            return False
        else:
            return True

    def A4B4_go_back(self, event):
        text = event.message.text
        return text.lower() == "exit"
    
    def A4B4_success(self, event):
        text = event.message.text
        a = self.g.compare(text,1)

        if a == "-1":
            return True
        else:
            return False
    
    def is_going_to_A4B4_help(self, event):
        text = event.message.text
        return text.lower() == "help"
    
    def on_enter_A4B4(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, self.g.record + "please input 4 different integers : ")
    
    # A4B4_help
    def on_enter_A4B4_help(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "the guess number should be 4 different integers, you only can use different integers and it's length is 4")
        # send_text_message(reply_token, str(self.p.down) + " ~ " + str(self.p.up) + " : ")
        self.A4B4_help_back()

    # A4B4_done
    def A4B4_again(self, event):
        text = event.message.text
        if text.lower() == "y":
            self.g.generate()
            return True
        else:
            return False

    def A4B4_done_go_back(self, event):
        text = event.message.text
        return (text.lower() == "n") | (text.lower() == "exit")

    def on_enter_A4B4_done(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, self.g.record + "Congratulations !\nplay again ? (y/n) : ")