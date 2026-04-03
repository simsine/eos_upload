import streamlit as st
import pandas as pd

from atlantest.base_page import Base_Page

class Ready_To_Ship_Page(Base_Page):
	def main(self):
		st.write("# Components - Ready to Ship")
		st.write(":red[This page is under construction.]")
		st.set_page_config(page_title="Components - Ready to Ship", page_icon=":material/package_2:")
		
df = pd.DataFrame(
	{
		"serialnumber": ["12345", "67890"],
		"visualinspection": ["Pass", "Fail"],
		"metrology": ["Pass", "Fail"],
		"dc_test": ["Pass", "Fail"],
		"ready_to_ship": ["Yes", "No"]
	}
)

st.dataframe(
	df,
	column_config = {
		"serialnumber" : "Serial Number",
		"visualinspection" : st.column_config.TextColumn("Visual Inspection"),
		"metrology" : st.column_config.TextColumn("Metrology"),
		"dc_test" : st.column_config.TextColumn("DC Test"),
		"ready_to_ship" : st.column_config.TextColumn("Ready to Ship")
	}
)

Ready_To_Ship_Page().main()