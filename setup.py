import subprocess

from setuptools import setup, find_packages, Command


class GenerateProtoCommand(Command):
    description = 'Generate gRPC and Protobuf code'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = 'python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto'
        subprocess.call(command, shell=True)


setup(
    name="chatapp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'grpcio',
        'grpcio-tools'
    ],
    cmdclass={
        'genproto': GenerateProtoCommand,
    },
)
