import os
import youtube_dl
from bs4 import BeautifulSoup
import requests
#subclasses
#1. txt file of names
#2. single name
#3. single link
#4. playlist link
#5. txt file of links

def get_links(names):
    lst = []
    for name in names:
        source = requests.get('https://www.youtube.com/results?search_query=' + name).text
        soup = BeautifulSoup(source, 'lxml')
        link = soup.findAll('a', attrs={'class':'yt-uix-tile-link'})
        lst.append('https://www.youtube.com' + link[0].get('href'))
    return lst

def extract_txt(txt):
    with open(txt, 'r') as f:
        lst = f.read().split('\n')
    return lst


def downloader(link_lst, loc='', ext='mp3'):
    if ext == 'mp4':
        ydl_opts = {'outtmpl': loc + '/%(title)s-%(id)s.%(ext)s'}
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': loc + '/%(title)s-%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    for link in link_lst:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

def main():
    if __name__ == '__main__':
        while True:
            option1 = int(input('\nWhat do you have:\n1.Link\n2.Text\n3.Name\n'))
            option2 = int(input('\nWhat do you want\n1.mp3\n2.mp4\n'))
            if option1 not in range(1, 4) or option2 not in range(1, 3):
                print('\nSelect from available options\n')
                continue
            if option2 == 1:
                ext = 'mp3'
            else:
                ext = 'mp4'
            loc = input('\nEnter location to dowmload:\n')
            if option1 == 1:
                link = input('\nEnter Link\n')
                downloader(link_lst=[link], loc=loc, ext=ext)
            elif option1 == 2:
                option3 = int(input('\nWhat is in the text:\n1.Links\n2.Names'))
                txt = input('\nEnter the location of text file')
                if option3 == 1:
                    link_lst = extract_txt(txt)
                    downloader(link_lst=link_lst, loc=loc, ext=ext)
                else:
                    name_lst = get_links(txt)
                    link_lst = extract_txt(name_lst)
                    downloader(link_lst=link_lst, loc=loc, ext=ext)
            elif option1 == 3:
                name = input('\nEnter name of video:\n')
                link_lst = get_links([name])
                downloader(link_lst=link_lst, loc=loc, ext=ext)
            option4 = int(input('\nDo you want to continue:\n1.Yes\n2.No\n'))
            if option4 == 1:
                continue
            else:
                break


main()