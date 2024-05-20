### Requirement
- python version: > 3.8
- pip 

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
normal: 
```
{
    "artist_ids": [],
    "song_ids": [1563],
    "emotions": [],
    "genres": [],
    "limit": 10,
    "type": "normal"
} 
zohioliin:
{
    "artist_ids": [],
    "song_ids": [5907],
    "emotions": [],
    "genres": [],
    "limit": 10,
    "type": "zohioliin"
} 
ardiin:
{
    "artist_ids": [],
    "song_ids": [1247],
    "emotions": [],
    "genres": [],
    "limit": 10,
    "type": "ardiin"
} 


```

### Proxy config

#### Install Caddy

Log into your instance of Ubuntu Server and add the necessary dependencies with:

`sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https -y`

Once that installation completes, add the official Caddy GPG key with:

`curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg`

Create the repository file with the command:

`curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list`

Update apt:

`sudo apt-get update`

Finally, install Caddy with the command:

`sudo apt-get install caddy -y`

Start and enable the Caddy service with:

`sudo systemctl enable --now caddy`


#### Config
path: `/etc/caddy/Caddyfile`
```
recommendation.mmusic.mn {
        reverse_proxy localhost:5002	

}

```
