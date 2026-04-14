import streamlit as st

from atlantest.base_page import Base_Page

class DC_Test_Page(Base_Page):
	def main(self):
		st.write("# DC Test")
		st.write(":red[This page is under construction.]")
		st.set_page_config(page_title="DC Test", page_icon=":material/bolt:")
		
		input_code = st.text_input(
			label = "Code",
			placeholder = "Component serial number or test run number"
		)

		input_description = st.text_input(
			label = "Description",
			placeholder = "File description"
		)

		input_upload_type = st.selectbox(
			label = "Upload type",
			options = ()
		)

		if (not input_code or not input_description):
			return

if __name__ == "__main__":
	DC_Test_Page().main()