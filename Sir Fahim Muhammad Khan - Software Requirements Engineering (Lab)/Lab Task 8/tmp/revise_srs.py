"""Build the revised document and an equivalent standalone LaTeX source.

This script operates only on the SRS artifacts in the lab workspace.
"""
from pathlib import Path
import re
import json
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
source=(ROOT/'tmp/build_srs.py').read_text(encoding='utf-8')
source=source.replace("dest=OUT/'Enterprise RAG Assistant SRS.docx'", "dest=OUT/'Enterprise RAG Assistant SRS Revised.docx'")
scope={'__file__':str(ROOT/'tmp/build_srs.py'),'__name__':'__srs_build__'}
exec(compile(source,'build_srs.py','exec'),scope)
doc=scope['doc']

def remove(element):
    parent=element.getparent()
    if parent is not None:parent.remove(element)

def replace(para,text):
    # Preserve the label emphasis while replacing the sentence as a whole.
    was_bold=bool(para.runs and para.runs[0].bold)
    para.clear()
    if was_bold and '. ' in text and not re.match(r'FR-\d',text):
        first,rest=text.split('. ',1)
        para.add_run(first+'. ').bold=True
        para.add_run(rest)
    else:
        para.add_run(text).bold=was_bold

revisions={
 'This specification defines the intended first release': 'This SRS defines the planned first release of Enterprise RAG Assistant and its acceptance criteria. Document approval establishes the requirements baseline; product acceptance follows implementation and verification.',
 'Interpretation.': 'Interpretation. Shall denotes a requirement, should a desired behaviour, and may an option. Provisional targets require the measurement conditions in Section 6.3 before acceptance.',
 'Requirement control.': 'Requirement control. FR-01 to FR-13 and NFR-01 to NFR-07 retain their existing identifiers. BR, IR, DR, and DC identify supporting business, interface, data, and operating rules.',
 'Priority.': 'Priority. High marks a version 1 obligation. Medium marks a provisional quality target. These priorities are subject to review.',
 'Enterprise RAG Assistant helps employees': 'Enterprise RAG Assistant answers employee questions from approved company documents. This SRS defines its required behaviour, permissions, interfaces, data rules, and quality targets. It gives the owner, developer, tester, and course reviewer a common basis for implementation and acceptance.',
 'The intended readers are': 'The owner uses the SRS to control scope. Developers use Section 3 to implement the system; testers and reviewers use Section 6 to check coverage and record results.',
 'The product accepts employee questions': 'The assistant accepts questions in English and returns answers supported by documents the employee may access. A substantive answer includes a source citation. If the available evidence is insufficient, the system returns a generic not-found result.',
 'Version 1 includes offline': 'Version 1 covers offline Markdown and text-based PDF ingestion, department tagging, signed-token login, restricted question answering, a REST API, browser chat, query metrics, evaluation, and a deployed demo. Acme Corp is a fictional company represented by selected public GitLab Handbook pages.',
 'Voice interaction, multilingual support': 'Voice, multilingual support, native mobile apps, model training, document editing through chat, live company-system synchronisation, SSO, and multi-tenant hosting are excluded. OCR for scanned PDFs is a possible later extension.',
 'The following sources establish': 'References R1 and R2 supply the course structure; R3 to R6 establish the project baseline. R1 discusses ISO/IEC/IEEE 29148, and R2 identifies its outline as adapted from IEEE Std 830-1993. This SRS follows the supplied guidance without claiming certified conformity.',
 'Project repository:': 'Project repository: https://github.com/abdulsamad-codes/enterprise-rag-assistant. References R3 to R6 are in the project repository; the supplied PDFs accompany this document.',
 'Section 2 explains': 'Section 2 sets the product context and release boundary. Section 3 specifies behaviour and quality. Sections 4 and 5 govern changes and approval. Section 6 holds verification, traceability, provenance, and unresolved decisions.',
 'The assistant is a standalone': 'The assistant serves one organisation and supplements its document collection. It does not edit policies or perform the payroll, leave, purchasing, or other transactions described in them. Employees follow the cited policy and its existing approval process.',
 'The system boundary includes': 'The system includes ingestion, authentication, access filtering, retrieval, generation, citation checking, the API, chat, logging, and evaluation. It reads approved files offline. At query time, the external model service receives the question and authorised evidence; the assistant does not browse the live handbook.',
 'Table 1 defines': 'The table describes the external context. Internal retrieval and storage components are specified in R4.',
 'The employee interface communicates': 'The employee interface uses the API for login and questions. Ingestion reads local files; evaluation exercises the system under recorded roles. Version 1 has no payroll, HR-system, SSO-provider, or live document-management integration.',
 'Employees use a browser-based': 'Employees use login and chat screens showing questions, answers, citations, and request outcomes. They cannot assign themselves another role or add files to the approved collection. Operators use command-line ingestion and evaluation tools.',
 'The system has no specialised': 'No specialised hardware interfaces are required. The application uses ordinary storage, networking, and a browser; it does not control external devices.',
 'The application exchanges requests': 'The backend exchanges requests with a hosted model service. R4 selects Groq behind a replaceable client interface. Storage engines, retrieval libraries, and the UI framework are internal design choices. Provider versions and limits are deployment settings subject to OD-03 and OD-04.',
 'The deployed UI and API': 'The deployed client and API communicate over HTTPS; authenticated requests carry a bearer token. The backend needs outbound access to the model provider. No custom device or messaging protocol is used.',
 'No fixed RAM or storage': 'RAM, storage, throughput, and concurrent-user limits are not yet baselined. They will be measured against the selected models, document collection, and host under OD-01.',
 'The first release has separate': 'The operator prepares documents offline while serving is stopped. After ingestion, the service restarts and checks consistency between the chunk collection and retrieval indexes. Employees then log in and ask questions. Evaluation is a separate operator-run activity.',
 'Evaluation is an operator-run': 'Retention, backup, and recovery arrangements remain open under OD-02. Continuous service during document updates is outside the first-release commitment.',
 'Before deployment, the operator': 'The operator configures source paths, department mapping, accounts, provider credentials, storage, retrieval settings, and content logging. Private company deployment also requires an agreed access map and approval of the provider data flow. No physical site changes are required.',
 'Employee users are expected': 'Employees need English reading skills and ordinary browser experience, not knowledge of retrieval or language models. The roles below determine permissions, not technical skill. The operator must be able to configure the deployment and run its command-line tools.',
 'The operator is an operational': 'Operator is a maintenance responsibility, not a fifth employee role. The handbook is public; its access restrictions are simulated for this project.',
 'The requirements are based': 'The baseline comes from the owner’s goals and project specification; no enterprise stakeholder interview has been completed. The operator is responsible for source accuracy, approval, and classification.',
 'Users are assumed to have': 'Employees need a browser and network access; generation depends on the model provider. Roles are trusted only after backend verification. A revoked account may retain access until its token expires; immediate revocation is deferred.',
 'The original quality thresholds': 'Quality targets remain provisional until the environment and scoring protocol are recorded. Changes to these assumptions follow Section 4.',
 'An item listed for a later': 'Later-release capabilities require an approved scope change before becoming version 1 obligations.',
 'The requirements in this section': 'This section specifies the complete planned version 1. All functional and supporting rules are High priority. NFR priorities are stated separately. Source references identify their basis; verification IDs name planned procedures, not completed tests.',
 'No fixed screen resolution': 'Browser support, screen assumptions, and accessibility scope remain OD-07. The required login, question, answer, and citation interactions apply regardless of the final layout.',
 'No direct hardware interfaces': 'No direct hardware interfaces apply. Host capacity is governed by OD-01.',
 'The question field is text.': 'The question field is text. Final JSON fields, credential format, input limits, error codes, and invalid-input behaviour remain OD-04. These must be fixed before API-contract approval.',
 'There is no application-specific': 'Provider secrets belong in deployment configuration. Timeouts, retries, and service-error messages remain OD-04.',
 'The feature descriptions below': 'Each feature states its purpose and operating context, followed by requirements and acceptance criteria. Original IDs are retained for traceability to R3.',
 'Exception handling.': 'Exception handling. Malformed, excluded, or unmapped paths receive no default department. Ingestion errors must not expose unclassified content. Corrupt-file handling and partial-run reporting remain OD-04.',
 'The design calls for bounded': 'Evaluation uses bounded concurrency, backoff for provider rate limits, and resumable cached results as specified in R4. Cache reuse must preserve role, source-revision, and configuration boundaries. Numeric settings remain open.',
 'The excluded source prefixes': 'finance/readmes and finance/jihu-support are excluded case-insensitively. Approved mapping matches are case-sensitive; the complete path map remains in R5.',
 'These targets retain the existing': 'The following targets are provisional. The measured environment, workload, scoring method, and cost basis must be recorded before a pass is declared.',
 'The first demonstration uses': 'The 190-document demo is a reproducible dataset, not a production-capacity limit. Concurrency, throughput, and memory remain OD-01; input-size limits remain OD-04. One API worker does not imply one user.',
 'The logical information model': 'Each document belongs to one department and has a checksum for its ingested revision. It produces chunks referenced by citations and query records. Retrieval indexes derive from the authoritative chunk collection.',
 'Rules DR-01 and DR-02': 'DR-01 and DR-02 derive from FR-02 and R4 Section 5; DR-03 to DR-05 from R4 Section 3.1; DR-06 from R5; DR-07 from FR-08. The current ID convention uses the source path for document_id and a suffix such as #000 for chunk_id.',
 'Documents remain in the approved': 'Offline ingestion removes obsolete documents and chunks. Log retention, record deletion, and backup policy remain OD-02; credential storage remains OD-03.',
 'The SRS records established': 'R4 selects Python, FastAPI, Streamlit, SQLite, ChromaDB, BM25, local embeddings, a reranker, and Groq. These are design choices, subject to review if the SRS behaviour is preserved. The following operating constraints already affect the baseline.',
 'This document uses the supplied': 'The document follows the supplied course guidance and template. The project records the handbook under CC BY-SA 4.0 and retains its attribution. No regulatory, accessibility, or security certification is claimed.',
 'The product is a document-information': 'Any domain-specific compliance obligations for a real deployment must be identified before that deployment is approved.',
 'Reliability is evaluated through': 'FR-06 refuses unsupported questions, FR-13 suppresses answers without valid citations, and DR-05 blocks inconsistent serving data. QT-01 evaluates the support for generated claims. No MTBF target has been agreed.',
 'No numerical mean-time-between': 'Provider and infrastructure failures are service errors, not evidence that an answer is absent. Recovery and timeout behaviour remain OD-04.',
 'The demonstration is available': 'The demo depends on its host and model provider. Updates stop and restart the service. No uptime percentage, recovery-time objective, or recovery-point objective is approved; OD-02 and OD-06 cover these decisions.',
 'Security also depends': 'Access security is specified by FR-05 and FR-10 to FR-13. A public not-found result must not expose a restricted source. Client deployments disable content logging by default; automatic personal-data masking is deferred.',
 'A valid token expires': 'The design expires tokens after 30 minutes; immediate revocation is not guaranteed. Credential protection, provisioning, signing, browser token handling, and provider data handling remain OD-03 and OD-04.',
 'The established design isolates': 'The design uses replaceable model and vector-store interfaces and one role-policy table. A component change must preserve access, refusal, and citation behaviour and pass the affected acceptance checks.',
 'No numerical code-complexity': 'No numerical complexity, coverage, or repair-time target is agreed. Maintainability review checks interface separation and continued use of the acceptance procedures.',
 'Development uses Windows': 'Development uses Windows and PowerShell; tests are intended to remain compatible with Linux. The supported deployment and browser matrix remains OD-06 and OD-07.',
 'IR-01 requires the basic': 'IR-01 defines the basic employee interactions. A measured usability target and accessibility conformance level are not approved; OD-07 records the required decisions.',
 'The one-worker deployment': 'Capacity is measured under OD-01. Multi-worker serving, finer permissions, and multiple organisations belong to later releases.',
 'Section 3.2 uses the feature': 'Section 3.2 follows the template’s feature organisation. Its alternative outlines by mode, user class, object, stimulus, response, functional hierarchy, and use case are not additional required functions and are not duplicated.',
 'A not-found result is an ordinary': 'Not found is distinct from invalid authentication, invalid input, and service failure. Citation membership confirms which evidence was supplied; faithfulness evaluation checks whether that evidence supports the answer.',
 'A proposed change is recorded': 'A change request is recorded in a repository issue or equivalent written record. It identifies affected IDs, revised wording, the reason, and expected scope impact. Informal discussion alone does not alter the baseline.',
 'The project owner checks': 'The owner reviews the effect on permissions, data, interfaces, implementation, verification, cost, and schedule. Access changes require revised denial tests. Performance changes need an agreed protocol or measurements.',
 'For this individual project': 'Abdul Samad records acceptance, rejection, or deferral of each request. Changes to an academically approved baseline are submitted to the course reviewer when review is required. This procedure takes effect on document approval.',
 'An accepted change updates': 'An accepted change updates the requirement, verification, traceability, relevant design, and revision history. Unchanged obligations retain their IDs; withdrawn IDs are not reused. Approved document versions are retained with their implementation and test references.',
 'No change approvals are implied': 'Proposed rules and provisional targets are not approval records.',
 'Approval confirms that': 'Approval records agreement on the identified document version. Signatures and dates remain blank until review. Academic approval does not represent enterprise-customer approval.',
 'The reviewer checks scope': 'Review covers scope, clarity, permissions, sources, and verification. A draft may retain open decisions, but operational acceptance must identify their resolution or explicit deferral.',
 'Document approval and product': 'Product acceptance is recorded separately after testing. The record identifies the product revision, dataset, configuration, environment, procedures, results, unresolved defects, and final decision.',
 'Sections 6.1 and 6.2': 'Sections 6.1 and 6.2 define verification and traceability. Section 6.3 controls open decisions. Sections 6.4 to 6.6 provide provenance, implementation context, and a subject index.',
 'Verification uses tests': 'Verification combines tests, inspection, analysis, and demonstration. The core evaluation file, eval/questions.csv, contains the planned 30 questions, with expected answers derived from the pinned source pages.',
 'The 30 questions are the original': 'Authentication, injection, citation, integrity, and interface fixtures supplement the 30 questions. Permission tests cover every role and allowed/denied department pair, not only the six core refusal questions.',
 'Acceptance rule.': 'Acceptance rule. Required procedures must produce their expected evidence. Any restricted-content leak fails safety acceptance. Provisional targets require approved measurement conditions; failures and unexecuted checks remain in the report.',
 'Comparison control.': 'Comparison control. Vector-only, hybrid, and hybrid-plus-reranker runs use the same dataset and question set, with their configuration and threshold recorded. Reports include false refusals and false answers.',
 'The matrix links each original': 'The matrix links each baseline requirement to its source, SRS section, and verification. Supporting obligations are grouped below it.',
 'The following values and policies': 'The owner records the decisions below before approving the affected acceptance results. Undecided values do not mean unlimited capacity or indefinite retention.',
 'No real enterprise customer': 'Enterprise stakeholder validation and the signatures in Section 5 remain outstanding.',
 'The demonstration uses the public': 'The dataset uses GitLab Handbook commit 2c77a1f5b8c8a80cb7b5151ff11cfad84f98bfbb, downloaded on 11 October 2026 according to R5. Selected files are copied unchanged to the local department folders and excluded from Git.',
 'Selection uses a minimum': 'Each selected page has at least 150 real words after the documented exclusions. Deterministic round-robin selection spreads topics; the manifest is sorted by source path. SHA-256 checksums normalise CRLF to LF.',
 'The reviewed application source': 'The reviewed source implements role permissions, department-path mapping, deterministic page selection, checksums, and Markdown chunking with front-matter removal. Title extraction and the complete citation metadata are still in progress.',
 'The authenticated API, chat UI': 'The API, chat, storage, retrieval, generation, logging, evaluation, Docker setup, and live demo remain planned work. Their inclusion in the SRS states the intended release, not completed delivery.'
}

