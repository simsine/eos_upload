import streamlit as st
import itkdb as itk

MAX_FILE_UPLOAD_SIZE_MB = 1000
INPUT_KEY_ITKDB_ACCESS_CODE1 = "input_itk_key_1"
INPUT_KEY_ITKDB_ACCESS_CODE2 = "input_itk_key_2"

st.write("# Please authenticate")

st.text_input("Access code 1", key = INPUT_KEY_ITKDB_ACCESS_CODE1)
st.text_input("Access code 2", key = INPUT_KEY_ITKDB_ACCESS_CODE2)

itkdb_user = itk.core.User(
	access_code1 = st.session_state[INPUT_KEY_ITKDB_ACCESS_CODE1],
	access_code2 = st.session_state[INPUT_KEY_ITKDB_ACCESS_CODE2],
)

if st.session_state[INPUT_KEY_ITKDB_ACCESS_CODE1] and st.session_state[INPUT_KEY_ITKDB_ACCESS_CODE2]:
	itkdb_user.authenticate()
	itk_client = itk.Client(use_eos=True, user=itkdb_user)

	if itk_client.user.is_authenticated:
		st.write("Authenticated as:")
		st.write(itk_client.get("getUser", json = {"userIdentity": itkdb_user.identity}))

	# We prompt the user to upload test images
	uploaded_test_images = st.file_uploader(
		label = "Please upload a file",
		type = ["jpg", "jpeg", "png", "gif"],
		max_upload_size = MAX_FILE_UPLOAD_SIZE_MB,
		accept_multiple_files = True,
	)

	# We print each uploaded image to the page
	if len(uploaded_test_images) >= 1:
		for image in uploaded_test_images:
			st.image(image.getvalue())
