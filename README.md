# Spotify playlist audiobook

A small python script saving your position in a playlist and restoring it when a specific song in that playlist is started.

## Dependencies
- spotipy

## Usage

### Spotipy setup and Spotify Credentials
See [spotipy documentation](https://spotipy.readthedocs.io/) for details.
In short, create a spotify application at https://developer.spotify.com/ and set environment variables `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI`.

### Configure playlists

Configure playlists the program should listen to in a `config.json` with the ID of the playlist and the trigger song. You can get the IDs from their link by the sharing the playlist and song. For example, in the link `https://open.spotify.com/playlist/3IRnNJYzErcSzEXxu2Y1NX?si=aaaaaaaaaaaaaaaa` the ID is `3IRnNJYzErcSzEXxu2Y1NX`. Similarly, for a song `https://open.spotify.com/intl-de/track/7HVdUaGEPc5tH2BjriNvGa?si=aaaaaaaaaaaaaaaa` the ID is `7HVdUaGEPc5tH2BjriNvGa`. The `config.json` should look like this:

```json
[
    {
        "id": "3IRnNJYzErcSzEXxu2Y1NX",
        "trigger": "7HVdUaGEPc5tH2BjriNvGa"
    },
    ...
]
```

Run the program with `main.py [your-username]`. `spotipy` caches the token.