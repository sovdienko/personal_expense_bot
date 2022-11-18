Telegram for personal expenses collecting 

Complete ENV variables (above) into Dockerfile.
`TELEGRAM_API_TOKEN` — Bot API token 

`TELEGRAM_ACCESS_ID` — ID of Telegram account working available

 
SQLite db in `expense.db`.

```
docker build -t soexpense ./
docker run -d --name so soexpense
```

Enter into running container:

```
docker exec -ti so bash
```

Enter into SQL shell inside of Docker container:

```
docker exec -ti so bash
sqlite3 /home/expenses.db
```
DOCKER HUB

1) Login to the docker.
```
docker login -u serhiiovd
```
2) Tag your image build

my image name here is : soexpense and by default it has tag : latest
and my username is : serhiiovd as registered with docker cloud, and I created a public repository named : repo

so my personal repository becomes now : serhiiovd/repo and I want to push my image with tag : soexpense

I tagged as below :
```
docker tag soexpense:latest serhiiovd/repo:soexpense
```
3) Pushed the image to my personal docker repository as below
```
docker push serhiiovd/repo:soexpense
```
And it successfully pushed to my personal docker repo.
```

