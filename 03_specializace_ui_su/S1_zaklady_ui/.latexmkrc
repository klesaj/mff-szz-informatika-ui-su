# Lokální konfigurace latexmk pro tento okruh.
# Umožňuje sestavení bare příkazem `latexmk` přímo z adresáře okruhu.
$pdf_mode = 4;            # LuaLaTeX
$out_dir  = 'out';        # výsledné PDF
$aux_dir  = 'tmp';        # všechny pomocné soubory (aux, log, ...)
@default_files = ('src/main.tex');
# Najde sdílený styl ../../common_latex/szzstyl.sty
ensure_path('TEXINPUTS', '../../common_latex//');
# Sekce okruhu jsou rozdělené do fragmentů v src/ a vkládají se přes \input.
ensure_path('TEXINPUTS', 'src//');
