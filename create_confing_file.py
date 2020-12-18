import json


if __name__ == '__main__':
    config = {}

    try:
        config['devices'] = int(input('Введи кол-во устройств, которые будут участвовать в вычеслениях: '))
    except:
        config['devices'] = None

    try:
        config['threads'] = int(input('Введи кол-во потокок: '))
    except:
        config['threads'] = None

    try:
        script = input('Какой скрипт запускать? (Напиши цифру):\n[0] main (по умолчанию)\n[1] reverse\nВвод: ')
        if script != '1':
            config['script'] = 'main'
        else:
            config['script'] = 'reverse'
    except:
        config['script'] = 'main'

    try:
        script = input('Как запускать детектор ошибок? (Напиши цифру):\n[0] В отдельном потоке '
                       '(по умолчанию)\n[1] В каждом потоке\nВвод: ')
        if script != '1':
            config['checker_in_separate_thread'] = True
        else:
            config['checker_in_separate_thread'] = False
    except:
        config['script'] = True

    with open('config.json', 'w') as file:
        json.dump(config, file)

    print()
    for option in config:
        print(f'{option}: {config[option]}')

    print()
    print('config.json успешно создан!')
