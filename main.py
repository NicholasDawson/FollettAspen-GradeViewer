import requests
from bs4 import BeautifulSoup

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0}'
}

login_data = {
'org.apache.struts.taglib.html.TOKEN': 'c299670f8d1550e46601001f79361fb5',
'userEvent': '930',
'deploymentId':	'ct-portland',
'formFocusField': 'username',
'mobile': 'false',
'username':	'INPUT_USERNAME',
'password': 'INPUT_PASSWORD'
}

with requests.Session() as s:
    url = 'https://ct-portland.myfollett.com/aspen/logon.do'
    academics = 'https://ct-portland.myfollett.com/aspen/portalClassList.do?navkey=academics.classes.list'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    login_data['org.apache.struts.taglib.html.TOKEN'] = soup.find('input', attrs={'name': 'org.apache.struts.taglib.html.TOKEN'})['value']

    r = s.post(url, data=login_data, headers=headers) # LOGIN
    r = s.get(academics, headers=headers) # GO TO ACADEMICS

    soup = BeautifulSoup(r.content, 'html5lib')
    soup = soup.find('div', attrs={'id': 'dataGrid', 'class': 'listGrid'})
    soup = soup.find_all('tr', attrs={"class": "listCell"})

    classes = []
    for school_class in soup:
        classes.append(school_class.find_all('td', attrs={"nowrap": ""})[2].string.lstrip().rstrip())

    grades = []
    for school_grade in soup:
        grades.append(school_grade.find_all('td', attrs={"nowrap": ""})[8].string.lstrip().rstrip())

    for x in range(len(classes)):
        if grades[x] == '':
            print(classes[x], "->", "NO GRADE")
        else:
            print(classes[x], "->", grades[x])




