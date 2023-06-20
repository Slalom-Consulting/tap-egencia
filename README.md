# tap-egencia
Singer tap for the Egencia REST API

`tap-egencia` is a Singer tap for egencia.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.


## Configuration

### Accepted Config Options

List of tap-egencia config values

```
  start_date: ${START_DATE}
    required: false
  end_date: ${END_DATE}
    required: false
  egencia_base_url: ${EGENCIA_BASE_URL}
    required: true
  client_id: ${EGENCIA_CLIENT_ID}
    required: true
  client_secret: ${EGENCIA_SECRET_ID}
    required: true

```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

Egencia API requies OAuth authentication. client_Id & client_secret passed as configs are required for authentication. 

## Usage

You can easily run `tap-egencia` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-egencia --version
tap-egencia --help
tap-egencia --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-egencia` CLI interface directly using `poetry run`:

```bash
poetry run tap-egencia --help
```


Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-egencia
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-egencia --version
# OR run a test `elt` pipeline:
meltano run tap-egencia target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

## Dev Notes

Singer taps require schema declaration for extraction. If fields pulled from the API are not listed in the schema documentation the extraction will throw an error. However default behavior for listed schema values are set to `require=false`. Expected output values have been added to the transaction stream schema which do not show up in the current extraction job but however may down the line. consider this when building future tap streams. 

Schema creation can be be found under `./Schema` using the `CustomObject` util to structure the schema to the Singer data structure requirement.