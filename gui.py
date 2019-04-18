import PySimpleGUI as sg
import aspen_web as aspen
import pickle
import os
import sys


def enter_password(incorrect=False):
    layout = [
        [sg.Text('Enter Login', font=('Arial', 25))],
        [sg.Text('Enter Username: ', size=(15, 1)), sg.InputText(key="username")],
        [sg.Text('Enter Password: ', size=(15, 1)), sg.InputText(key="password", password_char='*')],
        [sg.Checkbox('Remember Login?', default=True, key='remember')],
        [sg.Save()]
    ]

    if incorrect:
        layout.insert(1, [sg.Text('Incorrect Password', text_color='red')])

    window = sg.Window('Aspen - Grade Viewer').Layout(layout)

    event, values = window.Read()

    if event is None or event == 'Quit':
        sys.exit()

    if values['remember']:
        pickle.dump(values, open('stored_user_data', 'wb'))

    window.Close()

    return values

def display_grades(classes, grades, user_data):
    class_layout = [

    ]
    grade_layout = [

    ]
    cell_size = len(max(classes, key=len))
    for c, g in zip(classes, grades):
        class_layout.append([sg.Text(c)])
        class_layout.append([sg.Text('_' * cell_size)])
        grade_layout.append([sg.Text(g)])
        grade_layout.append([sg.Text('_' * cell_size)])

    menu_def = [
        ['Options', ['Sign Out']]
    ]

    main_layout = [
        [sg.Menu(menu_def)],
        [sg.Text('Grades for ' + user_data['username'], font=('Arial, 25'))],
        [sg.Column(class_layout), sg.VerticalSeparator(), sg.Column(grade_layout)]
    ]



    window = sg.Window('Grades for ' + user_data['username']).Layout(main_layout )

    while True:
        event, values = window.Read()
        if event is None or event == 'Quit':
            sys.exit()
        if event == 'Sign Out':
            window.Close()
            os.remove('stored_user_data')
            user_data = enter_password()
            classes, grades = aspen.get_grades(user_data)
            display_grades(classes, grades, user_data)

# ------------MAIN------------
if os.path.isfile('stored_user_data'):
    user_data = pickle.load(open('stored_user_data', 'rb'))
else:
    user_data = enter_password()



classes, grades = aspen.get_grades(user_data)

if classes == None:
    user_data = enter_password(True)
else:
    display_grades(classes, grades, user_data)