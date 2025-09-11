\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{deltaphi-report}[12/05/2021 Class for the ESA Standard Document]
% ------------------------------------------------------------------------------
% ESA Standard Document (2021) LaTeX Class by Jeroen Van den Eynde.
% Contact: jeroen.van.den.eynde@esa.int
%

% ------------------------------------------------------------------------------
% REQUIRED PACKAGES
% ------------------------------------------------------------------------------
\LoadClass[12pt]{article}

\RequirePackage{geometry}		  % 	Change the page dimensions and margins
\RequirePackage[parfill]{parskip} % Non-zero paragraph
\RequirePackage{tocloft}          % Improved ToC
\RequirePackage{etoolbox}         % Various tools (used here to patch the \section command)
\RequirePackage{titlesec}         % Change style of sections
\RequirePackage{graphicx}         % Ability to insert graphics
\RequirePackage{float}            % Ability to insert graphics
\RequirePackage{tikz}             % Ability to insert graphics
\RequirePackage{fontspec}         % Specify system fonts
%\RequirePackage[table]{xcolor}	  % Colours
\RequirePackage{xcolor}	  % Colours
\RequirePackage{lastpage}         % Get total number of pages
\RequirePackage{fancyhdr}         % Headers and footers
\RequirePackage{setspace}         % Allow multi-line spacing
\RequirePackage{caption}          % Improve spacing between caption and tables
\RequirePackage[hang, flushmargin]{footmisc}
\RequirePackage{tabularx,booktabs,colortbl}            % Improved tables
\RequirePackage[
	colorlinks=true,
	citecolor=esadeepspace,
	urlcolor=blue,
	linkcolor=black
]{hyperref}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{ulem}  % Package for advanced underlining
% ------------------------------------------------------------------------------
% SITE :-)
% ------------------------------------------------------------------------------

\newcommand{\bopen}{%
	{\color{esadeepspace}\small{%
	B-Open Solutions S.r.l.\\
	Viale Palmiro Togliatti, 1639, \\
    00155 Roma (RM)\\
	Italy\\
	}}
}


% ------------------------------------------------------------------------------
% DOCUMENT CLASS OPTIONS
% ------------------------------------------------------------------------------

% Set site by supplied options. [Default: bopen]
%\newcommand{\sitedata}{\bopen}
%\DeclareOption{bopen}{\renewcommand{\sitedata}{\bopen}}

