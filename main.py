import base64
import os
from multiprocessing import Process, current_process
import multiprocessing
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
    common_packets_amount = len(packets) // threads

    for _ in range(threads):
        delegated_packets.append([])

    for i in range(threads):
        delegated_packets[i] = packets[i*common_packets_amount:i*common_packets_amount+common_packets_amount]

    packets = packets[common_packets_amount*threads:]

    for i in range(len(packets)):
        delegated_packets[i] += [packets[0]]
        packets.pop(0)  # delete what was taken

    first_packets = 1
    for i in range(len(delegated_packets) - 1):
        if len(delegated_packets[i]) == len(delegated_packets[i + 1]):
            first_packets += 1
        else:
            break
    if first_packets == len(delegated_packets):
        print(f'Будет {threads} потоков. По {len(delegated_packets[0])} пакетов для каждого потока')
    else:
        print(f'Будет {threads} потоков. По {len(delegated_packets[0])} пакетов для первых {first_packets} потоков и '
              f'по {len(delegated_packets[first_packets])} пакетов для последних '
              f'{len(delegated_packets) - first_packets} потоков')

    print('</DELEGATOR>')
    return {'threads': threads, 'packets': delegated_packets}


def find_answer(all_packets, key=None):
    if not key:
        try:
            file = open('success.txt', 'r')
            line = file.readline()
            key = int(line.split()[0])
        except:
            return False

    packs = all_packets
    mac_server = ''

    for packet in packs:
        data = decode_text(packs[packet]['Data'], key)
        if data is not None and phrase in data:
            mac_server = packs[packet]['Destination MAC Address']
            mac_client = packs[packet]['Source MAC Address']
            break

    data = []
    decr_data = []
    for packet in packs:
        dec = decode_text(packs[packet]['Data'], key)
        if dec is not None:
            if packs[packet]["Source MAC Address"] == mac_server and packs[packet]['Destination MAC Address'] == mac_client:
                data.append(dec)
                decr_data.append(packs[packet])

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
        result += str(hex((int(message[i:i + 8], 16) - int(hex(secret_key), 16)) % int(hex(m), 16)))[2:]

    # print('Decoding steps:')
    if len(result) % 8 and add_symbols:
        result += '0' * (8 - len(result) % 8)
    # print('0)', message)
    try:
        # print('1)', end=' ')
        # for i in range(0, len(result), 8):
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
    while not answer_exist():
        pass
    return


def answer_exist():
    folder = os.listdir()
    if 'success.txt' in folder:
        return True
    else:
        return False


def define_key(packets, phrase, reverse=False, check_answer_=False):
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

    possible_keys = list(range((2 ** 32 - 2 ** 22), 2 ** 32 + 1))

    if reverse:
        possible_keys.reverse()
        key_progress.reverse()

    def write_key(key, packet, result):
        with open('success.txt', 'w') as file:
            file.write(f'{key} {packet} {result}')

    for key in possible_keys:
        if check_answer_:
            if answer_exist():
                 return

        if key in key_progress:
            key_progress_index = key_progress.index(key)
            print(current_process().name,
                  f'перебрал {key_progress_index * 41943} ключей ({key_progress_index} %). Текущий: {key}')

        for i, packet in enumerate(packets):
            res = decode_text(packet, key)
            if res and phrase in res:
                print('\nNice!!!!\n')
                write_key(key, packet, res)
                return


def start_multiprocessing(function, deligator_data: dict, phrase, extra_function_args=(), extra_info='', checker_in_separate_thread=True, reverse_brute_force=False):
    if extra_info:
        print(f'\n<MULTIPROCESSING> ({extra_info})')
    else:
        print('\n<MULTIPROCESSING>')

    threads = deligator_data['threads']
    packets = deligator_data['packets']

    print('Запускаю потоки...')
    processes = []
    for i in range(threads):
        process = Process(target=function, args=(packets[i], phrase) + extra_function_args,
                          name=f'Поток {i}', kwargs={'reverse': reverse_brute_force, 'check_answer_': not checker_in_separate_thread})
        processes.append(process)
        process.start()
        print(process.name, 'запущен!')

    if checker_in_separate_thread:
        checker = Process(target=check_answer, name='Checker')
        checker.start()
        print('Детектор ответа запущен в отдельном потоке!')

        checker.join()
        print(checker.name, 'завершен')
        for proc in processes:
            proc.terminate()
    else:
        print('Проверка ответа будет осуществляться потоками')

    for i, proc in enumerate(processes):
        proc.join()
        print(proc.name, 'завершен')

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

    if 'script' in config and config['script'] == 'main':
        reverse_brute_force = False
    else:
        reverse_brute_force = True
    print('Реверс:', reverse_brute_force)

    if 'checker_in_separate_thread' in config and config['checker_in_separate_thread']:
        checker_in_separate_thread = True
    elif 'checker_in_separate_thread' in config:
        checker_in_separate_thread = False
    else:
        checker_in_separate_thread = True
    print('Детектор в отдельном потоке:', checker_in_separate_thread)

    packets, all_packets, phrase = load_data()
    thread_delegator_data = thread_delegator(packets)

    start_time = datetime.now()
    start_multiprocessing(define_key, thread_delegator_data, phrase, extra_info=f'Начало в {datetime.now()}', reverse_brute_force=reverse_brute_force, checker_in_separate_thread=checker_in_separate_thread)
    print('Поиск занял:', datetime.now() - start_time)

    answer = find_answer(all_packets)
    if answer:
        print(answer)
    else:
        print('Ответ не был найден')

    #winsound.MessageBeep()
    #os.system('pause')
