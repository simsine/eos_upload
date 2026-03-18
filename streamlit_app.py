import streamlit as st
import itkdb as itk
import os

### Authentication
ITKDB_ACCESS_CODE1 = os.environ.get("ITKDB_ACCESS_CODE1")
ITKDB_ACCESS_CODE2 = os.environ.get("ITKDB_ACCESS_CODE2")

if ITKDB_ACCESS_CODE1 is None or ITKDB_ACCESS_CODE2 is None:
	raise EnvironmentError("ITKDB_ACCESS_CODE1 or ITKDB_ACCESS_CODE2 is missing, did you forget to set them?")

itkdb_user = itk.core.User(
	access_code1 = ITKDB_ACCESS_CODE1,
	access_code2 = ITKDB_ACCESS_CODE2,
)

itkdb_user.authenticate()
itk_client = itk.Client(use_eos=True, user=itkdb_user)

if not itk_client.user.is_authenticated:
	raise Exception("Authentication error, are your codes correct?")

# Save client to state to fetch in pages
st.session_state["itk_client"] = itk_client

### Authentication

### Init Streamlit page structure
PAGES_DIR = "atlantest/streamlit_pages/"
streamlit_pages = st.navigation([
	st.Page(PAGES_DIR + "index.py"),
	st.Page(PAGES_DIR + "eos_uploader.py"),
])
# Render the page navigation bar
streamlit_pages.run()
### Init streamlit page sctructure
