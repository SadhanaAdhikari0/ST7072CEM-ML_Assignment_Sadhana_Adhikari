\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{IEEEtran}[2022/10/01 V1.8b IEEE standard conference class wrapper]

\DeclareOption{conference}{}
\DeclareOption{journal}{}
\DeclareOption{10pt}{}
\DeclareOption{11pt}{}
\DeclareOption{12pt}{}
\DeclareOption{twocolumn}{}
\DeclareOption{onecolumn}{}
\DeclareOption{letterpaper}{}
\DeclareOption{a4paper}{}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\LoadClass[10pt,twocolumn,letterpaper]{article}

\RequirePackage[margin=0.75in,top=0.75in,bottom=0.75in,columnsep=0.25in]{geometry}
\RequirePackage{amsmath,amssymb}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{cite}
\RequirePackage{url}
\RequirePackage{xcolor}

\newcommand{\IEEEauthorblockN}[1]{{\large\bfseries #1\par\vskip 0.2em}}
\newcommand{\IEEEauthorblockA}[1]{{\small #1\par\vskip 0.4em}}
\newcommand{\IEEEPARstart}[2]{\textbf{#1}#2}

\newenvironment{IEEEkeywords}{%
  \vskip 0.5em\noindent\textbf{\textit{Index Terms---}}\ignorespaces
}{\vskip 1em}

\setlength{\parindent}{1em}
\setlength{\parskip}{0pt}

% Custom IEEE conference title block
\def\@maketitle{%
  \newpage
  \null
  \vskip 1em%
  \begin{center}%
  \let \footnote \thanks
    {\LARGE\bfseries \@title \par}%
    \vskip 1.2em%
    {\normalsize \@author \par}%
    \vskip 1em%
  \end{center}%
  \par
  \vskip 1.5em}

