"""
SQLAlchemy ORM models for Tic Tac Toe persistent game state and moves.
Defines Game and Move tables.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


# PUBLIC_INTERFACE
class Game(Base):
    """
    Database model for a Tic Tac Toe game.
    Includes board state, status, and timestamps.
    """
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    # Board as comma-separated positions. Example: "X,O,X, ,O, , ,X,O"
    board_state = Column(String(32), nullable=False, default=" " * 9)
    current_player = Column(String(1), nullable=False, default="X")
    # in_progress, finished, draw, etc.
    status = Column(String(16), nullable=False, default="in_progress")
    winner = Column(String(1), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    moves = relationship(
        "Move",
        back_populates="game",
        cascade="all, delete-orphan",
        lazy="joined"
    )


# PUBLIC_INTERFACE
class Move(Base):
    """
    Database model for a move in a Tic Tac Toe game.
    Stores move position, symbol (X or O), turn number, and timestamps.
    """
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"),
                     nullable=False, index=True)
    # Index on (game_id, turn)
    turn = Column(Integer, nullable=False)
    player = Column(String(1), nullable=False)  # "X" or "O"
    position = Column(Integer, nullable=False)  # 0 - 8
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="moves")
