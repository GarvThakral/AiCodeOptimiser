from email.policy import default
from logging import PlaceHolder
import tkinter as tk
from turtle import width
from api_call import optimize_code
from pygments.lexers import guess_lexer    
from tkinter import ttk
from tkcode import CodeEditor
from tkcode import codebox
import sqlite3
con = sqlite3.connect("tutorial.db")

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
        self.root.geometry("1400x900")
        self.language = "Python"
        self.root.columnconfigure(0, weight=1)  
        self.root.columnconfigure(1, weight=1)  
        self.root.columnconfigure(2, weight=1)  
        self.root.rowconfigure(10, weight=1)
        
        
        self.labelMain = tk.Label(self.root, text="Welcome to the AI Code Optimiser", font=("Arial", 16, "bold"))
        self.labelMain.grid(row=0, column=1, pady=10, sticky="n")  

        self.languageLabel = tk.Label(self.root, text="Language: ", font=("Arial", 16, "bold"))
        self.languageLabel.grid(row=0, column=2, pady=10, sticky="n")


        self.code_editor = CodeEditor(self.root, language=self.language, width = 50)
        self.code_editor.grid(row=1, column=0, pady=10, sticky="nsew")
        self.code_editor.bind("<<Modified>>",self.detectLanguage)
        self.code_editor.bind("<KeyPress>",self.detectLanguage)
        self.code_editor.bind("<KeyRelease>",self.detectLanguage)

        self.code_editor1 = CodeEditor(self.root, language=self.language, width = 50)
        self.code_editor1.grid(row=1, column=2, pady=10, sticky="nsew")

        self.buttonOptimise = tk.Button(self.root, text="Optimise Code", command=lambda: self.callOptimise(self.code_editor.get("1.0", tk.END)))
        self.buttonOptimise.grid(row=2, column=1, pady=10)  

        self.optimisationLabel = ttk.Label(self.root, text="Optimisation parameter : ", font=("Arial", 16, "bold"))
        self.optimisationLabel.grid(row=3, column=1, pady=10, sticky="n")

        self.optimisationCombo = ttk.Combobox(self.root, font=("Arial", 16, "bold") , values = ["All","Speed" , "Memory" , "Readability"])
        self.optimisationCombo.grid(row=4, column=1, pady=10, sticky="n")  
        self.optimisationCombo.current(0)

        self.detectorLabel = tk.Label(self.root, text="", font=("Arial", 12))
        self.detectorLabel.grid(row=5, column=1, pady=10, sticky="n")  


        # self.aiTextLabel = tk.Label(self.root, text="")
        # self.aiTextLabel.grid(row=5, column=1, pady=10, rowspan=3)

    def detectLanguage(self, event):
        print('Triggered')
        code = self.code_editor.get("1.0", "end-1c")
        lexer = guess_lexer(code)
        detected_language = lexer.name

        mapped_language = LANGUAGE_MAP.get(detected_language, "text") 

        self.language = mapped_language
        self.languageLabel.config(text = "Language : " + detected_language)

        self.language = mapped_language
        self.language = mapped_language
 
        
    def callOptimise(self, code_snippet):
        if(len(code_snippet) == 1 or code_snippet == "The code cannot be empty"):
            # self.aiTextLabel.config(text="The code cannot be empty")
            return
        response = optimize_code(code_snippet,self.optimisationCombo.get())
        self.code_editor1.delete("1.0", tk.END)  # Clear previous content
        self.code_editor1.insert("1.0", response['code'])  # Insert new content

        # self.aiTextLabel.config(text=response['text'])
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AICodeOptimizer()
    app.run()
    app.detectLanguage()