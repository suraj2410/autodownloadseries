#!/usr/bin/env python3

"""
Maintainer : Suraj Nair
Created : 5th May, 2017
Version: 1.0
"""

from selenium import webdriver
import subprocess
#from selenium.webdriver.common.keys import Keys
#import selenium.webdriver.support.expected_conditions as EC
#from selenium.webdriver.firefox.options import Options
import time

# Function to print the number of episodes found for a particular search


def printer():

    if len(results) == 0:
        print("No results found.. Try again with a different search string..\n")
        driver.quit()
        exit()
    elif len(results) == 1:
        print("I've found a total of {} results for {} as seen below: \n".format(len(results),
                                                                               season_to_find + "" + episode_to_find))
    else:
        print("I've found a total of {} results for {} as seen below: \n".format(len(results),
                                                                               season_to_find + "" + episode_to_find))
    total_results = len(results)
    index = 1
    print("Index \t" + "Description\t")
    print("=" * 60)
    while index <= total_results:
        if len(results) == 1:
            print(str(index) + "\t" + results[0][0] + "\n")
            break
        else:
            print(str(index) + "\t" + results[index - 1][0] + "\n")
        index += 1

# Function to ask inputs from the user and take necessary download actions


def asker():
    input_index = input("Select the index number from above options which you want to download or 'q' to quit or 'm' to go back to menu again: ").upper()
    if input_index == "":
        asker()
    elif input_index == 'Q':
        driver.quit()
        exit()
    elif input_index == 'M':
        printer()
        asker()
    else:
        try:
            link_to_download = results[int(input_index) - 1][1]
        except IndexError:
            print("You gave a bad index which is not in the above list.. Try again \n")
            printer()
            asker()
        # driver.get(results[int(input_index)-1][1])
        """
        The following commented sub-process actually works for windows in that it opens the downloading part in a totally
        new detached CMD and allows us to add multiple downloads
        But couldn't find a similar one for linux shells and could only make the downloads to be detached in to the backend without
        any progress bar options for us to view.
        """
        # CREATE_NO_WINDOW = 0x08000000
        #DETACHED_PROCESS = 0x00000010
        # subprocess.Popen(['wget', '-P', '/home/suraj/Downloads/', link_to_download], creationflags=DETACHED_PROCESS)
        subprocess.Popen(['wget', '-P', '/home/suraj/Downloads/', link_to_download], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Download has been started in a the background \n")
        # driver.manage().timeouts().implicitlyWait(300, TimeUnit.SECONDS);
        printer()
        asker()

if __name__ == "__main__":

    season_to_find = input("Enter the name of the season to search for: ")
    episode_to_find = input("Enter the Season and episode number to search for in the format SxxExx: ").upper()
    search_string = "index of " + season_to_find + " " + episode_to_find

    """  Web driver Firefox profile which is not mandatory here as we are not using firefox for downloads
         This is because the program waits for the download to complete if done via Firefox before handling over the charge back to
         the terminal for future interactions 
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 0)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", "/home/suraj/Download")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.implicitly_wait(30)
    driver.maximize_window()
    try:
        driver.get("https://www.google.com")
    except:
        print("Internet not available")
        driver.quit()

    search_field = driver.find_element_by_id("lst-ib")
    search_field.clear()
    search_field.send_keys(search_string)
    time.sleep(3)
    search_field.submit()
    # Getting the first href path link assuming the result would be there
    link = driver.find_element_by_xpath("//h3[@class='r']/a[@href]")
    titlegoogle = link.text.encode('utf8')
    urlgoogle = link.get_attribute('href')

    try:
        time.sleep(5)
        driver.get(urlgoogle)
    except:
        print("Internet not available")
        driver.quit()
    # Finding those href links that have the partial text for the episode to find in them and adding them to a list
    elements = driver.find_elements_by_partial_link_text(episode_to_find)
    results = []

    for element in elements:
        new_title = element.text
        new_url = element.get_attribute('href')
        title_url = (new_title, new_url)
        results.append(title_url)
        # driver.get(new_url)
    printer()
    asker()
    driver.quit()
