This is a Telegram Bot written in Python-Pyrogram for Managing Membership of Users in Paid-Leech-Group or Dumps.

---

<b>Fill this Values in [config.env](config.env)</b>
- `BOT_TOKEN`: The Telegram Bot Token that you got from [@BotFather](https://t.me/BotFather). `Str`
- `TELEGRAM_API`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from <https://my.telegram.org>. `Int`
- `TELEGRAM_HASH`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from <https://my.telegram.org>. `Str`
- `OWNER_ID`: Only this ID can add, remove, modify Users Membership. You can get this from [Rose Bot](https://t.me/missrose_bot), by using /info Cmd. `Int`
- `DATABASE_URL`: Enter your MongoDB URL. Generate a Database and Get the Url. <https://www.mongodb.com> `Str`

---
### All Commands/Set from [@Botfather](https://t.me/botfather):
```
start - Start the Bot/all info about Bot
my_subscriptions - Get Info about Your Purchases
add - Add User/Providing him Membership (Owner Only)
remove - Remove User/Revoking his Membership (Owner Only)
info - Check Users Info (Owner Only)
all_users - List all Users in Database (Owner Only)
```


---
### For farther assistance visit my support group: [**@JetMirror**](https://telegram.me/JetMirror).
---

## Deploy using CLI on Heroku

- Deployment instructions uploaded [**HERE**](https://gist.github.com/Hrishi2861/e0305da57d772eee7a82ee69a08b78cc)
- Carefully copy-paste every CMD one by one. If you miss maybe your BOT will not run.

---
## Deploy on VPS
---
## Prerequisites

### 1. Installing requirements

- Clone this repo:

```
git clone https://github.com/Hrishi2861/Membership-Management-Bot/ && cd Membership-Management-Bot
```

- For Debian based distros

```
sudo apt install python3 python3-pip
```

Install Docker by following the [Official docker docs](https://docs.docker.com/engine/install/#server).
Or you can use the convenience script: `curl -fsSL https://get.docker.com |  bash`


- For Arch and it's derivatives:

```
sudo pacman -S docker python
```

------

### 2. Build And Run the Docker Image

Make sure you still mount the app folder and installed the docker from official documentation.

- There are two methods to build and run the docker:
  1. Using official docker commands.
  2. Using docker-compose.

------

#### Build And Run The Docker Image Using Official Docker Commands

- Start Docker daemon (SKIP if already running, mostly you don't need to do this):

```
sudo dockerd
```

- Build Docker image:

```
sudo docker build . -t dbmanage
```

- Run the image:

```
sudo docker run -p 80:80 -p 8080:8080 dbmanage
```

- To stop the running image:

```
sudo docker ps
```

```
sudo docker stop id
```

----

#### Build And Run The Docker Image Using docker-compose

**NOTE**: If you want to use ports other than 80 and 8080 change it in [docker-compose.yml](docker-compose.yml).

- Install docker compose

```
sudo apt install docker-compose
```

- Build and run Docker image:

```
sudo docker-compose up --build
```

- To stop the running image:

```
sudo docker-compose stop
```

- To run the image:

```
sudo docker-compose start
```

- To get latest log from already running image (after mounting the folder):

```
sudo docker-compose up
```
