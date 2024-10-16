<p align="center">
  <img src="https://duckduckgo.com/i/d11af3c7.png" alt="Keybase Banner">
</p>

# What's Keybase?

Keybase is a key directory that maps social media identities to encryption keys in a publicly auditable manner. Additionally it offers an end-to-end encrypted chat and cloud storage system, called Keybase Chat and the Keybase Filesystem respectively. Files placed in the public portion of the filesystem are served from a public endpoint, as well as locally from a filesystem mounted by the Keybase client. 
# K-MS4 (Keybase Username Availability Checker)

K-MS4 is a Python script that checks the availability of usernames from a provided file or generates random words to verify their availability. The script checks usernames asynchronously using the [Keybase](https://keybase.io/) API and can notify you through Discord using a webhook.

## Features

- Check the availability of usernames from a file.
- Generate random words and check their availability.
- Asynchronous checking for improved performance.
- Removes duplicates and invalid usernames (spaces, symbols, etc.).
- Saves available usernames to a file (`availables.txt`).
- Discord webhook integration to send notifications with the result file.
- Configuration stored in `config.json` for reuse.

## Requirements

- Python 3.x
- The following Python modules:
  - `os`
  - `re`
  - `json`
  - `asyncio`
  - `aiohttp`
  - `tkinter`
  - `requests`
  - `random`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MrShadowDev/K-MS4.git
    cd K-MS4
    ```

2. Install the required dependencies by running setup.bat

## Usage

1. **Run the script**:
    ```bash
    python main.py
    ```

2. **Choose an option**:
    - **Option 1**: Check usernames from a `.txt` file. The script will prompt you to select a file using a file dialog.
    - **Option 2**: Generate random words. Specify how many random words to generate.

3. **Discord webhook** (optional):
   - Enter a Discord webhook URL when prompted, or store it in the `config.json` file for future use. If provided, the script will send the list of available usernames to Discord.

4. **Check the results**:
    - The available usernames will be saved in a file called `availables.txt`.
    - If a Discord webhook is set up, the file will also be sent to the specified Discord channel.

## Configuration

The `config.json` file stores your configuration (Discord webhook URL and the number of workers). When running the script, it will automatically load the saved values from the file. You can edit the file manually or through the script.

### Example `config.json`

```json
{
    "webhook_url": "YOUR_WEBHOOK_HERE",
    "max_workers": 100,
    "default_word_count": 3927
}
```

### Contributing
Feel free to open issues or submit pull requests if you'd like to improve the script or add new features!
