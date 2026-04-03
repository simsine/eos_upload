import streamlit as st

from atlantest.base_page import Base_Page

class Visual_Inspection_Page(Base_Page):
	PIXELS_PROJECT_CODE = "P"
	# Names of fields to be graded 1-3
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
		st.write(":red[This page is under construction.]")

		input_code = st.text_input(
			label = "Component serial number or test run number",
			placeholder = "",
		)

		input_institution = st.selectbox(
			label = "Institution",
			options = ("UNIBERGEN", "UNIOSLO")
		)

		st.divider()

		range_input_fields = []
	
		for grade_field_name in self.GRADE_FIELDS_DTO:
			with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
				range_input_fields.append(
					st.radio(
						key = grade_field_name,
						label = f"{grade_field_name} (grade 1-3)",
						options = (1, 2, 3),
						horizontal = True,
						index = None,
						label_visibility="collapsed"
					)
				)
				st.text(f"{grade_field_name} (grade 1-3)")

		st.divider()

		input_overall_grade = st.radio(
			label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
			options = (1, 2, 3, 4, 5),
			horizontal = True,
			index = None
		)

		input_observation = st.text_area(
			label = "Observations",
		)
		
		ALL_RANGE_FIELDS_FILLED = all(range_input_fields)

		if st.button(label = "Submit test", disabled = not ALL_RANGE_FIELDS_FILLED, help = "Please fill all fields before submitting results" if not ALL_RANGE_FIELDS_FILLED else ""):
			# st.json(self.itk_client.get('generateTestTypeDtoSample', json={'project': self.PIXELS_PROJECT_CODE, 'componentType': 'PCB', 'code': 'VISUAL_INSPECTION', 'requiredOnly': True}))

			upload_data = {
				"component": input_code,
				"institution": input_institution,
				"testType": "VISUAL_INSPECTION",
				"runNumber": "14",
				"passed": "false",
				"problems": "false",
				"properties": {},
				"results": {
					"OVERALL_GRADE": input_overall_grade,
					"OBSERVATION": input_observation,
				} | { key: value for key, value in zip(self.GRADE_FIELDS_DTO, range_input_fields) }
			}

			st.write("Upload result:")
			upload_res = self.itk_client.post("uploadTestRunResults", json = upload_data)

			st.json(upload_res)

Visual_Inspection_Page().main()
