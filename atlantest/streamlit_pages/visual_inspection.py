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
			input_component_code = st.text_input(
				label = "Component serial number",
				placeholder = "",
			)

			auth_user: dict = self.itk_client.get("getUser", json = {"userIdentity": self.itk_client.user.identity}) # type: ignore
			user_institution_code = auth_user["institutions"][0].get("code")

			input_institution = st.selectbox(
				label = "Institution",
				accept_new_options = False,
				options = user_institution_code,
				index = 0, # Since the user institution should be at index 0
			)

			excel_test_run_number = st.number_input(
				label = "Test run number",
				key = "form_test_run_number",
				step = 1,
				min_value = 1,
			)

			st.divider()

			st.write("Grade the following fields from 1 to 3, where 1 is the best grade and 3 the worst grade.")

			grade_input_fields = []

			for grade_field_dto in self.RANGE_DTO_FIELDS:
				with st.container(horizontal = True, vertical_alignment = "center", horizontal_alignment = "left"):
					grade_input_fields.append(
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

			input_overall_grade = st.radio(
				label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
				options = (1, 2, 3, 4, 5),
				horizontal = True,
				index = None,
			)

			input_observation = st.text_input(
				label = "Observations",
			)

			input_thickness = st.text_input(
				label = "Thickness",
			)

			excel_test_result = st.checkbox(
				label = "Did the test pass?",
				key = "form_test_passed",
			)

			st.write("## Upload test images")

			input_test_images = st.file_uploader(
				label = "Please upload a file",
				key = "form_test_images",
				type = ["jpg", "jpeg", "png", "gif"],
				max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
				accept_multiple_files = True,
			)

			REQUIRED_FIELDS_FILLED = input_component_code and all(grade_input_fields) and input_overall_grade

			if st.button(
				label = "Submit test results",
				disabled = not REQUIRED_FIELDS_FILLED,
				help = "Please fill all required fields before submitting results" if not REQUIRED_FIELDS_FILLED else "",
				width = "stretch",
			):
				# Upload test data

				range_results = { key: value for key, value in zip(self.RANGE_DTO_FIELDS, grade_input_fields) }
				upload_data = {
					"testType": "VISUAL_INSPECTION",
					"component": input_component_code,
					"institution": input_institution,
					"runNumber": str(excel_test_run_number),
					"passed": excel_test_result,
					"problems": False,
					"properties": {},
					"results": {
						"OVERALL_GRADE": input_overall_grade,
						"OBSERVATION": input_observation,
						"THICKNESS": input_thickness,
					} | range_results
				}

				st.write("Upload result:")
				upload_res: dict = self.itk_client.post("uploadTestRunResults", json = upload_data) # type: ignore

				if not upload_res:
					st.error(f"Error in uploading test results: \n {upload_res}")
					return

				st.success("Results uploaded successfully")

				testrun_id = upload_res["testRun"]["id"]

				# Upload test images
				for image in input_test_images:
					res = EOS_Uploader_Page().upload_file(
						file_data = image,
						file_name = image.name,
						file_id = image.file_id,
						code = testrun_id,
						description = "",
						upload_type = UploadType.Testrun.value,
					)

					if not res:
						st.error(f"Error in uploading file: {image.name}")
						return

				st.success("Attachments uploaded successfully")

			with excel_tab:
				excel_file = st.file_uploader(
						label = "Upload excel file with results",
						type = ["xlsx"],
					)

				excel_test_run_number = st.number_input(
					label = "Test run number",
					key= "excel_test_run_number",
					step = 1,
					min_value = 1,
				)

				excel_test_result = st.checkbox(
					label = "Did the test pass?",
					key = "excel_test_passed",
				)

				st.write("## Upload test images")

				excel_test_images = st.file_uploader(
					label = "Please upload a file",
					key = "excel_test_images",
					type = ["jpg", "jpeg", "png", "gif"],
					max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
					accept_multiple_files = True,
				)

				if not excel_file:
					return

				excel_df = pd.read_excel(
					excel_file,
					usecols = ["Description", "Summary"],
				)

				st.divider()
				st.write("## Parsed test results")
				st.dataframe(
					data = excel_df,
					height = "content"
				)

				if st.button(
					label = "Submit test results",
					width = "stretch",
				):
					# Component code from filename
					VI_excel_component_code: str = excel_file.name.split(".")[0]

					auth_user: dict = self.itk_client.get("getUser", json = {"userIdentity": self.itk_client.user.identity}) # type: ignore
					user_institution_code = auth_user["institutions"][0].get("code")

					excel_results = { key: value for key, value in zip(self.ALL_DTO_FIELDS, excel_df["Summary"]) }

					upload_data = {
						"testType": "VISUAL_INSPECTION",
						"component": VI_excel_component_code,
						"institution": user_institution_code,
						"runNumber": str(excel_test_run_number),
						"passed": excel_test_result,
						"problems": False,
						"properties": {},
						"results": excel_results
					}

					st.write("Upload result:")
					upload_res: dict = self.itk_client.post("uploadTestRunResults", json = upload_data) # type: ignore

					if not upload_res:
						st.error(f"Error in uploading test results: \n {upload_res}")
						return

					st.success("Results uploaded successfully")

					testrun_id = upload_res["testRun"]["id"]

					# Upload test images
					for image in excel_test_images:
						res = EOS_Uploader_Page().upload_file(
							file_data = image,
							file_name = image.name,
							file_id = image.file_id,
							code = testrun_id,
							description = "",
							upload_type = UploadType.Testrun.value,
						)

						if not res:
							st.error(f"Error in uploading file: {image.name}")
							return

					st.success("Attachments uploaded successfully")

if __name__ == "__main__":
	Visual_Inspection_Page().main()
