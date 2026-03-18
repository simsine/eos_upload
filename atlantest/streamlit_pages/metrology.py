import streamlit as st

from atlantest.base_page import Base_Page

class Metrology_Page(Base_Page):
	def main(self):
		st.write("# Metrology")
		st.write("This page is under construction.")
		st.set_page_config(page_title="Metrology", page_icon=":material/straighten:")
		
Metrology_Page().main()