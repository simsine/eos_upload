import streamlit as st

from atlantest.base_page import Base_Page

class All_Components_Page(Base_Page):
	MAX_FILE_UPLOAD_SIZE_MB = 1000

	def main(self):
		st.write("# All components")
		st.write("This page is under construction.")
		
All_Components_Page().main()