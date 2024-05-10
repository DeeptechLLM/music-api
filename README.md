### Install requirements
`pip install -r requirements.txt`


### Prepare virtualenv
`python -m venv music`

#### Linux:
`source music/bin/activate`

#### Windows: 
`music/Scripts/activate`

### Sample Request
```
{
    "artist_ids": [1, 2],
    "song_ids": [1, 2],
    "emotion_ids": [],
    "genre_ids": [],
    "limit": 10
}
```