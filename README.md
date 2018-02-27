## How do I run this thing?

`docker build -t flask-sample-one:latest .`

`docker run --rm -v $PWD:/home/ds -p 5000:5000 -it flask-sample-one`
