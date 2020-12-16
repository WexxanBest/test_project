import json, os


def read_from_dataset_file():
    folder = os.listdir()
    dataset_filename = ''
    for file in folder:
        if file.startswith('dataset'):
            dataset_filename = file
            print(dataset_filename, 'был октрыт!')
            break

    if dataset_filename:
        with open(dataset_filename, 'r') as file:
            phrase = file.readline().strip()
            traffic = file.readline().strip()
        return (phrase, traffic)
    else:
        return False


def load_config_file():
    try:
        file = open('config.json', 'r')
        config = json.load(file)
        file.close()
    except:
        config = {}

    return config


def save_config_file(config_data):
    with open('config.json', 'w') as file:
        json.dump(config_data, file)


if __name__ == '__main__':
    result = read_from_dataset_file()
    if result:
        phrase, traffic = result
    else:
        print('Датасет не был найден!')
        quit()

    print('Фраза:', phrase)
    print('Трафик:', traffic)

    config = load_config_file()
    if not config:
        os.system('python create_config_file.py')

    config['phrase'] = phrase
    config['traffic'] = traffic
    save_config_file(config)

    os.system('python load_traffic_data.py')

    if 'script' in config and config['script']:
        if config['script'] == 'main':
            os.system('python main.py')
        else:
            os.system('python main_reverse.py')
    else:
        script = input('Какой скрипт запускать? (Напиши цифру):\n[0] main.py\n[1] main_reverse.py\nВвод: ')
        if script != '1':
            os.system('python main.py')
        else:
            os.system('python main_reverse.py')
