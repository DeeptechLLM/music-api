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
    "artists_ids": [1, 2],
    "songs_ids": [1, 2],
    "emotions_ids": [],
    "genres_ids": [],
    "limit": 10
}
```