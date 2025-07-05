from llm_utils import clean_and_structure_text

# Replace with your actual OCR output
ocr_text = """
DLNo. TG/22/02/2015/-11374
GSTIN :
36ABBPB3ASACAZF
DLNo.
TG/22/02/2015/-11375
CASH BILL
Date.
3ol<ly:
No_
PVR MEDICALS
183
Chemists & Druggist
Ganesh Temple, M.G Road, KOTHAGUDEM-507 101.
Patient's Name.
XlKri_Shma(_ AcutAddress:
Prescribed By:
2
Bladi
M(EM
Name
Batch
Amount
Qty:
PARTICULARS
Sch:
of Mfr
No
Date
Rs
Ps
6
Aua_4y
CV:
Fs)
4 (
33/14
6
Dololana (
#
nle
6K3
Wu
6 ; l
9
52
3
1f oe €
38
0)
1y
)x
cbvz
M
041
42a
A8B1cALS
Signature:
Gane Inclusive Taxes G Rc
4, 429 /20 _
Otkagunfratc
Opp:
Nm
Exp-
JA/
31X
sl
0
Aop
4/w
Mex
K/2
"""

structured_output = clean_and_structure_text(ocr_text)
print("Structured JSON Output : ")
print(structured_output)