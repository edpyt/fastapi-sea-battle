import asyncio

from fastapi import WebSocket

from src.api.ws.managers.redis import RedisPubSubManager
from src.core.services.board import GameBoard


class SeaBattleManager:
    """WebSocket manager for game 'Sea Battle'"""
    
    def __init__(self) -> None:
        """
        Initializes the WebSocketManager.

        Attributes:
            rooms (dict): A dictionary to store WebSocket connections in
            different rooms 
            self.pub
        """
        self.rooms: dict = {}
        self.pubsub_client = RedisPubSubManager()
    
    async def add_user_to_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Adds a user's WebSocket connection to a room.
        
        Args:
            room_id (str): Room ID or channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        await websocket.accept()
        
        if room_id not in self.rooms:
            await self.pubsub_client.connect()
            pubsub_subscriber = await self.pubsub_client.subscribe(room_id)
            await asyncio.create_task(
                self._pubsub_data_reader(pubsub_subscriber)
            )
        self.rooms.setdefault(room_id, {})

        user_connection_name: str = f'user{len(self.rooms[room_id]) + 1}'
        self.rooms[room_id].setdefault(user_connection_name, {})
        (
            self.rooms[room_id][user_connection_name]
            .setdefault('connection', websocket)
        )
        if not self.rooms[room_id][user_connection_name].get('game_board'):
            self.rooms[room_id][user_connection_name]['game_board'] = GameBoard()


    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        """
        Broadcasts a message to all connected WebSockets in a room.

        Args:
            room_id (str): Room ID or channel name.
            message (str): Message to be broadcasted.
        """
        await self.pubsub_client._publish(room_id, message)
    
    async def remove_user_from_room(
        self, room_id: str, websocket: WebSocket
    ) -> None:
        """
        Removes a user's WebSocket connection from a room.

        Args:
            room_id (str): Room ID or channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        self.rooms[room_id].remove(websocket)

        if len(self.rooms[room_id]) == 0:
            del self.rooms[room_id]
            await self.pubsub_client.unsubscribe(room_id)

    async def place_ship_to_a_board(self, room_id: str, ship_type: str) -> None:
        """
        Placing ship to the game board

        Args:
            room_id (str): Room ID or channel name,
            ship_type (str): Ship type which place to a board.
        """