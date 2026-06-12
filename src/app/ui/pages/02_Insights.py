import streamlit as st

from app.services.dataset_insights import generate_dataset_insights

st.title("Insights")

if "profile" not in st.session_state:
	st.warning("Analyze a dataset first")

	st.stop()

if st.button("Generate AI Insights"):
	insights = generate_dataset_insights(
		profile=st.session_state["profile"],
		schema=st.session_state["schema"],
		missing_values=st.session_state["missing_values"],
		duplicates=st.session_state["duplicates"]
	)

	st.session_state["insights"] = insights

if "insights" in st.session_state:
	st.markdown(
		st.session_state["insights"]
	)
