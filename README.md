# Setup and installation

## uv package manager

To run this project you need to have the uv package manage for python installed
Follow the instructions in [the uv docs](https://docs.astral.sh/uv/getting-started/installation/)

Confirm that uv is installed in your shell by typing uv help, this should print the help information from uv

## Initializing the project

After you have confirmed your installation of uv works you can run the following command to start the app
uv will automatically handle the setup and installation of the required project dependencies

```
uv run -- streamlit run --server.runOnSave=true --server.showEmailPrompt=false
```
