import argparse
import httpx

def send_request(url, command, data=None):
    full_url = f"{url}/{command}"
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
    parser.add_argument('--server_url_1', type=str, help="URL of the server to control (e.g., 'localhost:8000').")
    parser.add_argument('--pong_time_ms', type=int, help="Time in milliseconds between pongs.", default=1000)
    parser.add_argument('--server_url_2', type=str, help="URL of the other server to ping (e.g., 'localhost:8001').")

    args = parser.parse_args()

    if args.command == 'start':
        if not args.server_url_2:
            print("You must provide --other_server_url for 'start'.")
        else:
            send_request(args.server_url_1, 'initialize', {'self_url': args.server_url_1, 'other_server_url': args.server_url_2, 'pong_time_ms': args.pong_time_ms})
            send_request(args.server_url_2, 'initialize', {'self_url': args.server_url_2, 'other_server_url': args.server_url_1, 'pong_time_ms': args.pong_time_ms})
            send_request(args.server_url_1, 'start', {'self_url': args.server_url_1, 'other_server_url': args.server_url_2, 'pong_time_ms': args.pong_time_ms})
    elif args.command == 'stop':
        send_request(args.server_url_1, 'stop')

    elif args.command == 'pause':
        send_request(args.server_url_1, 'pause')

    elif args.command == 'resume':
        send_request(args.server_url_1, 'resume')


if __name__ == "__main__":
    main()