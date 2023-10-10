# google_map_dist_matrix

## Docker
Build the docker image:
```sh
docker build -t google_mat_dist_api .
```

Run like this:
```sh
docker run --env-file .env -v ./ODs_SP_Survey.csv:/csv.csv -t google_mat_dist_api --csv /csv.csv
```

The `.env` contains a line like this:
```txt
GOOGLE_MAPS_API_KEY=xxxx-xxxxxxxxxxxxxxx
```

## Poetry
```sh
pip install poetry
poetry install
poetry shell
./main.py --apikey xxx-xxxxxxxxxxxxx --csv ./ODs_SP_Survey.csv
```
