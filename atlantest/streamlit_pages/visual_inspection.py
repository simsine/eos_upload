import streamlit as st

from atlantest.base_page import Base_Page

class Visual_Inspection_Page(Base_Page):
	def main(self):

		st.set_page_config(page_title="Visual Inspection", page_icon=":material/visibility:")

	with st.form("Visual Inspection Form"):
		st.write("# Visual Inspection")
		st.write(":red[This page is under construction.]")

		input_code = st.text_input(
			label = "Component serial number or test run number",
			placeholder = ""
		)

		input_institution = st.selectbox(
			label = "Institution",
			options = ("UNIBERGEN", "UNIOSLO")
		)

		input_wirebond_pads_contamination_grade = st.radio(
			label = "Wirebond pads clear of contamination (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_particulate_contamination_grade = st.radio(
			label = "Particulate contamination (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_watermarks_grade = st.radio(
			label = "Watermarks (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_scratches_grade = st.radio(
			label = "Scratches (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_traces_grade = st.radio(
			label = "Traces (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_soldermask_irregularities_grade = st.radio(
			label = "Soldermask irregularities (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_hv_lv_connector_assembly_grade = st.radio(
			label = "HV LV Data connector assembly issue (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_solder_spills_grade = st.radio(
			label = "Solder spills (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_component_misalignment_grade = st.radio(
			label = "Component misalignment (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_shorts_or_close_proximity_grade = st.radio(
			label = "Shorts or close proximity (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_opens_tombstoning_grade = st.radio(
			label = "Tombstone or misalignment (grade 1-3)",
			options = (1, 2, 3),
			horizontal = True,
			index = None
		)

		input_overall_grade = st.radio(
			label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
			options = (1, 2, 3, 4, 5),
			horizontal = True,
			index = None
		)

		input_observation = st.text_area(
			label = "Observations",
		)
		
		st.form_submit_button()
	
		
Visual_Inspection_Page().main()