delete_prefixes=[
 'Source and priority.', 'Dependencies.',
 'Existing code and tests demonstrate implementation progress',
]

for para in list(doc.paragraphs):
    text=para.text
    if any(text.startswith(prefix) for prefix in delete_prefixes):
        remove(para._p);continue
    for prefix,new in revisions.items():
        if text.startswith(prefix):replace(para,new);break
    if para.text=='Version 1.0':replace(para,'Version 1.1')
    if para.text=='27 October 2026':replace(para,'28 October 2026')
    if para.text=='6.6 Subject Index':para.paragraph_format.page_break_before=False

# Merge each feature's context into two compact paragraphs.
current=''
contexts={
 '3.2.1': ('Purpose. Prepare approved documents while retaining source identity and department classification.',
           'Operating context. The operator runs ingestion while serving is stopped. The folder must be readable and source paths mapped. Ingestion extracts text, prepares labelled chunks, updates changed documents, and removes deleted sources.'),
 '3.2.2': ('Purpose. Authenticate employees and enforce their permissions before evidence reaches generation.',
           'Operating context. A valid demo account has an assigned role. Login issues a signed token; the backend verifies it on each question and selects permitted departments. Unknown roles receive no fallback access. The design sets a 30-minute expiry.'),
 '3.2.3': ('Purpose. Answer from permitted evidence and refuse unsupported conclusions.',
           'Operating context. An authenticated employee submits a question to a ready service. Relevant permitted passages are assessed for sufficiency. Insufficient evidence produces not found; supported generation proceeds to citation checking.'),
 '3.2.4': ('Purpose. Trace each substantive answer to evidence actually supplied for generation.',
           'Operating context. The generator returns an answer and citation IDs. The system retains only IDs from the supplied chunks. If none remain, it suppresses the answer and returns not found without another model call to repair citations.'),
 '3.2.5': ('Purpose. Record query metrics and measure the quality and safety of answering.',
           'Operating context. Query completion writes metrics under the configured privacy setting. An operator runs evaluation under recorded roles and reports outcomes against the pinned dataset and configuration.'),
}
for para in list(doc.paragraphs):
    if para.style.name=='Heading 3':current=para.text.split(' ',1)[0]
    if current in contexts:
        if para.text.startswith('Purpose.'):replace(para,contexts[current][0])
        elif para.text.startswith('Actor and trigger.'):replace(para,contexts[current][1])
        elif para.text.startswith(('Preconditions.','Sequence and result.')):remove(para._p)

