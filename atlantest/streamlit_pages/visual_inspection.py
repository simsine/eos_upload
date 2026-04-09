from itkdb.responses import PagedResponse
import streamlit as st

from atlantest.base_page import Base_Page
from atlantest.streamlit_pages.eos_uploader import EOS_Uploader_Page, UploadType

class Visual_Inspection_Page(Base_Page):
	# Names of test-fields to be graded 1-3
	GRADE_FIELDS_DTO = {
		"WIREBOND_PADS_CONTAMINATION_GRADE",
		"PARTICULATE_CONTAMINATION_GRADE",
		"WATERMARKS_GRADE",
		"SCRATCHES_GRADE",
		"TRACES_GRADE",
		"SOLDERMASK_IRREGULARITIES_GRADE",
		"HV_LV_CONNECTOR_ASSEMBLY_GRADE",
		"DATA_CONNECTOR_ASSEMBLY_GRADE",
		"SOLDER_SPILLS_GRADE",
		"COMPONENT_MISALIGNMENT_GRADE",
		"SHORTS_OR_CLOSE_PROXIMITY_GRADE",
		"OPENS_TOMBSTONING_GRADE",
	}

	def main(self):
		st.set_page_config(page_title="Visual Inspection", page_icon=":material/visibility:")

		st.write("# Visual Inspection")

		input_component_code = st.text_input(
			label = "Component serial number",
			placeholder = "",
			value = st.session_state[self.CURRENT_COMPONENT_CODE_KEY] if self.CURRENT_COMPONENT_CODE_KEY in st.session_state else ""
		)

		if input_component_code:
			st.session_state[self.CURRENT_COMPONENT_CODE_KEY] = input_component_code

		auth_user: dict = self.itk_client.get("getUser", json = {"userIdentity": self.itk_client.user.identity}) # type: ignore
		user_institution_code = auth_user["institutions"][0].get("code")

		institutions: PagedResponse = self.itk_client.get("listInstitutions") # type: ignore
		institution_codes = list(map(lambda institution: institution.get("code"), institutions.data))
		# We move the institution of the user to the front
		institution_codes.insert(0, institution_codes.pop(institution_codes.index(user_institution_code)))

		input_institution = st.selectbox(
			label = "Institution",
			accept_new_options = False,
			options = institution_codes,
			index = 0, # Since the user institution should be at index 0
		)

		input_test_run_number = st.number_input(
			label = "Test run number",
			step = 1,
			min_value = 1,
		)

		st.divider()

		st.write("## Inspection grades 1-3")

		range_input_fields = []

		for grade_field_name in self.GRADE_FIELDS_DTO:
			with st.container(horizontal = True, vertical_alignment = "center", horizontal_alignment = "left"):
				range_input_fields.append(
					st.radio(
						key = grade_field_name,
						label = grade_field_name,
						options = (1, 2, 3),
						horizontal = True,
						index = None,
						label_visibility="collapsed",
					)
				)
				st.text(grade_field_name)

		st.divider()

		input_overall_grade = st.radio(
			label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
			options = (1, 2, 3, 4, 5),
			horizontal = True,
			index = None,
		)

		input_observation = st.text_area(
			label = "Observations",
		)

		input_test_result = st.checkbox(
			label = "Did this test get a passing grade?",
		)

		st.write("## Upload test images")

		input_test_images = st.file_uploader(
			label = "Please upload a file",
			type = ["jpg", "jpeg", "png", "gif"],
			max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
			accept_multiple_files = True,
		)

		REQUIRED_FIELDS_FILLED = all(range_input_fields)

		if st.button(
			label = "Submit test",
			disabled = not REQUIRED_FIELDS_FILLED,
			help = "Please fill all required fields before submitting results" if not REQUIRED_FIELDS_FILLED else "",
		):
			# Upload test data
			upload_data = {
				"testType": "VISUAL_INSPECTION",
				"component": input_component_code,
				"institution": input_institution,
				"runNumber": str(input_test_run_number),
				"passed": input_test_result,
				"problems": False,
				"properties": {},
				"results": {
					"OVERALL_GRADE": input_overall_grade,
					"OBSERVATION": input_observation,
				} | { key: value for key, value in zip(self.GRADE_FIELDS_DTO, range_input_fields) }, # Adding all grading field values to results
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

Visual_Inspection_Page().main()
