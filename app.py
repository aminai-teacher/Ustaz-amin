import streamlit as st
import google.generativeai as genai

# إعدادات صفحة الموقع مع اتجاه النص من اليمين لليسار لدعم العربية بشكل ممتاز
st.set_page_config(page_title="مساعدك التعليمي - الأستاذ أمين", layout="centered")

# حقن كود CSS بسيط لضبط اتجاه النص ونقاط القائمة لتظهر في المكان الصحيح باللغة العربية
st.markdown("""
    <style>
    body, .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    ul, ol {
        direction: rtl;
        text-align: right;
        padding-right: 20px;
        padding-left: 0px;
    }
    li {
        list-style-position: inside;
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
        
        # استخدام النموذج المحدث والموصى به
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
                    
                    # استخدام stream=True لظهور الرد الفوري الحرفي
                    response = model.generate_content(chat_prompt, stream=True)
                    
                    # عرض الرد تدريجياً وبشكل حي
                    response_container = st.empty()
                    full_response = ""
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_container.markdown(full_response + " ▌")
                    
                    # إزالة مؤشر الكتابة المؤقت في النهاية وعرض النص النهائي
                    response_container.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as inner_e:
                    st.error(f"خطأ في توليد الرد: {inner_e}")
    except Exception as e:
        st.error(f"خطأ في الاتصال بمفتاح الـ API: {e}")
else:
    st.info("الرجاء إدخال مفتاح الـ API في الخانة بالأعلى لكي يبدأ الأستاذ أمين العمل معك.")
