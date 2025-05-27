import flet as ft
import math

# Constants (from JS)
BATTERY_VOLTAGE = 9.0
MOTOR_MIN_VOLTAGE = 7.0
MOTOR_MAX_VOLTAGE = 9.5
MOTOR_STUTTER_THRESHOLD = 0.5
MOTOR_CURRENT_DRAW = 0.1
ASSUMED_FREQUENCY = 120.0  # Hz

# Colors (approximations)
COLOR_BACKGROUND = ft.Colors.BLUE_GREY_50  # #f0f4f8
COLOR_CONTAINER_BG = ft.Colors.WHITE
COLOR_TEXT_PRIMARY = ft.Colors.BLACK87
COLOR_TEXT_SECONDARY = ft.Colors.BLACK54
COLOR_BUTTON_BLUE = ft.Colors.BLUE_500
COLOR_BUTTON_INDIGO = ft.Colors.INDIGO_600  # For selection buttons

# Motor states
MOTOR_STATE_OFF = "off"
MOTOR_STATE_STUTTERING = "stuttering"
MOTOR_STATE_SMOOTH = "smooth"
MOTOR_STATE_OVERVOLTAGE = "overvoltage"

# Message types
MSG_TYPE_INFO = "info"
MSG_TYPE_SUCCESS = "success"
MSG_TYPE_WARNING = "warning"
MSG_TYPE_ERROR = "error"