# Remove duplicated acceptance rows; the requirement records already contain AT-01 to AT-13.
for t in list(doc.tables):
    if t.cell(0,0).text=='Procedure' and t.cell(1,0).text=='AT-01':remove(t._tbl)

# Replace the repeated supporting-source matrix with a concise cross-reference.
for t in list(doc.tables):
    if t.cell(0,0).text=='Supporting IDs':
        rows=[
          ['IR-01 to IR-06','R3 FR-05, FR-07, FR-11, FR-12; R4 Sections 2, 4 and 6','3.1','AT-05, AT-07, AT-11, AT-12'],
          ['BR-01 to BR-04','R3 role policy; R4 access filtering; R5 path rules','3.2.6','AT-02, AT-05, AT-11'],
          ['BR-05 to BR-08','R4 thresholds, citations and updates; R5 selection','3.2.6','AT-06, AT-13, DT-01, DT-02'],
          ['DR-01 to DR-07','R3 FR-02, FR-08; R4 data integrity; R5 checksums','3.4','AT-02, AT-08, DT-01, DT-02'],
          ['DC-01 to DC-04','R4 operating and API constraints; R5 provenance','3.5','AT-05, AT-11, DT-01, DT-02, DI-01'],
        ]
        for row in list(t.rows)[1:]:remove(row._tr)
        for rowdata in rows:
            cells=t.add_row().cells
            for cell,text in zip(cells,rowdata):cell.text=text

