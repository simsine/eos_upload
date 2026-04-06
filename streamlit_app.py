import streamlit as st
import itkdb as itk
import os

### Authentication
ITKDB_ACCESS_CODE1 = os.environ.get("ITKDB_ACCESS_CODE1")
ITKDB_ACCESS_CODE2 = os.environ.get("ITKDB_ACCESS_CODE2")

if ITKDB_ACCESS_CODE1 is None or ITKDB_ACCESS_CODE2 is None:
	raise EnvironmentError("ITKDB_ACCESS_CODE1 or ITKDB_ACCESS_CODE2 is missing from your global environment, did you forget to set them?")

itkdb_user = itk.core.User(
	access_code1 = ITKDB_ACCESS_CODE1,
	access_code2 = ITKDB_ACCESS_CODE2,
)

itkdb_user.authenticate()
itk_client = itk.Client(use_eos = True, user = itkdb_user)

if not itk_client.user.is_authenticated:
	raise Exception("Authentication error, are your codes correct?")

# Save client to state to fetch in pages
st.session_state["itk_client"] = itk_client

### Authentication

### Init Streamlit page structure
# Create Streamlit navigation object
PAGES_DIR = "atlantest/streamlit_pages/"

LOGO_URL_LARGE = "atlantest/static/logoipsum.svg"
LOGO_URL_SMALL = "atlantest/static/logoipsum.svg"

st.logo(
	LOGO_URL_LARGE,
	size = "large",
	link = None,
	icon_image=LOGO_URL_SMALL,
)

streamlit_pages = st.navigation({
	"Tests" : [
		st.Page(PAGES_DIR + "eos_uploader.py", title="EOS Uploader", icon=":material/add_photo_alternate:"),
		st.Page(PAGES_DIR + "visual_inspection.py", title="Visual Inspection", icon=":material/visibility:"),
		st.Page(PAGES_DIR + "metrology.py", title="Metrology", icon=":material/straighten:"),
		st.Page(PAGES_DIR + "dc_test.py", title = "DC Test", icon=":material/bolt:"),
		],
	"Components" : [
		st.Page(PAGES_DIR + "all_components.py", title="All", icon=":material/list:"),
		st.Page(PAGES_DIR + "ready_to_ship.py", title="Ready to Ship", icon=":material/package_2:"),
	]
})

auth_user: dict = itk_client.get("getUser", json={"userIdentity": itk_client.user.identity}) # type: ignore
institution_code = None

if "institutions" in auth_user:
	institution_code = auth_user["institutions"][0].get("code")

with st.sidebar:
	st.write(f":material/account_circle: {itk_client.user.name}")
	if institution_code:
		st.write(f":material/account_balance: {institution_code}")
	else:
		st.write("Institution: Unknown")

# Render the currently selected page
streamlit_pages.run()
### Init streamlit page sctructure