class VoltageGraph(ft.LineChart):
    def __init__(self, ref=None, width=560, height=200, ripple_voltage=2.0):
        self.samples = 100  # Number of points to plot for the ripple
        self.min_graph_voltage = BATTERY_VOLTAGE - 5
        self.max_graph_voltage = BATTERY_VOLTAGE + 1

        self.current_left_axis = ft.ChartAxis(
            labels_size=40, 
            title=ft.Text("Voltage (V)", size=12, weight=ft.FontWeight.BOLD),
            title_size=22,
            show_labels=True
        )
        self.current_bottom_axis = ft.ChartAxis(
            labels_size=32, 
            title=ft.Text("Time (samples)", size=12, weight=ft.FontWeight.BOLD),
            title_size=22,
            show_labels=True
        )

        super().__init__(
            ref=ref,
            width=width,
            height=height,
            left_axis=self.current_left_axis,
            bottom_axis=self.current_bottom_axis,
            min_y=self.min_graph_voltage,
            max_y=self.max_graph_voltage,
            min_x=0,
            max_x=self.samples,
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY), # Changed ft.colors to ft.Colors
            border=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.BLUE_GREY_300),
                left=ft.BorderSide(1, ft.Colors.BLUE_GREY_300)
            ),
            bgcolor=ft.Colors.BLUE_GREY_100,
            data_series=[],  # Initialize with empty data series
            expand=True, # Use available width/height
            animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        )
        self.ripple_voltage = ripple_voltage
        self.draw_graph()  # Initial draw

    def draw_graph(self, ripple_voltage_param=None):
        if ripple_voltage_param is not None:
            self.ripple_voltage = ripple_voltage_param

        # --- Configure Axes Labels ---
        left_labels = []
        # Generate Y-axis labels at 0.5V intervals
        v = math.floor(self.min_y * 2) / 2 # Start from a rounded .0 or .5 value
        while v <= self.max_y:
            left_labels.append(ft.ChartAxisLabel(
                value=v,
                label=ft.Text(f"{v:.1f}", size=9, color=ft.Colors.BLACK54) # Adjusted size, format to 1 decimal
            ))
            v += 0.5
        self.left_axis.labels = left_labels

        bottom_labels = []
        num_bottom_label_segments = 10  # Increased from 4 to 10 for more X-axis labels (0, 10, ..., 100)
        for i in range(num_bottom_label_segments + 1):
            val = (self.samples / num_bottom_label_segments) * i
            bottom_labels.append(ft.ChartAxisLabel(
                value=val,
                label=ft.Text(f"{val:.0f}", size=9, color=ft.Colors.BLACK54) # Adjusted size
            ))
        self.bottom_axis.labels = bottom_labels
        
        # --- Ideal Voltage Line (Battery Voltage) ---
        ideal_voltage_points = [
            ft.LineChartDataPoint(0, BATTERY_VOLTAGE),
            ft.LineChartDataPoint(self.samples, BATTERY_VOLTAGE)
        ]
        ideal_line_series = ft.LineChartData(
            data_points=ideal_voltage_points,
            color=ft.Colors.GREEN_500,
            stroke_width=2
        )

        # --- Motor Voltage Ripple Line ---
        motor_voltage_points = []
        # This calculation attempts to match the visual output of the original canvas version
        ripple_visual_center = BATTERY_VOLTAGE 
        # The original canvas code's y_value_voltage calculation:
        # ripple_max_voltage_val = BATTERY_VOLTAGE + (self.ripple_voltage / 2)
        # y_value_voltage = ripple_max_voltage_val - (cycle_progress_original * 2 * self.ripple_voltage)
        # This created a sawtooth wave.
        # For LineChart, we plot (x, actual_voltage_value)

        for i in range(self.samples + 1):
            x_coord = float(i)
            
            # Normalized progress through the two cycles shown (0 to 1 for each cycle)
            norm_progress_total_samples = i / self.samples if self.samples > 0 else 0
            cycle_progress_0_to_1 = (norm_progress_total_samples * 2.0) % 1.0

            # Replicating the original waveform shape:
            # It started at BATTERY_VOLTAGE + self.ripple_voltage / 2
            # And dropped by self.ripple_voltage * 2 over the 0-1 cycle_progress.
            # This means it went from (B + R/2) to (B + R/2 - 2R) = (B - 3R/2).
            # This is a large swing. Let's assume ripple_voltage is peak-to-peak.
            # A triangle wave oscillating +/- ripple_voltage/2 around BATTERY_VOLTAGE:
            # Amplitude = self.ripple_voltage / 2.0
            # Waveform value (-1 to 1 for triangle): (1.0 - 4.0 * abs(cycle_progress_0_to_1 - 0.5)) if it's a symmetric triangle
            # Or, for the original sawtooth-like drop:
            y_offset = (0.5 - cycle_progress_0_to_1) * self.ripple_voltage # Symmetrical ripple around BATTERY_VOLTAGE
            y_value_voltage = ripple_visual_center + y_offset

            # Clamp voltage to graph physical display limits (min_y, max_y for chart)
            y_value_display = max(self.min_y, min(self.max_y, y_value_voltage))
            
            motor_voltage_points.append(ft.LineChartDataPoint(x_coord, y_value_display))
        
        motor_line_series = ft.LineChartData(
            data_points=motor_voltage_points,
            color=ft.Colors.RED_500,
            stroke_width=2,
            curved=False # Original was straight lines
        )
        
        self.data_series = [ideal_line_series, motor_line_series]
        
        # Tooltips will show point values. Legends can be added externally if needed.
        # Example: self.tooltip_content = ft.Text(...) for custom tooltips per series.

        if self.page: # Ensure page context for update
            self.update()
        # Flet LineChart should auto-update on data_series change, but explicit update is safer.

