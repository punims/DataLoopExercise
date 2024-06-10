import argparse
import httpx

def send_request(url, command, data=None):
    full_url = f"http://{url}/{command}"
    try:
        if data:
            response = httpx.post(full_url, json=data)
        else:
            response = httpx.post(full_url)
        print(response.json())
    except Exception as e:
        print(f"Failed to connect to the server at {full_url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Control the pong game servers.")
    parser.add_argument('command', type=str, choices=['start', 'stop', 'pause', 'resume'], help="Command to execute (start or stop).")
    parser.add_argument('self_url', type=str, help="URL of the server to control (e.g., 'localhost:8000').")
    parser.add_argument('--pong_time_ms', type=int, help="Time in milliseconds between pongs.", default=1000)
    parser.add_argument('--other_server_url', type=str, help="URL of the other server to ping (e.g., 'localhost:8001').")

    args = parser.parse_args()

    if args.command == 'start':
        if not args.other_server_url:
            print("You must provide --other_server_url for 'start'.")
        else:
            print(args.other_server_url)
            print("Sending data:", {'other_server_url': args.other_server_url, 'pong_time_ms': args.pong_time_ms})
            send_request(args.self_url, 'start', {'self_url': args.self_url, 'other_server_url': args.other_server_url, 'pong_time_ms': args.pong_time_ms})
    elif args.command == 'stop':
        send_request(args.self_url, 'stop')

    elif args.command == 'pause':
        send_request(args.self_url, 'pause')

    elif args.command == 'resume':
        send_request(args.self_url, 'resume')


if __name__ == "__main__":
    main()