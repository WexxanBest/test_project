import base64
import os
from multiprocessing import Process, current_process
import hashlib
from datetime import datetime
#import winsound
import json


def thread_delegator(packets: list, default_threads=6):
    if 'threads' in config and config['threads']:
        threads = config['threads']
    else:
        try:
            threads = int(input('Введи кол-во потоков (по умолчанию 6): '))
        except:
            threads = default_threads

    print('\n<DELEGATOR>')
    delegated_packets = []
    if len(packets) % threads == 0:
        print(f'Будет {threads} потоков. {len(packets)//threads} пакетов для каждого потока.')
        for i in range(0, len(packets), len(packets)//threads):
            delegated_packets += [packets[i:i+len(packets)//threads]]
    else:
        print(f'Будет {threads} потоков. {len(packets)//threads} пакетов для первых {threads - 1} потоков и '
               f'{len(packets) - (len(packets)//threads)*threads} для последнего потока')
        for i in range(0, (len(packets)//threads)*threads, len(packets)//threads):
            delegated_packets += [packets[i:i+len(packets)//threads]]
        delegated_packets += [packets[-(len(packets) - (len(packets)//threads)*threads):]]
    print('</DELEGATOR>')
    return {'threads': threads, 'packets': delegated_packets}


def find_answer(all_packets):
    try:
        file = open('success.txt', 'r')
        line = file.readline()
        key = int(line.split()[0])
    except:
        return False

    data = []
    decr_data = []
    packs = all_packets
    mac_server = ''
    for packet in packs:
        dec = decode_text(packs[packet]['Data'], key)
        if dec != None:
            if dec.isdigit():
                mac_server = packs[packet]["Ethernet Header"][0:12]
                #print(mac_server)
            if packs[packet]["Ethernet Header"][12:24] == mac_server:
                data.append(dec)
                decr_data.append(packs[packet])
    #print(data)
    answer = hashlib.sha256("\n".join(data).encode()).hexdigest()
    with open('answer.txt', 'w') as file:
        file.write(str(answer))

    return answer


def decode_text(message: str, secret_key, add_symbols=False, m=2038074743):
    # print = DebugPrint(debugging).debug_print
    # print('\n<Decoding>')
    result = ''
    for i in range(0, len(message), 8):
        # print(message[i:i+8])
        # print(str(hex((int(message[i:i+8], 16) - int(hex(secret_key), 16)) % int(hex(m), 16))))
        result += str(hex((int(message[i:i+8], 16) - int(hex(secret_key), 16)) % int(hex(m), 16)))[2:]

    # print('Decoding steps:')
    if len(result) % 8 and add_symbols:
        result += '0' * (8 - len(result) % 8)
    # print('0)', message)
    try:
        # print('1)', end=' ')
        #for i in range(0, len(result), 8):
            # print(result[i:i + 8], end=' ')
        # print('')

        result = bytes.fromhex(result)
        # print('2)', result)

        result = base64.b64decode(result)
        result = result.decode()

        # print('3)', result)

    except UnicodeDecodeError as er:
        # print('<!> UnicodeDecodeError occurred! <!>', er)
        result = None
    except Exception as ex:
        # print('<!> Error occurred!', ex)
        result = None
    # print('-'*20)
    # print('Key:', secret_key)
    # print(f'Original message: {"0x" + message} (len: {len(message)})\nDecoded message: {result}')
    # if result:
    #     # print('</Decoding> (SUCCESS)\n')
    # else:
    #     # print('</Decoding> (FAIL)\n')
    return result


def check_answer():
    try:
        file = open('success.txt', 'r')
        file.close()
        return True
    except IOError:
        return False


def define_key(packets, phrase):
    key_progress = [4290772992, 4290814935, 4290856878, 4290898821, 4290940764, 4290982707, 4291024650, 4291066593,
                    4291108536, 4291150479, 4291192422, 4291234365, 4291276308, 4291318251, 4291360194, 4291402137,
                    4291444080, 4291486023, 4291527966, 4291569909, 4291611852, 4291653795, 4291695738, 4291737681,
                    4291779624, 4291821567, 4291863510, 4291905453, 4291947396, 4291989339, 4292031282, 4292073225,
                    4292115168, 4292157111, 4292199054, 4292240997, 4292282940, 4292324883, 4292366826, 4292408769,
                    4292450712, 4292492655, 4292534598, 4292576541, 4292618484, 4292660427, 4292702370, 4292744313,
                    4292786256, 4292828199, 4292870142, 4292912085, 4292954028, 4292995971, 4293037914, 4293079857,
                    4293121800, 4293163743, 4293205686, 4293247629, 4293289572, 4293331515, 4293373458, 4293415401,
                    4293457344, 4293499287, 4293541230, 4293583173, 4293625116, 4293667059, 4293709002, 4293750945,
                    4293792888, 4293834831, 4293876774, 4293918717, 4293960660, 4294002603, 4294044546, 4294086489,
                    4294128432, 4294170375, 4294212318, 4294254261, 4294296204, 4294338147, 4294380090, 4294422033,
                    4294463976, 4294505919, 4294547862, 4294589805, 4294631748, 4294673691, 4294715634, 4294757577,
                    4294799520, 4294841463, 4294883406, 4294925349, 4294967296]

    key_progress.reverse()

    possible_keys = list(range((2 ** 32 - 2 ** 22), 2 ** 32 + 1))
    possible_keys.reverse()

    def write_key(key, packet, result):
        with open('success.txt', 'w') as file:
            file.write(f'{key} {packet} {result}')

    for key in possible_keys:
        if key in key_progress:
            key_progress_index = key_progress.index(key)
            print(current_process().name, f'перебрал {key_progress_index * 41943} ключей ({key_progress_index} %). Текущий: {key}')
        if check_answer():
            return
        for i, packet in enumerate(packets):
            res = decode_text(packet, key)
            if res and phrase in res:
                print('\nNice!!!!\n')
                write_key(key, packet, res)
                return


def start_multiprocessing(function, deligator_data: dict, phrase, extra_function_args=(), extra_info=''):
    if extra_info:
        print(f'\n<MULTIPROCESSING> ({extra_info})')
    else:
        print('\n<MULTIPROCESSING>')

    threads = deligator_data['threads']
    packets = deligator_data['packets']

    print('Запускаю потоки...')
    processes = []
    for i in range(threads):
        process = Process(target=function, args=(packets[i], phrase) + extra_function_args, name=f'Поток {i}')
        processes.append(process)
        process.start()
        print(f'Поток {i} запущен.')

   # print(processes)

    for i, proc in enumerate(processes):
        proc.join()
        print(f'Поток {i} завершен')

    print('</MULTIPROCESSING>')


def load_config_file():
    try:
        file = open('config.json', 'r')
        config = json.load(file)
    except:
        config = {}

    return config


def load_data():
    for i in range(10):
        try:
            file = open(f'packets{i}.json', 'r')
            print(f'packets{i}.json был открыт!')
            break
        except:
            pass
    data, all_packets, packets, phrase = {}, {}, {}, ''
    try:
        data = json.load(file)
        all_packets = data['all packets']
        packets = data['packets']
        phrase = data['phrase']
    except:
        print('Данных нет! Сначала загрузи данные в load_traffic_data.py')
        quit()
    return packets, all_packets, phrase


if __name__ == '__main__':
    config = load_config_file()

    packets, all_packets, phrase = load_data()
    thread_delegator_data = thread_delegator(packets)

    start_time = datetime.now()
    start_multiprocessing(define_key, thread_delegator_data, phrase, extra_info=f'Начало в {datetime.now()}')
    print('Поиск занял:', datetime.now() - start_time)

    answer = find_answer(all_packets)
    if answer:
        print(answer)
    else:
        print('Ответ не был найден')

    #winsound.MessageBeep()
    #os.system('pause')
