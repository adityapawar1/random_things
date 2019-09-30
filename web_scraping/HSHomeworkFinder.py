import requests
from bs4 import BeautifulSoup as bs
import re

"""
date1 = input('Give the date you want homework in this format: Month A-Day Date/B-Day Date \n')
date2 = date1.split(' ')[0] + ' ' + date1.split('/')[-1]
date3 = date1.split(' ')[0] + ' ' + date1.split('/')[0].split(' ')[-1]
"""
try:
    num_of_courses = input('How many courses are you taking?')
    if (len(num_of_courses) == 0):
        num_of_courses = 7
except:
    print("Enter a number")
    
password = input('Enter your password')
if (len(password) == 0):
    password = 'SaltArmyWith37'
    
login = {
    'username': 'Aditya.Pawar',
    'password': password,
    'anchor': '',
    'logintoken': ''
}

homework_data = {}

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
    if len(soup.find_all('div', attrs={'class':'loginerrors'})) != 0:
        print('Invalid Login')
    else:
        print('Logged in')
    
    classes = soup.find_all('div', attrs={'class': 'column c1'})
#[print("{} \n".format(c)) for c in classes[3:num_of_courses + 3]]

class_names = []

classes = classes[3:num_of_courses + 3]
for class_ in classes:
    href = class_.find('a')
    link = href['href']
    
    class_name = href['title']
    class_names.append(class_name)
    print(class_name)
    
    r = s.get(link)
    soup = bs(r.content, 'html.parser')
    lesson_plans_page = soup.find('a', attrs={'title': 'Lesson Plans and Homework'})
    plans = lesson_plans_page['href']
    try:
        r = s.get(plans)
        soup = bs(r.content, 'html.parser')
        lesson_plans = soup.find('div', attrs={'class': 'activityinstance'})
        lessons = lesson_plans.find('a')
        lessons_link = lessons['href']
        #print(lessons_link)
    except:
        print('Error')
        continue
    
    r = s.get(lessons_link)
    soup = bs(r.content, 'html.parser')
    possible_lessons = soup.find_all('li', attrs={'class':'notselected'})
    lesson = soup.find('li', attrs={'class':'selected'})
    possible_lessons.append(lesson)
    homework_dict_temp = {}
    
    #print(possible_lessons)
    
    for lesson in possible_lessons:
        #print(lesson)
        try:
            lesson_link = lesson.find('a')['href']
            date = lesson.find('a').text
            print(date)
            print(lesson_link)
            print('\n')
        except:
            print('Error on lesson links')
            
   
            
        r = s.get(lesson_link)
        t = r.content.decode("utf-8")
        soup = bs(t, 'html.parser')
        
        
        
        main = soup.find('div', attrs={'role':'main'})
        contents = main.find('div', attrs={'class':'box contents'})
        
        if 'Homework' in str(contents):
#             print(True)
            hw = contents.find('h3', text=re.compile('Homework'))
            hw_contents = bs(str(contents).split(str(hw))[-1], 'html.parser')
            
            homework = hw_contents.find('ul')
            try:
#                 print(homework.text)
                str(homework.text)
                homework_dict_temp.__setitem__(date, homework.text)
            except:
                print('No Homwork found on {}\n'.format(lesson_link))
        else:
            print('No Homwork found on {}\n'.format(lesson_link))
        
    
    print('\n\n')
    homework_data.__setitem__(class_name, homework_dict_temp)
        
print(homework_data)
