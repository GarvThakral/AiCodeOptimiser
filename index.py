import tkinter as tk
from tkinter import Menu, ttk, font
from tkcode import CodeEditor
import sqlite3
from pygments.lexers import guess_lexer
from api_call import optimize_code
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
LANGUAGE_MAP = {
    "Python": "python",
    "C++": "cpp",
    "JavaScript": "javascript",
    "HTML": "html",
    "CSS": "css",
    "Java": "java",
    "Ruby": "ruby",
    "Go": "go",
    "Rust": "rust",
    "PHP": "php",
    "SQL": "sql",
    "Markdown": "markdown",
    "Shell": "shell",
    "TypeScript": "typescript",
    "Scala": "scala",
    "Lua": "lua",
    "Swift": "swift",
    "Objective-C": "objective-c",
    "Kotlin": "kotlin",
    "Perl": "perl",
    "Dart": "dart",
    "R": "r",
    "Haskell": "haskell",
    "VHDL": "vhdl",
    "Pascal": "pascal",
    "Elixir": "elixir",
    "Julia": "julia",
    "ShellSession": "shell",
    "Plain Text": "text",
    "Assembly": "asm",
    "Objective-C++": "cpp",
    "TeX": "tex",
    "YAML": "yaml",
    "Tcl": "tcl",
}

class AICodeOptimizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Code Optimizer")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f2f5")
        
        self.colors = {
            "primary": "#3498db",
            "primary_dark": "#2980b9",
            "secondary": "#2ecc71",
            "secondary_dark": "#27ae60",
            "dark": "#34495e",
            "light": "#ecf0f1",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "bg": "#f0f2f5",
            "editor_bg": "#272822"
        }
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.colors["light"], foreground=self.colors["dark"], 
                             padding=[15, 5], font=('Arial', 11))
        self.style.map("TNotebook.Tab", background=[("selected", self.colors["primary"])], 
                       foreground=[("selected", self.colors["light"])])
        
        self.style.configure("TFrame", background=self.colors["bg"])
        
        self.style.configure("Primary.TButton", background=self.colors["primary"], foreground="white", 
                             font=('Arial', 11, 'bold'), padding=10)
        self.style.configure("Danger.TButton", background=self.colors["danger"], foreground="white", 
                             font=('Arial', 11), padding=5)
        self.style.configure("Secondary.TButton", background=self.colors["secondary"], foreground="white", 
                             font=('Arial', 11), padding=5)
        
        self.style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["dark"], 
                             font=('Arial', 11))
        self.style.configure("Header.TLabel", background=self.colors["bg"], foreground=self.colors["primary"], 
                             font=('Arial', 16, 'bold'))
        
        self.style.configure("TCombobox", background=self.colors["light"], 
                             fieldbackground=self.colors["light"], foreground=self.colors["dark"])
        
        self.con = sqlite3.connect("tutorial.db")
        self.cur = self.con.cursor()
        self.language = "Python"

        self.create_layout()
        
    def create_layout(self):

        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        
        menubar = tk.Menu(self.tabControl)
        menubar.configure(bg=self.colors["editor_bg"], fg=self.colors["editor_bg"])
        file = Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label ='File', menu = file) 
        file.add_command(label ='import file', command = self.handleFileUpload) 
        file.add_command(label ='save optimised', command = self.handleFileSave) 
        file.add_separator() 

        self.root.config(menu = menubar)

        self.tabControl.add(self.tab1, text='Optimize Code')
        self.tabControl.add(self.tab2, text='History')
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)
        
        for i in range(3):
            self.tab1.columnconfigure(i, weight=1)
        self.tab1.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(self.tab1)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        
        self.labelMain = ttk.Label(header_frame, text="AI Code Optimizer", style="Header.TLabel")
        self.labelMain.pack(side="left", padx=10)
        
        self.languageLabel = ttk.Label(header_frame, text="Language: Python", style="TLabel")
        self.languageLabel.pack(side="right", padx=10)

        editors_frame = ttk.Frame(self.tab1)
        editors_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        editors_frame.columnconfigure(0, weight=1)
        editors_frame.columnconfigure(2, weight=1)
        
        editors_frame.columnconfigure(0, weight=1)
        editors_frame.columnconfigure(2, weight=1)
        editors_frame.rowconfigure(0, weight=1)

        left_frame = ttk.Frame(editors_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        
        ttk.Label(left_frame, text="Original Code", style="TLabel").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.code_editor = CodeEditor(left_frame, language=self.language, width=50, height=30, 
                                      background=self.colors["editor_bg"], font=('Consolas', 11) )
        self.code_editor.grid(row=1, column=0, sticky="nsew")
        self.code_editor.bind("<<Modified>>", self.detectLanguage)
        self.code_editor.bind("<KeyPress>", self.detectLanguage)
        self.code_editor.bind("<KeyRelease>", self.detectLanguage)
        
        middle_frame = ttk.Frame(editors_frame)
        middle_frame.grid(row=0, column=1, sticky="ns", padx=10)
        
        ttk.Label(middle_frame, text="Optimization Target", style="TLabel").pack(pady=(20, 5))
        self.optimisationCombo = ttk.Combobox(middle_frame, values=["All", "Speed", "Memory", "Readability"], 
                                              width=15, state="readonly")
        self.optimisationCombo.pack(pady=5)
        self.optimisationCombo.current(0)
        
        self.buttonOptimise = ttk.Button(middle_frame, text="Optimize Code ➡", style="Primary.TButton", 
                                        command=lambda: self.callOptimise(self.code_editor.get("1.0", tk.END)))
        self.buttonOptimise.pack(pady=20)
        
        self.detectorLabel = ttk.Label(middle_frame, text="", style="TLabel")
        self.detectorLabel.pack(pady=10)
        
        right_frame = ttk.Frame(editors_frame)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
        
        ttk.Label(right_frame, text="Optimized Code", style="TLabel").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.code_editor1 = CodeEditor(right_frame, language=self.language, width=50, height=30, 
                                       background=self.colors["editor_bg"], font=('Consolas', 11))
        self.code_editor1.grid(row=1, column=0, sticky="nsew")
        
        status_bar = ttk.Frame(self.tab1)
        status_bar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        status_text = ttk.Label(status_bar, text="Ready", style="TLabel")
        status_text.pack(side="left")
        
        self.tab2.columnconfigure(0, weight=1)
        self.tab2.rowconfigure(0, weight=1)
        
        self.history_container = ttk.Frame(self.tab2)
        self.history_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
    def handleFileSave(self):
        if(len(self.code_editor1.get("1.0",tk.END)) == 1):
            self.detectorLabel.config(text="Cannot save empty file.")
        else:
            name=asksaveasfile(mode='w',defaultextension=".txt")
            text2save=str(self.code_editor1.get(0.0,tk.END))
            name.write(text2save)
            name.close


    def handleFileUpload(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.process_file()

    def process_file(self):
        try:
            print(self.file_path)
            with open(self.file_path, 'r') as file:
                file_contents = file.read()
                print(file_contents)
                self.code_editor.delete('1.0', tk.END)
                self.code_editor.insert(tk.END, file_contents)
        except Exception as e:
            print(str(e))

    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        
        if tab_text == "History":
            # Clear previous content
            for widget in self.history_container.winfo_children():
                widget.destroy()
            
            # Create scrollable frame for history items
            history_canvas = tk.Canvas(self.history_container, bg=self.colors["bg"])
            scrollbar = ttk.Scrollbar(self.history_container, orient="vertical", command=history_canvas.yview)
            scrollable_frame = ttk.Frame(history_canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
            )
            
            history_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            history_canvas.configure(yscrollcommand=scrollbar.set)
            
            history_canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.cur.execute("SELECT * FROM History")
            self.history = self.cur.fetchall()
            
            header_frame = ttk.Frame(scrollable_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 20))
            ttk.Label(header_frame, text="Code Optimization History", style="Header.TLabel").pack(side="left")
            
            if not self.history:
                ttk.Label(scrollable_frame, text="No history records found.", style="TLabel").pack(pady=20)
            else:
                # Create history items
                for index, item in enumerate(self.history):
                    history_item = ttk.Frame(scrollable_frame)
                    history_item.pack(fill="x", padx=10, pady=5)
                    
                    # Item number and code preview
                    preview_text = item[1].strip()[:40] + "..." if len(item[1]) > 40 else item[1].strip()
                    ttk.Label(history_item, text=f"{index+1}. {preview_text}", style="TLabel").pack(side="left", padx=5)
                    
                    # Buttons
                    buttons_frame = ttk.Frame(history_item)
                    buttons_frame.pack(side="right")
                    
                    ttk.Button(buttons_frame, text="Review", style="Secondary.TButton", 
                              command=lambda i=item: self.review_history_item(i)).pack(side="left", padx=5)
                    
                    ttk.Button(buttons_frame, text="Delete", style="Danger.TButton", 
                              command=lambda pk=item[0]: self.deleteQuery(pk)).pack(side="left", padx=5)
                    
                    # Separator
                    ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", padx=10, pady=5)
    
    def review_history_item(self, item):
        self.tabControl.select(0)
        
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", item[1])
        
        self.code_editor1.delete("1.0", tk.END)
        self.code_editor1.insert("1.0", item[2])
        
        self.detectorLabel.config(text="History item loaded")
        
    def deleteQuery(self, primaryKey):
        self.cur.execute(f"DELETE FROM History WHERE id = {primaryKey}")
        self.con.commit()
        
        # Refresh the history tab
        self.on_tab_changed(tk.Event())
        
    def detectLanguage(self, event):
        code = self.code_editor.get("1.0", "end-1c")
        if code.strip():
            try:
                lexer = guess_lexer(code)
                detected_language = lexer.name
                
                mapped_language = LANGUAGE_MAP.get(detected_language, "text")
                self.language = mapped_language
                self.languageLabel.config(text="Language: " + detected_language)
                self.code_editor.language = self.language
            except:
                pass
        
    def callOptimise(self, code_snippet):
        if not code_snippet.strip():
            self.detectorLabel.config(text="The code cannot be empty")
            return
            
        # Update status
        self.detectorLabel.config(text="Optimizing...")
        self.root.update()
        
        # Call the optimization function (unchanged)
        response = optimize_code(code_snippet, self.optimisationCombo.get())
        
        # Update the optimized code display
        self.code_editor1.delete("1.0", tk.END)
        self.code_editor1.insert("1.0", response['code'])
        
        # Save to history
        self.cur.execute(
            "INSERT INTO History (original, optimised, response) VALUES (?,?,?)",
            (self.code_editor.get("1.0", tk.END), response['code'], response['text'])
        )
        self.con.commit()
        
        # Update status
        self.detectorLabel.config(text="Optimization complete!")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AICodeOptimizer()
    app.run()