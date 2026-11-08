from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

def test_root():
    response = client.get('/') 
    assert response.status_code == 200

def test_missing_route():
    response = client.get('/missing') 
    assert response.status_code == 404

def test_mock_chat():
    with patch('main.ai_platform.chat', return_value="mockreply") as mock_chat:
        response = client.post('/chat', json={"prompt": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"response": "mockreply"}
    mock_chat.assert_called_once_with("Hello")

#this test is expected to fail-
def test_failing_chat():
    with patch('main.ai_platform.chat', return_value="mockreply") as mock_chat:
        response = client.post('/chat', json={"prompt": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"response": "wronganswer"}
    mock_chat.assert_called_once_with("Hello")