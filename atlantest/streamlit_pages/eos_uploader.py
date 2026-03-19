from enum import Enum
from io import BytesIO
from requests import Response
import streamlit as st
import itkdb as itk
import itkdb.utils as itk_utils

from atlantest.base_page import Base_Page

class UploadType(Enum):
	Component = "Component"
	Testrun = "Testrun"

class EOS_Uploader_Page(Base_Page):
	MAX_FILE_UPLOAD_SIZE_MB = 1000

	def main(self):
		st.write("# EOS Uploader")
		st.write(":red[This page is under construction.]")
		st.set_page_config(page_title="EOS Uploader", page_icon=":material/add_photo_alternate:")

		input_code = st.text_input(
			label = "Code",
			placeholder = "Component serial number or test run number"
		)

		input_description = st.text_input(
			label = "Description",
			placeholder = "File description"
		)

		input_upload_type = st.selectbox(
			label = "Upload type",
			options = (UploadType.Component.value, UploadType.Testrun.value)
		)

		if (not input_code or not input_description):
			return
		
		# We prompt the user to upload test images
		input_test_images = st.file_uploader(
			label = "Please upload a file",
			type = ["jpg", "jpeg", "png", "gif"],
			max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
			accept_multiple_files = True,
		)

		# We print each uploaded image to the page
		# if len(input_test_images) >= 1:
		# 	for image in input_test_images:
		# 		st.image(image.getvalue())

		if len(input_test_images) <= 0:
			return
	
		if not st.button("Upload files"):
			return

		for image in input_test_images:
			res = self.upload_file(image, image.name, image.file_id, input_code, input_description, input_upload_type)

			if not res:
				st.error(f"Error in uploading file: {image.name}")
				return

			st.success("Files uploaded successfully")

	def upload_file(
		self,
		file_data: BytesIO,
		file_name: str,
		file_id: str,
		code: str,
		description: str,
		upload_type: str,
	) -> Response | None:
		data = {
			"title": file_name,
			"description": description,
			"url": file_id,
			"type": "file",
		}

		if upload_type == UploadType.Component.value:
			data["component"] = code
		elif upload_type == UploadType.Testrun.value:
			data["testRun"] = code

		response = None
		try:
			files = {"data": itk_utils.get_file_components({"data": file_data})}
			if upload_type == UploadType.Component.value:
				response = self.itk_client.post("createComponentAttachment", data=data, files=files)
			elif upload_type == UploadType.Testrun.value:
				response = self.itk_client.post("createTestRunAttachment", data=data, files=files)
		except itk.exceptions.ResponseException as e:
			st.error(str(e))
			return None

		return response

EOS_Uploader_Page().main()
