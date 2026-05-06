import streamlit as st
import json

from atlantest.base_page import Base_Page

class DC_Test_Page(Base_Page):
	def main(self):
		st.write("# DC Test")
		st.set_page_config(page_title="DC Test", page_icon=":material/bolt:")

		HV_test_file = st.file_uploader(
			label = "HV test results",
			type = ['json'],
		)

		RES_test_file = st.file_uploader(
			label = "Resistance test results",
			type = ['json'],
		)

		if HV_test_file is None or RES_test_file is None:
			return

		HV_component_code, HV_test_type, HV_date, HV_passed_state = HV_test_file.name.split("_")
		RES_component_code, RES_test_type, RES_date, RES_passed_state = RES_test_file.name.split("_")

		if HV_component_code != RES_component_code:
			st.error("Component serial numbers do not match")
			return
		
		if HV_test_type != "HV":
			st.error("HV test filename does not contain *HV*, is this the correct file?")
			return
		
		if RES_test_type != "resistance":
			st.error("Resistance test filename does not contain *resistance*, is this the correct file?")
			return

		if st.button(
			label = "Submit test results",
			width = "stretch",
		):
			HV_json = json.loads(HV_test_file.getvalue())[0]
			RES_json = json.loads(RES_test_file.getvalue())[0]

			HV_upload_data = {
				"testType": "Electrical_HV",
				"component": HV_component_code,
				"institution": HV_json["institution"],
				"date": HV_json["date"],
				"runNumber": "1",
				"passed": HV_passed_state == "passed",
				"problems": False,
				"properties": {},
				"results": HV_json["results"]
			}

			RES_upload_data = {
				"testType": "Electrical_RES",
				"component": RES_component_code,
				"institution": RES_json["institution"],
				"date": RES_json["date"],
				"runNumber": "1",
				"passed": RES_passed_state == "passed",
				"problems": False,
				"properties": {},
				"results": RES_json["results"]
			}

			st.write("Upload results:")

			try:
				self.itk_client.post("uploadTestRunResults", json = HV_upload_data) # type: ignore
				self.itk_client.post("uploadTestRunResults", json = RES_upload_data) # type: ignore
			except Exception as e:
				st.error(f"Error in uploading test results: \n\n {e}")
				return
			
			st.success("Results uploaded successfully")

if __name__ == "__main__":
	DC_Test_Page().main()
