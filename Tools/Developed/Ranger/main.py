import argparse
import ipaddress
import requests
import json
import os

out_path = "./"
out_format = "json"


# Function for creating directories for the output
def directory_check(output):
    if os.path.exists(output):
        if os.path.exists(f"{output}/shodan-results"):
            print("[+] Directories exist")
            return
        else:
            os.mkdir(f"{output}/shodan-results/")
            print(f"[*] Created directory {output}/shodan-results/")
    else:
        print("[!] Directory does not exist, creating...")
        os.mkdir(f"{output}")
        os.mkdir(f"{output}/shodan-results/")
        print(f"[*] Creted directory {output}")
        print(f"[*] Created directory {output}/shodan-results/")

    return


def shodan(ip, output, last_octet):
    info = requests.get(
        f"https://internetdb.shodan.io/{ip}"
    )  # Shodan free api endpoint
    if "No information available" in info.text:
        print(f"Nothing for: {ip}")
        with open(f"./{output}/no_info_ips.txt", "a") as no_info_ips:
            no_info_ips.write(ip + "\n")
        return
    else:
        result_json = json.loads(str(info.text))
        with open(f"{output}/shodan-results/{last_octet}.json", "w") as ip_result:
            ip_result.write(str(info.text))
    return


def file(file, output):
    with open(f"{file}", "r") as listIP:
        for line in listIP:
            print(line)
            last_octet = line.rsplit(".", 1)[1]
            print(last_octet)
            shodan(line, output, last_octet)


def scan(range, output):
    ip_list = ipaddress.ip_network(range, strict=False)
    ips = [str(ip) for ip in ip_list]
    with open(f"./{output}/ip_list.txt", "w") as ips_output:
        ips_output.write(str(ips))
    with open(f"./{output}/no_info_ips.txt", "w") as no_info_ips:
        no_info_ips.close()

    for ip in ips:
        last_octet = ip.rsplit(".", 1)[1]
        shodan(ip, output, last_octet)
    return


def main():
    parser = argparse.ArgumentParser("parser")
    parser.add_argument(
        "--range", help="example: main.py --range 10.10.10.0/24", type=str
    )
    parser.add_argument("--file", help="example: main.py --file ip_list.txt", type=str)
    parser.add_argument("--output", help="example: main.py --output file.txt", type=str)
    parser.add_argument(
        "--output-format", help="example: main.py --output-format json/txt", type=str
    )
    parser.add_argument("--level", help="example: main.py --level 1/2/3", type=str)
    args = parser.parse_args()

    if args.output != None:
        output = args.output
        directory_check(output)
    elif args.file:
        file = args.file
        output = args.output
        directory_check(output)
    else:
        output = out_path
        directory_check(output)

    # scan(args.range, output)
    file(file, output)

    return


while main() == __name__:
    main()
