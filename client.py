import socketio
import asyncio
import aiohttp
import time
import threading

# Print loading animation by overwriting the same line
def LoadingAnimation(message: str, is_connected: threading.Event):
    while True:
        for s in ["|", "/", "-", "\\"]:
            if is_connected.is_set():
                return
            print("\r" + message + s, end="")
            time.sleep(0.5)

class Client(socketio.AsyncClient):
    async def ConnectCallback(self, is_connected):
        await self.connect("wss://ws.generals.io", transports=["websocket"])
        is_connected.set()

    async def DisconnectCallback(self, is_disconnected):
        await self.disconnect()
        is_disconnected.set()

    async def run(self) -> None:
        try:
            # Connect to server
            is_connected = threading.Event()
            ani_thread = threading.Thread(target=LoadingAnimation, args=["Connecting to generals.io ... ", is_connected, ])
            connect_thread = threading.Thread(target=asyncio.run, args=[self.ConnectCallback(is_connected), ])
            ani_thread.start()
            connect_thread.start()
            ani_thread.join()
            connect_thread.join()
            print("\rConnecting to generals.io ... Connected")
            time.sleep(3)
        finally:
            # Disconnect from server
            is_disconnected = threading.Event()
            ani_thread = threading.Thread(target=LoadingAnimation, args=["Disconnecting from generals.io ... ", is_disconnected, ])
            disconnect_thread = threading.Thread(target=asyncio.run, args=[self.DisconnectCallback(is_disconnected), ])
            ani_thread.start()
            disconnect_thread.start()
            ani_thread.join()
            disconnect_thread.join()
            print("\rDisconnecting from generals.io ... Disconnected")

if __name__ == "__main__":
    client = Client()

    asyncio.run(client.run())
