from .splash_page import get_view as splash_page
from .welcome_page import get_view as welcome_page
from .login_page import get_view as login_page
from .signup_page import signup_page  # This already exports the function with this name
from .dashboard_page import dashboard_page  # This already exports the function with this name
from .settings_page import settings_page  # This already exports the function with this name
from .assessment_pages import get_assessment_pages  # Added import for get_assessment_pages
from .path_game import path_game # Added import for path_game
from .profile_page import profile_page # Added import for path_game
from .utils import click1_audio,play_audio1,audio1,error_audio,play_error_sound,play_click_sound,BG_COLOR, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_PADDING,APPBAR_FONT_SIZE