for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.text=run.text.replace('1.0 | 27 October 2026','1.1 | 28 October 2026')
                    run.text=run.text.replace('Version 0.2.','Version 0.2.').replace('Local review on 27 October 2026.','Project review on 27 October 2026.')
    if t.cell(0,0).text=='Version':
        # Keep the initial baseline and record the substantive revision.
        cells=t.add_row().cells
        vals=['1.1','28 October 2026','Shortened repeated context and verification material; retained baseline requirements, acceptance criteria and open decisions. Added an equivalent LaTeX edition.','Abdul Samad']
        for c,v in zip(cells,vals):c.text=v
    if t.cell(0,0).text=='Ref':
        concise=[
          ('R1','Software Requirement Specification (SRS); supplied course handout, SRS.pdf.','Four pages; date not stated.'),
          ('R2','Software Requirements Specification (SRS) Template; CS3911, supplied PDF.','30 pages; header 08/15/22.'),
          ('R3','Requirements Document: Enterprise RAG Assistant; Abdul Samad; docs/01-requirements.md.','Version 0.2.'),
          ('R4','Design Document: Enterprise RAG Assistant; Abdul Samad; docs/02-design.md.','Version 0.3.'),
          ('R5','Data Sources and manifest; docs/data-sources.md and docs/data-manifest.csv.','Dataset downloaded 11 October 2026.'),
          ('R6','Project README, AGENTS.md, application source, and tests.','Reviewed 27 October 2026.'),
          ('R7','GitLab Handbook; GitLab; source revision and locations in Section 6.4.','Pinned commit in Section 6.4.'),
          ('R8','Handbook attribution record in the project README and R5.','CC BY-SA 4.0; URL in Section 6.4.'),
        ]
        for row,vals in zip(list(t.rows)[1:],concise):
            for c,v in zip(row.cells,vals):c.text=v

# Format for a readable, compact academic report rather than a fixed page-count trick.
normal=doc.styles['Normal']
normal.font.size=Pt(11)
normal.paragraph_format.line_spacing=1.05
normal.paragraph_format.space_after=Pt(5)
for name in ['Heading 1','Heading 2','Heading 3']:
    doc.styles[name].paragraph_format.space_before=Pt(9)
    doc.styles[name].paragraph_format.space_after=Pt(5)
for para in doc.paragraphs:
    if para.style.name=='Normal':
        para.paragraph_format.keep_with_next=False
        para.paragraph_format.keep_together=False
    para.paragraph_format.widow_control=True
    if para.text=='6.6 Subject Index':para.paragraph_format.page_break_before=False
for i,para in enumerate(doc.paragraphs):
    if re.match(r'^FR-\d{2} ',para.text):
        for part in doc.paragraphs[i:i+2]:part.paragraph_format.keep_with_next=True
    if para.text.startswith('Purpose.'):
        para.paragraph_format.keep_with_next=True
for t in doc.tables:
    for j,row in enumerate(t.rows):
        for cell in row.cells:
            pr=cell._tc.get_or_add_tcPr()
            for old in list(pr):
                if old.tag in [qn('w:tcBorders'),qn('w:tcMar')]:pr.remove(old)
            borders=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                node=OxmlElement('w:'+side)
                node.set(qn('w:val'),'single');node.set(qn('w:sz'),'4');node.set(qn('w:color'),'D9D9D9')
                borders.append(node)
            pr.append(borders)
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                node=OxmlElement('w:'+side);node.set(qn('w:w'),'85');node.set(qn('w:type'),'dxa');margins.append(node)
            pr.append(margins)
            for para in cell.paragraphs:
                para.paragraph_format.keep_with_next=(j==0)
                para.paragraph_format.space_before=Pt(2)
                para.paragraph_format.space_after=Pt(2)
                para.paragraph_format.line_spacing=1.02
                for run in para.runs:run.font.size=Pt(10.5)
    # Keep small tables together without stranding long tables on the next page.
    if len(t.rows)<=5:
        for row in t.rows[:-1]:
            for cell in row.cells:
                for para in cell.paragraphs:para.paragraph_format.keep_with_next=True

