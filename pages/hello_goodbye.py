import streamlit as st

st.header('st.button')

if st.button('Say Hello'):
    st.write('Why hello there!')
else:
    st.write('Bah-bye!')

# if st.button('Say Hello') and st.write('Why hello there!'):
#     st.button('Say Goodbye')


if 'score' not in st.session_state:
    st.session_state.score = 0

# st.write(st.session_state.score)
st.write('')
st.write('')

col1, col2, col3 = st.columns(3)

if col1.button('Free Throw'):
    st.session_state.score += 1

if col2.button('Jumper'):
    st.session_state.score += 2

if col3.button('Triple!'):
    st.session_state.score += 3

st.write(st.session_state.score)

# score = 0
#
# st.write(score)
#
# if st.button('Scored'):
#     score += 1
#
# st.write(score)
