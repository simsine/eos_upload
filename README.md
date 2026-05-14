# Setup and installation

## uv package manager

To run this project you need to have the uv package manager for python installed
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

# Running the program

After you have confirmed your installation of uv works you can run the following command to start the app. 
uv will automatically handle the installation of the required project dependencies and run the program.

```bash
uv run -- streamlit run --server.runOnSave=true --server.showEmailPrompt=false
```

There are also provided shell scripts in the form of `run.ps1` for Windows and `run.sh` which contain the same command as the one above.
These scripts can potentially be used as entrypoints for desktop-shortcuts, background process schedulers such as systemd or similar use cases for easy access to starting the application.

# Documentation

For documentation on the used libraries see the following:

- [ITkdb Docs](https://itkdb.docs.cern.ch/latest/) for docs on the ITkdb python wrapper
- [ITkpd Docs](https://uuapp.plus4u.net/uu-bookkit-maing01/41f76117152c4c6e947f498339998055/book/page?code=home) for docs on the application model of the ITkpd system
- [Streamlit Docs](https://docs.streamlit.io/) for docs on the Streamlit UI framework
- [uv Docs](https://docs.astral.sh/uv/) for docs on managing dependencies
