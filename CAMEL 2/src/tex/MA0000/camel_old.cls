%!TEX encoding = UTF-8 Unicode filename: camel.cls
% author: scmde
% date: 01/05/2015
\NeedsTeXFormat{LaTeX2e}
\def\fileversion{1.1}
\def\filedate{2015/05/01}
\ProvidesClass{camel}[\filedate \space v\fileversion \space (scmde)]
\ProvidesFile{camel.cls}[\filedate \space v\fileversion \space (scmde)]

% options
\newif\if@cymraeg\@cymraegfalse
\newif\if@screen\@screenfalse
\newif\if@booklet\@bookletfalse
\newif\if@blanks\@blanksfalse
\newif\if@answers\@answersfalse

% shortcuts (to set options in preamble)
\def\cymraegtrue{\@cymraegtrue} 
\def\screentrue{\@screentrue\@bookletfalse} 
\def\booklettrue{\@booklettrue\@screenfalse} 
\def\blankstrue{\@blankstrue} 
\def\answerstrue{\@answerstrue} 

% command line options
\ifnum\interactionmode = 2
	\def\optionYes{Y}
	\def\optionNo{N}
	\ifx\cymraeg\undefined\typein[\cymraeg]{Cymraeg? (Y/N)}\fi
	\ifx\cymraeg\optionYes\@cymraegtrue\fi
	\ifx\screen\undefined\typein[\screen]{Screen? (Y/N)}\fi
	\ifx\screen\optionYes\@screentrue\fi
	\ifx\booklet\undefined\typein[\booklet]{Paper? (Y/N)}\fi
	\ifx\booklet\optionYes\@booklettrue\fi
	\ifx\blanks\undefined\typein[\blanks]{Blanks? (Y/N)}\fi
	\ifx\blanks\optionYes\@blankstrue\fi
	\ifx\answers\undefined\typein[\answers]{Answers? (Y/N)}\fi
	\ifx\answers\optionYes\@answerstrue\fi
\fi

% class options
\DeclareOption{cymraeg}{\ifx\cymraeg\undefined\@cymraegtrue\else\message{^^J'cymraeg' option has no effect^^J}\fi}
\DeclareOption{screen}{\ifx\screen\undefined\@screentrue\else\message{^^J'screen' option has no effect^^J}\fi}
\DeclareOption{booklet}{\ifx\booklet\undefined\@booklettrue\else\message{^^J'booklet' option has no effect^^J}\fi}
\DeclareOption{blanks}{\ifx\blanks\undefined\@blankstrue\else\message{^^J'blanks' option has no effect^^J}\fi}
\DeclareOption{answers}{\ifx\answers\undefined\@answerstrue\else\message{^^J'answers' option has no effect^^J}\fi}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions
\relax

% message
\message{>>>>> OPTIONS:}
\if@cymraeg\message{ CYMRAEG}\fi
\if@screen\message{ SCREEN}\fi
\if@booklet\message{ BOOKLET}\fi
\if@blanks\message{ BLANKS}\fi
\if@answers\message{ ANSWERS}\fi
\message{<<<<<}

% load class
\if@booklet
	\LoadClass[twoside]{book}
\else
	\LoadClass[oneside]{book}
\fi

% common packages
\RequirePackage{amsmath,amsfonts}
\RequirePackage[a4paper,margin=20mm]{geometry}
\if@booklet
	\geometry{bindingoffset=15mm}
\fi

% GB date format
\def\today{\number\day/\number\month/\number\year}

%-------------------------------------------------
% module/document information
%-------------------------------------------------
\newcommand{\academicyear}[1]{\newcommand{\theacademicyear}{#1}}
\newcommand{\modulecode}[1]{\newcommand{\themodulecode}{#1}}
\newcommand{\moduletitle}[1]{\newcommand{\themoduletitle}{#1}}
\newcommand{\booktitle}[1]{\newcommand{\thebooktitle}{#1}}

%-------------------------------------------------
% names (english/cymraeg)
%-------------------------------------------------
\newcommand{\academicyearname}{Year}
\newcommand{\modulecodename}{Code}
\newcommand{\modulename}{Module}
\newcommand{\versionname}{Version}
\newcommand{\instructionsname}{Instructions}
\newcommand{\exercisename}{Exercise}
\newcommand{\questionname}{Question}
\newcommand{\answername}{Answer}
\newcommand{\solutionname}{Solution}
\newcommand{\proofname}{Proof}
\newcommand{\assessmentname}{Assessment}
\if@cymraeg
	\renewcommand{\academicyearname}{Blwyddyn}
	\renewcommand{\modulecodename}{C\^{o}d}
	\renewcommand{\modulename}{Modiwl}
	\renewcommand{\instructionsname}{Cyfarwyddiadau}
	\renewcommand{\exercisename}{Ymarfer}
    \renewcommand{\questionname}{Cwestiwn}
	\renewcommand{\answername}{Ateb}
	\renewcommand{\solutionname}{Datrysiad}
	\renewcommand{\proofname}{Prawf}
	\renewcommand{\assessmentname}{Asesiad}
\fi	

% theorem names
\newcommand{\theoremnamex}{Theorem}
\newcommand{\lemmanamex}{Lemma}
\newcommand{\hypothesisnamex}{Hypothesis}
\newcommand{\propositionnamex}{Proposition}
\newcommand{\corollarynamex}{Corollary}
\newcommand{\conjecturenamex}{Conjecture}
\newcommand{\algorithmnamex}{Algorithm}
\newcommand{\definitionnamex}{Definition}
\newcommand{\remarknamex}{Remark}
\newcommand{\problemnamex}{Problem}
\newcommand{\notenamex}{Note}
\newcommand{\notationnamex}{Notation}
\newcommand{\claimnamex}{Claim}
\newcommand{\summarynamex}{Summary}
\newcommand{\conclusionnamex}{Conclusion}
\newcommand{\examplenamex}{Example}
\newcommand{\exercisenamex}{Exercise}
\if@cymraeg
	\renewcommand{\lemmanamex}{Lema}
	\renewcommand{\propositionnamex}{Gosodiad}
	\renewcommand{\corollarynamex}{Canlyneb}
	\renewcommand{\conjecturenamex}{Dyfaliad}
	\renewcommand{\definitionnamex}{Diffiniad}
	\renewcommand{\remarknamex}{Sylwad}
	\renewcommand{\notenamex}{Nodyn}
	\renewcommand{\notationnamex}{Nodiant}
	\renewcommand{\claimnamex}{Honiad}
	\renewcommand{\summarynamex}{Crynodeb}
	\renewcommand{\conclusionnamex}{Casgliad}
	\renewcommand{\examplenamex}{Enghraifft}
	\renewcommand{\exercisenamex}{Ymarfer}
\fi

%-------------------------------------------------
% default settings (override in screen section)
%-------------------------------------------------

% hyperref
\RequirePackage{hyperref}
\hypersetup{pdfborder = {0 0 0}}
    
% tweaks
\setlength{\parindent}{0ex}
\setlength{\parskip}{0.5ex}

\renewcommand{\labelenumi}{(\arabic{enumi})}
\renewcommand{\labelenumii}{(\alph{enumii})}

% chapters, sections, headers & footers
\usepackage[pagestyles]{titlesec}
\usepackage{titletoc}
\setcounter{tocdepth}{1}
\renewcommand{\chaptername}{Lecture}
\titleformat{\chapter}
	{\bfseries\huge}{\chaptername~\thechapter}{1em}{}
\titleformat{\section}
	{\Large\bfseries}{\thesection}{1em}{}
\newpagestyle{main}[\small\scshape]{
\headrule
\sethead{\themodulecode}{}{\thechapter.~\chaptertitle} % odd
\setfoot{}{}{\thepage}
}
\pagestyle{main}

% steps (used with show/hide)
\newenvironment{steps}{\begin{enumerate}}{\end{enumerate}}
\newcommand{\step}[1]{\item {{#1}}}

% theorems
\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage[hyperref, thmmarks, amsmath]{ntheorem}
\theoremstyle{break}
\setlength\theorempreskipamount{4ex}
\setlength\theorempostskipamount{2ex}
\theorembodyfont{\upshape}
\qedsymbol{\rule{1ex}{1ex}}

\newcounter{theorem}[chapter]
\newtheorem{theorem}{\theoremnamex}
\newtheorem{lemma}[theorem]{\lemmanamex}
\newtheorem{proposition}[theorem]{\propositionnamex}
\newtheorem{corollary}[theorem]{\corollarynamex}
\newtheorem{conjecture}[theorem]{\conjecturenamex}
\newtheorem{hypothesis}[theorem]{\hypothesisnamex}
\newtheorem{algorithm}[theorem]{\algorithmnamex}
\newtheorem{definition}[theorem]{\definitionnamex}
\newtheorem{problem}[theorem]{\problemnamex}
\newtheorem{example}[theorem]{\examplenamex}
\newtheorem{remark}[theorem]{\remarknamex}
\newtheorem{note}[theorem]{\notenamex}
\newtheorem{notation}[theorem]{\notationnamex}
\newtheorem{claim}[theorem]{\claimnamex}
\newtheorem{summary}[theorem]{\summarynamex}
\newtheorem{conclusion}[theorem]{\conclusionnamex}
\newtheorem{exercise}[theorem]{\exercisenamex}


%-------------------------------------------------
% boxes
%-------------------------------------------------
\RequirePackage{tcolorbox}
\tcbuselibrary{breakable}
\RequirePackage{xcolor}

% colours
\newcommand{\de@ShowColour}{black}
\newcommand{\de@HideColour}{black}
\newcommand{\sethidecolour}[1]{\renewcommand{\de@HideColour}{#1}}
\if@blanks
	\renewcommand{\de@HideColour}{white}
\fi

% inline show/hide commands
\newcommand{\hideon}{\color{\de@HideColour}}
\newcommand{\hideoff}{\color{\de@ShowColour}}
\newcommand{\hide}[1]{{\hideon{{#1}}\hideoff}}

% box environment (not to be used in the document)
\newcommand{\deboxtitle}{}
\newenvironment{debox}{%
	\vspace{\parskip}
	\begin{tcolorbox}[breakable,notitle,boxrule=0.5pt,colback=white,coltext=\de@HideColour]
	\textcolor{\de@ShowColour}{\deboxtitle}
	\hideon
}{%
	\hideoff
    \end{tcolorbox}
}
% hide box 
\newcommand{\hideboxtitle}{}
\newenvironment{hidebox}{%
	\renewcommand{\deboxtitle}{\hideboxtitle}
	\begin{debox}
}{%
    \end{debox}
}
% proof box
\newcommand{\prooftitle}{\noindent\textbf{\proofname}\enspace}
\newenvironment{proof}{%
	\renewcommand{\deboxtitle}{\prooftitle}
	\begin{debox}
}{%
    \end{debox}
}
% solution box
\newcommand{\solutiontitle}{\noindent\textbf{\solutionname}\enspace}
\newenvironment{solution}{%
	\renewcommand{\deboxtitle}{\solutiontitle}
	\begin{debox}
}{%
    \end{debox}
}
% answer box
\newcommand{\answertitle}{\noindent\textbf{\answername:}\enspace}
\RequirePackage{environ}
\NewEnviron{answer}{%
    \if@answers%
    	\par\vspace*{\parskip}
		\begin{tcolorbox}[breakable,notitle,boxrule=0.5pt,colback=blue!10,colframe=black]
        \answertitle%
        \BODY%
        \end{tcolorbox}
		\par\vspace*{\parskip}%
    \fi%
}{}


% counters
\renewcommand{\theequation}{\thechapter.\arabic{equation}}
\renewcommand{\thetheorem}{\thechapter.\arabic{theorem}}
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}


% assessments (with optional title)
\RequirePackage{xifthen} % provides \isempty test (for optional arguments)
\newcounter{assessment}[chapter]
\renewcommand{\theassessment}{\thechapter.\arabic{assessment}}
\newcommand{\assessmenttitle}{}
\newenvironment{assessment}[1][]{%
  \refstepcounter{assessment}
  \ifthenelse{\isempty{#1}}{\renewcommand{\assessmenttitle}{}}{\renewcommand{\assessmenttitle}{(#1)}}
  \par\vspace{2ex}\noindent\textbf{\assessmentname\space\theassessment\space\assessmenttitle\normalsize} \par
}{}

% diagnostic, formative and summative assessments
\newenvironment{diagnostic}{\begin{assessment}[Diagnositic]}{\end{assessment}}
\newenvironment{formative}{\begin{assessment}[Formative]}{\end{assessment}}
\newenvironment{summative}{\begin{assessment}[Summative]}{\end{assessment}}


%-------------------------------------------------
% screen option (overrides default options defined above)
%-------------------------------------------------
\if@screen

	% layout
	\geometry{a4paper,landscape}
	\geometry{left=15mm,right=15mm,top=18mm,bottom=18mm}
	
	% fonts
	\renewcommand{\familydefault}{\sfdefault}
	\RequirePackage[T1]{fontenc}
	\RequirePackage{lmodern}
	\RequirePackage{exscale} 
	\RequirePackage{scrextend}
	\changefontsizes{16pt}

	% spacing
	\renewcommand\baselinestretch{1.1}
	\setlength{\parskip}{0.5ex}
	\setlength{\parindent}{0ex}
	\addtolength{\topskip}{4ex}
	\addtolength{\tabcolsep}{1ex}
	\renewcommand{\arraystretch}{1.3}
	\addtolength{\arraycolsep}{0.5ex}

	% custom itemize 
	\renewenvironment{itemize}{%
	\begin{list}{$\bullet$\ }{%
	    \setlength{\itemsep}{0ex plus 0.2ex}
	    \setlength{\leftmargin}{4ex}
	    \setlength{\rightmargin}{2ex}
	    \setlength{\topsep}{1ex}
	}}{\end{list}}
	
	% custom enumerate
	\renewenvironment{enumerate}{%
	\begin{list}{(\arabic{enumi})}{%
	    \usecounter{enumi}
	    \setlength{\itemsep}{0.25ex plus 0.15ex}
	    \setlength{\leftmargin}{4ex}
	    \setlength{\rightmargin}{2ex}
	}} {\end{list}}

\fi

%-------------------------------------------------
% cymraeg option
%-------------------------------------------------
\RequirePackage{comment}
\newcommand{\cy}[1]{}
\newcommand{\en}[1]{{#1}}
\newcommand{\ec}[2]{\en{#1}\cy{#2}}
\newenvironment{cymraeg}{\comment}{\endcomment}
\newenvironment{english}{}{}
\if@cymraeg
    \renewcommand{\cy}[1]{{#1}}
    \renewcommand{\en}[1]{}
	\renewenvironment{cymraeg}{}{}
	\renewenvironment{english}{\comment}{\endcomment}
\fi

%-------------------------------------------------
% frontmatter (ugly)
%-------------------------------------------------
\RequirePackage{emptypage}
\newcommand{\makefrontmatter}{%
	\renewcommand{\thepage}{(\roman{page})}
	\if@screen
		\makescreentitle
		\tableofcontents
		\newpage
	\else
		\maketitle
		\tableofcontents
	\fi
	\if@booklet
		\cleardoublepage
	\fi
	\setcounter{page}{1}
	\renewcommand{\thepage}{\arabic{page}}
}
\renewcommand{\maketitle}{%
    \thispagestyle{empty}
	\begin{center}
		\scshape
		\Large Cardiff University \hfill School of Mathematics \\[10ex]
		\huge \themodulecode \\ [7ex]
		\huge \themoduletitle \\[8ex]
		\huge \@ifundefined{thebooktitle}{Lecture Notes}{\thebooktitle} \\[8ex]
		\huge \theacademicyear 
	\end{center}
	\vfill
	\normalsize
	\raggedleft
	\texttt{Version: \today}
	\flushleft
	\normalsize
}
\newcommand{\makescreentitle}{%
    \thispagestyle{empty}
	\begin{center}
		\scshape
		\Large Cardiff University \hfill School of Mathematics \\[5ex]
		\huge \themodulecode \\ [1ex]
		\huge \themoduletitle \\[5ex]
		\huge \@ifundefined{thebooktitle}{Lecture Notes}{\thebooktitle} \\[1ex]
		\huge \theacademicyear 
	\end{center}
	\vfill
	\normalsize
	\raggedleft
	\texttt{Version: \today}
	\flushleft
}

%-------------------------------------------------
% headers and footers (fancyhdr can't override paper settings for screen)
%-------------------------------------------------
%\RequirePackage{fancyhdr}
%\fancyhf{}
%\pagestyle{fancy}
%\if@screen
%	\addtolength{\headheight}{1ex}
%    \renewcommand{\headrulewidth}{0.01pt}
%	\fancyhead[L]{\footnotesize\scshape\nouppercase\leftmark}
%    \fancyfoot[R]{\footnotesize\scshape\thepage}
%\else
%	\renewcommand{\headrulewidth}{0.01pt}
%	\fancyhead[L]{\small\scshape\nouppercase\leftmark}
%	\fancyhead[C]{\small\scshape\themodulecode}
%	\fancyhead[R]{\small\scshape\nouppercase\rightmark}
%	\fancyfoot[C]{\small\thepage}
%\fi
%% answers page style
%\fancypagestyle{answers}{
%	\fancyhf{}
%	\renewcommand{\headrulewidth}{0pt}
%	\fancyhead[L,R]{ANSWERS}
%	\fancyhead[C]{\scshape\themodulecode}
%	\fancyfoot[L,R]{ANSWERS}
%	\fancyfoot[C]{(\thepage)}
%}



%------------------------------------------------
%------------------------------------------------
% exam.cls rip-off starts here
%------------------------------------------------
%------------------------------------------------

% counters
\newcounter{question}
\newcounter{partno}
\newcounter{subpart}
\newcounter{subsubpart}
\newcounter{choice}

% hooks (for user customization)
\newcommand\questionshook{}
\newcommand\partshook{}
\newcommand\subpartshook{}
\newcommand\subsubpartshook{}
\newcommand\choiceshook{}
\newcommand\checkboxeshook{}

%--------------------
% questions
\newenvironment{questions}{%
  \def\@queslevel{question}%
  \def\question{%
    \def\thequestiontitle{\questionname~thequestion}%
    \@checkqueslevel{question}%
    \item
  } % end question
  \def\subpart{%
    \@checkqueslevel{subpart}%
    \item
  } % end subpart
  \def\subsubpart{%
    \@checkqueslevel{subsubpart}%
    \item
  } % end subsubpart 
  \list{\question@number}{%
    \usecounter{question}%
    \settowidth{\leftmargin}{10.\hskip\labelsep}%
    \labelwidth\leftmargin\advance\labelwidth-\labelsep
    \partopsep=0pt
    \questionshook
    }%
}{%
	\endlist
}% end questions environment
  
\def\question@number{\questionlabel}
\newcommand\questionlabel{\thequestion.}

%--------------------
% parts
\newenvironment{parts}{%
	\def\@queslevel{part}%
	\def\part{%
    	\@checkqueslevel{part}%
    	\item
	} % end part
	\list{\partlabel}{%
    	\usecounter{partno}\def\makelabel##1{\hss\llap{##1}}%
    	\settowidth{\leftmargin}{(m)\hskip\labelsep}%
    	\labelwidth\leftmargin\advance\labelwidth-\labelsep
    	\topsep=0pt
    	\partopsep=0pt
    	\partshook
	}%
}{%
	\endlist
} % end parts environmen

\newcommand\partlabel{\thepartno}
\def\thepartno{(\alph{partno})}

%--------------------
% subparts
\newenvironment{subparts}{%
	\def\@queslevel{subpart}%
	\list{\subpartlabel}{%
    	\usecounter{subpart}\def\makelabel##1{\hss\llap{##1}}%
    	\settowidth{\leftmargin}{vii.\hskip\labelsep}%
    	\labelwidth\leftmargin\advance\labelwidth-\labelsep
    	\topsep=0pt
    	\partopsep=0pt
    	\subpartshook
    }%
}{%
	\endlist 
} % end subparts environment

\newcommand\subpartlabel{\thesubpart}
\def\thesubpart{(\roman{subpart})}

%--------------------
% subsubparts
\newenvironment{subsubparts}{%
	\def\@queslevel{subsubpart}%
	\list{\subsubpartlabel}{%
	    \usecounter{subsubpart}\def\makelabel##1{\hss\llap{##1}}%
    	\settowidth{\leftmargin}{($\psi$)\hskip\labelsep}%
    	\labelwidth\leftmargin\advance\labelwidth-\labelsep
    	\topsep=0pt
    	\partopsep=0pt
    	\subsubpartshook
    }%
}{%
	\endlist 
} % end subsubparts environment

\newcommand\subsubpartlabel{\thesubsubpart.}
\def\thesubsubpart{\alph{subsubpart}}

%-----------------------
% validatte nesting level
\def\@checkqueslevel#1{%
  \begingroup
    \def\@temp{#1}%
    \ifx\@temp\@queslevel
      % do nothing.
    \else
      \ClassError{exam}{%
        I found a #1 where I expected to find a \@queslevel
        \MessageBreak
      }{%
        Both #1 and \@queslevel \space can be used only inside the correct 
        \MessageBreak \space \space
        environment and outside of any smaller environment
        \MessageBreak
      }%
    \fi
  \endgroup
}

%-----------------------
% choices
\renewcommand\thechoice{\Alph{choice}.}
\newcommand\choicelabel{\thechoice}
\newif\if@correctchoice
\@correctchoicefalse
\newcommand\CorrectChoiceEmphasis[1]{%
  \def\CorrectChoice@Emphasis{#1}%
}
\CorrectChoiceEmphasis{\bfseries}
\let\correctchoiceemphasis\CorrectChoiceEmphasis

% begin choices
\newenvironment{choices}{%
	\list{\choicelabel}{%
		\usecounter{choice}\def\makelabel##1{\hss\llap{##1}}%
		\settowidth{\leftmargin}{W.\hskip\labelsep}%
       	\def\choice{%
       		\if@correctchoice
           		\endgroup
         	\fi
         	\item
		} % end choice
		\def\CorrectChoice{%
			\if@correctchoice
       			\endgroup
       		\fi
       		\if@answers
				\begingroup 
                \@correctchoicetrue
				\CorrectChoice@Emphasis
			\fi
			\item
			\if@answersatend
        		\ans@write{\thechoice}
			\fi
		} % end CorrectChoice
		\let\correctchoice\CorrectChoice
       	\topsep=2pt
       	\partopsep=0pt
       	\choiceshook
	}
}{%
	\if@correctchoice 
		\endgroup 
	\fi 
	\endlist
} % end choices

%-----------------------
% checkboxes
\RequirePackage{amssymb}
\newcommand{\checkboxchar}[1]{\def\checkbox@char{#1}}
\newcommand{\checkedchar}[1]{\def\checked@char{#1}}
\checkboxchar{$\square$}
\checkedchar{$\checkmark$}

% begin checkboxes
\newenvironment{checkboxes}%
  {\list{\checkbox@char}%
     {\usecounter{choice}%
       \settowidth{\leftmargin}{W.\hskip\labelsep}%
       \def\choice{%
         \if@correctchoice
           \endgroup
         \fi
         \item
       } % choice
       \def\CorrectChoice{%
         \if@correctchoice
           \endgroup
         \fi
         \if@answers
           \begingroup 
           \@correctchoicetrue
           \CorrectChoice@Emphasis
           \item[\checked@char]
         \else
           \item
         \fi
         \if@answersatend
            \ans@write{\thechoice}
         \fi
       } % CorrectChoice
       \let\correctchoice\CorrectChoice
       \topsep=2pt
       \partopsep=0pt
       \checkboxeshook
     }%
}{%
    \if@correctchoice 
        \endgroup 
    \fi 
    \endlist
} % enc checkboxes

%-----------------------
% move up one level
\long\def\uplevel#1{%
  \par\bigskip
  \vbox{%
    \leftskip=\@totalleftmargin
    \advance\leftskip-\leftmargin
    \advance\@totalleftmargin-\leftmargin
    \advance\linewidth\leftmargin
    #1%
  }% vbox
  \nobreak
}

%------------------------------------------------
% the end	
\endinput
%------------------------------------------------
