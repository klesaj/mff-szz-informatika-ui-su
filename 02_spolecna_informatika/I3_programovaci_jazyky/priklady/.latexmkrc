# Lokální konfigurace latexmk pro složku priklady/ tohoto okruhu.
# Umožňuje sestavení bare příkazem `latexmk` přímo z adresáře priklady/.
$pdf_mode = 4;            # LuaLaTeX
$out_dir  = 'out';        # výsledné PDF
$aux_dir  = 'tmp';        # všechny pomocné soubory (aux, log, ...)
@default_files = ('src/main.tex');
# priklady/ je o úroveň hlouběji než okruh -> tři úrovně k common_latex
ensure_path('TEXINPUTS', '../../../common_latex//');
