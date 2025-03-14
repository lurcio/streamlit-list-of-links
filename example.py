import streamlit as st
from list_of_links import list_of_links

st.subheader("Component with constant args")

people = ["Alice", "Bob", "Charlie", "David", "Eve"]
people_links = [{"subject": name, "link": str(idx)} for idx, name in enumerate(people)]
link_target = list_of_links("World", people_links)
st.markdown("You chose link target %s!" % link_target)

st.markdown("---")
st.subheader("Component with variable args")

name_input = st.text_input("Enter a title", value="Streamlit")
link_target_2 = list_of_links(name_input, people_links, key="foo")
st.markdown("You chose link target %s!" % link_target_2)

st.markdown("---")
st.subheader("Component with selected link")

link_target_3 = list_of_links("Hello", people_links, default_link="1")
st.markdown("You chose link target %s!" % link_target_3)