for section in doc.sections:
    for para in section.footer.paragraphs:
        for run in para.runs:
            if 'Version 1.0' in run.text:run.text=run.text.replace('Version 1.0','Version 1.1')
doc.core_properties.version='1.1'
doc.core_properties.comments=''
dest=OUT/'Enterprise RAG Assistant SRS Revised.docx'
doc.save(dest)

# Serialize one content model for LaTeX and content-parity checks.
blocks=[]
for child in doc.element.body:
    if child.tag==qn('w:p'):
        para=Paragraph(child,doc)
        if para.text.strip():
            blocks.append({'kind':'paragraph','style':para.style.name,'text':para.text,
                           'bold':bool(para.runs and para.runs[0].bold)})
    elif child.tag==qn('w:tbl'):
        t=Table(child,doc)
        blocks.append({'kind':'table','rows':[[c.text for c in r.cells] for r in t.rows],
                       'widths':[float(c.width or 1) for c in t.columns]})
(ROOT/'tmp'/'srs-revised-content.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')

def tex(s):
    s=s.replace('\u2019',"'").replace('\u2018',"'").replace('\u201c','"').replace('\u201d','"').replace('\u2013','--').replace('\u2014','---')
    chars={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}
    # URLs and the pinned hash can break safely across narrow cells.
    parts=re.split(r'(https?://[^\s,;]+|\b[0-9a-f]{40}\b)',s)
    result=[]
    for part in parts:
        if part.startswith(('https://','http://')):
            suffix=''
            if part.endswith('.'):part=part[:-1];suffix='.'
            result.append(r'\url{'+part+'}'+suffix)
        elif re.fullmatch(r'[0-9a-f]{40}',part):result.append(r'\nolinkurl{'+part+'}')
        else:result.append(''.join(chars.get(c,c) for c in part))
    return ''.join(result).replace('\n',r'\newline ')

