import os

os.system('pip install PySimpleGUI')

import PySimpleGUI as sg


layout = [
    [sg.Text('Как дела, Танюха?')],
    [sg.Button('Норм'), sg.Button('Чотко')]
]


window = sg.Window('Fuck', layout)
while True:
    event, values = window.read()

    if event in (None, sg.WINDOW_CLOSED):
        break

    elif event == 'Норм':
        sg.popup('У тебя дела норм, у меня тоже')

    elif event == 'Чотко':
        sg.popup(
            'У тебя дела чотко, крч не придумал, что ещё можно сделать',
            'Но можно сделать абсолютно всё'.upper())

window.close()
