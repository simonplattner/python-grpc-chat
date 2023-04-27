import sys
import threading

import chat_pb2
import chat_pb2_grpc
import grpc


def run(username):
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatStub(channel)

    def receive_messages():
        request = chat_pb2.StreamMessagesRequest()
        for response in stub.StreamMessages(request):
            print(f"{response.username}: {response.message}")

    def send_messages():
        while True:
            message = input()
            request = chat_pb2.SendMessageRequest(username=username, message=message)
            stub.SendMessage(request)

    threading.Thread(target=receive_messages).start()
    threading.Thread(target=send_messages).start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <username>")
        sys.exit(1)

    run(sys.argv[1])
