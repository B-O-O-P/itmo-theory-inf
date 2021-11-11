from sys import argv, exit
import numpy as np
import pathlib
from tqdm import tqdm
import warnings
warnings.simplefilter('ignore')

from c_types import char, size_t, uint8_t

from bwt import bwt, inverse_bwt
from mtf import mtf_encode, mtf_decode
from monotone import monotone_encode, monotone_decode
from metrics import count_hx, count_hxx, count_hxxx


def count_metrics(x, res):
    Z = size_t(len(res) + np.dtype(size_t).itemsize)

    # print(f"{round(count_hx(x), 3)} & {round(count_hxx(x), 3)} & {round(count_hxxx(x), 3)} & {round(8 * Z / len(x), 3)} & {Z}")
    print(f"H(X): {count_hx(x)}")
    print(f"H(X|X): {count_hxx(x)}")
    print(f"H(X|XX): {count_hxxx(x)}")
    print(f"Average byte per symbol: {8 * Z / len(x)}")
    print(f"Size of file in bytes: {Z}")


def encode(s, progress_bar=None, status=None):
    if progress_bar is not None:
        progress_bar.set_description(desc='Starting BWT...', refresh=True)

    s_, start = bwt(s, progress_bar=progress_bar, whole_status=(40 - status))

    if progress_bar is not None:
        progress_bar.set_description(desc='Starting MTF...', refresh=True)

    mtf_encoded = mtf_encode(s_, progress_bar=progress_bar, whole_status=30)

    if progress_bar is not None:
        progress_bar.set_description(desc='Starting monotone encoding...', refresh=True)

    monotone_encoded = monotone_encode(mtf_encoded, progress_bar=progress_bar, whole_status=20)

    return monotone_encoded, start


def decode(s, start, progress_bar=None, status=None):
    if progress_bar is not None:
        progress_bar.set_description(desc='Starting monotone decoding...', refresh=True)

    monotone_decoded = monotone_decode(s, progress_bar=progress_bar, whole_status=(20 - status))

    if progress_bar is not None:
        progress_bar.set_description(desc='Starting MTF...', refresh=True)

    mtf_decoded = mtf_decode(monotone_decoded, progress_bar=progress_bar, whole_status=30)

    if progress_bar is not None:
        progress_bar.set_description(desc='Starting Inverse BWT...', refresh=True)

    decoded = inverse_bwt(mtf_decoded, start, progress_bar=progress_bar, whole_status=40)

    return decoded


def main():
    arguments = argv

    if len(arguments) < 4:
        print('Wrong arguments: {encode, decode} input_file output_file')
        exit(1)

    current_working_dir = pathlib.Path().absolute()

    if arguments[1] == 'encode':
        with tqdm(total=100) as progress_bar:
            progress_bar.set_description(desc='Opening file...', refresh=True)
            code_file = arguments[2]
            with open(f'{current_working_dir}/{code_file}', 'rb') as file:
                progress_bar.update(2)
                progress_bar.set_description(desc='Reading bytes...', refresh=True)

                bytes = np.fromfile(file, dtype=char)

                progress_bar.update(2)

                result, start = encode(np.array(bytes, dtype=uint8_t), progress_bar=progress_bar, status=4)

                progress_bar.set_description(desc='Saving file...', refresh=True)

                if len(arguments) > 4 and arguments[4] == '--metrics':
                    count_metrics(bytes, result)

                coded_file = arguments[3]
                with open(f'{current_working_dir}/{coded_file}', 'wb') as write_file:
                    start_data = np.ndarray.tobytes(np.array([start], dtype=size_t))
                    result_data = np.ndarray.tobytes(result)
                    data = np.array(start_data + result_data)
                    data.tofile(write_file)
                    progress_bar.update(10)

                    write_file.close()
                progress_bar.set_description(desc='Completed', refresh=True)
                progress_bar.close()
                file.close()
    elif arguments[1] == 'decode':
        with tqdm(total=100) as progress_bar:
            progress_bar.set_description(desc='Opening file...', refresh=True)

            coded_file = arguments[2]
            with open(f'{current_working_dir}/{coded_file}', 'rb') as file:
                progress_bar.update(2)
                progress_bar.set_description(desc='Reading bytes...', refresh=True)


                bytes = np.fromfile(file, dtype=char)

                type_size = np.dtype(np.uintp).itemsize
                start_bytes = bytes[0:type_size]
                buffer = np.frombuffer(bytes[type_size:], dtype=uint8_t)
                start_borrow = np.frombuffer(start_bytes, dtype=size_t)

                progress_bar.update(2)

                result = decode(buffer, start_borrow[0], progress_bar=progress_bar, status=4)

                progress_bar.set_description(desc='Saving file...', refresh=True)

                code_file = arguments[3]
                with open(f'{current_working_dir}/{code_file}', 'wb') as write_file:
                    result_data = np.ndarray.tobytes(result)
                    data = np.array(result_data)
                    data.tofile(write_file)

                    write_file.close()
                    progress_bar.update(10)

                progress_bar.set_description(desc='Completed', refresh=True)
                progress_bar.close()
                file.close()
    else:
        print('Wrong arguments: first arguments should be in {encode, decode}')
        exit(1)


if __name__ == "__main__":
    main()
