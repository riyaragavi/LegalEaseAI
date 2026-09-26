import requests
import gradio as gr


BACKEND_URL = "http://127.0.0.1:8000"


def generate_document(
    document_type,
    language,
    jurisdiction,
    parties,
    effective_date,
    terms
):

    if not parties.strip():
        return "Please enter the parties involved."

    if not terms.strip():
        return "Please enter the terms and conditions."

    payload = {
        "document_type": document_type,
        "parties": parties,
        "effective_date": effective_date,
        "jurisdiction": jurisdiction,
        "language": language,
        "terms": terms,
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/generate",
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            return response.json()["content"]

        return f"Backend error: {response.text}"

    except requests.exceptions.ConnectionError:
        return "Could not connect to FastAPI. Please make sure the backend is running."

    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."

    except Exception as exc:
        return f"Unexpected error: {exc}"


def export_document(content, document_type, export_type):

    if not content.strip():
        return None

    payload = {
        "content": content,
        "document_type": document_type
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/export/{export_type}",
            json=payload,
            timeout=60
        )

        if response.status_code == 200:

            filename = f"legalease_document.{export_type}"

            file_path = filename

            with open(file_path, "wb") as file:
                file.write(response.content)

            return file_path

        return None

    except Exception:
        return None


def export_txt(content, document_type):
    return export_document(content, document_type, "txt")


def export_docx(content, document_type):
    return export_document(content, document_type, "docx")


def export_pdf(content, document_type):
    return export_document(content, document_type, "pdf")


with gr.Blocks(title="LegalEase") as demo:

    gr.Markdown(
        """
        # ⚖️ LegalEase

        ### AI-Powered Legal Document Generator

        > **Important:** LegalEase creates AI-generated legal document
        > drafts for informational and drafting purposes. Always review
        > important documents with a qualified legal professional.
        """
    )

    with gr.Row():

        with gr.Column():

            document_type = gr.Dropdown(
                choices=[
                    "Employment Contract",
                    "Non-Disclosure Agreement",
                    "Lease Agreement",
                    "Freelance Contract",
                    "Service Agreement",
                    "Partnership Agreement",
                    "Offer Letter",
                    "General Agreement",
                    "Custom Legal Document"
                ],
                value="Employment Contract",
                label="Document Type"
            )

            language = gr.Dropdown(
                choices=[
                    "English",
                    "Tamil",
                    "Hindi",
                    "Malayalam",
                    "Telugu",
                    "Kannada"
                ],
                value="English",
                label="Language"
            )

            jurisdiction = gr.Textbox(
                value="India",
                label="Jurisdiction"
            )

            parties = gr.Textbox(
                label="Parties Involved",
                placeholder=(
                    "Example:\n"
                    "Riya (Employee)\n"
                    "ABC Technologies Pvt. Ltd. (Employer)"
                ),
                lines=6
            )

            effective_date = gr.Textbox(
                label="Effective Date",
                placeholder="DD/MM/YYYY"
            )

            terms = gr.Textbox(
                label="Terms & Conditions",
                placeholder=(
                    "Enter each term on a new line.\n\n"
                    "- Salary shall be paid monthly.\n"
                    "- Employee must maintain confidentiality.\n"
                    "- Either party may terminate with 30 days notice."
                ),
                lines=8
            )

            generate_button = gr.Button(
                "✨ Generate Legal Document",
                variant="primary"
            )

        with gr.Column():

            generated_document = gr.Textbox(
                label="📄 Generated Document",
                lines=25
            )

    generate_button.click(
        fn=generate_document,
        inputs=[
            document_type,
            language,
            jurisdiction,
            parties,
            effective_date,
            terms
        ],
        outputs=generated_document
    )

    gr.Markdown("### ⬇️ Download Document")

    with gr.Row():

        txt_button = gr.Button("Prepare TXT")
        docx_button = gr.Button("Prepare DOCX")
        pdf_button = gr.Button("Prepare PDF")

    txt_file = gr.File(label="TXT Download")
    docx_file = gr.File(label="DOCX Download")
    pdf_file = gr.File(label="PDF Download")

    txt_button.click(
        fn=export_txt,
        inputs=[generated_document, document_type],
        outputs=txt_file
    )

    docx_button.click(
        fn=export_docx,
        inputs=[generated_document, document_type],
        outputs=docx_file
    )

    pdf_button.click(
        fn=export_pdf,
        inputs=[generated_document, document_type],
        outputs=pdf_file
    )


if __name__ == "__main__":

    demo.launch(
        server_name="127.0.0.1",
        server_port=7860
    )