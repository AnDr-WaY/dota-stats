# **Dota-stats**

Dota-stats is a parser that gets statistics of dota 2 accaunt from [dotabuff](https://www.dotabuff.com/). It was created to get information of your opponents quickly on drafts stage of the game
### Preview
![preview](https://github.com/user-attachments/assets/cd50ac35-bb8f-48e7-8240-ab56d5f23f35)
## **Installation**

To install dota-stats, follow these steps:

1. Clone the repository: **`git clone https://github.com/AnDr-WaY/dota-stats.git`**
2. Navigate to the project directory: **`cd dota-stats`**
3. Install dependencies: **`pip install -r requirements.txt`**
4. Run the project: **`python main.py`**

## **Contributing**

If you'd like to contribute to dota-stats, here are some guidelines:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes.
4. Write tests to cover your changes.
5. Run the tests to ensure they pass.
6. Commit your changes.
7. Push your changes to your forked repository.
8. Submit a pull request.

## **License**

Dota-stats is released under the MIT License. See the **[LICENSE](https://github.com/AnDr-WaY/dota-stats/blob/main/LICENSE)** file for details.

## Configuration System

The application now saves user settings in a configuration file located in the appropriate directory based on the operating system:

- Windows: `%APPDATA%\DotaStats\config.json`
- macOS: `~/Library/Application Support/DotaStats/config.json`
- Linux/Unix: `~/.config/DotaStats/config.json`

### Currently Saved Settings

The following settings are currently saved in the configuration:

- **Theme Mode**: Light, Dark, or System
- **Color Scheme**: The color theme used by the application
- **Opacity**: Window opacity setting

### Extending the Configuration System

The configuration system is designed to be easily extendable for future settings. To add new settings:

1. Add your new setting to the `default_config` dict in `utils/config_manager.py` if it's a new section
2. Use `config_manager.set_setting("section", "key", value)` to save settings
3. Use `config_manager.get_setting("section", "key", default_value)` to retrieve settings

Example:

```python
# Save a setting
self.config_manager.set_setting("notifications", "enabled", True)

# Get a setting with a default fallback
enabled = self.config_manager.get_setting("notifications", "enabled", False)
```