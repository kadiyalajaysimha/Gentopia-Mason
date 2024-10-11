from typing import AnyStr
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
import requests
import io

class PDFReaderArgs(BaseModel):
    pdf_url: str = Field(..., description="url of the pdf file")


class PDFReader(BaseTool):
    """Tool that adds the capability to read pdf files."""

    name = "pdf_read"
    description = ("Read from a pdf"
                   "Input should be the url of the pdf.")

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, pdf_url: AnyStr) -> str:
        res = requests.get(pdf_url)
        if res.status_code != 200:
            raise Exception("Error while retrieving the pdf from the url: " + pdf_url)
        reader = PdfReader(io.BytesIO(res.content))
        pdfContent = ""
        i = 0
        while i < len(reader.pages):
            currentPage = reader.pages[i]
            pdfContent += currentPage.extract_text()
            i += 1
        return pdfContent

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PDFReader()._run("Attention for transformer")
    print(ans)