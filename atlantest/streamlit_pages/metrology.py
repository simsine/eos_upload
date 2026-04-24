import streamlit as st
import pandas as pd
import json

from atlantest.base_page import Base_Page

class Metrology_Page(Base_Page):
	def main(self):
		st.write("# Metrology")
		st.set_page_config(page_title="Metrology", page_icon=":material/straighten:")
		
		st.write("## CSV to JSON Converter")
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

				except Exception as exc:
					st.error(f"Failed to read {uploaded_file.name}: {exc}")
		
		st.write("---")
		
		input_code = st.text_input(
			label = "Code",
			placeholder = "Component serial number or test run number"
		)

		if (not input_code):
			return

if __name__ == "__main__":
	Metrology_Page().main()
