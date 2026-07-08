"""
services/watchlist_service.py - CineLog

Business logic for managing a user's watchlist (films they plan to watch).
All functions follow the project's verb_to_noun naming convention.
"""

from app import db
from models import Film, WatchlistEntry


class FilmNotFoundError(Exception):
    """Raised when a film_id does not exist in the database."""
    pass


class AlreadyInWatchlistError(Exception):
    """Raised when a film is already in the user's watchlist."""
    pass


class NotInWatchlistError(Exception):
    """Raised when trying to remove a film that is not in the watchlist."""
    pass


def add_to_watchlist(user_id, film_id, public=True):
    """
    Add a film to a user's watchlist.

    Args:
        user_id (str): UUID of the user.
        film_id (str): UUID of the film.
        public (bool, optional): Whether this entry is visible to others.

    Returns:
        WatchlistEntry: The newly created entry.

    Raises:
        FilmNotFoundError: If film_id does not exist.
    """
    film = Film.query.get(film_id)
    if film is None:
        raise FilmNotFoundError(f"No film found with id '{film_id}'")

    entry = WatchlistEntry(user_id=user_id, film_id=film_id, public=public)
    db.session.add(entry)
    db.session.commit()
    return entry


def get_watchlist(user_id):
    """
    Return all films in a user's watchlist, sorted by date added (newest first).

    Args:
        user_id (str): UUID of the user.

    Returns:
        list[dict]: List of film dicts with watchlist metadata attached.
    """
    entries = (
        WatchlistEntry.query
        .filter_by(user_id=user_id)
        .order_by(WatchlistEntry.date_added.desc())
        .all()
    )

    result = []
    for entry in entries:
        film_dict = entry.film.to_dict()
        film_dict["date_added"] = entry.date_added.isoformat()
        film_dict["public"] = entry.public
        result.append(film_dict)

    return result
