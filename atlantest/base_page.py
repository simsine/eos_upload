from abc import ABCMeta, abstractmethod

import itkdb as itk
import streamlit as st

class Base_Page(metaclass = ABCMeta):
	itk_client: itk.Client

	# Constants
	PIXELS_PROJECT_CODE = "P"
	MAX_FILE_UPLOAD_SIZE_MB = 1000

	# Session state keys
	CURRENT_COMPONENT_CODE_KEY: str = "current_component_code"

	def __init__(self) -> None:
		itk_client = st.session_state.get("itk_client")
		if itk_client is None:
			raise Exception("Failure in getting itk client")
		self.itk_client = itk_client

	@abstractmethod
	def main(self):
		"""
		Main page render method to be overridden
		"""
		pass
