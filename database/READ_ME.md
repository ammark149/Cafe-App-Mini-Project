## Start Centos VM

Boot up for centos vm instance.

## Centos VM Directory

Make a directory called mini_project on the vm (/home/centos/mini_project)

In this directory you need to have two files:

- docker-compose.yml
- .env file

## Docker file

```
# version: "3.8"

services:
  db:
    image: docker.io/postgres:latest
    container_name: my-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
   
    volumes:
      - postgres_data:/var/lib/postgresql

  adminer:
    image: docker.io/adminer
    container_name: adminer
    restart: always
    ports:
      - 8080:8080

volumes:
  postgres_data:
```

## .env file

```
POSTGRES_HOST=<YOUR_CENTOS_VM_IP_HERE>
DB_PORT=5432
POSTGRES_USER=<SET_YOUR_POSTGRES_USERNAME_HERE>
POSTGRES_DB=mini_project_db
POSTGRES_PASSWORD=<SET_YOUR_POSTGRES_PASSWORD_HERE>
```

**Note** if your chosen password is/has numbers, they need to be wrapped in quotation marks. eg. POSTGRES_PASSWORD="123"

## .env file (Local Computer)

The details inside of this .env file are the same as the above remote .env file **apart from** the additional variables <mark>REMOTE_HOST</mark> and <mark>REMOTE_USER</mark>. This file should be in your database directory on your local computer (./Blasted-Turtles-Mini-Project/database/.env). <mark>DO NOT UPLOAD YOUR .env FILE!</mark>

```
REMOTE_HOST=miniproject-server
REMOTE_USER=centos
POSTGRES_HOST=<YOUR_CENTOS_VM_IP_HERE>
DB_PORT=5432
POSTGRES_USER=<YOUR_POSTGRES_USERNAME_HERE>
POSTGRES_DB=mini_project_db
POSTGRES_PASSWORD=<YOUR_POSTGRES_PASSWORD_HERE>
```
## Setup SSH key (Local Computer)

Now on your local computer that you use to ssh into your vm instance. We need an ssh key that does not require a passphrase. If you run this and it already exists **do not** overwrite it.

We are creating an ssh key specifically for our project so it should not mess with your other ssh keys.

Run this:

**Bash:**

```
ssh-keygen -t ed25519 -f ~/.ssh/mini_project_key -C "mini-project-script"
```

**Powershell:**

```
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\mini-project_key -C "mini-project-script"
```

When asked, just press enter (twice). First is to confirm the location of the key and the second is the passphrase. We just press enter to keep it blank.

Now we want to copy this key over to our server environment

**Bash:**

```
ssh-copy-id -i ~/.ssh/mini_project_key.pub centos@<YOUR_CENTOS_VM_IP_HERE>
```

**Powershell:**

```
Get-Content "$env:USERPROFILE\.ssh\mini_project_key.pub" | ssh centos@<YOUR_CENTOS_VM_IP_HERE> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

We now want edit the config file in the .ssh directory, on Windows that's:

C:\Users\Username\\.ssh\config

Inside the config file add this block:

```
Host miniproject-server
    HostName <YOUR_CENTOS_VM_IP_HERE>
    User centos
    IdentityFile ~/.ssh/mini_project_key
    IdentitiesOnly yes
```

SSH into your remote server instance to see if it worked. Use:

```
ssh miniproject-server
```

If that worked... Yay! You're all setup! You can now run* setup.py to automatically setup your database!

*Make sure you have the additional python packages outlined in requirements.txt installed.
