import streamlit as st

from atlantest.base_page import Base_Page

class Ready_To_Ship_Page(Base_Page):
	MAX_FILE_UPLOAD_SIZE_MB = 1000

	def main(self):
		st.write("# Ready to ship")
		st.write("This page is under construction.")
		st.set_page_config(page_title="Ready to Ship", page_icon="📦")
		
Ready_To_Ship_Page().main()