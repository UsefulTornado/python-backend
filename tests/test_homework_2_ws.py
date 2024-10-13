from fastapi.testclient import TestClient

from lecture_2.hw.shop_api.main import app

client = TestClient(app)


def test_chat():
    chat_name = "test"

    with client.websocket_connect(f"/chat/{chat_name}") as ws1:
        with client.websocket_connect(f"/chat/{chat_name}") as ws2:
            data = ws1.receive_text()
            assert "subscribed" in data

            data = ws1.receive_text()
            assert "subscribed" in data

            data = ws2.receive_text()
            assert "subscribed" in data

            test_message = "Hello, WebSocket!"
            ws1.send_text(test_message)

            data = ws1.receive_text()
            assert f":: {test_message}" in data

            data = ws2.receive_text()
            assert f":: {test_message}" in data

            ws1.close()
            data = ws2.receive_text()
            assert "unsubscribed" in data
