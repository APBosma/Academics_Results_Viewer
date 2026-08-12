import customtkinter as ctk

class CollapsibleFrame(ctk.CTkFrame):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.is_expanded = False
        
        # Tog butt
        self.toggle_button = ctk.CTkButton(
            self, 
            text=f"▶ {title}", 
            anchor="w", 
            fg_color="transparent", 
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.toggle
        )
        self.toggle_button.pack(fill="x")
        
        # frame thingy (im confused)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        
    def toggle(self):
        # Swap the triangle icon and show/hide stuff
        if self.is_expanded:
            self.content_frame.pack_forget()
            self.toggle_button.configure(text=self.toggle_button.cget("text").replace("▼", "▶"))
            self.is_expanded = False
        else:
            self.content_frame.pack(fill="x", padx=15, pady=5)
            self.toggle_button.configure(text=self.toggle_button.cget("text").replace("▶", "▼"))
            self.is_expanded = True

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UIL Results Viewer")
        self.geometry("900x600")
        
        # columnz
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # bar o n left
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        sidebar_title = ctk.CTkLabel(self.sidebar, text="Filters", font=("Arial", 20, "bold"))
        sidebar_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        # 1. Conf filt
        self.conf_frame = CollapsibleFrame(self.sidebar, "Conference")
        self.conf_frame.pack(fill="x", padx=10, pady=5)
        for i in range(1, 7):
            # Using buttons assuming you only view one at a time
            btn = ctk.CTkRadioButton(self.conf_frame.content_frame, text=f"{i}A")
            btn.pack(anchor="w", pady=4)
            
        # 2. Competitions Filt
        self.comp_frame = CollapsibleFrame(self.sidebar, "Competitions")
        self.comp_frame.pack(fill="x", padx=10, pady=5)
        for comp in ["Number Sense", "Calculator Applications", "Mathematics", "Science"]:
            btn = ctk.CTkRadioButton(self.comp_frame.content_frame, text=comp)
            btn.pack(anchor="w", pady=4)
            
        # 3. District Filter (With Checkboxes for Multiple Selection)
        self.dist_frame = CollapsibleFrame(self.sidebar, "District")
        self.dist_frame.pack(fill="x", padx=10, pady=5)
        for dist in ["District 1", "District 2", "District 3", "District 4"]:
            # multiple select
            chk = ctk.CTkCheckBox(self.dist_frame.content_frame, text=dist)
            chk.pack(anchor="w", pady=4)
            
        # other stuff
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        welcome_lbl = ctk.CTkLabel(self.main_area, text="UIL Results Table Here", font=("Arial", 24))
        welcome_lbl.pack(expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()