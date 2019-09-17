import requests
from bs4 import BeautifulSoup as bs


date1 = input('Give the date you want homework in this format: Month A-Day Date/B-Day Date \n')
date2 = date1.split(' ')[0] + ' ' + date1.split('/')[-1]
date3 = date1.split(' ')[0] + ' ' + date1.split('/')[0].split(' ')[-1]

password = input('Enter your password')

login = {
    'username': 'Aditya.Pawar',
    'password': password,
    'anchor': '',
    'logintoken': ''
}


b = False


"""Make a session to login and get info"""
with requests.Session() as s:
    url = 'https://learn.vcs.net/login/index.php'
    res = s.get(url)
    soup = bs(res.content, 'html.parser')
    login['logintoken'] = soup.find('input', attrs={'name': 'logintoken'})['value']
    """Save the login token and sign in"""
    # print(login['logintoken'])

    """Get the website data"""
    res = s.post(url, data=login)
    soup = bs(res.content, 'html.parser')
    # print(type(soup))
    #print(soup.find('div', attrs={'class': 'menus'}))
    classes = soup.find('div', attrs={'class': 'menus'})
    # .find('a', attrs={'title': 'Bible 8 - Mr. Delke - 2018-19'}
    # print(classes.find_all('a')[::-1][3:12])
    """Find the names of the classes(reverse array([::-1]) then take the 3 - 12 value in the array([3:12]))"""
    for tag in classes.find_all('a')[::-1][3:12]:
        """Print the names of the classes"""
        #print(tag['title'])
        title = tag['title']
        page = s.get(tag['href'] + '&section=2')
        soup = bs(page.content, 'html.parser')
        """Go to the pages and get data"""
        # lessonplans = soup.find('a', attrs={'title': 'Lesson Plans and Homework'})
        # print(soup.find('a', attrs={'title': 'Lesson Plans and Homework'}))
        #try:
        if True:
            #Quarter 4 (2018-19)
            #print(soup.find_all('a'))
            """Loop through anchor tags"""
            for c, a in enumerate(soup.find_all('a', attrs={'class': ''})[::-1]):
                # print(len(a.find_all('span')))
                #print(c)
                """Check if tag has a 'data-action' attribute and ignore if it does"""
                try:
                    temp = a['data-action']
                except:
                    """Get tag with Homework page link"""
                    if len(a.find_all('span')) == 2:

                        """Check if it the date we want"""
                        if len(a['href'].split('/')) > 2 and not a['href'].split('/')[-2] == 'forum':
                            r = s.get(a['href'])
                            soup = bs(r.content, 'html.parser')

                            if soup.find('a', string=date1) != None:
                                b = True
                                #print(soup.find('a', string='April 26'))
                                link = soup.find('a', string=date1)


                            elif soup.find('a', string=date2) != None:
                                b = True
                                #print(soup.find('a', string='April 25/26'))
                                link = soup.find('a', string=date2)


                            elif soup.find('a', string=date3) != None:
                                b = True
                                #print(soup.find('a', string='April 25'))
                                link = soup.find('a', string=date3)


                            #else:
                            #   print(a)
                            #   print('?')
                        if b:
                            #print(link['href'])
                            r = s.get(link['href'])
                            soup = bs(r.content, 'html.parser')

                            """Find Homework"""
                            if soup.find('b', string='Homework') != None:
                                find = 'b'
                            elif soup.find('h3', string='Homework') != None:
                                find = 'h3'
                            elif soup.find('h4', string='Homework') != None:
                                find = 'h4'
                            else:
                                find = None

                            #print(str(soup.find(find, string='Homework')))
                            """Get Homework"""
                            if find != None:
                                i = str(r.content).find(str(soup.find(find, string='Homework'))) + len(str(soup.find(find, string='Homework')))
                                #print("Homework? : {}".format(str(r.content)[i : i + 300]))
                                homework = bs(str(r.content)[i:i+500], 'html.parser')
                                print('Homework for {} is: \n'.format(title))
                                [print(tag.text.replace('\\', '')) for tag in homework.find_all('li')]
                                #print("Tag : {}".format(find))
                            else:
                                print("No Homework for {}".format(title))

                            #print(a)
                            b = False
                            print()
                            break
