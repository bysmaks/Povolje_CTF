import requests
import base64
from tqdm import tqdm
import time

API_URL = input("API URL: ")

def is_padding_ok(data):
	encoded_ciphertext = base64.b64encode(data).decode('utf-8')
	start = time.time()
	response = requests.post(API_URL, json={"ciphertext": encoded_ciphertext})
	return response.json()['status'] == "data wasn't send"

BLOCK_SIZE=16
def attack(ciphertext):
	guessed_clear = b''

	split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]
	blocks = split_string(ciphertext, BLOCK_SIZE)
	
	for block_n in range(1, len(blocks))[::-1]:
		spliced_ciphertext = blocks[block_n - 1] + blocks[block_n]

		decoded_bytes = b'?' * BLOCK_SIZE

		for byte in range(BLOCK_SIZE)[::-1]:
			new_pad_len = BLOCK_SIZE - byte

			hacked_ciphertext_tail = b''
			for padder_index in range(1, new_pad_len):
				hacked_ciphertext_tail += bytearray.fromhex('{:02x}'.format(new_pad_len ^ decoded_bytes[byte + padder_index]))
			
			for i in tqdm(range( 0, 256 )):
				attack_str = bytearray.fromhex('{:02x}'.format((i ^ spliced_ciphertext[byte])))
				hacked_ciphertext = spliced_ciphertext[:byte] + attack_str + hacked_ciphertext_tail + spliced_ciphertext[byte + 1 + new_pad_len - 1:]

				if (is_padding_ok(hacked_ciphertext)):

					test_correctness = hacked_ciphertext[:byte - 1] + bytearray.fromhex('{:02x}'.format( ( 1 ^  hacked_ciphertext[byte])))  + hacked_ciphertext[byte:]
					if (not is_padding_ok(test_correctness)):
						continue
					
					decoded_bytes = decoded_bytes[:byte] + bytearray.fromhex('{:02x}'.format( hacked_ciphertext[byte] ^ new_pad_len)) + decoded_bytes[byte + 1:]
					guessed_clear = bytearray.fromhex('{:02x}'.format(i ^ new_pad_len)) + guessed_clear
					break
	
	return guessed_clear[:-guessed_clear[-1]]

ciphertext_b64 = input("enc data: ")
data = base64.b64decode(ciphertext_b64)
print(attack(data))
