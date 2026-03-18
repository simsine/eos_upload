import streamlit as st

from atlantest.base_page import Base_Page

class Index_Page(Base_Page):
	MAX_FILE_UPLOAD_SIZE_MB = 1000

	def main(self):
		st.write("# UiB ATLAS")
		st.write("Welcome " + self.itk_client.user.name)

Index_Page().main()
