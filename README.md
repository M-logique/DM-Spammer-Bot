
# DM Spammer Discord Bot 

![Build Status](https://img.shields.io/github/workflow/status/M-logique/DM-Spammer-Bot/CI) 
![GitHub release (latest by date)](https://img.shields.io/github/v/release/M-logique/DM-Spammer-Bot)
![License](https://img.shields.io/github/license/M-logique/DM-Spammer-Bot)
![Stars](https://img.shields.io/github/stars/M-logique/DM-Spammer-Bot)
![Forks](https://img.shields.io/github/forks/M-logique/DM-Spammer-Bot)
![Languages](https://img.shields.io/github/languages/top/M-logique/DM-Spammer-Bot)

---

A Discord bot for sending a large number of direct messages to someone and trolling your friends. 

This project is written in Python and Golang (for speed and efficiency). 🚀

If you want to run it yourself, you can follow the steps below: 👇

## Installation and Setup 🛠️

Start by cloning the project repository: 📂
```bash
git clone https://github.com/M-logique/DM-Spammer-Bot
```
(Or download the ZIP file from GitHub. 📦)

### 1. Open the Project 📁

Navigate to the project directory: 🏃‍♂️
```bash
cd DM-Spammer-Bot
```

### 2. Set Up the Environment Variables and Tokens 🔑

Fill in the `.env` file with the required environment variables and paste your tokens into the `tokens.txt` file. 📝

### Using Docker 🐳:

Install Docker by following the instructions in the [official Docker documentation](https://docs.docker.com/engine/install/).

### 3. Run the Project with Docker Compose 🚀

To start the project using Docker Compose, run:
```bash
docker compose up -d
```

### Without Docker ❌🐳:

### 3. Install Python Dependencies 📦

- It's recommended to use a virtual environment (`venv`) to manage dependencies.

**Setting up a virtual environment:**
```bash
python3 -m venv .venv
```

Activate the virtual environment:

For Linux/macOS: 🐧🍏
```bash
source .venv/bin/activate
```
or
```bash
.venv/bin/activate
```

For Windows: 🪟
```bash
.\.venv\Scripts\activate
```

Install the required Python packages using `pip`: 🧰

```bash
python3 -m pip install -r requirements.txt
```

### 4. Run the Main File 🎬

Run the application by executing the main Python script:
```bash
python3 main.py
```

## Optional: Building Go Files 🛠️

Since the bot uses shared files that are already compiled, some users may prefer not to use these precompiled files for personal or security reasons. 🔒

- If you wish, you can build the `spammer.so` file yourself using the following steps:

### 1. Install Golang 🦫

Install Go (Golang) by following the instructions in the [official Go documentation](https://go.dev/doc/install).

### 2. Install GCC 🛠️

Ensure that `gcc` (GNU Compiler Collection) is installed on your system. Follow the instructions below based on your operating system:

- **For Debian/Ubuntu-based systems:** 🐧
  ```bash
  sudo apt-get install gcc
  ```

- **For Red Hat/CentOS-based systems:** 🐧
  ```bash
  sudo yum install gcc
  ```

- **For macOS:** 🍏
  ```bash
  xcode-select --install
  ```

- **For Windows:** 🪟
  You can install `gcc` on Windows by installing [MinGW-w64](http://mingw-w64.org/), which provides a GCC toolchain for Windows.

  1. Visit the [MinGW-w64 downloads page](https://sourceforge.net/projects/mingw-w64/files/).
  2. Download the appropriate installer (e.g., `mingw-w64-install.exe`).
  3. Run the installer and select the architecture (32-bit or 64-bit) and version of GCC you want to install.
  4. Follow the installation instructions, and add the `bin` directory of MinGW to your system's `PATH` environment variable. For example, `C:\Program Files\mingw-w64\bin`.

  To verify that `gcc` is installed correctly, open a Command Prompt and run:
  ```bash
  gcc --version
  ```

### 3. Navigate to the Go Source Directory 📂

Move to the Go source directory within the project:

```bash
cd DM-Spammer-Bot/go_spammer
```

### 4. Build the Go Shared Library 🔧

Compile the Go code into a shared object file (`spammer.so`). This file will be placed in the `shared` directory of the project. Run the following command:

```bash
go build -o ../shared/spammer.so -buildmode=c-shared main.go
```

### Additional Notes 📝

- Make sure your Go environment is properly set up. You can verify this by running `go version` to check if Go is correctly installed and available in your system's `PATH`.

- The `-buildmode=c-shared` flag is used to generate a shared object file that can be loaded and used by other programming languages such as Python. 🐍

- After building, you can verify that the new `spammer.so` file is created in the `shared` directory. The bot will now use this freshly built file instead of the precompiled one. ✔️

---

### Disclaimer ⚠️

This bot is intended for educational and testing purposes only. Misusing this tool to spam or harass others is against Discord's Terms of Service and could result in your account being banned. 🚫 Use it responsibly! 🙏

