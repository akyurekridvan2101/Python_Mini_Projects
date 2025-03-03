#!/usr/bin/env python3

import os
import subprocess
import stat
import argparse

def get_translations(lang):
    translations = {
        "welcome": {"en": "\n🔧 Welcome to the Linux Package Installer!", "tr": "\n🔧 Linux Paket Yükleyiciye Hoş Geldiniz!"},
        "file_path_prompt": {"en": "\nEnter the full path of the file to install: ", "tr": "\nKurulacak dosyanın tam yolunu girin: "},
        "no_exec_permission": {"en": "\n⚠ The file does not have execution permission. Grant permission? (Y/N): ", "tr": "\n⚠ Dosyanın çalıştırma izni yok. İzin vermek ister misiniz? (E/H): "},
        "exec_permission_granted": {"en": "✅ Execution permission granted.", "tr": "✅ Çalıştırma izni verildi."},
        "exec_permission_denied": {"en": "❌ Operation canceled.", "tr": "❌ İşlem iptal edildi."},
        "file_not_found": {"en": "\n❌ File not found!", "tr": "\n❌ Dosya bulunamadı!"},
        "unsupported_file": {"en": "\n⚠ Unsupported file type!", "tr": "\n⚠ Desteklenmeyen dosya türü!"},
    }
    return {key: translations[key].get(lang, translations[key]["en"]) for key in translations}

def detect_linux_distro():
    """Detects the Linux distribution."""
    try:
        result = subprocess.run(["lsb_release", "-is"], capture_output=True, text=True)
        return result.stdout.strip().lower()
    except FileNotFoundError:
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.split("=")[1].strip().strip('"').lower()
        except FileNotFoundError:
            return "unknown"

def check_and_fix_permissions(file_path, lang):
    """Checks and fixes file execution permissions."""
    translations = get_translations(lang)
    
    if not os.access(file_path, os.X_OK):
        choice = input(translations["no_exec_permission"]).strip().lower()
        if choice in ["y", "e"]:
            os.chmod(file_path, os.stat(file_path).st_mode | stat.S_IXUSR)
            print(translations["exec_permission_granted"])
            return True
        else:
            print(translations["exec_permission_denied"])
            return False
    return True

def install_package(file_path, lang):
    """Installs the package based on the file extension."""
    distro = detect_linux_distro()
    
    if file_path.endswith(".deb"):
        subprocess.run(["sudo", "dpkg", "-i", file_path])
        subprocess.run(["sudo", "apt-get", "-f", "install", "-y"])
    elif file_path.endswith(".rpm"):
        if distro in ["fedora", "centos", "rhel"]:
            subprocess.run(["sudo", "dnf", "install", "-y", file_path])
        else:
            subprocess.run(["sudo", "rpm", "-i", file_path])
    elif file_path.endswith(".sh") or file_path.endswith(".run"):
        subprocess.run(["bash", file_path])
    elif file_path.endswith(".AppImage"):
        os.chmod(file_path, os.stat(file_path).st_mode | stat.S_IXUSR)
        subprocess.run([file_path])
    elif file_path.endswith(".tar.gz") or file_path.endswith(".tar.xz"):
        extract_dir = os.path.splitext(os.path.splitext(file_path)[0])[0]
        os.makedirs(extract_dir, exist_ok=True)
        subprocess.run(["tar", "-xvf", file_path, "-C", extract_dir])
        os.chdir(extract_dir)
        if os.path.exists("./configure"):
            subprocess.run(["./configure"])
            subprocess.run(["make"])
            subprocess.run(["sudo", "make", "install"])
    elif file_path.endswith(".pkg.tar.zst"):
        subprocess.run(["sudo", "pacman", "-U", file_path])
    elif file_path.endswith(".flatpak"):
        subprocess.run(["flatpak", "install", "-y", file_path])
    elif file_path.endswith(".snap"):
        subprocess.run(["snap", "install", file_path])
    elif file_path.endswith(".bin"):
        subprocess.run(["chmod", "+x", file_path])
        subprocess.run([file_path])
    elif file_path.endswith(".py"):
        subprocess.run(["python3", file_path])
    else:
        print(get_translations(lang)["unsupported_file"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🔧 Linux Package Installer: Easily install various package types on Linux."
    )
    parser.add_argument("-force", action="store_true", help="Force default language to Turkish")
    parser.add_argument("--lang", choices=["en", "tr"], default="en", help="Select language (default: English)")
    
    args = parser.parse_args()

    if args.force:
        args.lang = "tr"

    translations = get_translations(args.lang)
    print(translations["welcome"])
    file_path = input(translations["file_path_prompt"]).strip().strip("'").strip('"')
    
    if os.path.exists(file_path):
        if check_and_fix_permissions(file_path, args.lang):
            install_package(file_path, args.lang)
    else:
        print(translations["file_not_found"])

