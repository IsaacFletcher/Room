import argparse
import ipaddress
import requests
import json
import os
from termcolor import colored


# Function for creating directories for the output
def directory_check(output, subdir_name=None):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output):
        print(colored("[!] Directory does not exist, creating...", 'red'))
        os.mkdir(f"{output}")
        print(colored(f"[*] Created directory {output}", 'green'))

    # If subdir_name is provided, create a subdirectory for a specific range
    if subdir_name:
        range_dir = os.path.join(output, subdir_name)
        if not os.path.exists(range_dir):
            os.mkdir(range_dir)
            print(colored(f"[*] Created directory {range_dir}", 'green'))
        return range_dir
    return output


# Function to handle Shodan scan for each IP
def shodan(ip, output, last_octet, range_dir):
    info = requests.get(f"https://internetdb.shodan.io/{ip}")  # Shodan free API endpoint
    if "No information available" in info.text:
        print(colored(f"Nothing for: {ip}", 'yellow'))
        with open(f"{range_dir}/no_info_ips.txt", "a") as no_info_ips:
            no_info_ips.write(ip + "\n")
        return
    else:
        result_json = json.loads(info.text)
        with open(f"{range_dir}/{last_octet}.json", "w") as ip_result:
            ip_result.write(info.text)
        print(colored(f"[*] Shodan results saved for: {ip}", 'green'))
    return


# Function to handle file input (can be IP ranges or single IPs)
def file(file_path, output):
    with open(file_path, "r") as listIP:
        for line in listIP:
            line = line.strip()  # Remove any trailing whitespace or newline characters
            print(colored(f"Processing {line}", 'blue'))
            # Check if it's a valid IP range (CIDR) or a single IP
            try:
                ip_list = ipaddress.ip_network(line, strict=False)
                range_dir = directory_check(output, line.replace("/", "_"))
                for ip in ip_list:
                    last_octet = str(ip).rsplit(".", 1)[1]
                    shodan(str(ip), output, last_octet, range_dir)
            except ValueError:
                # If it's a single IP, process it
                last_octet = line.rsplit(".", 1)[1]
                range_dir = directory_check(output, line.replace(".", "_"))
                shodan(line, output, last_octet, range_dir)


# Function to extract IPs from a range and save them to a file
def extract_ips_from_range(range, output):
    ip_list = ipaddress.ip_network(range, strict=False)
    ips = [str(ip) for ip in ip_list]
    with open(f"{output}/ip_list.txt", "w") as ips_output:
        ips_output.write("\n".join(ips) + "\n")
    print(colored(f"[*] Extracted IPs and saved to {output}/ip_list.txt", 'green'))
    return


# Function to scan a specific range of IPs and save Shodan results
def scan(range, output):
    ip_list = ipaddress.ip_network(range, strict=False)
    ips = [str(ip) for ip in ip_list]
    range_dir = directory_check(output, range.replace("/", "_"))
    with open(f"{output}/ip_list.txt", "w") as ips_output:
        ips_output.write("\n".join(ips) + "\n")
    with open(f"{output}/no_info_ips.txt", "w") as no_info_ips:
        no_info_ips.close()

    for ip in ips:
        last_octet = ip.rsplit(".", 1)[1]
        shodan(ip, output, last_octet, range_dir)
    return


def main():
    parser = argparse.ArgumentParser("parser")
    parser.add_argument(
        "--range", help="example: main.py --range 10.10.10.0/24", type=str
    )
    parser.add_argument("--file", help="example: main.py --file ip_list.txt", type=str)
    parser.add_argument("--output", help="example: main.py --output ./output", type=str)
    parser.add_argument(
        "--extract-ips", help="example: main.py --extract-ips", action="store_true"
    )
    args = parser.parse_args()

    if args.output:
        output = args.output
        directory_check(output)
    elif args.file:
        file_path = args.file
        output = args.output
        directory_check(output)
    else:
        output = "./"
        directory_check(output)

    # Process range or file
    if args.extract_ips:
        if not args.range:
            print(colored("[!] Please provide a range with --range to extract IPs.", 'red'))
            return
        extract_ips_from_range(args.range, output)
    elif args.range:
        scan(args.range, output)
    elif args.file:
        file(file_path, output)


if __name__ == "__main__":
    main()

