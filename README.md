# GameChanger Python Client

An easy-to-use, community-driven Python SDK for interacting with the [GameChanger](https://gc.com) APIs.

Automate the collection of player stats, videos, standings, and more from GameChanger. This library is designed for developers, analysts, and enthusiasts who want to programmatically access GameChanger data.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Overview](#api-overview)
- [Authentication](#authentication)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Simple, Pythonic interface to GameChanger APIs
- Retrieve teams, players, stats, videos, and more
- Customizable HTTP session with retries and error handling
- Extensible endpoint structure
- Actively tested with `pytest`

---

## Installation

The package is available on PyPI:

```bash
pip install gamechanger-client
```

Or, to install the latest development version:

```bash
git clone https://github.com/TheAlanNix/gamechanger-client.git
cd gamechanger-client
pip install .
```

---

## Quick Start

```python
from gamechanger_client import GameChangerClient

# You can pass your token directly, or set the GC_TOKEN environment variable
client = GameChangerClient(token="YOUR_GC_TOKEN")

# Get your teams
teams = client.me.teams()
print(teams)

# Get players for a team
team_id = teams['teams'][0]['id']
players = client.teams.players(team_id)
print(players)
```

---

## API Overview

The main entrypoint is `GameChangerClient`, which provides access to all endpoints:

```python
from gamechanger_client import GameChangerClient
client = GameChangerClient(token="YOUR_GC_TOKEN")

# Endpoints
client.teams         # Team-related data
client.players       # Player-related data
client.me            # Your user/account info
client.organizations # Organization data
client.clips         # Video clips
client.public        # Public data
client.search        # Search endpoints
```

Each endpoint exposes methods for interacting with the corresponding API routes. See the [examples](#examples) below.

---

## Authentication

Currently, you must provide a valid GameChanger token. You can either:

- Pass it directly to the client:
  ```python
  client = GameChangerClient(token="YOUR_GC_TOKEN")
  ```
- Or set it as an environment variable:
  ```bash
  export GC_TOKEN=your_token_here
  ```

> **Note:** If you need help obtaining your token, please open an issue or discussion on GitHub.

---

## Examples

### Get Team Stats
```python
team_id = "your_team_id"
stats = client.teams.season_stats(team_id)
print(stats)
```

### Get Player Family Relationships
```python
player_id = "your_player_id"
relationships = client.players.family_relationships(player_id)
print(relationships)
```

### Download Clips
```python
clips = client.clips.clips(team_id)
for clip in clips['clips']:
    print(clip['title'], clip['id'])
```

---

## Contributing

Contributions are **very welcome**! If you have ideas, bugfixes, or want to add new endpoints, please:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes and add tests
4. Run the test suite with `pytest`
5. Submit a pull request with a clear description

If you have questions or want to discuss ideas, open an issue or start a discussion.

**Ways to contribute:**
- Add new endpoints or features
- Improve documentation
- Report or fix bugs
- Help with authentication improvements
- Write or improve tests

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Links & Acknowledgements
- [GameChanger](https://gc.com)
- [PyPI: gamechanger-client](https://pypi.org/project/gamechanger-client/)
- [GitHub Issues](https://github.com/TheAlanNix/gamechanger-client/issues)

---

*This project is not affiliated with or endorsed by GameChanger. It is a community effort to make their data more accessible for developers.*
