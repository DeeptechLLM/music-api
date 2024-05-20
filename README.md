Project execution
------
------

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

```
normal: 
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

Genre mapping
------
------
| id | mmusic_genres_en | mmusic_genres_mn | dt_model_genres |
| ---|:----------------|:----------------|----------------:|
| 1 | instrumentals | Хөгжмийн бүтээлүүд |  |
| 2 | mongol_country | Монгол Кантри |  |
| 3 | movie_songs | Киноны дуу |  |
| 4 | zohioliin | Нийтийн |  |
| 5 | ardiin | Ардын |  |
| 6 | children | Хүүхдийн |  |
| 7 | long | Уртын дуу |  |
| 8 | pop | Поп | pop |
|  |  |  | electropop |
|  |  |  | poprock |
|  |  |  | popfolk |
|  |  |  | easylistening |
|  |  |  | contemporary |
|  |  |  | instrumentalpop |
|  |  |  | lounge |
|  |  |  | dance |
|  |  |  | eurodance |
|  |  |  | disco |
| 9 | rock_alternative | Рок, Алтернатив | alternative |
|  |  |  | alternativerock |
|  |  |  | bluesrock |
|  |  |  | grunge |
|  |  |  | hardrock |
|  |  |  | punkrock |
|  |  |  | rock |
|  |  |  | rocknroll |
|  |  |  | postrock |
|  |  |  | progressive |
|  |  |  | psychedelic |
|  |  |  | indie |
|  |  |  | instrumentalrock |
|  |  |  | classicrock |
| 10 | hiphop_rap | Хип хоп, реп | hiphop |
|  |  |  | rap |
|  |  |  | triphop |
| 11 | jazz | Жазз | acidjazz |
|  |  |  | jazz |
|  |  |  | jazzfunk |
|  |  |  | jazzfusion |
|  |  |  | swing |
|  |  |  | improvisation |
|  |  |  | fusion |
| 12 | electronics | Электроник (Диско, техно...) | ambient |
|  |  |  | breakbeat |
|  |  |  | chillout |
|  |  |  | club |
|  |  |  | darkambient |
|  |  |  | deephouse |
|  |  |  | drumandbass |
|  |  |  | dubstep |
|  |  |  | edm |
|  |  |  | electronic |
|  |  |  | electronica |
|  |  |  | house |
|  |  |  | idm |
|  |  |  | minimal |
|  |  |  | synthpop |
|  |  |  | techno |
|  |  |  | trance |
|  |  |  | downtempo |
|  |  |  | atmospheric |
|  |  |  | experimental |
|  |  |  | darkwave |
| 13 | classic | Сонгодог | classical |
| 14 | r_and_b | R&B | blues |
|  |  |  | funk |
|  |  |  | rnb |
|  |  |  | soul |
|  |  |  | dub |
|  |  |  | groove |
|  |  |  | sk |
| 15 | reggae | Регги | reggae |
| 16 | pop_opera | Поп опера | chanson |
| 17 | ethnic | Этник | african |
|  |  |  | celtic |
|  |  |  | ethnicrock |
|  |  |  | ethno |
|  |  |  | latin |
|  |  |  | medieval |
|  |  |  | oriental |
|  |  |  | world |
|  |  |  | worldfusion |
|  |  |  | tribal |
|  |  |  | newage |
|  |  |  | bossanova |
| 18 | metal | Метал | hard |
|  |  |  | heavymetal |
|  |  |  | metal |
|  |  |  | gothic |
|  |  |  | industrial |
| 19 | country | Кантри | country |
|  |  |  | folk |
|  |  |  | singersongwriter |
| 20 | trap | Трап | trap |
| 21 | orchestral | Оркестр | choir |
|  |  |  | orchestral |
|  |  |  | soundtracks |
|  |  |  | symphonic |



