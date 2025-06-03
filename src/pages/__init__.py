from .splash_page import get_view as splash_page
from .welcome_page import get_view as welcome_page
from .login_page import get_view as login_page
from .signup_page import signup_page  # This already exports the function with this name
from .dashboard_page import dashboard_page,settings_page  # This already exports the function with this name
from .assessment_pages import get_assessment_pages  # Added import for get_assessment_pages
from .path_game import path_game # Added import for path_game
from .utils import BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING