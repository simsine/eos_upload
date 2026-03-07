import itkdb as itk
import streamlit as st

class App_Page():
	itk_client: itk.Client

	def __init__(self, itk_client: itk.Client|None = None) -> None:
		if itk_client:
			self.itk_client = itk_client
		else:
			itk_client = st.session_state.get("itk_client")
			if itk_client is None:
				raise Exception("Failure in getting itk client")
			self.itk_client = itk_client
