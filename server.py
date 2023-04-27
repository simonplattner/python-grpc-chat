import time
from concurrent import futures

import chat_pb2
import chat_pb2_grpc
import grpc


class ChatService(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.messages = []

    def SendMessage(self, request, context):
        self.messages.append((request.username, request.message))
        print(f"{request.username}: {request.message}")
        return chat_pb2.SendMessageResponse(success=True)

    def StreamMessages(self, request, context):
        last_index = 0
        while True:
            while len(self.messages) > last_index:
                username, message = self.messages[last_index]
                last_index += 1
                yield chat_pb2.StreamMessagesResponse(username=username, message=message)
            time.sleep(0.1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
