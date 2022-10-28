import pyaudio
import socket
import select

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

audio = pyaudio.PyAudio()
print(audio.get_default_input_device_info())

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 4444))
serversocket.listen(5)

def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        s.send(in_data)
    return (None, pyaudio.paContinue)

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)

read_list = [serversocket]

print("recording")

try:
    while True:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s in serversocket:
                (clientsocket, address) = serversocket.accept()
                read_list.append(clientsocket)
                print("Connection from", address)
            else:
                data = s.recv(1024)
                if not data:
                    read_list.remove(s)
except KeyboardInterrupt:
    pass

print("Finished recording")

serversocket.close()

stream.stop_stream()
stream.close()
audio.terminate()