import flet as ft
import math

def main(page: ft.Page):
    page.title = "Resistor to Prevent LED Blowout"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 700
    page.window_height = 800
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT # Ensure light mode for consistent colors
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap"
    }
    page.theme = ft.Theme(font_family="Inter")

    def show_info_snackbar(e):
        page.appbar = ft.AppBar(
            title=ft.Text("LED Circuit Simulator"),
            center_title=True,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.INFO_OUTLINE,
                    tooltip="So, the required current for the LED to be lit safely and visibly is between 5mA and 20mA."
                )
            ]
        )

    # Constants for the circuit simulation
    battery_voltage = 9.0  # Volts
    led_vf = 2.0  # LED Forward Voltage Drop in Volts
    led_max_current = 0.020  # Maximum safe current for LED in Amperes (20mA)
    led_min_current = 0.005  # Minimum current for LED to be visibly lit in Amperes (5mA)

    # State variables (using Ref for dynamic updates)
    led_state = ft.Ref[ft.Container]()
    resistor_value_display = ft.Ref[ft.Text]()
    message_box_text = ft.Ref[ft.Text]()
    message_box_container = ft.Ref[ft.Container]()

    # Enum-like classes for LED states and message types
    class LEDState:
        OFF = "off"
        LIT_SAFE = "litSafe"
        LIT_DIM = "litDim"
        BLOWN = "blown"

    class MessageType:
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"

    current_led_state = LEDState.OFF
    current_message_type = MessageType.INFO

    # Resistor options for the dropdown
    resistor_options = [
        ft.dropdown.Option("0", "No Resistor (0 Ω)"),
        ft.dropdown.Option("100", "100 Ω"),
        ft.dropdown.Option("220", "220 Ω"),
        ft.dropdown.Option("330", "330 Ω"),
        ft.dropdown.Option("470", "470 Ω"),
        ft.dropdown.Option("1000", "1 kΩ"),
        ft.dropdown.Option("2200", "2.2 kΩ"),
        ft.dropdown.Option("10000", "10 kΩ"),
    ]

    def update_led_visual(state: str):
        nonlocal current_led_state
        current_led_state = state
        
        # Reset LED properties
        led_state.current.bgcolor = ft.Colors.BLUE_GREY_200
        led_state.current.border = ft.border.all(2, ft.Colors.BLUE_GREY_400)
        led_state.current.shadow = None
        led_state.current.content = None # Remove 'X' content

        if state == LEDState.LIT_SAFE:
            led_state.current.bgcolor = ft.Colors.GREEN_300
            led_state.current.shadow = ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.7, ft.Colors.GREEN),
            )
        elif state == LEDState.LIT_DIM:
            led_state.current.bgcolor = ft.Colors.YELLOW_300
            led_state.current.shadow = ft.BoxShadow(
                spread_radius=3,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.5, ft.Colors.YELLOW),
            )
        elif state == LEDState.BLOWN:
            led_state.current.bgcolor = ft.Colors.RED_300
            led_state.current.border = ft.border.all(2, ft.Colors.RED_500)
            led_state.current.shadow = ft.BoxShadow(
                spread_radius=5,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.8, ft.Colors.RED),
            )
            # Add 'X' for blown LED
            led_state.current.content = ft.Stack(
                [
                    ft.Container(
                        width=35,
                        height=4,
                        bgcolor=ft.Colors.RED_600,
                        rotate=ft.Rotate(angle=math.pi / 4), # 45 degrees
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        width=35,
                        height=4,
                        bgcolor=ft.Colors.RED_600,
                        rotate=ft.Rotate(angle=-math.pi / 4), # -45 degrees
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.alignment.center,
            )
        page.update()

    def display_message(message: str, type: str):
        nonlocal current_message_type
        current_message_type = type
        message_box_text.current.value = message

        if type == MessageType.INFO:
            message_box_container.current.bgcolor = ft.Colors.BLUE_100
            message_box_text.current.color = ft.Colors.BLUE_800
        elif type == MessageType.SUCCESS:
            message_box_container.current.bgcolor = ft.Colors.GREEN_100
            message_box_text.current.color = ft.Colors.GREEN_800
        elif type == MessageType.WARNING:
            message_box_container.current.bgcolor = ft.Colors.YELLOW_100
            message_box_text.current.color = ft.Colors.YELLOW_800
        elif type == MessageType.ERROR:
            message_box_container.current.bgcolor = ft.Colors.RED_100
            message_box_text.current.color = ft.Colors.RED_800
        page.update()

    def simulate_circuit(e):
        selected_resistor_value = float(resistor_dropdown.value)

        # Update resistor visual display
        resistor_value_display.current.value = f"{round(selected_resistor_value)} Ω"

        # If no resistor is selected (0 Ohms), it's a short circuit for the LED
        if selected_resistor_value == 0:
            update_led_visual(LEDState.BLOWN)
            display_message('No resistor! The LED is immediately blown due to excessive current. Always use a resistor!', MessageType.ERROR)
            return

        # Calculate voltage across the resistor (V_resistor = V_source - V_LED)
        voltage_across_resistor = battery_voltage - led_vf

        # Calculate actual current through the circuit (I = V/R)
        actual_current = voltage_across_resistor / selected_resistor_value  # Amperes

        # Check conditions
        if actual_current > led_max_current:
            update_led_visual(LEDState.BLOWN)
            display_message(f'Current is {round(actual_current * 1000)} mA. Too high! The LED is blown. Try a larger resistor.', MessageType.ERROR)
        elif actual_current < led_min_current:
            update_led_visual(LEDState.LIT_DIM)
            display_message(f'Current is {round(actual_current * 1000)} mA. Too low! The LED is dimly lit or not lit at all. Try a smaller resistor.', MessageType.WARNING)
        else:
            update_led_visual(LEDState.LIT_SAFE)
            display_message(f'Current is {round(actual_current * 1000)} mA. Perfect! The LED is lit safely.', MessageType.SUCCESS)

    def on_resistor_change(e):
        # Update resistor display immediately when selection changes, before connecting
        resistor_value_display.current.value = f"{round(float(resistor_dropdown.value))} Ω"
        update_led_visual(LEDState.OFF) # Turn off LED when resistor changes
        display_message('Resistor changed. Connect the circuit to simulate!', MessageType.INFO)

    # UI Components
    battery_component = ft.Column(
        [
            ft.Container(
                width=60,
                height=80,
                bgcolor=ft.Colors.AMBER_300,
                border=ft.border.all(2, ft.Colors.AMBER_600),
                border_radius=ft.border_radius.all(8),
                content=ft.Stack(
                    [
                        ft.Container( # For '+' sign
                            content=ft.Text(
                                '+',
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED_600,
                            ),
                            alignment=ft.alignment.top_right, # Align to top right
                            padding=ft.padding.only(right=5, top=5) # Small padding from edge
                        ),
                        ft.Container( # For '-' sign
                            content=ft.Text(
                                '-',
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_600,
                            ),
                            alignment=ft.alignment.bottom_left, # Align to bottom left
                            padding=ft.padding.only(left=5, bottom=5) # Small padding from edge
                        ),
                    ]
                ),
            ),
            ft.Text('Battery (9V)', size=14, color=ft.Colors.BLACK54),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    resistor_component = ft.Column(
        [
            ft.Container(
                width=80,
                height=30,
                bgcolor=ft.Colors.YELLOW_200,
                border=ft.border.all(2, ft.Colors.YELLOW_400),
                border_radius=ft.border_radius.all(4),
                alignment=ft.alignment.center,
                content=ft.Text(f"{round(float(resistor_options[2].key))} Ω", # Default to 220 Ohm
                                ref=resistor_value_display,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BROWN_900,
                                size=14),
            ),
            ft.Text('Resistor', size=14, color=ft.Colors.BLACK54),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    led_component = ft.Column(
        [
            ft.Container(
                ref=led_state,
                width=50,
                height=50,
                border_radius=ft.border_radius.all(25),
                bgcolor=ft.Colors.BLUE_GREY_200, # Initial off state
                border=ft.border.all(2, ft.Colors.BLUE_GREY_400),
                alignment=ft.alignment.center,
            ),
            ft.Text('LED', size=14, color=ft.Colors.BLACK54),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    resistor_dropdown = ft.Dropdown(
        options=resistor_options,
        value="220", # Default selected value
        on_change=on_resistor_change,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border_radius=ft.border_radius.all(8),
        border_color=ft.Colors.GREY_300,
        focused_border_color=ft.Colors.BLUE_500,
        label="Select Resistor",
        text_style=ft.TextStyle(size=14),
    )

    connect_button = ft.ElevatedButton(
        content=ft.Text(
            'Connect Circuit',
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        on_click=simulate_circuit,
        style=ft.ButtonStyle(
            bgcolor={"": ft.Colors.BLUE_500},
            color={"": ft.Colors.WHITE},
            padding={"": ft.padding.symmetric(horizontal=32, vertical=16)},
            shape={"": ft.RoundedRectangleBorder(radius=12)},
            elevation={"": 6},
            shadow_color={"": ft.Colors.BLUE_300},
        ),
    )

    message_box = ft.Container(
        ref=message_box_container,
        margin=ft.margin.only(top=24),
        padding=ft.padding.all(16),
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        bgcolor=ft.Colors.BLUE_100, # Initial info state
        content=ft.Text(
            'Select a resistor and connect the circuit!',
            ref=message_box_text,
            size=18,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.BLUE_800, # Initial info state
            text_align=ft.TextAlign.CENTER,
        ),
    )

    # Main layout
    page.add(
        ft.Container(
            padding=ft.padding.all(32),
            width=600,
            border_radius=ft.border_radius.all(24),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                [
                    ft.Text(
                        'Resistor to Prevent LED Blowout',
                        size=28,
                        weight=ft.FontWeight.W_800,
                        color=ft.Colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        'Select a resistor value and connect the circuit to see if the LED lights up safely!',
                        size=16,
                        color=ft.Colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        padding=ft.padding.all(16),
                        margin=ft.margin.only(top=24),
                        border=ft.border.all(2, ft.Colors.BLUE_GREY_200),
                        border_radius=ft.border_radius.all(16),
                        content=ft.Row(
                            [
                                battery_component,
                                resistor_component,
                                led_component,
                            ],
                            wrap=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=32,
                            run_spacing=24,
                        ),
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        'Select Resistor:',
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.BLACK87,
                                    ),
                                    ft.Container(width=12),
                                    resistor_dropdown,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Container(height=16),
                            connect_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0, # No extra spacing between row and button
                    ),
                    message_box,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
        )
    )

# To run this Flet app:
# 1. Save the code as a Python file (e.g., `main.py`).
# 2. Run from your terminal: `flet run main.py`
#    For web app: `flet run main.py -w`

ft.app(main)
