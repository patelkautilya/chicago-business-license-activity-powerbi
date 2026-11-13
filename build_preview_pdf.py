"""Combine the two Power BI export images into a printable report preview."""

from pathlib import Path

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
IMAGES = [
    ROOT / "previews" / "activity_overview.png",
    ROOT / "previews" / "license_community_mix.png",
]
OUTPUT = ROOT / "previews" / "chicago_business_license_activity_preview.pdf"
PAGE_SIZE = (960, 540)  # Power BI export aspect ratio, 16:9


def main() -> None:
    pdf = canvas.Canvas(str(OUTPUT), pagesize=PAGE_SIZE)
    pdf.setTitle("Chicago Business License Activity | Power BI Report Preview")
    pdf.setAuthor("Kautilya Patel")
    for image in IMAGES:
        if not image.is_file():
            raise FileNotFoundError(image)
        pdf.drawImage(str(image), 0, 0, width=PAGE_SIZE[0], height=PAGE_SIZE[1])
        pdf.showPage()
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
