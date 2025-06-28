"""
Pydantic schemas for Tic Tac Toe game requests and responses.
Defines serialization and validation for API payloads.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# PUBLIC_INTERFACE
class MoveCreate(BaseModel):
    """Request schema for making a move."""
    position: int = Field(..., ge=0, le=8, description="Board cell index (0-8).")
    player: str = Field(..., regex="^(X|O)$", description="Player symbol.")


# PUBLIC_INTERFACE
class MoveResponse(BaseModel):
    """Response schema describing a move."""
    id: int
    turn: int
    player: str
    position: int
    created_at: datetime

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class GameCreateResponse(BaseModel):
    """Response after creating a new game."""
    id: int
    board_state: str
    current_player: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class GameStateResponse(BaseModel):
    """Describes the full state of a game."""
    id: int
    board_state: str
    current_player: str
    status: str
    winner: Optional[str]
    created_at: datetime
    updated_at: datetime
    moves: List[MoveResponse]

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class GameListResponse(BaseModel):
    """Summary info for listing games."""
    id: int
    board_state: str
    status: str
    winner: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class MakeMoveRequest(BaseModel):
    """Request body for making a move."""
    position: int = Field(..., ge=0, le=8)
    player: str = Field(..., regex="^(X|O)$")
