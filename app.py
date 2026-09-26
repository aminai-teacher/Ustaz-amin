import streamlit as st
import google.generativeai as genai

# عنوان الموقع والهوية البصرية
st.set_page_config(page_title="الأستاذ أمين - مساعدك التعليمي", page_icon="🎓")
st.title("🎓 الأستاذ أمين")
st.write("مرحباً بك! أنا أستاذك الذكي، جاهز لشرح الدروس، حل المسائل، والإجابة عن كل أسئلتك الدراسية.")

# إدخال مفتاح الـ API من المستخدم بأمان
api_key = st.text_input("أدخل مفتاح الـ API الخاص بك (الذي يبدأ بـ AIza أو AQ):", type="password")

if api_key:
    # إعداد الذكاء الاصطناعي
    genai.configure(api_key=api_key)
    
    # اختيار موديل فلاش السريع والذكي
    model = genai.GenerativeModel("gemini-1.5-flash")

    # تهيئة سجل المحادثة إذا لم يكن موجوداً
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # توجيه النظام (System Prompt) ليصبح الأستاذ أمين
        st.session_state.chat = model.start_chat(history=[{
            "role": "user", 
            "parts": ["أنت الآن 'الأستاذ أمين'، معلم ذكي وصبور ومحب للطلاب. تشرح المناهج الدراسية بطريقة مبسطة جداً، وتساعد الطلاب في حل واجباتهم بطريقة تعليمية صحيحة وليس فقط بإعطاء الحل الجاهز. تحدث دائماً باللغة العربية الفصحى المبسطة وبطريقة ودودة."]
        }, {
            "role": "model", 
            "parts": ["أهلاً بك يا بني! أنا الأستاذ أمين، مستعد دائماً لمساعدتك في دروسك والإجابة عن أي سؤال يواجهك. ما هو الدرس الذي تريد أن نراجعه سوياً اليوم؟"]
        }])

    # عرض الرسائل السابقة في الدردشة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # صندوق كتابة الرسالة من الطالب
    if prompt := st.chat_input("اكتب سؤالك أو صور مسألتك هنا..."):
        # عرض رسالة الطالب
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # توليد رد الأستاذ أمين
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير والكتابة..."):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("الرجاء إدخال مفتاح الـ API في الأعلى لبدء التشغيل التفاعلي.")
