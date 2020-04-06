from selenium import webdriver
from time import sleep

class Bot:

    # In case you get an "Element Not Found Error" just right click on the element.
    # Inspect the element.
    # Copy the XPath of that element and replace with the XPath present in the code.

    def __init__(self, username, pw):

        self.username = username
        # Place the chromium web driver in the same directory or add it in the PATH.
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")

        # To wait before the webpage gets completely loaded.
        sleep(5)

        # Entering the username and password.
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)

        # Attempting to log in using the given username and password.
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        sleep(5)

        # Removing the dialogue box which asks to show notification.
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

        sleep(2)

    def get_unfollowers(self):

        # Clicking on the profile button.
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').click()
        sleep(5)

        # Clicking the "Following" button to get a list of people whom you follow.
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()

        # Fetching the name and storing them in a list.
        following = self.get_names()

        # Clicking the "Followers" button to get a list of people who follow you.
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()

        # Fetching the name and storing them in a list.
        followers = self.get_names()

        # Creating a list of accounts whom you follow but who do not follow back.
        not_following_back = [user for user in following if user not in followers]

        print(not_following_back)

    def get_names(self):

        # Initially waiting for the webpage to load completely.
        sleep(2)

        # Getting the scroll box element so we can iterate through it.
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]")
        last_hieght, hieght = 0, 1
        
        # Scrolling down to the end of the box so that all the names can get loaded.
        # A JS script is getting executed here which actually scrolls in the box.
        while last_hieght != hieght:
            last_hieght = hieght
            sleep(1)
            hieght = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        # Fetching all the 'a' html tags.
        links = scroll_box.find_elements_by_tag_name('a')

        # Filtering the list of 'a' tags for the names.
        names = [name.text for name in links if name.text != '']

        # Clicking the close button.
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/button").click()
        return names


#To read username and password from a seperate text file.
file = open('credentials.txt', 'r')
sender_email, sender_password = file.readlines()

obj = Bot(sender_email, sender_password)
obj.get_unfollowers()
