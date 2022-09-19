# Spotify - Tidal Converter

A command line script that converts spotify playlists to tidal ones, made using [Spotipy](https://spotipy.readthedocs.io/en/master/#) and [Tidalapi](https://tidalapi.netlify.app/index.html) for fun, before finding out that [Tune my Music](https://www.tunemymusic.com/it/?tidal=true#step1) already does that 😒.

## Usage

### Install dependencies

```
pip install spotipy
pip install tidalapi
pip install python-dotenv
```

### Define env variables

Create a new app on Spotify's developers dashboard, then create a file named `.env` containing the following parameters:

```bash
SPOTIPY_CLIENT_ID = your-client-id
SPOTIPY_CLIENT_SECRET = your-client-secret
SPOTIPY_REDIRECT_URI = your-redirect-uri
SPOTIPY_CLIENT_SCOPE = user-library-read
```

### Run the script

Run by using the following command

```python3
python3 main.py [spotify-playlist-id] [tidal-playlist]
```

Where:

- The Spotify's playlist id consists of the id that composes the playlist URI
- The Tidal's one consists of the name that the newly created playlist will have

## Notes

Since Tidal does not allow searching songs by their ISRC, some songs might be converted incorrectly. However, if no song is found on tidal the title will be skipped and printed on the command line in order to let you know which songs have not been synchronized.
