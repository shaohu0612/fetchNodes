import os
import base64
import concurrent.futures


def process_line(config, protocol_data, protocols):
    """
    处理每一行配置，分类到对应的协议。
    """
    protocol_found = None
    for protocol in protocols.keys():
        if config.startswith(protocol):
            protocol_found = protocol
            break

    if protocol_found:
        protocol_data[protocol_found].append(config)


def write_protocol_data(protocol_data, protocols, splitted_path):
    """
    将每个协议的数据编码并写入文件。
    """
    for protocol, data in protocol_data.items():
        file_path = os.path.join(splitted_path, protocols[protocol])
        encoded_data = base64.b64encode('\n'.join(data).encode("utf-8")).decode("utf-8")
        encoded_data = ('\n'.join(data).encode("utf-8")).decode("utf-8")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(encoded_data)


def sort_nodes():
    protocols = {
        'vmess': 'vmess.txt',
        'vless': 'vless.txt',
        'trojan': 'trojan.txt',
        'ss': 'ss.txt',
        'ssr': 'ssr.txt',
        'tuic': 'tuic.txt',
        'hy2': 'hysteria2.txt'
    }

    ptt = os.path.abspath(os.path.join(os.getcwd()))
    splitted_path = os.path.join(ptt, 'Splitted-By-Protocol')

    # Ensure the directory exists
    os.makedirs(splitted_path, exist_ok=True)

    protocol_data = {protocol: [] for protocol in protocols}

    # Fetching the configuration data
    with open("All_Subs.txt", "r", encoding="utf-8") as file:
        total_lines = sum(1 for _ in file)
        print(f'总共{total_lines}行')

    with open("All_Subs.txt", "r", encoding="utf-8") as file:
        content = file.readlines()

    # 使用线程池并行处理每一行
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i, config in enumerate(content):
            if not config.strip():  # 跳过空行
                continue
            futures.append(executor.submit(process_line, config, protocol_data, protocols))

        # 等待所有任务完成
        concurrent.futures.wait(futures)

    # 将分类后的数据写入文件
    write_protocol_data(protocol_data, protocols, splitted_path)
    print("所有配置已处理并写入文件。")


# if __name__ == '__main__':
#     sort_nodes()

