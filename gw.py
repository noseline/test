# virtual_lora_gw.py
import threading
import json
import time
import socket


def checksum(packet):
    sum = -1
    for i in range(len(packet)):
        sum += (packet[i])
    t = sum & 0xFE
    return t.to_bytes(1, 'big')


class VirtualLoRa:
    def __init__(self):
        self.lora_gw_ready = False
        self.lora_gw = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.lora_gw.bind(("0.0.0.0", 63501))

    def generate_res_msg(self):
        msg_head = bytearray(
            [0x41, 0x54, 0x2A, 0x54, 0x58, 0x5F, 0x52, 0x45, 0x51, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        msg_cont = bytearray([0x01, 0x00, 0x01])
        msg_tail = b'\x0D\x0A'
        c = msg_head + msg_cont
        t = bytes(c)
        cs = checksum(t)
        return t + cs + msg_tail

    def lora_gw_tx_task(self):
        while True:
            time.sleep(5)
            msg = self.generate_res_msg()
            print(msg)
            self.lora_gw.sendto(msg, ("100.100.100.2", 63500))

    def lora_gw_rx_task(self):
        while True:
            time.sleep(0.1)
            msg = self.lora_gw.recv(1024)
            if msg:
                print(msg)

    def loop(self):
        lora_gw_tx_thread = threading.Thread(target=self.lora_gw_tx_task)
        lora_gw_tx_thread.start()
        lora_gw_rx_thread = threading.Thread(target=self.lora_gw_rx_task)
        lora_gw_rx_thread.start()
        threading.Thread(target=self.key_task).start


if __name__ == "__main__":
    v = VirtualLoRa()
    v.loop()