prefix=r'''% Enterprise RAG Assistant SRS
% Compile main.tex with pdfLaTeX twice, or use latexmk -pdf main.tex.
% Content edition 1.1 dated 28 October 2026.
\documentclass[11pt,letterpaper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx}
\usepackage[margin=0.8in,headheight=14pt]{geometry}
\usepackage{array,longtable,booktabs}
\usepackage[table]{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{needspace}
\usepackage{microtype}
\usepackage{xurl}
\usepackage[hidelinks,bookmarksnumbered,pdfauthor={Abdul Samad},pdftitle={Enterprise RAG Assistant Software Requirements Specification}]{hyperref}
\usepackage{lastpage}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\linespread{1.05}
\setlength{\emergencystretch}{2em}
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.13}
\setlength{\LTpre}{6pt}
\setlength{\LTpost}{7pt}
\arrayrulecolor{black!20}
\setlist[itemize]{leftmargin=1.5em,itemsep=2pt,topsep=3pt}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\titleformat{\section}{\large\bfseries}{\thesection}{0.6em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.6em}{}
\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{12pt}{6pt}
\titlespacing*{\subsection}{0pt}{10pt}{5pt}
\titlespacing*{\subsubsection}{0pt}{9pt}{4pt}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize Enterprise RAG Assistant}
\fancyhead[R]{\footnotesize Software Requirements Specification}
\fancyfoot[R]{\footnotesize Version 1.1\quad Page \thepage\ of \pageref{LastPage}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}
\begin{document}
\begin{titlepage}
\centering
{\bfseries Institute of Management Sciences, Peshawar\par}
\vspace{6pt}
BS Software Engineering\par
Software Requirements Engineering Lab\par
\vspace{1.0cm}
{\LARGE\bfseries Enterprise RAG Assistant\par}
\vspace{9pt}
{\Large Software Requirements Specification\par}
\vspace{9pt}
Version 1.1\par
Complete planned version 1\par
\vspace{1.0cm}
Prepared by\par
{\bfseries Abdul Samad\par}
Student ID 243203624\par
\vspace{9pt}
Submitted to\par
{\bfseries Sir Fahim Muhammad Khan\par}
28 October 2026\par
\vspace{1.0cm}
Status: Prepared for review and approval\par
\end{titlepage}
\setcounter{page}{2}
'''

