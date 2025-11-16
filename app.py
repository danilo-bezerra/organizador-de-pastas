import tkinter as tk
from tkinter import filedialog, messagebox

from FolderOrganizer import FolderOrganizer
from utils import TARGET_FILES

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Organizador de Diretório")
        self.master.configure(padx=16, pady=16)

        self.dir_label = tk.Label(master, text="Diretório:")
        self.dir_label.grid(row=0, column=0, sticky=tk.W)

        self.dir_entry = tk.Entry(master, width=50)
        self.dir_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(master, text="Selecionar", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2)
        
        self.submit_button = tk.Button(master, text="Organizar", command=self.submit_form)
        self.submit_button.grid(row=1, columnspan=3)
        self.submit_button.configure(padx=10)
        
        self.log_label = tk.Label(master, text="Logs:")
        self.log_label.grid(row=2, column=0)
        

        self.log_text = tk.Text(master, height=10, width=60)
        self.log_text.grid(row=3, columnspan=3)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(tk.END, directory)
        
    def insert_log(self, log):
         self.log_text.insert(tk.END, f"{log} \n")
         self.log_text.see(tk.END)
         self.master.update_idletasks()

    def submit_form(self):
        directory = self.dir_entry.get()

        if not directory:
            self.log_text.insert(tk.END, "Por favor, selecione um diretório.\n")
            return

        try:
            organizer = FolderOrganizer(TARGET_FILES, directory, self.insert_log)
            organizer.run()
            self.log_text.insert(tk.END, "Ação concluída com sucesso!\n")
            messagebox.showinfo("Sucesso", "Ação concluída com sucesso!")
        except Exception as e:
            self.log_text.insert(tk.END, f"Erro: {str(e)}\n")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()