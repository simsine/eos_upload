import argparse
import itkdb
from pathlib import Path
from textual.app import App, ComposeResult
from textual_filedrop import FileDrop

class EOSUploadApp(App):
    client = None
    code = None
    description = None
    upload_type = None

    DEFAULT_CSS = """
        Screen {
            align: center middle;
        }
    """

    def __init__(self, client, code, description, upload_type="component"):
        self.client = client
        self.code = code
        self.description = description
        self.upload_type = upload_type
        super().__init__()

    def compose(self) -> ComposeResult:
        yield FileDrop(id="filedrop")

    def on_mount(self):
        #self.query_one("filedrop")
        self.query_one("#filedrop").focus()

    def on_file_drop_dropped(self, event: FileDrop.Dropped) -> None:
        path = event.path
        filepaths = event.filepaths
        filenames = event.filenames
        filesobj = event.filesobj

        response = self.upload_file(filenames[0], filepaths[0])
        if response:
            self.query_one("#filedrop").styles.border = ("round", "green")
            self.query_one("#filedrop").txt = (f"Uploaded '[yellow]{filenames[0]}[/yellow]' to [yellow]{self.code}[/yellow]\n\nURL")
            #self.query_one("#filedrop").txt = (f"Uploaded '[yellow]{filenames[0]}[/yellow]' to [yellow]{self.code}[/yellow]\n\nURL: {response['url']}\n\nComponent: https://itkpd-test.unicorncollege.cz/componentView?code={self.code}")
        else:
            self.query_one("#filedrop").styles.border = ("round", "red")
            self.query_one("#filedrop").txt = f"Failed to upload"

    def upload_file(self, filename, filepath):
        data = {
            "title": filename,
            "description": self.description,
            "url": Path(filepath),
            "type": "file"
        }
        if self.upload_type == "component":
            data["component"] = self.code
        elif self.upload_type == "testrun":
            data["testRun"] = self.code

        try:
            with Path(filepath).open("rb") as fpointer:
                files = {"data": itkdb.utils.get_file_components(
                    {"data": fpointer})}
                if self.upload_type == "component":
                    response = self.client.post("createComponentAttachment",
                                                data=data, files=files)
                elif self.upload_type == "testrun":
                    response = self.client.post("createTestRunAttachment",
                                                data=data, files=files)
        except itkdb.exceptions.ResponseException:
            return False

        return response


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--code",
        "-c",
        dest="code",
        type=str,
        required=True,
        help="Component serial number or test run number"
    )
    parser.add_argument(
        "--description",
        "-d",
        dest="description",
        type=str,
        required=True,
        help="File description"
    )
    parser.add_argument(
        "--upload-type",
        "-t",
        dest="upload_type",
        type=str.lower,
        default="component",
        choices=["component", "testrun"],
        help="upload component or test run attachment?"
    )

    args = parser.parse_args(inargs)

    client = itkdb.Client(use_eos=True)
    app = EOSUploadApp(client, args.code, args.description,
                       args.upload_type)
    app.run()

    #debugging
    #import pprint
    #component = client.get("getComponent", json={"component": args.component})["attachments"]
    #pprint.pprint(component)


if __name__ == "__main__":
    main()