# Setup and installation

## uv package manager

To run this project you need to have the uv package manage for python installed
Follow the instructions in [the uv docs](https://docs.astral.sh/uv/getting-started/installation/)

Confirm that uv is installed in your shell by typing uv help, this should print the help information from uv

## Provide ITk access codes

The program needs access to authorize against the EOS and ITkpd systems. Before you run the program you need to provide your Plus4U access codes in the form of environment variables.

### On Windows

Use the following shell commands to set each of the access codes.

```cmd
setx ITKDB_ACCESS_CODE1 '<code>'
```

```cmd
setx ITKDB_ACCESS_CODE2 '<code>'
```

### On Linux with bash shell

Add the following two lines to your `~/.bash_profile` file to set the variables globally in your shell.

```bash
export ITKDB_ACCESS_CODE1=<code>
export ITKDB_ACCESS_CODE2=<code>
```

### On MacOs

Add the following lines to your `/etc/launchd.conf` file.

```zsh
setenv ITKDB_ACCESS_CODE1 <code>
setenv ITKDB_ACCESS_CODE2 <code>
```

## Initializing the project

After you have confirmed your installation of uv works you can run the following command to start the app. 
uv will automatically handle the setup and installation of the required project dependencies and run the program.

```bash
uv run -- streamlit run --server.runOnSave=true --server.showEmailPrompt=false
```

