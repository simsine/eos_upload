from streamlit.testing.v1 import AppTest

def test_page_loads():
	"""
	Test that the page loads initially
	"""
	at = AppTest.from_file("./streamlit_app.py").run()
	assert at.markdown[0].value == "# Please authenticate"
