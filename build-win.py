from os import path, system, chdir, listdir
import sys
import subprocess

BASE_DIR = "./"
FRONTEND_DIR = "autonomus-app"
FRONTEND_GIT = "https://git.lais.huol.ufrn.br/ela/autonomus-app.git"
KEYBOARD_DIR = "back-end-teclado-interativo"
KEYBOARD_GIT = "https://git.lais.huol.ufrn.br/ela/back-end-teclado-interativo.git"


system("color")

def cprint(msg):
    YELLOW = "\033[33m"
    WHITE = "\033[0m"
    print(YELLOW + msg + WHITE)

def repo_exists(repo_dir, repo_git):
    exists = path.exists(repo_dir + "/.git")
    if exists:
        cprint("\n ## Atualizando repositorio " + repo_dir + ".\n")
        subprocess.call('', shell=True)
        chdir(repo_dir)
        system("git checkout dev")
        system("git pull")
        chdir("..")
    else:
        cprint("\n ## Repositorio " + repo_dir + " nao existe.\n ## Clonando o repositorio.\n")
        system("git clone " + repo_git)

def build_front():
    chdir(FRONTEND_DIR)
    cprint("\n ## Baixando dependencias de " + FRONTEND_DIR + "\n")
    system("npm install")
    cprint("\n ## Compilando " + FRONTEND_DIR + "\n")
    system("npm run build")
    system("npm run electron-build")
    #  system("npm run electron-pack")
    chdir("..")

def build_keyboard():
    chdir(KEYBOARD_DIR)
    if (not path.exists("venv")):
        system("virtualenv venv")
    VENV_DIR = "venv\\Scripts\\"
    CV2_DIR = "venv\\Lib\\site-packages\\cv2\\"
    OPENCV_FILE = ""
    cprint("\n ## Baixando dependencias de " + KEYBOARD_DIR + "\n")
    system("pip install pyinstaller")
    system(VENV_DIR + "pip install -r requirements.txt")
    cprint("\n ## Verificando versao do OpenCV e adicionando DLL ao instalador \n")
    for file in listdir(CV2_DIR):
        if file.endswith(".dll"):
            OPENCV_FILE = file
            system("copy /y " + CV2_DIR + OPENCV_FILE + ".")
    cprint("\n ## Compilando backend e modelo da piscada \n")
    system('pyinstaller --hidden-import=pyttsx3 -p venv\\lib\\site-packages --add-data src\\words_filtered.txt;. --add-data src\\big_text.txt;. --add-data src\\autocomplete\\models_compressed.pkl;autocomplete\\ --add-data "' + OPENCV_FILE + ';." --hidden-import=pyttsx3.drivers.sapi5 --hidden-import=pywin32 --hidden-import=pywin32-ctypes --hidden-import=pkg_resources.py2_warn src\\build.py')
    chdir("..")


if len(sys.argv) == 2:
    BASE_DIR = sys.argv[1]

chdir(BASE_DIR)
repo_exists(FRONTEND_DIR, FRONTEND_GIT)
repo_exists(KEYBOARD_DIR, KEYBOARD_GIT)
build_front()
build_keyboard()
