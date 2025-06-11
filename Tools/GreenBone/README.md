# Setting up GreenBone for penetration testing

The process is actually really simple.

We will use docker to set it up.

## Step 1: Getting docker_compose.yml

GreenBone provides an official docker_compose.yml with all the neccesary configurations in it already so we don't need to do it by hand

**To get the compose file just copy and paste the command below in your terminal**

**Note: create a directory and cd into it, so its more organized**

```
curl -f -O -L https://greenbone.github.io/docs/latest/_static/docker-compose.yml
```

## Step 2: Pulling images

After getting the compose file you need to pull the images that are neccesary for GreenBone to work.

Luckily you don't have to do it by hand.

```
docker compose -f docker_compose.yml pull
```

This command will pull all the images listed in the docker_compose.yml file

## Step 3: Change Admin Password

You would want to change the admin password, you don't want everyone to be able to login with default credentials and see your targets

```
docker compose -f docker-compose.yml \
    exec -u gvmd gvmd gvmd --user=admin --new-password='<password>'
```

## Step 4: Starting GreenBone

Now all is left to do is start the containers.

```
docker compose -f docker-compose.yml up -d
```

**Note: wait for about 10 minutes for all the containers to start**

To see real time logs:

```
docker compose -f docker-compose.yml logs -f
```

## Step 5: Login

Browse to localhost:9392 and login

![Alt text](login.png)

## Final Step: Enjoy:D

![Alt text](dashboard.png)
