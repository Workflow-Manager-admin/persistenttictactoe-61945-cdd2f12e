from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models
from .db import get_db, init_db
from . import schemas
from . import game_logic
from datetime import datetime

app = FastAPI(
    title="Tic Tac Toe API",
    description=(
        "Persistent Tic Tac Toe backend powered by FastAPI. "
        "Provides endpoints for creating games, making moves, "
        "retrieving game state, and listing games."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Game", "description": "Tic Tac Toe game lifecycle and state"},
        {"name": "Move", "description": "Making and listing moves"}
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Ensure DB tables exist
    init_db()


@app.get("/", tags=["Game"])
def health_check():
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.post(
    "/games/",
    response_model=schemas.GameCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Game"]
)
def create_game(db: Session = Depends(get_db)):
    """
    Create and persist a new Tic Tac Toe game.
    Returns serialized game state.
    """
    board_state = ",".join([" "] * 9)
    game = models.Game(
        board_state=board_state,
        current_player="X",
        status="in_progress",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


# PUBLIC_INTERFACE
@app.get(
    "/games/{game_id}/",
    response_model=schemas.GameStateResponse,
    tags=["Game"]
)
def get_game_state(game_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the full game state, including move history.
    """
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


# PUBLIC_INTERFACE
@app.get(
    "/games/",
    response_model=List[schemas.GameListResponse],
    tags=["Game"]
)
def list_games(db: Session = Depends(get_db)):
    """
    List all games, newest first.
    """
    games = db.query(models.Game).order_by(models.Game.created_at.desc()).all()
    return games


# PUBLIC_INTERFACE
@app.post(
    "/games/{game_id}/moves/",
    response_model=schemas.GameStateResponse,
    tags=["Move"]
)
def make_move(
    game_id: int,
    req: schemas.MakeMoveRequest,
    db: Session = Depends(get_db)
):
    """
    Make a move in a game.
    Validates turn, move, updates board and move list, checks for winner/draw.
    """
    # Load game
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail="Game is not in progress"
        )

    board = game.board_state.split(",")
    try:
        # Validate player turn
        game_logic.validate_player_turn(game.current_player, req.player)
        # Validate move is legal
        new_board = game_logic.apply_move(board, req.position, req.player)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Determine move number (turn)
    turn = len(game.moves) + 1

    # Record move
    move = models.Move(
        game_id=game.id,
        turn=turn,
        player=req.player,
        position=req.position,
        created_at=datetime.utcnow()
    )
    db.add(move)

    # Update board
    game.board_state = ",".join(new_board)
    # Check win/draw/state
    winner = game_logic.check_winner(new_board)
    if winner:
        game.status = "finished"
        game.winner = winner
    elif game_logic.check_draw(new_board):
        game.status = "draw"
        game.winner = None
    else:
        game.status = "in_progress"
        game.current_player = game_logic.next_player(game.current_player)
        game.winner = None

    game.updated_at = datetime.utcnow()
    db.add(game)
    db.commit()
    db.refresh(game)
    return game
