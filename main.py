import pyautogui
import pywinauto
import requests
from time import sleep


class Main:
    def __init__(self, port=21337):
        self.url = f"http://127.0.0.1:{port}/positional-rectangles"
        self.position = (312, 40)
        self.state = 'disabled'
        self.rate = 1

    def get_game_state(self):
        try:
            self.state = requests.get(self.url).json()['GameState']
        except requests.exceptions.ConnectionError:
            print('game is not running')
            self.state = 'off'

    def disable_emote(self):
        app = pywinauto.Application().connect(path='LoR.exe')
        old_position = pyautogui.position()
        try:
            app.UnityWndClass.click_input(coords=self.position)
        except RuntimeError as e:
            # get error message
            if str(e) == 'There is no active desktop required for moving mouse cursor!':
                return False
        pywinauto.mouse.move(coords=old_position)
        return True

    def valid_state(self):
        old_state = self.state
        self.get_game_state()
        if old_state in ['Menus', None] and self.state == 'InProgress':
            self.rate = 10
            return True
        else:
            self.rate = 1

    def run(self):
        while True:
            sleep(self.rate)
            if self.valid_state():
                sleep(10)
                disabled = False
                while not disabled:
                    disabled = self.disable_emote()
                    sleep(5)
            elif self.state == 'off':
                break


if __name__ == '__main__':
    main = Main()
    main.run()

