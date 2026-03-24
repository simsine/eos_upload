import streamlit as st

from atlantest.base_page import Base_Page

class Visual_Inspection_Page(Base_Page):
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
	
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					key="wire_pads",
					label = "Wirebond pads clear of contamination (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Wirebond pads clear of contamination (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					key="particulate_contamination",
					label = "Particulate contamination (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Particulate contamination (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					key="watermarks",
					label = "Watermarks (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Watermarks (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					key="scratches",
					label = "Scratches (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Scratches (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "Traces (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Traces (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "Soldermask irregularities (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Soldermask irregularities (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "HV LV Data connector assembly issue (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("HV LV Data connector assembly issue (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "Solder spills (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Solder spills (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "Component misalignment (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Component misalignment (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "Shorts or close proximity (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Shorts or close proximity (grade 1-3)")
		with st.container(horizontal = True, vertical_alignment="center", horizontal_alignment="left"):
			range_input_fields.append(
				st.radio(
					label = "Tombstone or misalignment (grade 1-3)",
					options = (1, 2, 3),
					horizontal = True,
					index = None,
					label_visibility="collapsed"
				)
			)
			st.text("Tombstone or misalignment (grade 1-3)")

		st.divider()

		st.radio(
			label = "Overall grade (1 no damages, 2 no action, 3 re-clean, 4 rework, 5 discard)",
			options = (1, 2, 3, 4, 5),
			horizontal = True,
			index = None
		)

		input_observation = st.text_area(
			label = "Observations",
		)
		
		ALL_RANGE_FIELDS_FILLED = all(range_input_fields)

		if st.button(label = "Submit test", disabled = not ALL_RANGE_FIELDS_FILLED):
			st.write("yay!")

Visual_Inspection_Page().main()
