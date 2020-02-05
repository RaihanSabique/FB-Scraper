import traceback
import getpass
from pprint import pprint
import pandas as pd
import glob

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import argparse
import csv
import calendar
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description='Non API public FB miner')

parser.add_argument('-p', '--pages', nargs='+',
                    dest="pages",
                    help="List the pages you want to scrape for recent posts")

parser.add_argument("-g", '--groups', nargs='+',
                    dest="groups",
                    help="List the groups you want to scrape for recent posts")

parser.add_argument("-d", "--depth", action="store",
                    dest="depth", default=5, type=int,
                    help="How many recent posts you want to gather -- in multiples of (roughly) 8.")

args = parser.parse_args()

BROWSER_EXE = '/usr/bin/firefox'
GECKODRIVER = dir_path +'/geckodriver'

FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

#  Code to disable notifications pop up of Chrome Browser

PROFILE = webdriver.FirefoxProfile()
# PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()


total_scrolls = 2500
current_scrolls = 0
scroll_time = 8
facebook_https_prefix = "https://"

class CollectPosts(object):
    """Collector of recent FaceBook posts.
           Note: We bypass the FaceBook-Graph-API by using a
           selenium FireFox instance!
           This is against the FB guide lines and thus not allowed.
           USE THIS FOR EDUCATIONAL PURPOSES ONLY. DO NOT ACTAULLY RUN IT.
    """

    def __init__(self, ids=["oxfess"], corpus_file=["oxfess"], depth=5, delay=2):
        self.ids = ids
        self.dump = corpus_file
        self.depth = depth + 1
        self.delay = delay
        # browser instance
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER,
                                         firefox_binary=FIREFOX_BINARY,
                                         firefox_profile=PROFILE,)

        # creating CSV header
        with open(self.dump, "w", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            writer.writerow(["Author", "uTime", "Text", "profileLink"])

    def strip(self, string):
        """Helping function to remove all non alphanumeric characters"""
        words = string.split()
        words = [word for word in words if "#" not in word]
        string = " ".join(words)
        clean = ""
        for c in string:
            if str.isalnum(c) or (c in [" ", ".", ","]):
                clean += c
        return clean

    def collect_page(self, page):
        # navigate to page
        self.browser.get(
            'https://www.facebook.com/' + page + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        with open(self.dump, "a+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            links = self.browser.find_elements_by_link_text("See More")
            for link in links:
                try:
                    link.click()
                except:
                    pass
            links_addition = self.browser.find_elements_by_link_text("Continue Reading")
            for link in links_addition:
                try:
                    link.click()
                except:
                    pass
            posts = self.browser.find_elements_by_class_name(
                "userContentWrapper")
            poster_names = self.browser.find_elements_by_xpath(
                "//a[@data-hovercard-referer]")

            for count, post in enumerate(posts):
                # Creating first CSV row entry with the poster name (eg. "Donald Trump")
                analysis = [poster_names[count].text]
                analysis.append(poster_names[count].get_attribute('href'))

                # Creating a time entry.
                time_element = post.find_element_by_css_selector("abbr")
                utime = time_element.get_attribute("data-utime")
                analysis.append(utime)

                # Creating post text entry
                text = post.find_element_by_class_name("userContent").text
                # status = self.strip(text)
                analysis.append(text)

                # Write row to csv
                writer.writerow(analysis)

    def collect_groups(self, group):
        # navigate to page
        self.browser.get(
            'https://www.facebook.com/groups/' + group + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        with open(self.dump, "a+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
# <<<<<<< HEAD
#             links = self.browser.find_elements_by_link_text("See More")
#             for link in links:
#                 try:
#                     link.click()
#                 except:
#                     pass
#             links_addition = self.browser.find_elements_by_link_text("Continue Reading")
#             for link in links_addition:
#                 try:
#                     link.click()
#                 except:
#                     pass
#             posts = self.browser.find_elements_by_class_name(
#                 "userContentWrapper")
#             poster_names = self.browser.find_elements_by_xpath(
#                 "//a[@data-hovercard-referer]")
#
#             for count, post in enumerate(posts):
#                 try:
#                     # Creating first CSV row entry with the poster name (eg. "Donald Trump")
#                     analysis = [poster_names[count].text]
#                     url=poster_names[count].get_attribute('href')
#                     print(url)
#                     user_id=self.create_original_link(url)
#                     # gender=self.scrape_genger(user_id)
#                     # print("Gender=====>",gender)
#                     # analysis.append(poster_names[count].get_attribute('href'))
#                     # analysis.append(self.scrape_genger(url))
#                     # Creating a time entry.
#                     time_element = post.find_element_by_css_selector("abbr")
#                     utime = time_element.get_attribute("data-utime")
#                     analysis.append(utime)
#                     pprint(post)
#                     # Creating post text entry
#                     text = post.find_element_by_class_name("userContent").text
#                     pprint(text)
#                     # text2=post.find_element_by_class_name('text_exposed_show').text
#                     # print(text2)
#                     # status = self.strip(text)
#                     analysis.append(text)
#                     print(user_id)
#                     analysis.append(user_id)
#                     # gender=self.scrape_genger(user_id)
#                     # print("Gender=====>",gender)
#
#                     # Write row to csv
#                     writer.writerow(analysis)
#                 except Exception as e:
#                     print("type error: " + str(e))
#                     print(traceback.format_exc())
# =======
            posts = self.browser.find_elements_by_class_name("userContentWrapper")
            # links = self.browser.find_elements_by_link_text("See More")
            # for link in links:
            #     try:
            #         link.click()
            #     except:
            #         pass
            poster_names = self.browser.find_elements_by_xpath("//a[@data-hovercard-referer]")

            for count, post in enumerate(posts):
                # Creating first CSV row entry with the poster name (eg. "Donald Trump")
                # analysis = [poster_names[count].text]
                flag = False
                data = ""
                continue_reading_author = ""
                continue_reading_post = ""
                try:
                    link = post.find_element_by_xpath(".//span[@class='text_exposed_link']//a")
                    link.click()
                    if (len(self.browser.window_handles) == 2):
                        self.browser.switch_to.window(window_name=self.browser.window_handles[-1])
                        flag = True
                except Exception as e: 
                    pass
                if flag:
                    element = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "userContentWrapper")))
                    post = self.browser.find_element_by_class_name("userContentWrapper")
                analysis = [post.find_element_by_xpath(".//a[@data-hovercard-referer]").text]
                print(analysis)

                # Creating a time entry.
                time_element = post.find_element_by_css_selector("abbr")
                utime = time_element.get_attribute("data-utime")
                analysis.append(utime)
                pprint(post)
                # Creating post text entry
                text = post.find_element_by_class_name("userContent").text
                pprint(text)
                # text2=post.find_element_by_class_name('text_exposed_show').text
                # print(text2)
                # status = self.strip(text)
                analysis.append(text)
                if flag:
                    self.browser.close()
                    self.browser.switch_to.window(window_name=self.browser.window_handles[0])

                # Write row to csv
                writer.writerow(analysis)
# >>>>>>> a12e07c417089cbf819629ac9e33a140799b0ebc

    def get_data_and_close_last_tab(self):
        if (len(self.driver.window_handles) == 2):
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(window_name=self.driver.window_handles[0])

    def collect(self, typ):
        if typ == "groups":
            print(self.ids)
            self.collect_groups(self.ids)
            # for iden in self.ids:
            #     self.collect_groups(iden)
        elif typ == "pages":
            self.collect_page(self.ids)
            # for iden in self.ids:
            #     self.collect_page(iden)
        # self.browser.close()

    def safe_find_element_by_id(self, elem_id):
        try:
            return self.browser.find_element_by_id(elem_id)
        except NoSuchElementException:
            return None

    def login(self, email, password):
        try:

            self.browser.get("https://www.facebook.com")
            self.browser.maximize_window()

            # filling the form
            self.browser.find_element_by_name('email').send_keys(email)
            self.browser.find_element_by_name('pass').send_keys(password)

            # clicking on login button
            self.browser.find_element_by_id('loginbutton').click()
            # if your account uses multi factor authentication
            mfa_code_input = self.safe_find_element_by_id('approvals_code')

            if mfa_code_input is None:
                return

            mfa_code_input.send_keys(input("Enter MFA code: "))
            self.browser.find_element_by_id('checkpointSubmitButton').click()

            # there are so many screens asking you to verify things. Just skip them all
            while self.safe_find_element_by_id('checkpointSubmitButton') is not None:
                dont_save_browser_radio = self.safe_find_element_by_id('u_0_3')
                if dont_save_browser_radio is not None:
                    dont_save_browser_radio.click()

                self.browser.find_element_by_id(
                    'checkpointSubmitButton').click()

        except Exception as e:
            print("There's some error in log in.")
            print(sys.exc_info()[0])
            exit()

##### Scrape Gender##########
class CollectGender:
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER,
                                         firefox_binary=FIREFOX_BINARY,
                                         firefox_profile=PROFILE, )

    def safe_find_element_by_id(self, elem_id):
        try:
            return self.browser.find_element_by_id(elem_id)
        except NoSuchElementException:
            return None
    def login(self):
        try:

            self.browser.get("https://www.facebook.com")
            self.browser.maximize_window()

            # filling the form
            self.browser.find_element_by_name('email').send_keys(self.email)
            self.browser.find_element_by_name('pass').send_keys(self.password)

            # clicking on login button
            self.browser.find_element_by_id('loginbutton').click()
            # if your account uses multi factor authentication
            mfa_code_input = self.safe_find_element_by_id('approvals_code')

            if mfa_code_input is None:
                return

            mfa_code_input.send_keys(input("Enter MFA code: "))
            self.browser.find_element_by_id('checkpointSubmitButton').click()

            # there are so many screens asking you to verify things. Just skip them all
            while self.safe_find_element_by_id('checkpointSubmitButton') is not None:
                dont_save_browser_radio = self.safe_find_element_by_id('u_0_3')
                if dont_save_browser_radio is not None:
                    dont_save_browser_radio.click()

                self.browser.find_element_by_id(
                    'checkpointSubmitButton').click()

        except Exception as e:
            print("There's some error in log in.")
            print(sys.exc_info()[0])
            exit()

    def check_height(self):
        new_height = self.browser.execute_script("return document.body.scrollHeight")
        return new_height != old_height

    def scroll(self):
        global old_height
        current_scrolls = 0

        while (True):
            try:
                if current_scrolls == total_scrolls:
                    return

                old_height = self.browser.execute_script("return document.body.scrollHeight")
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(self.browser, scroll_time, 0.05).until(lambda driver: self.check_height())
                current_scrolls += 1
            except TimeoutException:
                break

        return

    def scrape_data(self,user_id, scan_list, section, elements_path, save_status, file_names):
        """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
        about_information=[]
        page = []

        if save_status == 4:
            page.append(user_id)

        page += [user_id + s for s in section]

        for i, _ in enumerate(scan_list):
            try:
                self.browser.get(page[i])

                if (save_status == 0) or (save_status == 1) or (
                        save_status == 2):  # Only run this for friends, photos and videos

                    # the bar which contains all the sections
                    sections_bar = self.browser.find_element_by_xpath("//*[@class='_3cz'][1]/div[2]/div[1]")

                    if sections_bar.text.find(scan_list[i]) == -1:
                        continue

                if save_status != 3:
                    self.scroll()

                data = self.browser.find_elements_by_xpath(elements_path[i])

                about_information.append(data[0].text.split("\n"))


                # save_to_file(file_names[i], data, save_status, i)
            except Exception:
                print("Exception (scrape_data)", str(i), "Status =", str(save_status), sys.exc_info()[0])
        return about_information

    def scrape_genger(self,user_id):
        try:
            scan_list = [None] * 7
            section = ["/about?section=overview", "/about?section=education", "/about?section=living",
                       "/about?section=contact-info", "/about?section=relationship", "/about?section=bio",
                       "/about?section=year-overviews"]
            elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 7
            file_names = ["Overview.txt", "Work and Education.txt", "Places Lived.txt", "Contact and Basic Info.txt",
                          "Family and Relationships.txt", "Details About.txt", "Life Events.txt"]
            save_status = 3

            results=self.scrape_data(user_id, scan_list, section, elements_path, save_status, file_names)
            print(results)
            gender=None
            for i in range(len(results)):
                for j in range(len(results[i])):
                    if(results[i][j]=="Gender"):
                        gender=results[i][j+1]
                        break
            print("About Section Done!")
            return gender
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())
            return  None

    def clean_link(self,url):
        if('profile.php?' in url):
            indx1=url.find("id=")
            indx2=url.find('&fref')
            id=url[indx1+len('id='):indx2]
            u="https://www.facebook.com/"+id
            return u
        idx=url.find('?')
        u=url[:idx]
        return u

    def create_original_link(self,url):
        url=self.clean_link(url)
        if url.find(".php") != -1:
            original_link = facebook_https_prefix + ".facebook.com/" + ((url.split("="))[1])

            if original_link.find("&") != -1:
                original_link = original_link.split("&")[0]

        elif url.find("fnr_t") != -1:
            original_link = facebook_https_prefix + ".facebook.com/" + ((url.split("/"))[-1].split("?")[0])
        elif url.find("_tab") != -1:
            original_link = facebook_https_prefix + ".facebook.com/" + (url.split("?")[0]).split("/")[-1]
        else:
            original_link = url

        return original_link

    def retrive_gender(self,df):
        for link in df['profileLink']:
            print(link)
            g=self.scrape_genger(self.create_original_link(link))
            print(g)

if __name__ == "__main__":

    # with open('credentials.txt') as f:
    #     email = f.readline().split('"')[1]
    #     password = f.readline().split('"')[1]
    #
    #     if email == "" or password == "":
    #         print(
    #             "Your email or password is missing. Kindly write them in credentials.txt")
    #         exit()
    f = open("input.txt", "r")

    file_dir=dir_path+"/Data/"
    email=input("Enter your email/username : ")
    password=getpass.getpass(prompt='Enter Password:')
    url='https://www.facebook.com/MobassharRahman'
    scraper=CollectGender(email,password)
    scraper.login()
    files=glob.glob(file_dir+"/*.csv")
    for file in files:
        df = pd.read_csv(file)
        print(file)
        scraper.retrive_gender(df)
        # print(df['profileLink'])

    # C.login(email, password)
    # C.retrive_gender(df)
    # C.browser.quit()
    # object=[]
    # for x in f:
    #     try:
    #         x=x.split()
    #         print(x)
    #         type=int(x[0])
    #         group_name=x[1]
    #         depth=100
    #         file_name=file_dir+group_name + ".csv"
    #         print(type,group_name,depth)
    #         C = CollectPosts(ids=group_name, corpus_file=file_name, depth=depth)
    #         C.login(email, password)
    #         # user_id = C.create_original_link(url)
    #         # g=C.scrape_genger(user_id)
    #         # print("grnder:::",g)
    #         C.collect("groups")
    #         print("collection done from ", group_name)
    #         object.append(C)
    #         C.browser.close()
    #         del C
    #         # del C
    #     except Exception as e:
    #         print("type error: " + str(e))
    #         print(traceback.format_exc())
    #
    # while True:
    #     try:
    #         type = input("Enter 1 for scraping from Group or Enter 2 for scraping from Page: ")
    #         if(type=="1"):
    #             group_name=input("Enter Group Name:")
    #             print("Depth:")
    #             depth=int(input())
    #             file_name=input("Enter the filename you want to save:")
    #             file_name=file_dir+file_name + ".csv"
    #             C = CollectPosts(ids=group_name,corpus_file=file_name ,depth=depth)
    #             C.login(email, password)
    #             # user_id = C.create_original_link(url)
    #             # g=C.scrape_genger(user_id)
    #             # print("grnder:::",g)
    #             C.collect("groups")
    #             df=pd.read_csv(file_name)
    #             print(df.head())
    #             print(df['profileLink'])
    #             C.login(email, password)
    #             C.retrive_gender(df)
    #             C.browser.quit()
    #             # for link in df['profileLink']:
    #             #     user_id = C.create_original_link(str(link))
    #             #     g=C.scrape_genger(user_id)
    #             #     print("grnder:::",g)
    #         if (type == "2"):
    #             page_name = input("Enter Page Name:")
    #             print("Depth:")
    #             depth = int(input())
    #             file_name = input("Enter the filename you want to save:")
    #             file_name = file_dir+file_name + ".csv"
    #             C = CollectPosts(ids=page_name,corpus_file=file_name ,depth=depth)
    #             C.login(email, password)
    #             C.collect("pages")
    #     except Exception as e:
    #         print("type error: " + str(e))
    #         print(traceback.format_exc())