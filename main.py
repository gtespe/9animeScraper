#!/usr/bin/python
from bs4 import BeautifulSoup
#import jwplatform
#import json
from selenium import webdriver
import time
#import shutil
#import urllib

def main():

    # Set up the webdriver with extensiosn
    # options = webdriver.ChromeOptions() 
    # options.add_extension("./optional-chromedriver-plugins/ublockorigin.crx")
    # options.add_extension("./optional-chromedriver-plugins/blockimages.crx")
    # options.add_extension("./optional-chromedriver-plugins/disableautoplay.crx")
    # driver = webdriver.Chrome(chrome_options=options)
    # driver.get("https://www.kissanime.to/Login")

    #ffprofile = webdriver.FirefoxProfile("./366j48ag.selenium")
    #driver= webdriver.Firefox(firefox_profile=ffprofile)

    #driver.get("https://www.kissanime.ru/Login")

    #time.sleep(5)

    # Get inputs for login + serach -- OUTDATED
    # username = input("Username: ")
#    user_elem = driver.find_element_by_id("username")
#    user_elem.send_keys('pybot')

#    pass_elem = driver.find_element_by_id("password")
#    pass_elem.send_keys('thisisabotthing')

#    driver.find_element_by_id("btnSubmit").click()

    # get keywords to search
    keyword = input("Enter Search Terms: ")
    searchurl = "http://9anime.to/search?keyword=" + keyword
    print("Loading...")

    import requests
    search_request = requests.get(searchurl)
    search_html = search_request.text

    #print(search_html)

    # Send data
#    search_elem = driver.find_element_by_id("keyword")
   # search_elem.send_keys(keyword)
   

  #  driver.find_element_by_id("imgSearch").click()
    # check if you typed exact anime (kiss will forward to episodes page)

    # parse links
    links = []
    soup = BeautifulSoup(search_html, "html.parser")

    for a in soup.find_all('a', href=True):
        if "/watch/" in a['href']:
            if(a['href'] not in links):
                links.append(a['href'])

    # Get Input
    print("Enter which ones to download:")

    for i in range(0, len(links)):
        print("  " + str(i+1) + "  " + links[i][7:])
    print("--------------------------------------------------")

    num_string = input(">> ")

    # Map input to a list of ints
    nums = map(int, num_string.split(' '))

    #setup driver
    #ffprofile = webdriver.FirefoxProfile("./366j48ag.selenium")
    driver= webdriver.Firefox()#firefox_profile=ffprofile)

    # Cycle through the list of ints (Shows)
    for which in nums:
        theName = links[which-1][23:]

        #driver.get("9anime.to" + links[which-1])
        print(links[which-1])
        nexturl = requests.get(links[which-1])

        #find all the episodes
        #soup = BeautifulSoup(driver.page_source, "html.parser")
        soup = BeautifulSoup(nexturl.text, "html.parser")

        episode_links = []

        #parse episode links from html, get this first LEN links
        #  where LEN is the number of episodes in the series
        biggest_ep = -1
        for a in soup.find_all('a', href=True):
            if "/watch/" in a['href'] and "http://" not in a['href']:
                if(int(a['data-base']) > biggest_ep):
                    biggest_ep = int(a['data-base'])
                    episode_links.append(a['href'])
        
        #episode_links.sort()
        print("Enter which ones to download (Press ENTER for all):")

        for i in range(0, len(episode_links)):
            print("  " + str(i+1) + "  " + episode_links[i])
        print("--------------------------------------------------")

        episodes_in = input(">> ") 
        if(episodes_in == ""):
            which_episodes = list(range(1, 1+len(episode_links)))
        else:
            if '-' in episodes_in:
                episode_range = list(map(int, episodes_in.split('-')))
                which_episodes = list(range(episode_range[0], episode_range[1]+1))
            else:
                which_episodes = list(map(int, episodes_in.split(' ')))

        print("Downloading episodes ",  which_episodes)

        # Cycle through the episodes and download one at a time
        for n in which_episodes:
            #driver.get("https://kissanime.ru"+ episode_links[n-1])
            #soup = BeautifulSoup(driver.page_source, "html.parser")

            #episode_req = requests.get("https://9anime.to" + episode_links[n-1], stream=True)

            #get the episode key
        #    splits = episode_links[n-1].split('/')
        #    key = splits[len(splits)-1]

#            print(key)

#            jwclient = jwplatform.Client()
#            epreq = jwclient.videos.show(video_key=key)
            #print(epreq)

            time.sleep(0.1)

            #get the page in driver
            driver.get("http://9anime.to" + episode_links[n-1])
            soup = BeautifulSoup(driver.page_source, "html.parser")

            #return to blank to prevent page load
            driver.get("about:home")

            #thelink = 0
            thelink = soup.find("video").get("src")

            print(thelink)

            #for video in soup.find('div'):
            #    if "redirector.googlevideo.com" in video['src']:
            #        thelink = video['src']
            #        break

            # replace the 'redirector' with a wierd string
            #https://r16---sn-bvvbax-hn26.googlevideo.com/
            #newlink = 'https://r2---sn-bvvbax-hn26' + thelink[18:]

            filename = theName.split(".")[0] + "_" + str(n) + ".mp4"

            print("Downloading " + filename + "...")


            #urllib.request.urlcleanup()
            #req = urllib.request.Request(thelink, headers={'User-Agent': 'Mozilla/4.0'})
            #response = urllib.request.urlopen(req)


            #f = open(filename, "wb")
            
            #google made things difficult :\
            #r = requests.get(thelink, allow_redirects=True, 
            #testfile = urllib.URLopener()
            #testfile.retrieve(thelink, filename)

            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

            with open(filename, 'wb') as handle:
                response = requests.get(thelink, allow_redirects=True, stream=True, headers={'user-agent': user_agent})

                if not response.ok:
                    print('something wrong')
                # Something went wrong

                for block in response.iter_content(1024):
                    handle.write(block)

            #f.write(r.content)


    print("Done!")

#end main


if __name__ == "__main__":
    main()

