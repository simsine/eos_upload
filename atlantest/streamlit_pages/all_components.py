import streamlit as st

from atlantest.base_page import Base_Page

class All_Components_Page(Base_Page):
	def main(self):
		st.write("# Components - All")
		st.write("This page is under construction.")
		st.set_page_config(page_title="Components - All", page_icon=":material/list:")
		
All_Components_Page().main()