import pytest
from unittest.mock import MagicMock
from main import app
from db.session import get_session
from db.buddies import create_buddy_in_db
from models.buddy import BuddyFrontend

