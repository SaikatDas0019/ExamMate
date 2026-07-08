import streamlit as st
import base64
import os

# first e chack kore neoya je user asole login kore aseche kina.
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.user_catagory != "Teacher":
        st.error("**Access Denaid!** This page in only for Teachers.")
        st.stop()
    import streamlit as st

    # Page Title
    st.title("Profile")

    # 1. Photo gol kore dekhanor jonno html er akti function.
    def get_circular_image(image_data, is_path=False):
        if is_path:
            with open(image_data, "rb") as f:
                image_bytes = f.read()
        else:
            image_bytes = image_data

        encoded_img = base64.b64encode(image_bytes).decode()

        html_code = f'''
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{encoded_img}" 
                     style="width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 3px solid #4CAF50;">
            </div>
        '''
        st.markdown(html_code, unsafe_allow_html=True)

    # 2. .session_state e photo save korer babosta
    if "profile_pic" not in st.session_state:
        st.session_state.profile_pic = None

    # 3. Photo uploade korar option
    if st.session_state.profile_pic is None:
        default_profile_pic = "images\default_profile_pic.jpg"
        if os.path.exists(default_profile_pic):
            get_circular_image(default_profile_pic, is_path=True)
        col, col1, col = st.columns([2, 1, 2])
        with col1:
            uploaded_file = st.file_uploader("Upload your Profile Picture (JPG/PNG)", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            # Upload kora photo session_state e save kora
            st.session_state.profile_pic = uploaded_file.getvalue()
            st.rerun()

    # 4. Photo dekhano
    else:
        get_circular_image(st.session_state.profile_pic, is_path=False)

        col, col2, col = st.columns([4, 2, 4])
        with col2:
            if st.button("Edit", use_container_width=True):
                st.session_state.profile_pic = None
                st.rerun()

    # User data
    st.write(f"**Name:** {st.session_state.get('user_name', 'Student')}")
    st.write(f"**Email:** {st.session_state.get('user_email', 'student@email.com')}")

    st.write("---")
    st.subheader("Exam History")

    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        exam_1 = st.button("Math|Matrix", use_container_width=True)
        exam_2 = st.button("Physice|Electric Filds", use_container_width=True)
    with col4:
        exam_3 = st.button("JEE-Main|Math", use_container_width=True)
        exam_4 = st.button("WBJEE|Matrix", use_container_width=True)
    with col5:
        exam_5 = st.button("English|Ulesis", use_container_width=True)
        exam_6 = st.button("NEET|Biology", use_container_width=True)

else:
    st.warning("Please, sign-in first.")