import streamlit as st

from atlantest.base_page import Base_Page

class Visual_Inspection_Page(Base_Page):
	def main(self):
		st.write("# Visual Inspection")
		st.write(":red[This page is under construction.]")
		st.set_page_config(page_title="Visual Inspection", page_icon=":material/visibility:")

		input_code = st.text_input(
			label = "Component serial number or test run number",
			placeholder = ""
		)

		input_institution = st.selectbox(
			label = "Institution",
			options = ("UNIBERGEN", "UNIOSLO")
		)

		input_wirebond_pads_contamination_grade = st.text_input(
			label = "Wirebond pads clear of contamination (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_particulate_contamination_grade = st.text_input(
			label = "Particulate contamination (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_watermarks_grade = st.text_input(
			label = "Watermarks (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_scratches_grade = st.text_input(
			label = "Scratches (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_traces_grade = st.text_input(
			label = "Traces (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_soldermask_irregularities_grade = st.text_input(
			label = "Soldermask irregularities (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_hv_lv_connector_assembly_grade = st.text_input(
			label = "HV LV Data connector assembly issue (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_solder_spills_grade = st.text_input(
			label = "Solder spills (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_component_misalignment_grade = st.text_input(
			label = "Component misalignment (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_shorts_or_close_proximity_grade = st.text_input(
			label = "Shorts or close proximity (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_opens_tombstoning_grade = st.text_input(
			label = "Tombstone or misalignment (grade 1-3)",
			placeholder = "",
			max_chars = 1
		)

		input_overall_grade = st.text_input(
			label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
			placeholder = "",
			max_chars = 1
		)

		input_observation = st.text_area(
			label = "Observations",
			placeholder = ""
		)

		if (not input_code or not input_test or not input_institution or not input_optical_front or not input_optical_back or not input_wirebond_pads_contamination_grade or not input_particulate_contamination_grade or not input_watermarks_grade or not input_scratches_grade or not input_traces_grade or not input_soldermask_irregularities_grade or not input_hv_lv_connector_assembly_grade or not input_solder_spills_grade or not input_component_misalignment_grade or not input_shorts_or_close_proximity_grade or not input_opens_tombstoning_grade or not input_overall_grade):
			return
		
		# We prompt the user to upload test images
		input_test_images = st.file_uploader(
			label = "Please upload a file",
			type = ["jpg", "jpeg", "png", "gif"],
			max_upload_size = self.MAX_FILE_UPLOAD_SIZE_MB,
			accept_multiple_files = True,
		)
		
Visual_Inspection_Page().main()