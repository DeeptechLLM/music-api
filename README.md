### Prepare virtualenv
`python -m venv music`

#### Linux:
`source music/bin/activate`

#### Windows: 
`music/Scripts/activate`

### Install requirements
`pip install -r requirements.txt`

### Execute project
```
nohup gunicorn -b localhost:5002 app:app > music.log &
```

### Sample Request
Method: `POST`
URL: `https://recommendation.mmusic.mn/api/v1/recommendations`
```
{
    "artist_ids": [1, 2],
    "song_ids": [1, 2],
    "emotions": ["", ""],
    "genres": ["", ""],
    "limit": 10
}
```

### Proxy config
path: `/etc/caddy/Caddyfile`
```
recommendation.mmusic.mn {
        reverse_proxy localhost:5002	

}

```
