from dataclasses import dataclass, field
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ROOT = "/chat"

router = APIRouter(prefix=ROOT)


@dataclass(slots=True)
class Broadcaster:
    subscribers: list[WebSocket] = field(init=False, default_factory=list)

    async def subscribe(self, ws: WebSocket) -> None:
        await ws.accept()
        self.subscribers.append(ws)

    async def unsubscribe(self, ws: WebSocket) -> None:
        self.subscribers.remove(ws)

    async def publish(self, message: str) -> None:
        for ws in self.subscribers:
            await ws.send_text(message)


class ChatStorage:
    def __init__(self):
        self.broadcasters: dict[str, Broadcaster] = {}

    def get_broadcaster(self, chat_name: str) -> Broadcaster:
        if chat_name not in self.broadcasters:
            self.broadcasters[chat_name] = Broadcaster()
            return self.broadcasters[chat_name]
        return self.broadcasters[chat_name]


chat_storage = ChatStorage()


@router.websocket("/{chat_name}")
async def ws_subscribe(ws: WebSocket, chat_name: str):
    client_id = uuid4()

    broadcaster = chat_storage.get_broadcaster(chat_name)

    await broadcaster.subscribe(ws)
    await broadcaster.publish(f"client {client_id} subscribed")

    try:
        while True:
            text = f"{client_id} :: {await ws.receive_text()}"
            await broadcaster.publish(text)
    except WebSocketDisconnect:
        await broadcaster.unsubscribe(ws)
        await broadcaster.publish(f"client {client_id} unsubscribed")
