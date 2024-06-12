import subprocess
import platform
import argparse

if platform.system() == "Windows":
    MAX_MTU = 65500
    def ping_command(host, mtu, count, timeout):
        return ["ping", str(host), "-f", "-l", str(mtu), "-n", str(count), "-w", str(timeout)]
elif platform.system() == "Linux":
    MAX_MTU = 65600 
    def ping_command(host, mtu, count, timeout):
        return ["ping", str(host), "-M", "do", "-s", str(mtu), "-c", str(count), "-W", str(timeout)]
elif platform.system() == "Darwin":
    MAX_MTU = 65500
    def ping_command(host, mtu, count, timeout):
        return ["ping", str(host), "-D", "-s", str(mtu), "-c", str(count), "-t", str(timeout)]
else:
    print (f"Platform {platform.system()} unsupported")
    exit(1)

def ping(host, mtu):
    p = subprocess.run(ping_command(host, mtu, 1, 3), capture_output=True)
    out = str(p.stdout)
    err = str(p.stderr)
    all_out = out + err
    if "fragmented" in all_out or "too long" in all_out:
        return -1
    return p.returncode

def find_pmtu(host):
    min_mtu = 0
    max_mtu = MAX_MTU
    while max_mtu - min_mtu > 1:
        mtu = (max_mtu + min_mtu) // 2
        print (f"Checking MTU={mtu + 28}...")
        ret_code = ping(host, mtu)
        if ret_code == 0:
            min_mtu = mtu
            print (f"Valid MTU!")
        else:
            print (f"Invalid MTU!")
            max_mtu = mtu
    return min_mtu + 28

def main():
    try:
        parser = argparse.ArgumentParser(
                            prog='PMTU',
                            description='Finds minimal MTU along the path to specified host')
        parser.add_argument("host", default="127.0.0.1")
        args = parser.parse_args()

        ret_code = ping(str(args.host), 64)

        if ret_code != 0:
            print(f"{args.host} is unknown or unreachable")
            exit(1)

        mtu = find_pmtu(args.host)
        print(f"PMTU is equal to {mtu}")
    except Exception as ex:
        print (f"Failed to find PMTU due: {ex}")
        exit(1)

main()