def main(page: ft.Page):
    page.title = "Motor Smoothing Challenge"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 700
    page.window_height = 850 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap"}
    page.theme = ft.Theme(font_family="Inter")
    page.bgcolor = COLOR_BACKGROUND

    intro_text_ref = ft.Ref[ft.Text]()
    message_box_ref = ft.Ref[ft.Container]()
    message_box_text_ref = ft.Ref[ft.Text]()
    motor_visual_ref = ft.Ref[ft.Container]()
    motor_state_display_ref = ft.Ref[ft.Text]()
    capacitor_value_display_ref = ft.Ref[ft.Text]()
    capacitor_select_ref = ft.Ref[ft.Dropdown]()
    voltage_graph_ref = ft.Ref[VoltageGraph]()
    main_game_content_col_ref = ft.Ref[ft.Column]()
    component_selection_col_ref = ft.Ref[ft.Column]()

    def handle_capacitor_change(e):
        selected_cap_value_uF = float(e.control.value)
        
        if capacitor_value_display_ref.current:
            capacitor_value_display_ref.current.value = f"{selected_cap_value_uF:.0f} µF"
        
        update_motor_visual(MOTOR_STATE_OFF, 'OFF') # Reset motor state on cap change
        display_message('Capacitor value changed. Connect circuit to see effect.', MSG_TYPE_INFO) # Inform user
        
        selected_cap_value_F = selected_cap_value_uF / 1_000_000.0
        
        # Calculate effective_ripple (same logic as in simulate_circuit)
        # Default ripple if no cap or for initial state.
        base_ripple_voltage = 2.0 
        effective_ripple = base_ripple_voltage if selected_cap_value_F == 0 else max(0.05, MOTOR_CURRENT_DRAW / (ASSUMED_FREQUENCY * selected_cap_value_F))

        if voltage_graph_ref.current:
            voltage_graph_ref.current.draw_graph(effective_ripple)
            
        page.update()

    def update_motor_visual(state: str, display_text: str):
        motor_visual = motor_visual_ref.current
        motor_state_display = motor_state_display_ref.current
        if not motor_visual or not motor_state_display: return

        motor_visual.bgcolor = ft.Colors.GREY_200
        motor_visual.border = ft.border.all(2, ft.Colors.GREY_400)
        motor_state_display.color = ft.Colors.GREY_700

        if state == MOTOR_STATE_STUTTERING:
            motor_visual.bgcolor = ft.Colors.ORANGE_300
            motor_visual.border = ft.border.all(2, ft.Colors.ORANGE_500)
            motor_state_display.color = ft.Colors.ORANGE_800
        elif state == MOTOR_STATE_SMOOTH:
            motor_visual.bgcolor = ft.Colors.GREEN_300
            motor_visual.border = ft.border.all(2, ft.Colors.GREEN_500)
            motor_state_display.color = ft.Colors.GREEN_800
        elif state == MOTOR_STATE_OVERVOLTAGE:
            motor_visual.bgcolor = ft.Colors.RED_300
            motor_visual.border = ft.border.all(2, ft.Colors.RED_500)
            motor_state_display.color = ft.Colors.RED_900
        
        motor_state_display.value = display_text
        page.update()

    def display_message(message: str, msg_type: str):
        msg_box_container = message_box_ref.current
        msg_box_text = message_box_text_ref.current
        if not msg_box_container or not msg_box_text: return

        msg_box_text.value = message
        
        color_map = {
            MSG_TYPE_INFO: (ft.Colors.BLUE_100, ft.Colors.BLUE_800),
            MSG_TYPE_SUCCESS: (ft.Colors.GREEN_100, ft.Colors.GREEN_800),
            MSG_TYPE_WARNING: (ft.Colors.YELLOW_100, ft.Colors.YELLOW_800),
            MSG_TYPE_ERROR: (ft.Colors.RED_100, ft.Colors.RED_800),
        }
        bg_color, text_color = color_map.get(msg_type, (ft.Colors.GREY_100, ft.Colors.GREY_800))
        msg_box_container.bgcolor = bg_color
        msg_box_text.color = text_color
        page.update()

    def simulate_circuit(e):
        selected_cap_value_uF = float(capacitor_select_ref.current.value)
        selected_cap_value_F = selected_cap_value_uF / 1_000_000.0

        if capacitor_value_display_ref.current:
            capacitor_value_display_ref.current.value = f"{selected_cap_value_uF:.0f} µF"

        base_ripple_voltage = 2.0
        effective_ripple = base_ripple_voltage if selected_cap_value_F == 0 else max(0.05, MOTOR_CURRENT_DRAW / (ASSUMED_FREQUENCY * selected_cap_value_F))
        
        average_voltage = BATTERY_VOLTAGE

        if voltage_graph_ref.current:
            voltage_graph_ref.current.draw_graph(effective_ripple)

        if average_voltage < MOTOR_MIN_VOLTAGE:
            update_motor_visual(MOTOR_STATE_OFF, 'OFF')
            display_message(f"Voltage low ({average_voltage:.1f}V avg). Motor off.", MSG_TYPE_ERROR)
        elif average_voltage > MOTOR_MAX_VOLTAGE:
            update_motor_visual(MOTOR_STATE_OVERVOLTAGE, 'OVERVOLTAGE')
            display_message(f"Voltage high ({average_voltage:.1f}V avg). Motor damage risk.", MSG_TYPE_ERROR)
        elif effective_ripple > MOTOR_STUTTER_THRESHOLD:
            update_motor_visual(MOTOR_STATE_STUTTERING, 'STUTTERING')
            display_message(f"Ripple high ({effective_ripple:.1f}V p-p). Motor stutters. Larger capacitor?", MSG_TYPE_WARNING)
        else:
            update_motor_visual(MOTOR_STATE_SMOOTH, 'SMOOTH')
            display_message(f"Ripple low ({effective_ripple:.1f}V p-p). Motor smooth!", MSG_TYPE_SUCCESS)
        page.update()

    def handle_component_selection(e):
        selected_component = e.control.data
        
        if component_selection_col_ref.current:
            component_selection_col_ref.current.visible = (selected_component != 'capacitor')
        if main_game_content_col_ref.current:
            main_game_content_col_ref.current.visible = (selected_component == 'capacitor')

        if selected_component == 'capacitor':
            if intro_text_ref.current:
                intro_text_ref.current.value = 'Great choice! Select capacitor & connect.'
            if capacitor_value_display_ref.current and capacitor_select_ref.current:
                 capacitor_value_display_ref.current.value = f"{float(capacitor_select_ref.current.value):.0f} µF"
            update_motor_visual(MOTOR_STATE_OFF, 'OFF')
            display_message('Select capacitor and connect circuit!', MSG_TYPE_INFO)
            if voltage_graph_ref.current:
                voltage_graph_ref.current.draw_graph(2.0) 
        else:
            feedback_map = {
                'resistor': ('Resistor limits current, not smooths. Try Capacitor.', MSG_TYPE_WARNING),
                'diode': ('Diode rectifies, not smooths. Try Capacitor.', MSG_TYPE_WARNING),
                'transistor': ('Transistor switches/amplifies, not smooths. Try Capacitor.', MSG_TYPE_WARNING),
                'other': ('Other components might help, but Capacitor is key. Try Capacitor.', MSG_TYPE_WARNING),
            }
            message, msg_type = feedback_map.get(selected_component, ('Not for smoothing. Try Capacitor!', MSG_TYPE_ERROR))
            display_message(message, msg_type)
            if intro_text_ref.current:
                intro_text_ref.current.value = 'Try again! Which component smooths voltage?'
        page.update()

    # Define the Icon that will have a tooltip
    info_icon = ft.Icon(
        name=ft.Icons.INFO_OUTLINE, 
        color=ft.Colors.BLUE_400, 
        size=20
    )
    # Define the Tooltip and assign it to the Icon's tooltip property
    info_icon.tooltip = ft.Tooltip(
        message="Hint: Stores/releases charge, stabilizes voltage.",
        padding=10, 
        border_radius=8, 
        text_style=ft.TextStyle(size=12),
        bgcolor=ft.Colors.BLACK54, 
        show_duration=5000
    )
    title_row = ft.Row(
        [
            ft.Text("Motor not smooth. Which item to use?", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY, expand=True, text_align=ft.TextAlign.CENTER),
            info_icon # Use the Icon object here, which has the tooltip property set
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=5
    )
    _shared_intro_text = ft.Text(ref=intro_text_ref, value="Choose a component to begin!", color=COLOR_TEXT_SECONDARY, size=16, text_align=ft.TextAlign.CENTER)

    component_buttons_list = [
        ft.ElevatedButton(
            text, data=data_val, on_click=handle_component_selection, width=250,
            style=ft.ButtonStyle(bgcolor=COLOR_BUTTON_INDIGO, color=ft.Colors.WHITE, padding=12, shape=ft.RoundedRectangleBorder(radius=10))
        ) for text, data_val in [
            ("Capacitor", "capacitor"), ("Resistor", "resistor"), ("Diode", "diode"),
            ("Transistor", "transistor"), ("Other Components", "other")
        ]
    ]
    _component_selection_screen = ft.Column(
        ref=component_selection_col_ref, controls=component_buttons_list,
        spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=True
    )

    battery_visual = ft.Container(width=60, height=80, bgcolor=ft.Colors.AMBER_300, border=ft.border.all(2, ft.Colors.AMBER_600), border_radius=8, content=ft.Stack([ft.Container(content=ft.Text('+', weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600), top=5, right=5), ft.Container(content=ft.Text('-', weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600), bottom=5, left=5)]))
    cap_visual = ft.Container(width=50, height=70, bgcolor=ft.Colors.LIGHT_BLUE_200, border=ft.border.all(2, ft.Colors.LIGHT_BLUE_400), border_radius=4, content=ft.Column([ft.Container(width=30, height=4, bgcolor=ft.Colors.GREY_700, margin=2)]*2 + [ft.Text(ref=capacitor_value_display_ref, value="100 µF", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900)], alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center)
    motor_visual = ft.Container(ref=motor_visual_ref, width=60, height=60, bgcolor=ft.Colors.GREY_200, border=ft.border.all(2, ft.Colors.GREY_400), border_radius=8, content=ft.Text(ref=motor_state_display_ref, value="OFF", weight=ft.FontWeight.BOLD), alignment=ft.alignment.center)
    
    circuit_diagram = ft.Container(ft.Row([
        ft.Column([battery_visual, ft.Text("Battery (9V)")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), 
        ft.Column([cap_visual, ft.Text("Capacitor")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), 
        ft.Column([motor_visual, ft.Text("Motor")], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=15, vertical_alignment=ft.CrossAxisAlignment.START), padding=16, border=ft.border.all(1, ft.Colors.BLUE_GREY_200), border_radius=12)

    _capacitor_select = ft.Dropdown(ref=capacitor_select_ref, label="Capacitor:", value="100", width=220, options=[ft.dropdown.Option(v, l) for v, l in [("0", "No Cap (0 µF)"), ("1", "1 µF"), ("10", "10 µF"), ("100", "100 µF (Rec)"), ("470", "470 µF"), ("1000", "1000 µF"), ("2200", "2200 µF")]], on_change=handle_capacitor_change) # Changed to use the new handler
    connect_button = ft.ElevatedButton("Connect Circuit", on_click=simulate_circuit, style=ft.ButtonStyle(bgcolor=COLOR_BUTTON_BLUE, color=ft.Colors.WHITE, padding=ft.padding.symmetric(horizontal=20,vertical=12)))
    controls_row = ft.Row([_capacitor_select, connect_button], alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    _message_box = ft.Container(ref=message_box_ref, content=ft.Text(ref=message_box_text_ref, value="Select capacitor!", size=15, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER), padding=12, border_radius=10, margin=ft.margin.symmetric(vertical=10), bgcolor=ft.Colors.BLUE_100, shadow=ft.BoxShadow(blur_radius=3, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)), width=550, alignment=ft.alignment.center)
    _voltage_graph = VoltageGraph(ref=voltage_graph_ref, width=560, height=200, ripple_voltage=2.0)

    _main_game_content = ft.Column(ref=main_game_content_col_ref, controls=[circuit_diagram, controls_row, _message_box, _voltage_graph], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)
    
    game_container = ft.Container(content=ft.Column([title_row, _shared_intro_text, _component_selection_screen, _main_game_content], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, scroll=ft.ScrollMode.ADAPTIVE), width=600, padding=20, border_radius=20, bgcolor=COLOR_CONTAINER_BG, shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)))
    page.add(game_container)

    if intro_text_ref.current: intro_text_ref.current.value = "Choose a component to begin!"
    display_message('Choose a component to begin!', MSG_TYPE_INFO)
    if capacitor_value_display_ref.current and capacitor_select_ref.current: capacitor_value_display_ref.current.value = f"{float(capacitor_select_ref.current.value):.0f} µF"
    update_motor_visual(MOTOR_STATE_OFF, 'OFF')
    if voltage_graph_ref.current: voltage_graph_ref.current.draw_graph(2.0)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
