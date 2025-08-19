# PyP-Boy 3000: A Raspberry Pi Pip-Boy Replica

This project is a faithful, open-source replica of the Pip-Boy 3000 from the Fallout series, designed to run on a Raspberry Pi. Built with Python and Pygame, it provides an extensible framework for a functional, real-world Pip-Boy interface. It goes beyond a simple display, incorporating real-world data like maps, an interactive AI assistant, and direct hardware control over the Raspberry Pi's GPIO pins.

![Pip-Boy Screenshot](https://raw.githubusercontent.com/nfgOdin/pypboy3000/main/screenshots/pypboy-splash.png)

## Features

*   **Authentic Interface:** A retro-futuristic display with scanlines and a boot-up sequence, just like in the game.
*   **Modular System:** Easily extensible with modules for STATS, ITEMS, and DATA.
*   **Live World Map:** Fetches and displays real-time map data from OpenStreetMap for your current location or a configured focus point.
*   **Interactive GPIO Control Panel:** A dedicated module to view the status of all 40 Raspberry Pi GPIO pins, set them as INPUT/OUTPUT, and even control PWM devices with a real-time slider.
*   **V.I.N.C.E. AI Assistant:** An integrated, offline AI powered by a local Large Language Model (LLM) that you can interact with.
*   **Hardware Integration:** Responds to physical buttons and rotary encoders connected to GPIO pins for a true hardware experience.
*   **Highly Customizable:** Easily change the screen color, player name, level, keybindings, and more through a central `config.py` file.
*   **Sound & Radio:** Features classic Pip-Boy sound effects and a functional radio module.

## Requirements

### Hardware
*   **Raspberry Pi:** Recommended: Pi 4 or 5 for better performance.
*   **Display:** A display connected to the Pi. Touchscreen is supported for navigation.
*   **(Optional)** Physical buttons, rotary encoders, and LEDs for a more immersive build.

### Software
*   Python 3.x
*   Pygame and other core libraries.
*   Optional libraries for full functionality (GPIO, AI).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nfgOdin/pypboy3000.git
    cd pypboy3000
    ```

2.  **Install core dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install: `pygame`, `requests`, `xmltodict`, `numpy`, and `confuse`.

3.  **Install GPIO Libraries (for Raspberry Pi):**
    For the GPIO module to function, you'll need `gpiozero` and its dependencies.
    ```bash
    sudo apt-get update && sudo apt-get install -y libgpiod2
    pip install gpiozero lgpio
    ```

4.  **Install AI Library (Optional):**
    To enable the V.I.N.C.E. AI assistant, you need to install `llama-cpp-python`. This may require build tools. For GPU acceleration (recommended), you may need to set environment variables.
    ```bash
    # Example for NVIDIA GPUs. Adjust for your hardware.
    CMAKE_ARGS="-DLLAMA_CUBLAS=ON" pip install llama-cpp-python

    # For CPU-only, you can omit the CMAKE_ARGS
    # pip install llama-cpp-python
    ```

5.  **Download the AI Model:**
    *   The AI module is configured to use `Phi-3-mini-4k-instruct-q4.gguf`.
    *   Download the model from a source like Hugging Face.
    *   Create a `models` directory in the project root.
    *   Place the downloaded `.gguf` file inside the `models` directory.

## Configuration

The main configuration file is `pypboy/config.py`. Open this file to customize your Pip-Boy experience:

*   `WIDTH`, `HEIGHT`: Set the native resolution for the Pip-Boy display.
*   `TINTCOLOUR`: Change the classic green to amber, blue, or white.
*   `PLAYERNAME`, `PLAYERLEVEL`: Customize the player stats.
*   `MAP_FOCUS`: Set the default latitude and longitude for the map module.
*   `ACTIONS`: Map keyboard keys to in-game actions.
*   `GPIO_ACTIONS`: Map physical GPIO pins (using BCM numbering) to in-game actions like navigating menus.

## Running the Application

To start the Pip-Boy, run `main.py` from the root directory:
```bash
python main.py
```

### Command-line Options

*   **Cached Map:** To speed up the boot sequence by using a previously downloaded map, use the `-c` or `--cached-map` flag:
    ```bash
    python main.py -c
    ```

## Modules Overview

*   **HOME:** The main boot-up screen and status overview.
*   **STATS:** Displays player status, including HP, AP, and RAD levels, as well as SPECIAL, Skills, and Perks.
*   **ITEMS:** Shows inventory categories like Weapons, Armor, Aid, etc.
*   **DATA:** Contains submodules for the World Map, Local Map, and Quests.
*   **AI:** The V.I.N.C.E. (Vault-tec Integrated Neural-net Companion Entity) module, allowing you to chat with a local AI.
*   **GPIO:** An advanced control panel for interacting with the Raspberry Pi's hardware pins in real-time.

## Contributing

Contributions are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
