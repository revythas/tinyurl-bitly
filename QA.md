### Description
In this task we build a microservice called `shorty`, 
which supports two URL shortening providers: [bit.ly](https://dev.bitly.com/) and [tinyurl.com](https://gist.github.com/MikeRogers0/2907534).
The service exposes a single endpoint: `POST /shortlinks`. The endpoint should receive
JSON with the following schema:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The URL to shorten                 |
| provider | string | N        | The provider to use for shortening |

The response should be a `Shortlink` resource containing:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The original URL                   |
| link     | string | Y        | The shortened link                 |

For example:
```json
{
    "url": "https://example.com",
    "link": "https://bit.ly/8h1bka"
}
```
We have a fallback mechanism that means that if the first provider is fallen we try to short the link with the second provider. 
Also we assume that if the JSON doesn't clarify the provider we make tinyurl as the default. 
The endpoint returns a JSON response with a sensible HTTP status in case of errors or failures.


### How to Review

Firstly you can review the code and feel free to make any comments. 

1. Clone  the repo on your local and use **shortlink** branch
2. cd software-engineer-task
3. Install dependencies on a clean virtual environment : 
    - sudo apt-get install virtualenv -y
    - virtualenv -p python3 venv 
    - source venv/bin/activate
    - pip3 install -r requirements.txt
4. Run the tests as : pytest
You expected to see 3 passed. 

Now you have to test also manually the functionality. You have to run the API:  python3 run.py
Open a new terminal and cURL the API:


Use **tinyurl** as the default provider
1. ```curl -X POST "http://localhost:5000/shortlinks" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"url\":\"http://google.com/123/sssdsf\"}"```

Check **bitly** provider
2.```curl -X POST "http://localhost:5000/shortlinks" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"url\":\"http://google.com/123/sssdsf\",\"provider\":\"bitly\"}"```

Check **UNKONWN** provider
3. ```curl -X POST "http://localhost:5000/shortlinks" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"url\":\"http://google.com/123/sssdsf\",\"provider\":\"XYZ\"}"```

Check **tinyurl** provider
4. ```curl -X POST "http://localhost:5000/shortlinks" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"url\":\"http://google.com/123/sssdsf\",\"provider\":\"tinyurl\"}"```

Now you have to **check the fallback strategy**.
You have to edit `shortly/bitly.py` file and replace token with : 
```token = 'XYZ'```

Save the file and now the API should be restarted. cURL the API with bitly provider and check the response JSON. Should be tinyurl provider (because token isn't valid anymore)
```curl -X POST "http://localhost:5000/shortlinks" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"url\":\"http://google.com/123/sssdsf\",\"provider\":\"bitly\"}"```




### Sensitive data
**For your convenience, I give you my bitly token. This is a private repo so I suppose that there is no leak.**

### Further imporvments
We could use also FastAPI for performance reasons, you could check my GitHub profile here :arrow_right: https://github.com/revythas/FastAPI_EuroConvension

Also, we could dockerize the application or we could add some ansible tiers to automate the whole process. 

Finally, we could use the circuit breaker pattern to handle those failures and make a robust application. We could use pybreaker as a python module or Istio if we have a Kubernetes cluster up and running. 
