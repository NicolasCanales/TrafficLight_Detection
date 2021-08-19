import os

def leetexto(idioma, voz, tono, velocidad, texto):
	print('lectura de texto, idioma: "' + idioma + '", voz: ' + voz + ";")
	scommand='espeak -v' + idioma + '+' + voz + ' -p'+tono+' -s'+velocidad +' "' + texto + '"'
	print("$ " + scommand)
	os.system(scommand)

leetexto('es','f5','60','130', 'Espere la luz verde')
leetexto('es','f5','60','130', ' ')
leetexto('es','f5','60','130', 'Puede cruzar')