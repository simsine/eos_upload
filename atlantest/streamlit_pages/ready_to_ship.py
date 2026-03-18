import streamlit as st

from atlantest.base_page import Base_Page

class Ready_To_Ship_Page(Base_Page):
	def main(self):
		st.write("# Components - Ready to Ship")
		st.write("This page is under construction.")
		st.set_page_config(page_title="Components - Ready to Ship", page_icon=":material/package_2:")
		
Ready_To_Ship_Page().main()