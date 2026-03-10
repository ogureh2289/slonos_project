import streamlit as st
import requests
from datetime import datetime


API_URL = "http://localhost:8000/api/v1"

if 'messages'       not in st.session_state: st.session_state.messages       = []
if 'chat_histories' not in st.session_state: st.session_state.chat_histories = []
if 'current_chat'   not in st.session_state: st.session_state.current_chat   = None

with st.sidebar:
    st.caption("Компаньон для изучения Python")

    st.divider()

    st.markdown("**💡 Быстрые вопросы**")
    for q in [
        "Что такое список?",
        "Как написать функцию?",
        "Что такое ООП?",
        "Как работает декоратор?",
        "Что такое lambda?",
        "Как работает async/await?",
    ]:
        if st.button(q, key=f"q_{q}", use_container_width=True):
            st.session_state.messages.append({"role":"user","content":q})
            try:
                r = requests.post(f"{API_URL}/ask", json={"user_id":"guest","question":q,"context":{}}, timeout=60)
                if r.status_code == 200:
                    st.session_state.messages.append({"role":"assistant","content":r.json()["answer"]})
            except:
                st.session_state.messages.append({"role":"assistant","content":"⚠️ Сервер недоступен"})
            st.rerun()

    st.divider()

    st.markdown("**🌐 Полезные сайты**")

    st.markdown("📄 [Python.org](https://docs.python.org/3/)")
    st.caption("Официальная документация Python")

    st.markdown("📝 [Real Python](https://realpython.com/)")
    st.caption("Учебники, статьи и видеоуроки")

    st.markdown("📰 [Habr Python](https://habr.com/ru/hub/python/)")
    st.caption("Статьи и туториалы на русском")

    st.markdown("🎓 [Stepik](https://stepik.org/course/67/promo)")
    st.caption("Бесплатный курс по основам Python")

    st.markdown("🔧 [Pythontutor](http://pythontutor.ru/)")
    st.caption("Визуализация выполнения кода")

    st.markdown("💡 [LeetCode](https://leetcode.com/problemset/all/?languageTags=python)")
    st.caption("Задачи и алгоритмы на Python")

col_chat, col_hist = st.columns([3, 1])

with col_chat:
    c1, c2, c3 = st.columns([5, 1, 1])
    with c1:
        st.markdown("### 💬 Чат")
    with c2:
        if st.button("➕ Новый", use_container_width=True):
            if st.session_state.messages and st.session_state.current_chat is None:
                user_msgs = [m for m in st.session_state.messages if m["role"]=="user"]
                if user_msgs:
                    st.session_state.chat_histories.append({
                        "id":       len(st.session_state.chat_histories),
                        "title":    user_msgs[0]["content"][:35],
                        "time":     datetime.now().strftime("%d.%m %H:%M"),
                        "messages": st.session_state.messages.copy()
                    })
            st.session_state.messages = []
            st.session_state.current_chat = None
            st.rerun()
    with c3:
        if st.button("🗑️ Сброс", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_chat = None
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**Вы:** {msg['content']}")
        else:
            st.markdown(msg["content"])
        st.divider()

    question = st.chat_input("Задайте вопрос по Python...")
    if question:
        if st.session_state.current_chat is not None:
            st.session_state.messages = []
            st.session_state.current_chat = None

        st.session_state.messages.append({"role":"user","content":question})
        with st.spinner("Думаю..."):
            try:
                r = requests.post(f"{API_URL}/ask", json={"user_id":"guest","question":question,"context":{}}, timeout=60)
                if r.status_code == 200:
                    st.session_state.messages.append({"role":"assistant","content":r.json()["answer"]})
                else:
                    st.session_state.messages.append({"role":"assistant","content":f"⚠️ Ошибка {r.status_code}"})
            except requests.exceptions.ConnectionError:
                st.session_state.messages.append({"role":"assistant","content":"⚠️ Сервер недоступен"})
            except requests.exceptions.Timeout:
                st.session_state.messages.append({"role":"assistant","content":"⏱️ Timeout, попробуйте ещё раз"})
        st.rerun()

with col_hist:
    st.markdown("### 🕓 История")

    if not st.session_state.chat_histories:
        st.caption("Пока пусто")
    else:
        if st.button("🗑️ Очистить", use_container_width=True):
            st.session_state.chat_histories = []
            st.rerun()

        st.divider()

        for chat in reversed(st.session_state.chat_histories):
            cb, cd = st.columns([4, 1])
            with cb:
                if st.button(
                    f" {chat['title']}",
                    key=f"h_{chat['id']}",
                    use_container_width=True,
                    help=chat['time']
                ):
                    st.session_state.messages = chat["messages"].copy()
                    st.session_state.current_chat = chat["id"]
                    st.rerun()
            with cd:
                if st.button("✕", key=f"d_{chat['id']}"):
                    st.session_state.chat_histories = [
                        c for c in st.session_state.chat_histories if c["id"] != chat["id"]
                    ]
                    st.rerun()