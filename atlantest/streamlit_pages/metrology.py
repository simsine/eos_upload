from itkdb.exceptions import BadRequest
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

		st.write("## Upload metrology CSV file")
		uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
		
		if not uploaded_file:
			return
	
		try:
			df = pd.read_csv(uploaded_file)
			json_data = df.to_json(orient='records', indent=2)

			with st.expander("Show parsed data"):
				st.json(json.loads(json_data))

			# Store json_data in session_state to avoid re-reading CSV
			st.session_state[f'json_data_{uploaded_file.name}'] = json_data

		except Exception as exc:
			st.error(f"Failed to read {uploaded_file.name}: {exc}")

		st.divider()
	
		# Component code from filename
		metrology_csv_component_code: str = uploaded_file.name.split(".")[0]

		input_component_code = st.text_input(
			label = "Component serial number",
			placeholder = "",
			value = metrology_csv_component_code if metrology_csv_component_code else "",
		)

		input_test_run_number = st.number_input(
			label = "Test run number",
			step = 1,
			min_value = 1,
		)

		input_test_result = st.selectbox(
			label = "Test result",
			options = ("PASSED", "NOT PASSED"),
			index = None,
			placeholder = "Select test result",
		)

		REQUIRED_FIELDS_FILLED = input_component_code and input_test_run_number and input_test_result and uploaded_file

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
			json_str = st.session_state.get(f'json_data_{uploaded_file.name}')
			if json_str:
				data = json.loads(json_str)
				df = pd.DataFrame(data)  # Recreate df from json for processing
				
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

			# The component is cut out because the file has been created
			results["CUT_OUT"] = True

			results["HEIGHTS_ARRAY"] = {
				"Name": [],
				"X": [],
				"Y": [],
				"Height": [],
			}

			for name in df["Name"].unique():
				matching_rows = df[df['Name'] == name]
				max_height_row = matching_rows.loc[matching_rows["Z"].idxmax()]
				results["HEIGHTS_ARRAY"]["Name"].append(name)
				results["HEIGHTS_ARRAY"]["X"].append(max_height_row["X"])
				results["HEIGHTS_ARRAY"]["Y"].append(max_height_row["Y"])
				results["HEIGHTS_ARRAY"]["Height"].append(max_height_row["Z"])

			auth_user: dict = self.itk_client.get("getUser", json = {"userIdentity": self.itk_client.user.identity}) # type: ignore
			user_institution_code = auth_user["institutions"][0].get("code")

			# Upload test data
			upload_data = {
				"testType": "TRIPLET_PCB_METROLOGY",
				"component": input_component_code,
				"institution": user_institution_code,
				"runNumber": str(input_test_run_number),
				"passed": input_test_result == "PASSED",
				"problems": False,
				"properties": {},
				"results": results
			}

			st.json(upload_data)

			st.write("Upload result:")

			try:
				self.itk_client.post("uploadTestRunResults", json = upload_data) # type: ignore
			except BadRequest as e:
				error_content_json: dict = json.loads(e.response.content.decode())
				error_messages = [error["message"] for error in error_content_json["uuAppErrorMap"].values()]
				st.error(f"Failed uploading test results, errors: {error_messages}")
				with st.expander("See raw errors"):
					st.json(error_content_json["uuAppErrorMap"])
				return

			st.success("Results uploaded successfully")

if __name__ == "__main__":
	Metrology_Page().main()
