import tkinter as tk
from api_call import optimize_code
from matplotlib.offsetbox import TextArea
from scipy import optimize 


def callOptimise(code_snippet):
    if(len(code_snippet) == 0):
        
    response = optimize_code(code_snippet)
    codeTextArea1.insert("1.0",response['code'])
    print(response)

root = tk.Tk()
root.geometry("700x700")

labelMain = tk.Label(root , text = "Welcome to the AI code optimiser")
labelMain.pack()

codeTextArea = tk.Text(root)
codeTextArea.pack()

buttonOptimise = tk.Button(root,text = "Optimise code" , command = lambda:callOptimise(codeTextArea.get("1.0", tk.END)))
buttonOptimise.pack()

codeTextArea1 = tk.Text(root)
codeTextArea1.pack()



root.mainloop()