from os import system, name as os_name, get_terminal_size
from re import findall
from requests import post, get
from random import choice
from io import BytesIO
from enchant import Dict
from base64 import b64decode, b64encode
from time import sleep
from ctypes import windll
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver import ChromeOptions, Chrome
from PIL import ImageGrab, Image
from threading import Thread

class Zefoy:
    def __init__(self) -> None:
        self.captcha_box = '/html/body/div[5]/div[2]/form/div/div'
        self.captcha_res = '/html/body/div[5]/div[2]/form/div/div/div/input'
        self.captcha_button = '/html/body/div[5]/div[2]/form/div/div/div/div/button'
        self.video_url_box = '/html/body/div[-]/div/form/div/input'
        self.search_box    = '/html/body/div[-]/div/form/div/div/button'
        '/html/body/div[11]/div/form/div/div/button'
        '//*[@id="c2VuZC9mb2xsb3dlcnNfdGlrdG9s"]/div[1]/div/form/button'
        self.sent = 0

        self.paths = {
            1 : ('/html/body/div[6]/div/div[2]/div/div/div[2]/div/button', 'c2VuZF9mb2xsb3dlcnNfdGlrdG9r'),
            2 : ('/html/body/div[6]/div/div[2]/div/div/div[3]/div/button', 'c2VuZE9nb2xsb3dlcnNfdGlrdG9r'),
            3 : ('/html/body/div[6]/div/div[2]/div/div/div[4]/div/button', 'c2VuZC9mb2xsb3dlcnNfdGlrdG9r'),
            4 : ('/html/body/div[6]/div/div[2]/div/div/div[5]/div/button', 'c2VuZC9mb2xeb3dlcnNfdGlrdG9V'),
            5 : ('/html/body/div[6]/div/div[2]/div/div/div[6]/div/button', 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s'),
            6 : ('/html/body/div[6]/div/div[2]/div/div/div[7]/div/button', 'c2VuZF9mb2xsb3dlcnNfdGlrdG9L')
        }

        self.banner = """

███████╗███████╗███████╗ ██████╗ ██╗   ██╗
╚══███╔╝██╔════╝██╔════╝██╔═══██╗╚██╗ ██╔╝
  ███╔╝ █████╗  █████╗  ██║   ██║ ╚████╔╝ 
 ███╔╝  ██╔══╝  ██╔══╝  ██║   ██║  ╚██╔╝  
███████╗███████╗██║     ╚██████╔╝   ██║   
╚══════╝╚══════╝╚═╝      ╚═════╝    ╚═╝   

Plati ~ discord.gg/DaEBWuYUUJ

"""   

    def clear(self) -> int:
        return system('cls' if os_name == 'nt' else 'clear')
    
    def title(self, content: str) -> int:
        return system(f'title {content}') if os_name == 'nt' else windll.kernel32.SetConsoleTitleW(content)
    
    def _print(self, thing: str or int, content: str or int, new_line: bool = True, input: bool = False) -> None or str:

        print('\033[?25l', end='')

        size = get_terminal_size().columns - 10
        col = "\033[38;2;0;-;255m"
        first_part = f"[{thing}] | {content}"
        new_part = ""
        
        counter = 0
        for caracter in first_part:
            new_part += col.replace('-', str(225 - counter * int(255/len(first_part)))) + caracter
            counter += 1 
            
        if input:
            return f"{new_part}"
            
        if not new_line:
            print(f"{new_part}{' '*(size - len(first_part))}\033[38;2;255;255;255m", end="\r")

        else:
            print(f"{new_part}{' '*(size - len(first_part))}\033[38;2;255;255;255m")
    
    def display_banner(self) -> str:
        
        first_color, second_color = '\033[38;2;170;180;255m', '\033[38;2;255;255;255m'

        banner = ""
        display_banner = ""

        for line in self.banner.splitlines():
            display_banner += " " * (int((get_terminal_size().columns - len(line)) / 2)) + line + "\n"

        for caracter in display_banner:
            if caracter in ['╚', '═', '╝', '╔', '║', '╗']:
                banner += second_color + caracter
            
            elif caracter in ' ':
                banner += caracter
            
            else:
                banner += first_color + caracter

        return banner

    def setup_driver(self) -> Chrome:
        return Chrome(ChromeOptions().add_argument('--lang=es'))
    
    def convert(self, minutes: int, seconds: int) -> int:
        return minutes * 60 + seconds + 3
    
    def get_stats(self, video_id: str) -> list:
        res = get(f'https://tikstats.io/video/{video_id}').text
        return findall(r'\d+', findall(r'.innerText=(.*), 1' , res)[0])
    
    def display_stats(self, video_id: str) -> None:

        print(self.display_banner())

        while True:
            try:
                sleep(1)
                views, shares, likes, comments, saves = self.get_stats(video_id)
                self._print('➕', f'Stats: [Views: {views} | Shares: {shares} | Likes: {likes} | Comments: {comments} | Saves: {saves}]', new_line=False)
            except: continue

    def get_id(self, video_url: str) -> str:
        return video_url.split('?')[0].split('/')[-1]

    def wait_for_path(self, xpath: str) -> WebElement:
        while True:
            try: return self.driver.find_element(By.XPATH, xpath)
            except: continue

    def load_zefoy(self) -> None:
        self.driver = self.setup_driver()
        self.driver.set_window_size(600, 900)
        sleep(2)

        self.driver.execute_script('window.open("https://zefoy.com");')
        #self.driver.get('https://zefoy.com')
        
        res = ''

        while not 'Enter the word' in res:
            with BytesIO() as bytes_array:
                ImageGrab.grab().save(bytes_array, format='PNG')
                res = post('https://platipus9999.pythonanywhere.com', json={'image': b64encode(bytes_array.getvalue()).decode()}).text


        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    def solve(self, resolve: bool = False) -> None:
        image_xpath = self.captcha_box + '/img'

        failed = False

        while True:
            if failed:
                image_xpath, self.captcha_res, self.captcha_button = f"{image_xpath}:{self.captcha_res}:{self.captcha_button}".replace('5', '6').split(':')

            img = self.wait_for_path(image_xpath).screenshot_as_base64

            captcha_answer = post('https://platipus9999.pythonanywhere.com', json={'image': img}).text.split('\n')[0]

            self._print('!', f'{captcha_answer}') if resolve else ''

            try:
                if not Dict("en_US").check(captcha_answer):
                    captcha_answer = Dict("en_US").suggest(captcha_answer)[0]
                    self._print('!', f'Trying {captcha_answer}') if resolve else ''
            except: pass

            self.driver.find_element(By.XPATH, self.captcha_res).send_keys(captcha_answer)
            self.driver.find_element(By.XPATH, self.captcha_button).click()

            try:
                sleep(1)
                self.driver.find_element(By.XPATH, self.paths[4][0])
                break

            except:
                self.wait_for_path('//*[@id="errorcapthcaclose"]/div/div/div[3]/button').click()
                failed = True

    def choice_service(self) -> None:

        display_dict = {
            True  : '✅',
            False : '❌'
        }

        print(self.display_banner())

        for number, xpath in self.paths.items():
            is_enabled = self.driver.find_element(By.XPATH, xpath[0]).is_enabled()
            name   = self.driver.find_element(By.XPATH, xpath[0].replace('button', 'h5')).text
            
            self._print(number, f'{name}{" " * (len("Comments Hearts ") - len(name))} | Status: {display_dict[is_enabled]}')

        print()
        self.choice = int(input(self._print('?', 'Choice a service > ', input=True)))

    def wait(self, seconds: int) -> None:
        for second in range(seconds):
            self.title(f'Tiktok Zefoy Bot ~ Using Selenium ▏  Sent: {self.sent} ▏  Cooldown: {seconds - (second + 1)}')
            sleep(1)

    def task(self) -> None:
        self.driver.find_element(By.XPATH, self.search_box.replace('-', f'{self.div}')).click()
        sleep(3)
            
        seconds = self.check_submit()
        if type(seconds) == int:
            self.wait(seconds)
            sleep(2)
            self.driver.find_element(By.XPATH, self.search_box.replace('-', f'{self.div}'))
            
        sleep(2)

        while True:
            try:
                self.driver.execute_script("function find_element(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } find_element('" + f'//*[@id="{self.paths[self.choice][1]}"]/div[1]/div/form/button' + "').click();")
                break
            except:
                self.driver.find_element(By.XPATH, self.search_box.replace('-', f'{self.div}')).click()

                if 'Session expired' in self.driver.page_source:
                    sleep(2)
                    self.driver.find_element(By.XPATH, f'//*[@id="{self.paths[self.choice][1]}"]/div/span/a').click()

                    self.solve(True)

                    sleep(1)
                    self.driver.find_element(By.XPATH, self.paths[self.choice][0]).click()

                    self.driver.find_element(By.XPATH, self.video_url_box.replace('-', f'{self.div}')).send_keys(self.video_url)

            sleep(2)


        while True:
            source = self.driver.page_source

            if 'sent' in source:
                self.sent += 1
                self.title(f'Tiktok Zefoy Bot ~ Using Selenium ▏  Sent: {self.sent} ▏  Cooldown: 0')
                break

            elif 'Too many requests' in source:
                sleep(3)
                break


    def check_submit(self):
        try:
            timer_response = self.driver.find_element(By.XPATH, f'//*[@id="{self.paths[self.choice][1]}"]/span').text

            if 'READY' in  timer_response:
                return True
            
            elif "seconds for your next submit" in  timer_response:
                minutes, seconds = findall(r'\d+',  timer_response)
                return self.convert(int(minutes), int(seconds))

        except:
            return False
            
    def main(self) -> None:
        self.clear()
        print(self.display_banner())
        self.title('Tiktok Zefoy Bot ~ Using Selenium ▏  Status: Loading')

        self.video_url = input(self._print('?', 'Video Url > ', input=True))
        video_id = self.get_id(self.video_url)

        self._print('!', 'Browser is loading\n')
        self.load_zefoy()
        self.wait_for_path(self.captcha_box)

        self.title('Tiktok Zefoy Bot ~ Using Selenium ▏  Status: Solving')
        self._print('*', 'Solving The Captcha')
        self.solve()
        
        self.clear()
        self.title('Tiktok Zefoy Bot ~ Using Selenium ▏  Status: N/A')

        self.choice_service()

        self.driver.find_element(By.XPATH, self.paths[self.choice][0]).click()

        self.div = int(findall(r'\d+', self.paths[self.choice][0])[-1]) + 5

        self.clear()
        Thread(target = self.display_stats, args = [video_id,]).start()

        self.driver.find_element(By.XPATH, self.video_url_box.replace('-', f'{self.div}')).send_keys(self.video_url)

        while True:
            self.task()
        

if __name__ == '__main__':
    Zefoy().main()
