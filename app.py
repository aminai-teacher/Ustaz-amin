import streamlit as st
import google.generativeai as genai

# إعدادات صفحة الموقع
st.set_page_config(page_title="مساعدك التعليمي - الأستاذ أمين", layout="centered")

# تعديل كود الـ CSS لإجبار العناوين وكل النصوص والرسائل على التوجه لليمين (RTL) وضبط النقاط
st.markdown("""
    <style>
    /* توجيه الصفحة بالكامل لليمين */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* ضبط العناوين الرئيسية والفرعية لتكون لليمين */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        direction: rtl !important;
        text-align: right !important;
    }

    /* ضبط رسائل الدردشة واتجاهها */
    .stChatMessage {
        direction: rtl !important;
        text-align: right !important;
    }

    /* ضبط النقاط والقوائم لتظهر بشكل سليم من اليمين */
    ul, ol {
        direction: rtl !important;
        text-align: right !important;
        padding-right: 20px !important;
        padding-left: 0px !important;
    }
    li {
        list-style-position: inside !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("👨‍🏫 الأستاذ أمين")
st.write("مرحباً بك! أنا أستاذك الذكي، جاهز لمساعدتك في شرح الدروس، حل المسائل، والإجابة عن كل أسئلتك الدراسية.")

# خانة إدخال مفتاح الـ API بأمان
api_key = st.text_input("أدخل مفتاح API الخاص بك:", type="password")

if api_key:
    try:
        # إعداد الذكاء الاصطناعي
        genai.configure(api_key=api_key)
        
        # استخدام النموذج المحدث
        model = genai.GenerativeModel('gemini-3.8-flash')

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

            # توليد الرد من الأستاذ أمين مع خاصية التدفق (Streaming) للسرعة
            with st.chat_message("assistant"):
                try:
                    chat_prompt = f"أنت معلم خبير وودود تدعى الأستاذ أمين. أجب عن هذا السؤال التعليمي باللغة العربية الفصحى وبطريقة واضحة ومبسطة، مع ترتيب النقاط بشكل سليم: {prompt}"
                    
                    # استخدام stream=True لظهور الرد الفوري
                    response = model.generate_content(chat_prompt, stream=True)
                    
                    # عرض الرد تدريجياً وبشكل حي
                    response_container = st.empty()
                    full_response = ""
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_container.markdown(full_response + " ▌")
                    
                    # عرض النص النهائي
                    response_container.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as inner_e:
                    st.error(f"خطأ في توليد الرد: {inner_e}")
    except Exception as e:
        st.error(f"خطأ في الاتصال بمفتاح الـ API: {e}")
else:
    st.info("الرجاء إدخال مفتاح الـ API في الخانة بالأعلى لكي يبدأ الأستاذ أمين العمل معك.")
