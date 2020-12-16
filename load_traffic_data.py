import json, os


def organize_traffic_data(traffic: str, global_header_length=24, packet_header_length=16, packet_headers=None, use_cache=True, write_cache=True):
    print('\n<DATA ORGANIZING>')
    if use_cache:
        print('Checking if there is cached data...')
        traffic_dict = load_from_file()
        if traffic_dict and traffic_dict['traffic data'] == traffic:
            print('Cache was found! So cache will be used')
            print('</DATA ORGANIZING>\n')
            return traffic_dict
        else:
            print('There is no cache data.')

    if packet_headers is None:
        packet_headers = default_packets_header

    traffic_dict = {'traffic data': traffic, 'global header': traffic[global_header_length * 2:], 'packets': {}}

    # delete global header
    data = traffic[global_header_length * 2:]
    print('Organizing traffic data...')
    while data:
        packet = {}
        # Getting main headers
        main_header = data[:packet_header_length * 2]
        data = data[packet_header_length * 2:]
        packet['Main Header'] = main_header

        packet_length = int(main_header[-8:].rstrip('0'), 16) * 2
        packet['Packet Length'] = packet_length

        # Getting all headers length
        headers_length = 0
        for header in packet_headers:
            headers_length += header[1] * 2
        # Getting all headers
        for header in packet_headers:
            current_header_name = header[0]
            current_header_length = header[1] * 2
            packet[current_header_name] = data[:current_header_length]
            data = data[current_header_length:]

        # Getting packet data
        packet_data = data[:packet_length - headers_length]
        data = data[packet_length - headers_length:]
        packet['Data'] = packet_data

        traffic_dict['packets'][len(traffic_dict['packets'])] = packet

    print('Organizing finished!')
    if write_cache:
        print('Saving traffic data...')
        safe_to_file(traffic_dict)
        print('Traffic data was saved!')
    print('</DATA ORGANIZING>\n')
    return traffic_dict


def safe_to_file(organized_traffic):
    with open('traffic.json', 'w') as file:
        json.dump(organized_traffic, file)


def load_from_file():
    try:
        with open('traffic.json', 'r') as file:
            organized_traffic = json.load(file)
        return organized_traffic
    except IOError:
        return False


def load_config_file():
    try:
        file = open('config.json', 'r')
        config = json.load(file)
    except:
        config = {}

    return config


def get_packets_from_traffic_data(traffic_data):
    if isinstance(traffic_data, str):
        traffic_data = organize_traffic_data(traffic_data)

    clean_packets = []
    packets = traffic_data['packets']
    for packet in packets:
        clean_packets += [packets[packet]['Data']]

    return clean_packets, traffic_data


def clean_workspace():
    delete = input('Очистить старые результаты, если такие есть (по умолчанию - да) [y/n]:').strip()
    if delete not in ('No', 'n', 'N', '0') or delete in ('y', 'Y', 'Yes', ''):
        to_delete = ['answer.txt', 'success.txt'] + [f'packets{i}.json' for i in range(10)]
        for file in to_delete:
            try:
                os.remove(file)
                print(file, 'был удален.')
            except:
                pass
    print()


def device_delegator(packets, organized_traffic, default_device_amount=2):
    if 'devices' in config and config['devices']:
        devices = config['devices']
    else:
        devices = input('Введи кол-во устройств, между которыми будут распределены вычисленя: ')
    try:
        devices = int(devices)
    except:
        devices = default_device_amount

    print('\n<DEVICE DELEGATOR>')
    delegated_packets = []
    if len(packets) % devices == 0:
        print(f'Будет {devices} устройства. По {len(packets)//devices} пакетов для каждого устройства.')
        for i in range(0, len(packets), len(packets)//devices):
            delegated_packets += [packets[i:i+len(packets)//devices]]
    else:
        print(f'Будет {devices} устройства. По {len(packets)//devices} пакетов для первых {devices - 1} устройств и '
               f'{len(packets) - (len(packets)//devices)*devices} для последнего устройства')
        for i in range(0, (len(packets)//devices)*devices, len(packets)//devices):
            delegated_packets += [packets[i:i+len(packets)//devices]]
        delegated_packets += [packets[-(len(packets) - (len(packets)//devices)*devices):]]

    for device_index in range(devices):
        with open(f'packets{device_index}.json', 'w') as file:
            json.dump({'all packets': organized_traffic['packets'], 'packets': delegated_packets[device_index], 'phrase': phrase}, file)
            print(f'packets{device_index}.json был успешно создан')

    print('</DEVICE DELEGATOR>\n')


if __name__ == '__main__':
    default_packets_header = [['Ethernet Header', 14], ['IPv4 Header', 20], ['UDP Header', 8]]

    config = load_config_file()
    # clean_workspace()

    if 'phrase' in config and config['phrase']:
        phrase = config['phrase']
    else:
        phrase = input('Введи фразу: ').strip()
    if 'traffic' in config and config['traffic']:
        traffic = config['traffic']
    else:
        traffic = input('Введи трафик: ')

    packets, organized_traffic = get_packets_from_traffic_data(traffic)
    device_delegator(packets, organized_traffic)

    print('Необходимо теперь запустить main.py!')
