import os
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
from subprocess import Popen, PIPE
from GenerateCSV.categorias import categorias
import random
import json

SETTINGS_FILE = "settings.json"

accent_color_list = ["#800f00", "#004080", "#80005e", "#800000"]
accent_color = random.choice(accent_color_list)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

# Function to run a shell command Function to run a shell command
def run_command(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error: Command '{command}' failed with return code {process.returncode}")
        if stdout:
            print("stdout:")
            print(stdout)
        if stderr:
            print("stderr:")
            print(stderr)

def show_custom_error(message):
    error_window = tk.Toplevel(root)
    error_window.configure(bg="#2b2b2b")
    error_window.title("Cadê?!")
    error_window.wm_iconbitmap('meulindo.ico')
    error_label = tk.Label(error_window, text=message, bg="#2b2b2b", fg="#ffffff")
    error_label.pack(padx=20, pady=10)
    ok_button = tk.Button(error_window, text="Desculpe meu senhor", command=error_window.destroy, bg=accent_color, fg="#ffffff")
    ok_button.pack(pady=10, padx=20)


def upscale(folder_path):
    if upscale:
        if not os.path.exists(folder_path + "/realesrgan/"):
            command = f"python Utils/upscale.py {folder_path}"
            run_command(command)

def convertToJPG(folder_path):
    png_folder = folder_path + "/realesrgan/"
    if not os.path.exists(png_folder + "jpgs"):
        command = f"python Utils/convertToJPG.py {png_folder}"  
        run_command(command)



def createCVS(folder_path, selected_category, platform, noPrompt, language):
    if noPrompt:
        if platform == "Adobe":
            command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/ \"{selected_category}\" -p a --no-prompt --language {language}" 
            run_command(command)
        elif platform == "Freepik":
            command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/jpgs/ \"{selected_category}\" -p f --no-prompt --language {language}"
            run_command(command)
    else:
        if platform == "Adobe":
            command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/ \"{selected_category}\" -p a --language {language}" 
            run_command(command)
        elif platform == "Freepik":
            command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/jpgs/ \"{selected_category}\" -p f --language {language}" 
            run_command(command)

def upload(folder_path, platform):
    if platform == "Adobe":
        command = f"python Utils/sendSFTP.py {folder_path}/realesrgan/ -p a" 
        run_command(command)
    
    elif platform == "Freepik":
        command = f"python Utils/sendSFTP.py {folder_path}/realesrgan/jpgs/ -p f" 
        run_command(command)
    
def process_workflow():

    selected_adobe = adobe_var.get() 
    selected_freepik = freepik_var.get()
    selected_upscale = upscale_var.get()
    selected_convertToJPG = convertToJPG_var.get()
    selected_createCSV = createCSV_var.get()
    selected_upload = upload_var.get()
    selected_NoPrompt = noPrompt_var.get()
    selected_language = language_var.get()
    folder_path = folder_var.get()
    selected_category = category_var.get()

    settings = {
        "folder_path": folder_path,
        "selected_category": selected_category,
        "selected_adobe": selected_adobe,
        "selected_freepik": selected_freepik,
        "selected_upscale": selected_upscale,
        "selected_convertToJPG": selected_convertToJPG,
        "selected_createCSV": selected_createCSV,
        "selected_upload": selected_upload,
        "selected_NoPrompt": selected_NoPrompt,
        "selected_language": selected_language,
    } 
    save_settings(settings)

    if not folder_path:
        show_custom_error("A gente precisa de uma pasta bebê.")
        return
    
    if selected_category == "Categoria":
        show_custom_error("A gente precisa de uma categoria bebê.")
        return
    
    if selected_adobe:
        if selected_upscale:
            upscale(folder_path)
        if selected_createCSV:
            createCVS(folder_path, selected_category, "Adobe", selected_NoPrompt, selected_language)        
        if selected_upload:
            upload(folder_path, "Adobe")

    if selected_freepik:
        if selected_upscale:
            upscale(folder_path)
        if selected_convertToJPG:
            convertToJPG(folder_path)
        if selected_createCSV:
           createCVS(folder_path, selected_category, "Freepik", selected_NoPrompt, "en")
        if selected_upload:
            upload(folder_path, "Freepik")
    

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        root.configure(bg="#2b2b2b")
        

def runQC():
    folder_path = folder_var.get()
    if not folder_path:
        show_custom_error("A gente precisa de uma pasta bebê.")
        return
    command = f"python Utils/qc.py {folder_path}"  # Enclose folder path in quotes
    run_command(command)

# Main window
root = tk.Tk()
root.title("Autostock Utils")
root.geometry("300x900")
root.configure(bg="#2b2b2b")
root.wm_title("Autostock Utils")
root.wm_iconbitmap('meulindo.ico')

bold_font = Font(family="Arial", size=12, weight="bold")
small_font = Font(family="Arial", size=9)

settings = load_settings()

# Folder selection
folder_var = tk.StringVar(value=settings.get("folder_path", ""))
folder_label = tk.Label(root,text="Deixa eu fazer procê ❤️", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
folder_label.pack(pady=5, padx=20)

folder_entry = tk.Entry(root, textvariable=folder_var, width=16, bg="#4d4d4d", fg="#ffffff", font=("Arial", 20))  # Adjust background and foreground colors
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="🔎", command=select_folder, bg=accent_color, fg="#ffffff", font=("Arial", 20))
folder_button.pack(pady=20)

# Category selection
category_var = tk.StringVar(value=settings.get("selected_category", "Categoria"))

category_menu = tk.Menu(root, bg="#4d4d4d", fg="#ffffff")  # Configure the background and foreground colors for the dropdown menu
root.config(menu=category_menu)

category_optionmenu = tk.OptionMenu(root, category_var, *categorias.values())
category_optionmenu["menu"].config(bg="#4d4d4d", fg="#ffffff")  # Configure the background and foreground colors for the dropdown menu
category_optionmenu.config(bg="#4d4d4d", fg="#ffffff")  # Adjust background and foreground colors
category_optionmenu.pack(pady=25)

category_optionmenu.config(highlightthickness=1, highlightbackground=accent_color) 

# Button to run QC separately
qc_button = tk.Button(root, text="🔬 QC", command=runQC, bg=accent_color, width=12, height=2, fg="#ffffff")
qc_button.pack(pady=5)

process_labels = tk.Label(root,text="Quais processos?", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
process_labels.pack(pady=5, padx=20)

upscale_var = tk.BooleanVar(value=settings.get("selected_upscale", True))
upscale_checkbox = tk.Checkbutton(root, text="Upscale", variable=upscale_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
upscale_checkbox.pack(pady=5)

convertToJPG_var = tk.BooleanVar(value=settings.get("selected_convertToJPG", True))
convertToJPG_checkbox = tk.Checkbutton(root, text="Convert to JPG", variable=convertToJPG_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
convertToJPG_checkbox.pack(pady=5)

createCSV_var = tk.BooleanVar(value=settings.get("selected_createCSV", True))
createCSV_checkbox = tk.Checkbutton(root, text="Generate CSV's", variable=createCSV_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
createCSV_checkbox.pack(pady=5)

upload_var = tk.BooleanVar(value=settings.get("selected_upload", False))
upload_checkbox = tk.Checkbutton(root, text="Upload Files", variable=upload_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
upload_checkbox.pack(pady=5)

noPrompt_var = tk.BooleanVar(value=settings.get("selected_NoPrompt", False))
noPrompt_checkbox = tk.Checkbutton(root, text="Generate CSV's without prompt", variable=noPrompt_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
noPrompt_checkbox.pack(pady=5)

platform_labels = tk.Label(root,text="Qual idioma pra adobe?", bg="#2b2b2b", fg="#ffffff", font=small_font, height=1)
platform_labels.pack(pady=5, padx=20)

language_var = tk.StringVar(value=settings.get("selected_language", "en"))
language_menu = tk.OptionMenu(root, language_var, "pt", "en")
language_menu.config(bg="#4d4d4d", fg="#ffffff")  # Adjust background and foreground colors
language_menu.pack(pady=5)
language_menu.config(highlightthickness=1, highlightbackground=accent_color) 

platform_labels = tk.Label(root,text="Quais plataformas?", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
platform_labels.pack(pady=5, padx=20)

adobe_var = tk.BooleanVar(value=settings.get("selected_adobe", True))
adobe_checkbox = tk.Checkbutton(root, text="Adobe", variable=adobe_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
adobe_checkbox.pack(pady=5)

freepik_var = tk.BooleanVar(value=settings.get("selected_freepik", True))
freepik_checkbox = tk.Checkbutton(root, text="Freepik", variable=freepik_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff")
freepik_checkbox.pack(pady=5)

# Process button
process_button = tk.Button(root, text="🚀", command=process_workflow, bg=accent_color, fg="#ffffff", width=15, height=3, font=("Arial", 20))
process_button.pack(pady=50)

root.mainloop()