body=[]
started=False
in_bullets=False
for block in blocks:
    if block['kind']=='paragraph' and block['text']=='Document Control':started=True
    if not started:continue
    if in_bullets and not (block['kind']=='paragraph' and block['style']=='List Bullet'):
        body.append(r'\end{itemize}');in_bullets=False
    if block['kind']=='table':
        rows=block['rows'];n=len(rows[0]);w=block['widths'];total=sum(w)
        fractions=[x/total for x in w]
        colspec='|'.join('P{'+f'{fraction:.4f}'+r'\dimexpr\linewidth-'+str(2*n)+r'\tabcolsep-'+str(n+1)+r'\arrayrulewidth\relax}' for fraction in fractions)
        # Multiplying dimexpr requires a parenthesised width computed by TeX length arithmetic.
        available=r'\dimexpr\linewidth-'+str(2*n)+r'\tabcolsep-'+str(n+1)+r'\arrayrulewidth\relax'
        colspec='|'.join(r'P{\dimexpr'+f'{fraction:.4f}'+r'\linewidth-'+f'{fraction*2*n:.4f}'+r'\tabcolsep-'+f'{fraction*(n+1):.4f}'+r'\arrayrulewidth\relax}' for fraction in fractions)
        colspec='|'+colspec+'|'
        header=' & '.join(r'\textbf{'+tex(s)+'}' for s in rows[0])+r' \\ \hline'
        body.extend([r'\begingroup\small',r'\begin{longtable}{'+colspec+'}',r'\hline\rowcolor{black!8}',header,r'\endfirsthead',r'\hline\rowcolor{black!8}',header,r'\endhead',r'\hline\endfoot',r'\hline\endlastfoot'])
        for row in rows[1:]:body.append(' & '.join(tex(s) for s in row)+r' \\ \hline')
        body.extend([r'\end{longtable}',r'\endgroup'])
        continue
    text=block['text'];style=block['style']
    if text=='Document Control':body.extend([r'\section*{Document Control}',r'\addcontentsline{toc}{section}{Document Control}']);continue
    if text=='Revision History':body.append(r'\subsection*{Revision History}');continue
    if text=='Table of Contents':body.extend([r'\clearpage',r'\tableofcontents',r'\clearpage']);continue
    if style.startswith('Heading '):
        level=int(style[-1]);title=re.sub(r'^\d+(?:\.\d+)*\s+','',text)
        if level==1:body.append(r'\clearpage')
        body.append('\\'+['section','subsection','subsubsection'][level-1]+'{'+tex(title)+'}')
    elif style=='List Bullet':
        if not in_bullets:body.append(r'\begin{itemize}');in_bullets=True
        body.append(r'\item '+tex(text))
    elif re.match(r'^FR-\d{2} ',text):
        body.append(r'\Needspace{7\baselineskip}')
        body.append(r'\textbf{'+tex(text)+'}'+r'\par')
    elif block['bold'] and '. ' in text:
        lead,rest=text.split('. ',1)
        body.append(r'\textbf{'+tex(lead)+'.} '+tex(rest)+r'\par')
    elif block['bold']:body.append(r'\textbf{'+tex(text)+'}'+r'\par')
    else:body.append(tex(text)+r'\par')
if in_bullets:body.append(r'\end{itemize}')
latex=prefix+'\n\n'.join(body)+'\n\\end{document}\n'
latex_dir=OUT/'Enterprise RAG Assistant LaTeX'
(latex_dir/'main.tex').write_text(latex,encoding='utf-8')
(latex_dir/'README.txt').write_text('Enterprise RAG Assistant SRS - LaTeX edition 1.1\n\nOpen main.tex in Overleaf or another LaTeX editor. Select pdfLaTeX and compile twice so the contents and page references update.\n\nLocal build:\n  latexmk -pdf main.tex\nOr:\n  pdflatex main.tex\n  pdflatex main.tex\n\nAll content is contained in main.tex. No external images or bibliography files are required. The document uses standard LaTeX packages listed in its preamble.\n\nThis edition shares the revised SRS content with the Word edition. Font metrics may produce a different page count. Open decisions in Section 6.3 remain pending approval.\n',encoding='utf-8')
print('REVISED',dest)
print('WORDS',sum(len(p.text.split()) for p in doc.paragraphs)+sum(len(c.text.split()) for t in doc.tables for row in t.rows for c in row.cells))
print('LATEX',latex_dir/'main.tex')
