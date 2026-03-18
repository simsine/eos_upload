import streamlit as st

from atlantest.base_page import Base_Page

class DC_Test_Page(Base_Page):
	def main(self):
		st.write("# DC Test")
		st.write("This page is under construction.")
		st.set_page_config(page_title="DC Test", page_icon=":material/bolt:")
		
DC_Test_Page().main()