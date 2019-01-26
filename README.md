# Wordcount sample

A very simple word count function written in python. This demonstrates how an OpenFaaS function can be composed of mulitple files.

In python, using local imports allows the code to work in both your local environment (e.g. it will properly lint in VSCode) and in your function.

## Project initialization

```sh

$ conda env create -f environment.yml
$ conda source activate faaswordcount

$ kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
namespace "openfaas" created
namespace "openfaas-fn" created

$ helm repo add openfaas https://openfaas.github.io/faas-netes/ && helm repo update
"openfaas" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "incubator" chart repository
...Successfully got an update from the "contiamo" chart repository
...Successfully got an update from the "openfaas" chart repository
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈ Happy Helming!⎈

$ helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=false \
    --set faasnetesd.imagePullPolicy='IfNotPresent' \
    --set functionNamespace=openfaas-fn

$ faas-cli template store pull python3-flask
Fetch templates from repository: https://github.com/openfaas-incubator/python-flask-template at master
2019/01/19 10:55:34 Attempting to expand templates from https://github.com/openfaas-incubator/python-flask-template
2019/01/19 10:55:35 Fetched 3 template(s) : [python27-flask python3-flask python3-flask-armhf] from https://github.com/openfaas-incubator/python-flask-template
```

## Deploying

```sh
$ faas-cli build
$ faas-cli deploy
Deploying: wordcount.

Deployed. 202 Accepted.
URL: http://127.0.0.1:31112/function/wordcount
```

## Testing the function

```sh
$ curl -X POST http://127.0.0.1:31112/function/wordcount \
  -d 'This is some example text that we want to see a frequency response for.  It has text like apple, apples, apple tree, etc'
{"example": 1, "text": 2, "want": 1, "see": 1, "frequency": 1, "response": 1, "for": 1, "apple": 3, "tree": 1, "etc": 1}
```

## Function logs

```sh
$ kubectl -n openfaas-fn logs -l "faas_function=wordcount"
```
