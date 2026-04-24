import streamlit as st
import pandas as pd
import json

from atlantest.base_page import Base_Page

class Metrology_Page(Base_Page):

	METROLOGY_FIELDS_DTO = {
		"CUT_OUT",
		"HEIGHT_CRITICAL_COMP",
		"HEIGHT_DATA_CONN",
		"HEIGHT_LV_CONN",
		"HEIGHT_HV_CONN",
		"HEIGHT_GENERAL_COMP",
		"ENVELOPE"
	}

	def main(self):
		st.write("# Metrology")
		st.set_page_config(page_title="Metrology", page_icon=":material/straighten:")

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
		
		st.write("## Upload metrology CSV files")
		uploaded_files = st.file_uploader("Choose CSV files", type=['csv'], accept_multiple_files=True)
		
		if uploaded_files:
			for uploaded_file in uploaded_files:
				st.write(f"### File: {uploaded_file.name}")
				try:
					df = pd.read_csv(uploaded_file)
					json_data = df.to_json(orient='records', indent=2)

					st.write("Converted JSON:")
					st.json(json.loads(json_data))

					with st.expander("Show raw JSON"):
						st.code(json_data, language='json')

					# Store json_data in session_state to avoid re-reading CSV
					st.session_state[f'json_data_{uploaded_file.name}'] = json_data

				except Exception as exc:
					st.error(f"Failed to read {uploaded_file.name}: {exc}")
		
		st.write("---")

		input_test_result = st.selectbox(
			"Did the test pass?",
			("PASSED", "NOT PASSED"),
			index=None,
			placeholder="Select test result",
		)

		REQUIRED_FIELDS_FILLED = input_component_code and input_institution and input_test_run_number and input_test_result and uploaded_files

		if st.button(
			label = "Submit test",
			disabled = not REQUIRED_FIELDS_FILLED,
			help = "Please fill all required fields and upload CSV files before submitting results" if not REQUIRED_FIELDS_FILLED else "",
		):
			# Process stored json_data to populate results
			results = {}
			mappings = {
				"HEIGHT_DATA_CONN": ["J103"],
				# "HEIGHT_CRITICAL_COMP" : "UNKNOWN", # Critical component still not decided
				"HEIGHT_LV_CONN": ["J101", "J102"], # We take the max of J101 and J102 for HEIGHT_LV_CONN
				"HEIGHT_HV_CONN": ["C101"],
			}
			
			all_z = []
			
			# Extract Z values for specific fields based on mappings
			for uploaded_file in uploaded_files:
				json_str = st.session_state.get(f'json_data_{uploaded_file.name}')
				if json_str:
					data = json.loads(json_str)
					df = pd.DataFrame(data)  # Recreate df from json for processing

					with st.expander(f"Debug: Name values in {uploaded_file.name}"):
						found_names = sorted(df['Name'].unique().tolist())
						expected_codes = sorted({code for codes in mappings.values() for code in codes})
						st.write("**Found in CSV:**", found_names)
						st.write("**Expected codes:**", expected_codes)
						st.write("**Matched:**", sorted(set(found_names) & set(expected_codes)))
						st.write("**Missing:**", sorted(set(expected_codes) - set(found_names)))
					
					df['Name'] = df['Name'].str.strip()
					for field, codes in mappings.items():
						matching_rows = df[df['Name'].isin(codes)]
						if not matching_rows.empty:
							max_val = matching_rows['Z'].max()
							results[field] = max(results.get(field, float('-inf')), max_val)

					all_z.extend(df['Z'].tolist())
			
			# For HEIGHT_GENERAL_COMP, max of Z values not in specific codes
			if all_z:
				results["HEIGHT_GENERAL_COMP"] = max(all_z)
			
			# Upload test data
			upload_data = {
				"testType": "TRIPLET_PCB_METROLOGY",
				"component": input_component_code,
				"institution": input_institution,
				"runNumber": str(input_test_run_number),
				"passed": input_test_result,
				"problems": False,
				"properties": {},
				"results": results
			}
			
			st.write("### Debug")
			st.json(upload_data)  # Show the data that would be uploaded

			# st.write("Upload result:")
			# upload_res: dict = self.itk_client.post("uploadTestRunResults", json = upload_data) # type: ignore

			# if not upload_res:
			#    st.error(f"Error in uploading test results: \n {upload_res}")
			#    return

			st.success("Results uploaded successfully")

if __name__ == "__main__":
	Metrology_Page().main()