% Define 'strict' option to strictly match Word template spacing
\newtoggle{strict}
\DeclareOption{strict}{\togglefalse{strict}}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% ------------------------------------------------------------------------------
% ESA DOCUMENT PROPERTIES
% ------------------------------------------------------------------------------
% Issue, Issue Date, Revision, Reference Number
\newcommand\issue[1]{\renewcommand\@issue{#1}}
\newcommand\@issue{}
\newcommand\issuedate[1]{\renewcommand\@issuedate{#1}}
\newcommand\@issuedate{\today}
\newcommand\revision[1]{\renewcommand\@revision{#1}}
\newcommand\@revision{}
\newcommand\refnumber[1]{\renewcommand\@refnumber{#1}}
\newcommand\@refnumber{}
\newcommand\contract[1]{\renewcommand\@contract{#1}}
\newcommand\@contract{}

% Project Name
\newcommand\project[1]{\renewcommand\@project{#1}}
\newcommand\@project{}


% Organisational Entity
\newcommand\organisationalentity[1]{\renewcommand\@organisationalentity{#1}}
\newcommand\@organisationalentity{}

% Status (draft, final)
\newcommand\status[1]{\renewcommand\@status{#1}}
\newcommand\@status{Draft}

% Document Type
\newcommand\doctype[1]{\renewcommand\@doctype{#1}}
\newcommand\@doctype{~}

% Security Marking
\newcommand\securitymarking[1]{\renewcommand\@securitymarking{#1}}
\newcommand\@securitymarking{B-Open UNCLASSIFIED - For B-Open Official Use Only}

% Approval
\newcommand{\approvedentries}{}
\newcommand{\approved}[2]{%
	\protected@xdef\approvedentries{\approvedentries #1 & #2 \protect\\}
}

% Change log and record
\newcommand{\changelogentries}{}
\let\trules\relax
\newcommand{\changelog}[4]{%
\protected@xdef\changelogentries{\changelogentries #1 & #2 & #3 & #4 \protect\\ \trules} 
}
\newcommand{\changerecordentries}{}
\let\trules\relax
\newcommand{\changerecord}[4]{%
\protected@xdef\changerecordentries{\changerecordentries #1 & #2 & #3 & #4 \protect\\ \trules}
}

% Distribution
\newcommand{\distributionentries}{}
\let\trules\relax
\newcommand{\distribution}[1]{%
	\protected@xdef\distributionentries{\distributionentries #1 \protect\\ \trules}
}

% ------------------------------------------------------------------------------
% PAGE LAYOUT AND SETUP
% ------------------------------------------------------------------------------

% Basic page geometry
\geometry{a4paper,%
top=5.0cm, bottom=3.0cm,%
left=2.0cm, right=1.5cm,%
headsep=1.0cm,headheight=50pt,heightrounded,%
footskip=48pt}%

% Line spacing (strict doublespacing or reduced/improved)
\newcommand{\esalinespacing}{}
\iftoggle{strict}{%
    \renewcommand{\esalinespacing}{
    	\setstretch{1.43}% Strict linespacing to match Word template
    	\setlength{\parskip}{0pt}% Remove parskip
    }
}{
	\renewcommand{\esalinespacing}{
		\setstretch{1.15}% Improved linespacing for clarity
	}
}

% Section & subsection formats
\RequirePackage{titlesec}% Change style of sections
\titleformat{\section}{\color{esadeepspace-1}\LARGE\bfseries\uppercase}{\thesection.\hspace{0.25em}}{0.0cm}{}
\titleformat{\subsection}{\color{esadeepspace}\Large\bfseries}{\thesubsection.\hspace{0.25em}}{0.0cm}{}
\titleformat{\subsubsection}{\color{esadeepspace-1}\large\bfseries\itshape}{\thesubsubsection.\hspace{0.25em}}{0.0cm}{}
\titleformat{\paragraph}{\color{esadeepspace}\bfseries}{\theparagraph.\hspace{0.25em}}{0.0cm}{}
\titleformat{\subparagraph}{\color{esadeepspace}\bfseries\itshape}{\thesubparagraph.\hspace{0.25em}}{0.0cm}{}

% Spacing before/after sections titles according to ESA Word template
\titlespacing*{\section}{0pt}{12pt plus 1pt minus 1pt}{12pt plus 1pt}
\titlespacing*{\subsection}{0pt}{12pt plus 1pt minus 1pt}{12pt plus 1pt}
\titlespacing*{\subsubsection}{0pt}{12pt plus 1pt minus 1pt}{12pt plus 1pt}
\titlespacing*{\paragraph}{0pt}{12pt plus 1pt minus 1pt}{12pt plus 1pt}
\titlespacing*{\subparagraph}{0pt}{12pt plus 1pt minus 1pt}{12pt plus 1pt}

% ------------------------------------------------------------------------------
% TABLE OF CONTENT LAYOUT AND SETUP
% ------------------------------------------------------------------------------

% Depth of ToC and paragraphs
\setcounter{tocdepth}{3}          % Numbering of (sub-)paragraphs in ToC
\setcounter{secnumdepth}{5}       % Numbering of (sub-)paragraphs in document

% Set section name and font of ToC, LoF, LoT
\renewcommand{\contentsname}{Table of Contents}
\renewcommand{\cfttoctitlefont}{\tocsize\bfseries}
\renewcommand{\listfigurename}{List of Figures}
\renewcommand{\cftloftitlefont}{\tocsize\bfseries}
\renewcommand{\listtablename}{List of Tables}
\renewcommand{\cftlottitlefont}{\tocsize\bfseries}

% all ToC entries left aligned
\setlength{\cftsecindent}{0em}
\setlength{\cftsubsecindent}{0em}
\setlength{\cftsubsubsecindent}{0em}
\setlength{\cftparaindent}{0em}
\setlength{\cftsubparaindent}{0em}

% Fontsize in ToC
\renewcommand{\cftsecfont}{\tocsmall}
\renewcommand{\cftsecpagefont}{\tocsmall}
\renewcommand{\cftsubsecfont}{\tocsmall}
\renewcommand{\cftsubsecpagefont}{\tocsmall}
\renewcommand{\cftsubsubsecfont}{\tocsmall}
\renewcommand{\cftsubsubsecpagefont}{\tocsmall}
\renewcommand{\cftparafont}{\tocsmall}
\renewcommand{\cftparapagefont}{\tocsmall}
\renewcommand{\cftsubparafont}{\tocsmall}
\renewcommand{\cftsubparapagefont}{\tocsmall}

% Fontsize in ToF
\renewcommand\cftfigfont{\tocsmall}
\renewcommand\cftfigpagefont{\tocsmall}

% Fontsize in ToT
\renewcommand\cfttabfont{\tocsmall}
\renewcommand\cfttabpagefont{\tocsmall}

% Line spacing in ToC
\g@addto@macro\@cfttocstart{\setstretch{1.20}}

% Remove spacing after section in ToC
\setlength{\cftbeforesecskip}{0pt}

% dot after number in ToC
\renewcommand{\cftsecaftersnum}{.}%
\renewcommand{\cftsubsecaftersnum}{.}%
\renewcommand{\cftsubsubsecaftersnum}{.}%
\renewcommand{\cftparaaftersnum}{.}%
\renewcommand{\cftsubparaaftersnum}{.}%

% Use dots as filler for sections
\renewcommand\cftsecleader{\cftdotfill{\cftdotsep}}

% Reduce dot spacing in ToC
\renewcommand{\cftdotsep}{0.3}

%dots all the way to the page number 
\renewcommand{\cftsecfillnum}[1]{%
  {\cftsecleader}\nobreak
  {\cftsecpagefont #1}\cftsecafterpnum\par
}
\renewcommand{\cftsubsecfillnum}[1]{%
  {\cftsubsecleader}\nobreak
  {\cftsubsecpagefont #1}\cftsubsecafterpnum\par
}
\renewcommand{\cftsubsubsecfillnum}[1]{%
  {\cftsubsubsecleader}\nobreak
  {\cftsubsubsecpagefont #1}\cftsubsubsecafterpnum\par
}
\renewcommand{\cftparafillnum}[1]{%
  {\cftparaleader}\nobreak
  {\cftparapagefont #1}\cftparaafterpnum\par
}
\renewcommand{\cftsubparafillnum}[1]{%
  {\cftsubparaleader}\nobreak
  {\cftsubparapagefont #1}\cftsubparaafterpnum\par
}

% Add clearpage after toc, lof, lot
\g@addto@macro\@cfttocfinish{\clearpage\esalinespacing}

\tocloftpagestyle{fancy}% Set headers/footers on ToC pages

\renewcommand{\arraystretch}{1.3}% Get a bit more space in table rows

% ------------------------------------------------------------------------------
% FONTS, GRAPHICS AND COLOURS
% ------------------------------------------------------------------------------

%\setmainfont{Arial}

% Font Sizes
\renewcommand{\small}{\fontsize{8pt}{10pt}\selectfont}
\newcommand{\medium}{\fontsize{9pt}{10pt}\selectfont}
\renewcommand{\large}{\fontsize{13pt}{15pt}\selectfont}
\renewcommand{\Large}{\fontsize{14pt}{16pt}\selectfont}
\renewcommand{\LARGE}{\fontsize{16pt}{19pt}\selectfont}
\renewcommand{\huge}{\fontsize{22pt}{26pt}\selectfont}
\newcommand{\logsize}{\fontsize{9pt}{11pt}\selectfont}
\newcommand{\tocsize}{\fontsize{13pt}{16pt}\selectfont}
\newcommand{\tocsmall}{\fontsize{11pt}{13pt}\selectfont}

% Colours (as defined directly in the word template)
\definecolor{esadeepspace}{RGB}{0,50,71}
\definecolor{esadeepspace-1}{RGB}{51,94,111}
\definecolor{esadeepspace-2}{RGB}{129,151,166}
\definecolor{esadeepspace-log}{RGB}{3,49,66}
\definecolor{tableblue}{RGB}{204,229,255}
\definecolor{tablegrey}{HTML}{D9D9D9}

% More colors of the esa-colour-recap-charts.pdf
\definecolor{neutralspace}{RGB}{232,232,228}

\definecolor{excitered-1}{RGB}{241,102,106}
\definecolor{excitered}{RGB}{237,27,47}
\definecolor{excitered+1}{RGB}{207,29,57}
\definecolor{excitered+2}{RGB}{150,1,54}

\definecolor{trustyazure-1}{RGB}{109,207,246}
\definecolor{trustyazure}{RGB}{0,155,219}
\definecolor{trustyazure+1}{RGB}{0,97,158}
\definecolor{trustyazure+2}{RGB}{30,51,120}

\definecolor{enlightyellow-1}{RGB}{255,204,78}
\definecolor{enlightyellow}{RGB}{251,171,24}
\definecolor{enlightyellow+1}{RGB}{244,121,32}
\definecolor{enlightyellow+2}{RGB}{167,85,52}

\definecolor{pureteal-1}{RGB}{118,200,174}
\definecolor{pureteal}{RGB}{0,174,157}
\definecolor{pureteal+1}{RGB}{0,142,122}
\definecolor{pureteal+2}{RGB}{0,103,98}

\definecolor{tableblue}{RGB}{204,229,255}
\definecolor{tablegrey}{HTML}{D9D9D9}
% ------------------------------------------------------------------------------
% HEADER AND FOOTER
% ------------------------------------------------------------------------------

\fancyhf{}% Clear style
\renewcommand{\headrulewidth}{0pt}% Remove header line
\renewcommand{\footrulewidth}{0pt}% Remove footer line


% ESA Security Marking
% \rhead{\small{Contract Nº: \@contract \\
% Reference: \@refnumber \\
% Issue/Revision: \@issue.\@revision \\
% Date of Issue: \@issuedate \\
% }}

% \chead{\Large\textbf{Product Requirement \\ Specification}}
% ESA Logo & European Space Agency - Agence spatiale europeenne
% \rhead{\includegraphics[width=4.2cm]{Figures/DeltaPhi3.pdf}}% ESA LOGO
% \lhead{\includegraphics[width=4.2cm]{Figures/B-Open.png}}% ESA LOGO
%\rfoot{\includegraphics[width=4.2cm]{Figures/ESA_Logo_arrow.pdf}}% ESA logo bottom arrow
% \cfoot{\raisebox{1.2cm}{\color{esadeepspace}\small{\@securitymarking}}}
% \pagestyle{fancy}% Use these headers/footers everywhere

\setlength{\headheight}{53.81pt}

% ------------------------------------------------------------------------------
% FOOTNOTES
% ------------------------------------------------------------------------------

%\renewcommand{\footnoterule}{\vspace*{-1.5\baselineskip}\rule{5cm}{0.2mm}\\}% Footnote space
%\setlength{\skip\footins}{4\baselineskip}

% ------------------------------------------------------------------------------
% FRONTMATTER AND TITLE PAGE
% ------------------------------------------------------------------------------

% Approval Table
\newcommand{\approvaltable}{%
\begin{flushleft}
	{\color{esadeepspace-2}\huge\textbf{APPROVAL}\vspace{0.4cm}}
\end{flushleft}

\noindent
{\logsize
\color{esadeepspace-log}
\begin{tabularx}{\textwidth}{p{2.0cm}p{5.5cm}|p{2.5cm}p{6.0cm}}
	\hline
	Title & \multicolumn{3}{l}{\@title}\\\hline
	Issue Number & \@issue & Revision Number & \@revision\\\hline
	Author & \@author & Date & \@issuedate\\\hline
\end{tabularx}\vspace{-1pt}
\begin{tabularx}{\textwidth}{p{7.92cm}|p{8.08cm}}
	Approved by & Date of Approval \\\hline
	\approvedentries
	\hline
\end{tabularx}
}
}

% Change Log Table
\newcommand{\changelogtable}{%
\begin{flushleft}
    {\color{esadeepspace-2}\huge\textbf{CHANGE LOG}\vspace{0.4cm}}
\end{flushleft}

\noindent
{\logsize
\color{esadeepspace-log}
\let\trules\hline
\begin{tabularx}{\textwidth}{p{8.2cm}|p{1.8cm}|p{3.3cm}|p{2.0cm}}
    \hline
    Reason for change & Issue Nr. & Revision Number & Date\\\hline
    \changelogentries
\end{tabularx}
}
}

% Change Record Table
\newcommand{\changerecordtable}{%
\begin{flushleft}
    {\color{esadeepspace-2}\huge\textbf{CHANGE RECORD}\vspace{0.4cm}}
\end{flushleft}
%
\noindent{
	\logsize
	\color{esadeepspace-log}
	\let\trules\hline
	\begin{tabularx}{\textwidth}{p{8.2cm}|p{1.8cm}|p{2.7cm}|p{2.6cm}}
		\hline
		Issue Number\quad\@issue & \multicolumn{3}{l}{Revision Number\quad\@revision}\\\hline
		Reason for change & Date & Page(s) & Paragraph(s)\\\hline
		\changerecordentries
	\end{tabularx}
	}
}

% Distribution Table
\newcommand{\distributiontable}{%
\begin{flushleft}
	{\color{esadeepspace-2}\huge\textbf{DISTRIBUTION}\vspace{0.4cm}}
\end{flushleft}

\noindent{
	\logsize
	\color{esadeepspace-log}
	\let\trules\hline
	\begin{tabularx}{\textwidth}{p{16.6cm}}
		\hline
		Name/Organisational Unit\\
		\hline
		\distributionentries
	\end{tabularx}
	}
}

% ------------------------------------------------------------------------------
\renewcommand*{\maketitle}{%
\singlespacing
%\begin{flushright}
%{\vspace*{-1.2cm}
%	\sitedata}
%\end{flushright}
%
\vspace*{7.0cm}
%
\doublespacing
\begin{flushleft}
{\color{esadeepspace-1}\Large\textbf{\MakeUppercase{\@project}}}\\
{\color{esadeepspace-1}\Large\textbf{\MakeUppercase{\@title}}}
\end{flushleft}
\singlespacing
%

\begin{figure}[b]
\includegraphics[width=15.0cm]{Figures/AllLogos.png}
\centering
\end{figure}

\vfill%
%
{
\renewcommand{\arraystretch}{1.5}
\color{esadeepspace-1}\medium 
\begin{tabular}{p{4.2cm}p{8.7cm}}
	\hspace{-0.5em}Prepared by   & \@author \\
	\hspace{-0.5em} & \@organisationalentity\\
    %\hspace{-0.5em}Document Type & \@doctype \\
	\hspace{-0.5em}Contract Nº   & \@contract \\
    \hspace{-0.5em}Reference     & \@refnumber \\
    \hspace{-0.5em}Issue/Revision& \@issue.\@revision \\
    \hspace{-0.5em}Date of Issue & \@issuedate \\
    \hspace{-0.5em}Status        & \@status
\end{tabular}%
}
\vspace*{1.3cm}%
\clearpage
% ------ Main page footer ------
\lfoot{\scriptsize%
\vspace*{-3\baselineskip}
\color{esadeepspace-1}
Page \thepage/\pageref*{LastPage}\\
%Page \thepage\\
}
\esalinespacing
}
%
% ------------------------------------------------------------------------------
\newcommand*{\makelog}{%
\singlespacing
\approvaltable
\vspace*{1.5cm}
\changelogtable
\vspace*{1.5cm}
\changerecordtable
\vspace*{1.5cm}
%\distributiontable
\clearpage
\esalinespacing
}
%
% ------------------------------------------------------------------------------
% Number equations by section
\numberwithin{equation}{section}

%norm
\newcommand\norm[2]{\lVert#1\rVert _#2}

%graph style
\usetikzlibrary{shapes.geometric,arrows.meta}
\usetikzlibrary{positioning}
\usetikzlibrary{calc}
\tikzstyle{block} = [rectangle, draw,  fill=blue!20, text width=3cm, minimum height=1cm, text centered, rounded corners]
\tikzstyle{rectaux} = [rectangle, draw, fill=yellow!20, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{rectin} = [rectangle, draw=red, fill=orange!20, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{rectout} = [rectangle, draw=green, fill=green!20, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{rectauxd} = [rectangle, draw, dashed, fill=yellow!20, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{rectind} = [rectangle, draw=red, dashed, fill=orange!20, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{rectoutd} = [rectangle, draw=green, dashed, fill=green!20, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{empty} = [rectangle, fill=blue!0, minimum width=3cm, minimum height=1cm, text centered]
\tikzstyle{line} = [draw, -latex]

\pagenumbering{gobble}