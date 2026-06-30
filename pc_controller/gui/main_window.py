import customtkinter as ctk


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Brazo Robotico")
        self.geometry("1200x700")   

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================================
        # VIDEO
        # ==================================

        self.video_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.video_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.current_image = None

        # ==================================
        # PANEL DERECHO
        # ==================================

        self.side_frame = ctk.CTkFrame(self)

        self.side_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # ==================================
        # ESTADO ROBOT
        # ==================================

        self.lbl_base = ctk.CTkLabel(
            self.side_frame,
            text="Base: 0"
        )
        self.lbl_base.pack(pady=5)

        self.lbl_codo1 = ctk.CTkLabel(
            self.side_frame,
            text="Codo1: 0"
        )
        self.lbl_codo1.pack(pady=5)

        self.lbl_codo2 = ctk.CTkLabel(
            self.side_frame,
            text="Codo2: 0"
        )
        self.lbl_codo2.pack(pady=5)

        self.lbl_pinza = ctk.CTkLabel(
            self.side_frame,
            text="Pinza: 0"
        )
        self.lbl_pinza.pack(pady=5)

        self.lbl_servos = ctk.CTkLabel(
            self.side_frame,
            text="Servos: OFF"
        )
        self.lbl_servos.pack(pady=5)

        self.lbl_comm = ctk.CTkLabel(
            self.side_frame,
            text="Comunicacion: OFF"
        )
        self.lbl_comm.pack(pady=5)

        self.lbl_sync = ctk.CTkLabel(
            self.side_frame,
            text="HOME: NO SINCRONIZADO"
        )
        self.lbl_sync.pack(pady=5)

        self.lbl_fps = ctk.CTkLabel(
            self.side_frame,
            text="FPS: 0"
        )
        self.lbl_fps.pack(pady=5)

        # ==================================
        # SERIAL
        # ==================================

        self.entry_com = ctk.CTkEntry(
            self.side_frame,
            placeholder_text="COM3"
        )

        self.entry_com.pack(
            pady=10,
            padx=10,
            fill="x"
        )

        self.btn_connect = ctk.CTkButton(
            self.side_frame,
            text="Conectar"
        )

        self.btn_connect.pack(
            pady=5,
            padx=10,
            fill="x"
        )

        self.btn_disconnect = ctk.CTkButton(
            self.side_frame,
            text="Desconectar"
        )

        self.btn_disconnect.pack(
            pady=5,
            padx=10,
            fill="x"
        )

        # ==================================
        # COMUNICACION
        # ==================================

        self.btn_comm_on = ctk.CTkButton(
            self.side_frame,
            text="Activar Comunicacion"
        )

        self.btn_comm_on.pack(
            pady=5,
            padx=10,
            fill="x"
        )

        self.btn_comm_off = ctk.CTkButton(
            self.side_frame,
            text="Detener Comunicacion"
        )

        self.btn_comm_off.pack(
            pady=5,
            padx=10,
            fill="x"
        )

        # ==================================
        # SINCRONIZACION
        # ==================================

        self.btn_sync_home = ctk.CTkButton(
            self.side_frame,
            text="Sincronizar HOME"
        )

        self.btn_sync_home.pack(
            pady=5,
            padx=10,
            fill="x"
        )

        # ==================================
        # MODO
        # ==================================

        self.mode_var = ctk.StringVar(
            value="GESTOS"
        )

        self.mode_menu = ctk.CTkOptionMenu(
            self.side_frame,
            values=[
                "GESTOS",
                "MANUAL"
            ],
            variable=self.mode_var
        )

        self.mode_menu.pack(
            pady=10,
            padx=10,
            fill="x"
        )

    # ==================================
    # VIDEO
    # ==================================

    def update_video(
        self,
        pil_image
    ):

        self.current_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=(800, 600)
        )

        self.video_label.configure(
            image=self.current_image
        )

    # ==================================
    # ESTADO
    # ==================================

    def update_state(
        self,
        state
    ):

        self.lbl_base.configure(
            text=f"Base: {state.base}"
        )

        self.lbl_codo1.configure(
            text=f"Codo1: {state.codo1}"
        )

        self.lbl_codo2.configure(
            text=f"Codo2: {state.codo2}"
        )

        self.lbl_pinza.configure(
            text=f"Pinza: {state.pinza}"
        )

        self.lbl_servos.configure(
            text=(
                "Servos: ON"
                if state.servos_enabled
                else "Servos: OFF"
            )
        )

        self.lbl_comm.configure(
            text=(
                "Comunicacion: ON"
                if state.communication_enabled
                else "Comunicacion: OFF"
            )
        )

        self.lbl_sync.configure(
            text=(
                "HOME: SINCRONIZADO"
                if state.synced
                else "HOME: NO SINCRONIZADO"
            )
        )

        self.lbl_fps.configure(
            text=f"FPS: {state.fps:.1f}"
        )

    # ==================================
    # COM
    # ==================================

    def get_com_port(self):

        return (
            self.entry_com
            .get()
            .strip()
        )

    # ==================================
    # MODO
    # ==================================

    def get_mode(self):

        return self.mode_var.get()