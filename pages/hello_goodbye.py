import streamlit as st

st.header('st.button')

if st.button('Say Hello'):
    st.write('Why hello there!')
else:
    st.write('Bah-bye!')

# if st.button('Say Hello') and st.write('Why hello there!'):
#     st.button('Say Goodbye')
