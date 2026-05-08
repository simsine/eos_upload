import json
import math

from itkdb.exceptions import BadRequest
import streamlit as st
import pandas as pd

from atlantest.base_page import Base_Page
from atlantest.streamlit_pages.eos_uploader import EOS_Uploader_Page, UploadType

class Visual_Inspection_Page(Base_Page):
	# Names of testfields to be graded 1-3
	RANGE_DTO_FIELDS = [
		"VISUAL_INSPECTION_FRONT_GRADE",
		"VISUAL_INSPECTION_BACK_GRADE",
		"WIREBOND_PADS_CONTAMINATION_GRADE",
		"PARTICULATE_CONTAMINATION_GRADE",
		"WATERMARKS_GRADE",
		"SCRATCHES_GRADE",
		"SOLDERMASK_IRREGULARITIES_GRADE",
		"LV_CONNECTOR_ASSEMBLY_GRADE",
		"DATA_HV_CONNECTOR_ASSEMBLY_GRADE",
		"SOLDER_SPILLS_GRADE",
		"COMPONENT_MISALIGNMENT_GRADE",
		"SHORTS_OR_CLOSE_PROXIMITY_GRADE",
	]
	REST_DTO_FIELDS = [
		"OVERALL_GRADE",
		"OBSERVATION",
		"THICKNESS",
	]
	ALL_DTO_FIELDS = RANGE_DTO_FIELDS + REST_DTO_FIELDS

	def main(self):
		st.set_page_config(page_title="Visual Inspection", page_icon=":material/visibility:")

		st.write("# Visual Inspection")

		form_tab, excel_tab = st.tabs(("Form", "Excel upload"))

		with form_tab:
			form_component_code = st.text_input(
				label = "Component serial number",
				placeholder = "",
			)

			st.write("Grade the following fields from 1 to 3, where 1 is the best grade and 3 the worst grade.")

			form_grade_input_fields = []

			for grade_field_dto in self.RANGE_DTO_FIELDS:
				with st.container(horizontal = True, vertical_alignment = "center", horizontal_alignment = "left"):
					form_grade_input_fields.append(
						st.radio(
							key = grade_field_dto,
							label = grade_field_dto,
							options = (1, 2, 3),
							horizontal = True,
							index = None,
							label_visibility="collapsed",
						)
					)
					st.text(grade_field_dto)

			st.divider()

			form_overall_grade = st.radio(
				label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
				options = (1, 2, 3, 4, 5),
				horizontal = True,
				index = None,
			)

			form_observations = st.text_area(
				label = "Observations",
			)

			form_thickness = st.number_input(
				label = "Thickness (μm)",
				min_value = 0,
				step = 1,
			)

			st.divider()

			form_test_run_number = st.number_input(
				label = "Test run number",
				key = "form_test_run_number",
				step = 1,
				min_value = 1,
			)

			form_test_result = st.selectbox(
				label = "Test result",
				key = "form_test_result",
				options = ("PASSED", "NOT PASSED"),
				index = None,
				placeholder = "Select test result",
			)

			st.write("### Visual inspection images")

			form_test_images = st.file_uploader(
				label = "Upload corresponding visual inspection images",
				key = "form_test_images",
				type = ["jpg", "jpeg", "png"],
				max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
				accept_multiple_files = True,
			)

			REQUIRED_FIELDS_FILLED = form_component_code and all(form_grade_input_fields) and form_overall_grade and form_test_result

			if st.button(
				label = "Submit test results",
				key = "form_submit_button",
				disabled = not REQUIRED_FIELDS_FILLED,
				help = "Please fill all required fields before submitting results" if not REQUIRED_FIELDS_FILLED else "",
				width = "stretch",
			):
				# Upload test data

				auth_user: dict = self.itk_client.get("getUser", json = {"userIdentity": self.itk_client.user.identity}) # type: ignore
				user_institution_code = auth_user["institutions"][0].get("code")

				range_results = { key: value for key, value in zip(self.RANGE_DTO_FIELDS, form_grade_input_fields) }
				upload_data = {
					"testType": "VISUAL_INSPECTION",
					"component": form_component_code,
					"institution": user_institution_code,
					"runNumber": str(form_test_run_number),
					"passed": form_test_result == "PASSED",
					"problems": False,
					"properties": {},
					"results": {
						"OVERALL_GRADE": form_overall_grade,
						"OBSERVATION": form_observations,
						"THICKNESS": form_thickness,
					} | range_results
				}

				st.write("Upload result:")

				upload_res: dict
				try:
					upload_res = self.itk_client.post("uploadTestRunResults", json = upload_data) # type: ignore
				except BadRequest as e:
					error_content_json: dict = json.loads(e.response.content.decode())
					error_messages = [error["message"] for error in error_content_json["uuAppErrorMap"].values()]
					st.error(f"Failed uploading test results, errors: {error_messages}")
					with st.expander("See raw errors"):
						st.json(error_content_json["uuAppErrorMap"])
					return

				st.success("Results uploaded successfully")

				with st.expander("See results JSON"):
					st.json(upload_data)

				testrun_id = upload_res["testRun"]["id"]

				# Upload test images
				for image in form_test_images:
					try:
						EOS_Uploader_Page().upload_file(
							file_data = image,
							file_name = image.name,
							file_id = image.file_id,
							code = testrun_id,
							description = "",
							upload_type = UploadType.Testrun.value,
						)
					except Exception as e:
						st.error(f"Error in uploading file {image.name}. \n\n {e}")

				st.success("Attachments uploaded successfully")

			with excel_tab:
				excel_file = st.file_uploader(
						label = "Upload excel file with results",
						type = ["xlsx"],
				)

				if not excel_file:
					return
				
				excel_df = pd.read_excel(
					excel_file,
					usecols = ["Description", "Summary"],
				)

				with st.expander("Show parsed data"):
					st.dataframe(
						data = excel_df,
						height = "content"
					)

				st.divider()

				excel_file_component_code: str = excel_file.name.split(".")[0]

				excel_component_code = st.text_input(
					label = "Component serial number",
					placeholder = "",
					value = excel_file_component_code if excel_file_component_code else "",
				)

				excel_test_run_number = st.number_input(
					label = "Test run number",
					key= "excel_test_run_number",
					step = 1,
					min_value = 1,
				)

				excel_test_result = st.selectbox(
					label = "Did the test pass?",
					key = "excel_test_result",
					options = ("PASSED", "NOT PASSED"),
					index = None,
					placeholder = "Select test result",
				)

				st.write("## Upload test images")

				excel_test_images = st.file_uploader(
					label = "Please upload a file",
					key = "excel_test_images",
					type = ["jpg", "jpeg", "png", "gif"],
					max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
					accept_multiple_files = True,
				)

				if st.button(
					label = "Submit test results",
					key = "excel_submit_button",
					width = "stretch",
					disabled = not excel_test_result,
					help = "Please fill all required fields before submitting results" if not excel_test_result else "",
				):
					auth_user: dict = self.itk_client.get("getUser", json = {"userIdentity": self.itk_client.user.identity}) # type: ignore
					user_institution_code = auth_user["institutions"][0].get("code")

					excel_results = { key: value for key, value in zip(self.ALL_DTO_FIELDS, excel_df["Summary"]) }

					thickness = excel_results["THICKNESS"]

					if type(thickness) is str:
						split = thickness.split(", ")
						if len(split) == 2: # Field is in format of xxx, xxx
							value1 = float(split[0])
							value2 = float(split[1])
							sum = (value1 + value2) / 2
							excel_results["THICKNESS"] = sum
						else:
							st.error("Unexpected format in Thickness field")
							return
					
					if math.isnan(excel_results["OBSERVATION"]):
						excel_results["OBSERVATION"] = ""

					upload_data = {
						"testType": "VISUAL_INSPECTION",
						"component": excel_component_code,
						"institution": user_institution_code,
						"runNumber": str(excel_test_run_number),
						"passed": excel_test_result == "PASSED",
						"problems": False,
						"properties": {},
						"results": excel_results
					}

					st.write("Upload result:")

					with st.expander("See results JSON"):
						st.json(upload_data)

					upload_res: dict
					try:
						upload_res = self.itk_client.post("uploadTestRunResults", json = upload_data) # type: ignore
					except BadRequest as e:
						error_content_json: dict = json.loads(e.response.content.decode())
						error_messages = [error["message"] for error in error_content_json["uuAppErrorMap"].values()]
						st.error(f"Failed uploading test results, errors: {error_messages}")
						with st.expander("See raw errors"):
							st.json(error_content_json["uuAppErrorMap"])
						return

					st.success("Results uploaded successfully")

					testrun_id = upload_res["testRun"]["id"]

					# Upload test images
					for image in excel_test_images:
						try:
							EOS_Uploader_Page().upload_file(
								file_data = image,
								file_name = image.name,
								file_id = image.file_id,
								code = testrun_id,
								description = "",
								upload_type = UploadType.Testrun.value,
							)
						except Exception as e:
							st.error(f"Error in uploading file {image.name}. \n\n {e}")

					st.success("Attachments uploaded successfully")

if __name__ == "__main__":
	Visual_Inspection_Page().main()
