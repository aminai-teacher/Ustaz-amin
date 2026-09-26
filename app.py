
import streamlit as st
import google.generativeai as genai

# عنوان الموقع والهوية البصرية
st.set_page_config(page_title="مساعدك التعليمي - الأستاذ أمين")
st.title("👨‍🏫 الأستاذ أمين")
st.write("مرحباً بك! أنا أستاذك الذكي، جاهز لمساعدتك في شرح الدروس، حل المسائل، والإجابة عن كل أسئلتك الدراسية.")

# خانة إدخال مفتاح الـ API بأمان
api_key = st.text_input("أدخل مفتاح API الخاص بك:", type="password")

if api_key:
    # إعداد الذكاء الاصطناعي
    genai.configure(api_key=api_key)
    
    # استخدام النموذج الأساسي المستقر جداً في المكتبة القديمة
    model = genai.GenerativeModel('gemini-pro')

    # تهيئة الذاكرة للمحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال سؤال الطالب
    if prompt := st.chat_input("اكتب سؤالك أو صور مسألتك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # توليد الرد من الأستاذ أمين
        with st.chat_message("assistant"):
            try:
                chat_prompt = f"أنت معلم خبير وودود تدعى الأستاذ أمين. أجب عن هذا السؤال التعليمي بطريقة واضحة ومبسطة ومفيدة للطالب: {prompt}"
                response = model.generate_content(chat_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
else:
    st.info("الرجاء إدخال مفتاح الـ API في الخانة بالأعلى لكي يبدأ الأستاذ أمين العمل معك.")
