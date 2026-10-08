import requests
import streamlit as st


API_BASE_URL = "http://localhost:8000"


st.set_page_config(
    page_title="RAG Knowledge Platform",
    page_icon="📚",
    layout="wide",
)

st.title("📚 RAG Knowledge Platform")
st.write("Upload documents and ask questions based on your knowledge base.")


# =========================
# Upload Document
# =========================

st.divider()

st.subheader("Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF, TXT, or MD file",
    type=["pdf", "txt", "md"],
)

if uploaded_file is not None:
    if st.button("Upload and Index"):
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            with st.spinner("Uploading and indexing document..."):
                response = requests.post(
                    f"{API_BASE_URL}/documents/upload",
                    files=files,
                    timeout=120,
                )

            if response.status_code == 200:
                result = response.json()

                st.success(
                    "Document uploaded and indexed successfully!"
                )

                document_id = result.get("document_id")

                if document_id:
                    st.session_state["document_id"] = document_id
                    st.code(document_id)

                st.write(
                    f"Chunks: {result.get('chunk_count', 'N/A')}"
                )

            else:
                st.error(
                    f"Upload failed: {response.status_code}"
                )
                st.write(response.text)

        except requests.RequestException:
            st.error(
                "Cannot connect to the FastAPI backend."
            )


# =========================
# Ask Question
# =========================

st.divider()

st.subheader("Ask Your Document")
if st.button("Clear Conversation"):
    st.session_state["chat_history"] = []
    st.rerun()
try:
    response = requests.get(
        f"{API_BASE_URL}/documents",
        timeout=30,
    )

    if response.status_code == 200:
        documents = response.json()

    else:
        documents = []

except requests.RequestException:
    documents = []


document_options = {
    document["filename"]: document["document_id"]
    for document in documents
}


selected_filename = st.selectbox(
    "Select Document",
    options=["All Documents"] + list(document_options.keys()),
)
if "previous_selected_document" not in st.session_state:
    st.session_state["previous_selected_document"] = selected_filename

elif st.session_state["previous_selected_document"] != selected_filename:
    st.session_state["previous_selected_document"] = selected_filename
    st.session_state["chat_history"] = []
    st.rerun()

if selected_filename == "All Documents":
    document_id = None

else:
    document_id = document_options[selected_filename]

question = st.text_area(
    "Question",
    placeholder="Ask a question about your document...",
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        payload = {
            "query": question.strip(),
            "limit": 3,
            "document_id": document_id,
        }

        try:
            with st.spinner(
                "Searching and generating answer..."
            ):
                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json=payload,
                    timeout=120,
                )

            if response.status_code == 200:
                result = response.json()

                # Save result in session state
                if "chat_history" not in st.session_state:
                    st.session_state["chat_history"] = []

                st.session_state["chat_history"].append(
                    {
                        "question": question.strip(),
                        "answer": result.get(
                            "answer",
                            "No answer returned.",
                        ),
                        "sources": result.get(
                            "sources",
                            [],
                        ),
                    }
                )

            else:
                st.error(
                    f"Question failed: {response.status_code}"
                )
                st.write(response.text)

        except requests.RequestException:
            st.error(
                "Cannot connect to the FastAPI backend."
            )


# =========================
# Display Last Answer
# =========================

if "chat_history" in st.session_state:
    st.divider()
    st.subheader("Conversation")

    for item in st.session_state["chat_history"]:
        with st.chat_message("user"):
            st.write(item["question"])

        with st.chat_message("assistant"):
            st.write(item["answer"])

            sources = item.get("sources", [])

            if sources:
                st.markdown("**Sources**")

                for source in sources:
                    if isinstance(source, dict):
                        filename = source.get(
                            "source",
                            source.get(
                                "filename",
                                "Unknown source",
                            ),
                        )

                        page = source.get("page")

                        if page is not None:
                            st.write(
                                f"📄 {filename} — Page {page}"
                            )
                        else:
                            st.write(
                                f"📄 {filename}"
                            )

                    else:
                        st.write(
                            f"📄 {source}"
                        )