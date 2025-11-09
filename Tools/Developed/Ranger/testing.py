import ipaddress
import argparse
import os


def scan(range, output):
    ip_list = ipaddress.ip_network(range, strict=False)
    ips = [str(ip) for ip in ip_list]
    print(ips)

    if os.path.exists(output):
        with open(f"./{output}/ip_list.txt", "w") as ips_output:
            ips_output.write(str(ips))


def main():
    parser = argparse.ArgumentParser("parser")
    parser.add_argument(
        "--range", help="example: main.py --range 10.10.10.0/24", type=str
    )
    parser.add_argument("--output", help="example: main.py --output file.txt", type=str)
    parser.add_argument(
        "--output-format", help="example: main.py --output-format json/txt", type=str
    )
    args = parser.parse_args()
    scan(args.range, args.output)


while main() == __name__:
    main()
