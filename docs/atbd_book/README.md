# Build Instructions for ATBD LaTeX and PDF

This document describes the steps to build the LaTeX (`.tex`) document and generate the patched PDF for the **Algorithm Theoretical Baseline Document (ATBD)**.

---

## 1. Setup Environment

Follow the instructions in the main `README.md` of the repository to create and activate a suitable environment for building the documentation.

---

## 2. Navigate to the Book Directory

Change directory to the ATBD book repository:

```
cd docs/atbd_book
```

---

## 3. Modify the Cover Page (Optional)

If you need to update the cover page:

1. Go to the cover page directory:

```
cd _static/cover_page
```

2. Compile the cover page:

```
xelatex main.tex
```

3. Verify that the cover is correct. Once confirmed, copy the generated PDF:

```
cp main.pdf ../cover.pdf
```

---

## 4. Build the Book

Execute the following commands to clean and build the Jupyter Book:

```
jb clean .
rm -rf _build/
jb build . --all
echo | jb build . --builder pdflatex > build.log 2>&1
```

---

## 5. Patch the LaTeX File

Run the patching script to modify the `.tex` file for headers, footers, and other customizations:

```
./patch_texfile.sh
```

---

## 6. Compile the LaTeX Document

Change to the LaTeX build folder:

```
cd _build/latex
```

Compile the `.tex` document **twice** (only one `.tex` file should be present):

```
xelatex -interaction=batchmode *tex > tex_to_pdf.log
xelatex -interaction=batchmode *tex > tex_to_pdf.log
```

This ensures proper references, page numbers, and table of contents.

---

## 7. Complete Build Command (After Cover Is Ready)

For convenience, the complete build process can be executed with a single command:

```
jb clean .; rm -rf _build/; jb build . --all; echo | jb build . --builder pdflatex > build.log 2>&1; ./patch_texfile.sh; cd _build/latex; xelatex -interaction=batchmode *tex > tex_to_pdf.log; xelatex -interaction=batchmode *tex > tex_to_pdf.log
```
