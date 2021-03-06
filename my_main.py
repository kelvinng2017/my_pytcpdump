import socket
import codecs
import struct
print("hello")
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
handshake = 0
while True:
    packet, _ = s.recvfrom(65565)
    # print(packet)
    # print(type(packet))  # hi
    # packet_decode = packet.decode('ascii')
    packet_decode = codecs.encode(packet, 'hex')
    # print(packet_decode)
    # print(type(packet_decode))  # hi
    Eth_header = packet[:14]
    Eth_header_decode = codecs.encode(Eth_header, 'hex')
    # print(type(Eth_header_decode))
    # print(len(Eth_header_decode))
    Eth_header_decode_string = Eth_header_decode.decode("utf-8")
    # print(Eth_header_decode)
    Ip_header = packet[14:34]
    Ip_header_decode = codecs.encode(Ip_header, 'hex')
    iph = struct.unpack('!BBHHHBBH4s4s', Ip_header)
    IHL_VERSION, TYPE_OF_SERVICE, total_len, pktID, FRAGMENT_STATUS, TIME_TO_LIVE, PROTOCOL, check_sum_of_hdr, src_IP, dest_IP = iph
    icmp_header = packet[34:42]
    icmp_type, code, checksum, packetid, seq = struct.unpack(
        'BbHHh', icmp_header)

    HTYPE, PTYPE, HLEN, PLEN, Operation, SHA, SPA, THA, TPA = struct.unpack(
        '2s2s1s1s2s6s4s6s4s', packet[14:14+28])
    HTYPE_dec = int((codecs.encode(HTYPE, 'hex')).decode("utf-8"), 16)
    PTYPE_dec = int((codecs.encode(PTYPE, 'hex')).decode("utf-8"), 16)
    HLEN_dec = int((codecs.encode(HLEN, 'hex')).decode("utf-8"), 16)
    PLEN_dec = int((codecs.encode(PLEN, 'hex')).decode("utf-8"), 16)
    Operation_dec = int((codecs.encode(Operation, 'hex')).decode("utf-8"), 16)
    SHA_dec = (codecs.encode(SHA, 'hex')).decode("utf-8")
    THA_dec = (codecs.encode(THA, 'hex')).decode("utf-8")

    """
    src_port, dest_port, seq, ack_num, offset, flags, window, checksum, urgent_ptr = struct.unpack(
        '!HHLLBBHHH', packet[34:54])
    """
    tcp_packet = packet[34:54]
    tcp_packet_len = len(tcp_packet)

    # HTYPE_hex_decode_string = HTYPE_dec.decode("utf-8")

    print(
        f"Eth_header_from:{Eth_header_decode_string[0:2]}:{Eth_header_decode_string[2:4]}:{Eth_header_decode_string[4:6]}:{Eth_header_decode_string[6:8]}:{Eth_header_decode_string[8:10]}:{Eth_header_decode_string[10:12]}")
    print(
        f"Eth_header_to:{Eth_header_decode_string[12:14]}:{Eth_header_decode_string[14:16]}:{Eth_header_decode_string[16:18]}:{Eth_header_decode_string[18:20]}:{Eth_header_decode_string[20:22]}:{Eth_header_decode_string[22:24]}")
    print(f"EtherType:{Eth_header_decode_string[24:28]}")
    print(f"IHL_VERSION:{IHL_VERSION}")
    print(f"TYPE_OF_SERVICE:{TYPE_OF_SERVICE}")
    print(f"total_len:{total_len}")
    print(f"pktID:{pktID}")
    print(f"FRAGMENT_STATUS:{FRAGMENT_STATUS}")
    print(f"TIME_TO_LIVE:{TIME_TO_LIVE}")
    print(f"PROTOCOL:{PROTOCOL}")
    print(f"check_sum_of_hdr:{check_sum_of_hdr}")
    print(f"src_IP:{socket.inet_ntoa(src_IP)}")
    print(f"dest_IP:{socket.inet_ntoa(dest_IP)}")
    print(f"icmp_type:{icmp_type}")
    print(f"code:{code}")
    print(f"checksum:{checksum}")
    print(f"packetid:{packetid}")
    print(f"seq:{seq}")
    print(f"HTYPE:{HTYPE_dec}")
    print(f"PTYPE:{PTYPE_dec}")
    print(f"HLEN:{HLEN_dec}")
    print(f"PLEN:{PLEN_dec}")
    print(f"Operation:{Operation_dec}")
    print(f"SHA:{SHA_dec}")
    print(f"SPA:{socket.inet_ntoa(SPA)}")
    print(f"THA:{THA_dec}")
    print(f"TPA:{socket.inet_ntoa(TPA)}")
    print(f"tcp packet len:{len(tcp_packet)}")
    if len(tcp_packet) == 20:
        print("==============tcp_header===================")
        src_port, dest_port, seq, ack_num, offset, flags, window, checksum, urgent_ptr = struct.unpack(
            '!HHLLBBHHH', packet[34:54])

        tcp_data = packet[54:]

        reserved = offset & 0xF
        tcpip_length = offset >> 4
        packet = {}
        packet['SRC_PORT'] = src_port
        packet['DEST_PORT'] = dest_port
        packet['SEQ'] = seq
        packet['ACK_NUM'] = ack_num
        flags_arr = []
        flags_arr.append('CWR') if (flags >> 7) & 1 else flags_arr.append('_')
        flags_arr.append('ECE') if (flags >> 6) & 1 else flags_arr.append('_')
        flags_arr.append('URG') if (flags >> 5) & 1 else flags_arr.append('_')
        flags_arr.append('ACK') if (flags >> 4) & 1 else flags_arr.append('_')
        flags_arr.append('PSH') if (flags >> 3) & 1 else flags_arr.append('_')
        flags_arr.append('RST') if (flags >> 2) & 1 else flags_arr.append('_')
        flags_arr.append('SYN') if (flags >> 1) & 1 else flags_arr.append('_')
        flags_arr.append('FIN') if (flags >> 0) & 1 else flags_arr.append('_')
        packet['Flags'] = ','.join(flags_arr)
        packet['RESERVE'] = reserved
        packet['TCP_LENGTH'] = tcpip_length
        packet['WINDOW'] = window
        packet['CHECKSUM'] = checksum
        packet['PTR'] = urgent_ptr
        packet['DATAlen'] = len(tcp_data)
        packet['DATA'] = tcp_data
        print(f"packet:{packet}")

    """
    print(f"src_port:{src_port}")
    print(f"dest_port:{dest_port}")
    print(f"seq:{seq}")
    print(f"ack_num:{ack_num}")
    print(f"offset:{offset}")
    print(f"flags:{flags}")
    print(f"window:{window}")
    print(f"checksum:{checksum}")
    print(f"urgent_ptr:{urgent_ptr}")
    """
    print("===========================================")
