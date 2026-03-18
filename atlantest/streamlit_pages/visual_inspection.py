import streamlit as st

from atlantest.base_page import Base_Page

class Visual_Inspection_Page(Base_Page):
	def main(self):
		st.write("# Visual Inspection")
		st.write("This page is under construction.")
		st.set_page_config(page_title="Visual Inspection", page_icon=":material/biotech:")
		
Visual_Inspection_Page().main()