import csv
import os
import logging
from PIL import Image

logging.basicConfig(filename='resultado.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def compress():
	comp = open('comp.txt', 'r').read().split('=')

	if comp[1] == '1':
		carps = [f for f in os.listdir() if os.path.isdir(f)]
		for i in carps:
			for root, dirs, files in os.walk( i + "\\FOTOS"):
				for name in files:
					image = Image.open(os.path.join(root, name))
					width, height = image.size
					new_size = (width//2, height//2)
					resized_image = image.resize(new_size)
					resized_image.save(os.path.join(root, name), optimize=True, quality=50)
		with open('comp.txt', 'w') as file:
			file.write('compress=0')
			file.close()
	else:
		return

def estacion(num):
	with open('CCS-OESTE.csv', encoding="utf-8-sig") as csvfile:
		estaciones = csv.DictReader(csvfile, delimiter=';')

		for row in estaciones:
			if row['id'] == str(num):
				return((row['name'], row['geo']))

def data(arg, ruta):
	with open('%s/ficha.txt' % ruta) as data:
		ficha = data.readlines()

	for i in ficha:
		if i.startswith(arg):
			num = i.replace('\n','').split('_')
			return(num[1])
		
def analisis():
	files = [f for f in os.listdir() if os.path.isdir(f)]
	logging.info('%s estación(es) encontrada(s).' % len(files))
	logging.info('---------------------------------------------------')
	
	list_out = []
	list_she = []

	for i in files:
		if data('lista', i) == '1':
			tipo = data('tag', i)
			if tipo == 'out':
				list_out.append(i)
			elif tipo == 'she':
				list_she.append(i)


	logging.info('%s tipo outdoor completada(s).' % len(list_out))
	for i in list_out: logging.info('%s' % i)
	logging.info('---------------------------------------------------')
	logging.info('%s tipo shelter completada(s).' % len(list_she))
	for i in list_she: logging.info('%s' % i)
	logging.info('---------------------------------------------------')

	return(list_out, list_she)

def portada():
	files = [f for f in os.listdir() if os.path.isdir(f)]

	for i in files:
		num = data('id', i)
		date = data('fecha', i)
		et = estacion(num)

		port = open('portada.tex', 'r', encoding='utf-8')
		portada = port.readlines()
		port.close()

		rf = open('%s/rf.tex' % i, 'w', encoding='utf-8')
		rf.writelines(portada)
		rf.write('\t' + r'\node[align=center] at (10.7,7) {\LARGE \textbf{\textcolor{fttverde}{COD: RF-MP-ET' + '%s-' % num + date[3::] + '}}};\n')
		rf.write('\t' + r'\node[align=left] at (16,3) {\Large \textbf{\textcolor{fttazul}{ET: ' + str(num) + ' - ' + et[0] + r'}}\\' + '\n')
		rf.write('\t\t' + r'\Large \textbf{\textcolor{fttazul}{Geo: ' + et[1] + r'}}\\' + '\n')
		rf.write('\t\t' + r'\Large \textbf{\textcolor{fttazul}{Fecha: ' + date + r'}}\\' + '\n')
##		rf.write('\t\t' + r'\Large \textbf{\textcolor{fttazul}{Hora: ' + data('horain', i) + ' - ' + data('horaout', i) + r'}}\\' + '\n')
		rf.write('\t\t' + r'\Large \textbf{\textcolor{fttazul}{CDC: ' + data('cdc', i) + r'}}\\' + '\n')
		rf.write('\t\t' + r'\Large \textbf{\textcolor{fttazul}{SOC: ' + data('soc', i) + r'}}};' + '\n')
		rf.write(r'\end{tikzpicture}' + '\n')
		rf.write(r'\begin{tikzpicture}' + '\n')
		rf.write(r'\draw[color=fttazul, line width=2mm, rounded corners=40] (2, -2) rectangle (23.2, 12.8);' + '\n')
		rf.write(r'\end{tikzpicture}' + '\n')
		rf.write(r'\newpage' + '\n\n')
		rf.write(r'\restoregeometry' + '\n\n')
		rf.close()

def diap1(et, tit, sub, desc, fot1):
	with open('diap1.txt', 'r', encoding="utf-8") as file:
		filedata = file.read()
		filedata = filedata.replace('TITULO', tit)
		filedata = filedata.replace('SUBTIT', sub)
		filedata = filedata.replace('DESCRIPCION', desc)
		filedata = filedata.replace('FOTO1', fot1.replace('\\', '/'))
		file.close()

	with open(et + '\\rf.tex', 'a', encoding="utf-8") as file:
		file.write(filedata)
		file.close()

def diap2(et, tit, sub, desc, fot1, fot2):
	with open('diap2.txt', 'r', encoding="utf-8") as file:
		filedata = file.read()
		filedata = filedata.replace('TITULO', tit)
		filedata = filedata.replace('SUBTIT', sub)
		filedata = filedata.replace('DESCRIPCION', desc)
		filedata = filedata.replace('FOTO1', fot1.replace('\\', '/'))
		filedata = filedata.replace('FOTO2', fot2.replace('\\', '/'))
		file.close()

	with open(et + '\\rf.tex', 'a', encoding="utf-8") as file:
		file.write(filedata)
		file.close()

def diap3(et, tit, sub, desc, fot1, fot2, fot3):
	with open('diap3.txt', 'r', encoding="utf-8") as file:
		filedata = file.read()
		filedata = filedata.replace('TITULO', tit)
		filedata = filedata.replace('SUBTIT', sub)
		filedata = filedata.replace('DESCRIPCION', desc)
		filedata = filedata.replace('FOTO1', fot1.replace('\\', '/'))
		filedata = filedata.replace('FOTO2', fot2.replace('\\', '/'))
		filedata = filedata.replace('FOTO3', fot3.replace('\\', '/'))
		file.close()

	with open(et + '\\rf.tex', 'a', encoding="utf-8") as file:
		file.write(filedata)
		file.close()

def cuerpo(comp):
	for i in comp[0]:
		path = 'FOTOS\\PLANTA EXTERNA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA EXTERNA', '', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA EXTERNA', '', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA EXTERNA\\DESMALEZADO\\ANTES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'ANTES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'ANTES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA EXTERNA\\DESMALEZADO\\DESPUÉS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'DESPUÉS', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'DESPUÉS', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\TORRE\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'TORRE', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'TORRE', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\BATERIAS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'BATERIAS', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'BATERIAS', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\CARGA CONECTADA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'CARGA CONECTADA', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'CARGA CONECTADA', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\COMPONENTES DE TRANSMISIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'COMPONENTES DE TRANSMISIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'COMPONENTES DE TRANSMISIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\GABINETES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'GABINETES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'GABINETES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\IMPERMEABILIZACIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'IMPERMEABILIZACIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'IMPERMEABILIZACIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\LIMPIEZA DE RECTIFICADORES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'LIMPIEZA DE RECTIFICADORES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'LIMPIEZA DE RECTIFICADORES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\LUMINARIA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'LUMINARIA EXTERIOR', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'LUMIMARIA EXTERIOR', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\PUESTA A TIERRA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'PUESTA A TIERRA', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'PUESTA A TIERRA', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\ROUTER Y SWITCH\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'ROUTER Y SWITCH', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'ROUTER Y SWITCH', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\TABLERO PRINCIPAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\TABLERO PRINCIPAL\\TENSIONES FASE-FASE\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-FASE', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-FASE', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-FASE', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\TABLERO PRINCIPAL\\TENSIONES FASE-NEUTRO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-NEUTRO', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-NEUTRO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-NEUTRO', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\TABLERO PRINCIPAL\\CORRIENTES DE FASE\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTES DE FASE', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTES DE FASE', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTES DE FASE', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\TABLERO PRINCIPAL\\CORRIENTE Y TENSIÓN DE NEUTRO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTE Y TENSIÓN DE NEUTRO', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTE Y TENSIÓN DE NEUTRO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTE Y TENSIÓN DE NEUTRO', path + fot1)
				del files[0]

		with open(i + '\\rf.tex', 'a', encoding="utf-8") as file:
			file.write('\\end{document}')
			file.close()

		logging.info('Informe de ' + i + ' generado.')


	for i in comp[1]:
		path = 'FOTOS\\PLANTA EXTERNA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA EXTERNA', '', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA EXTERNA', '', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA EXTERNA\\DESMALEZADO\\ANTES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'ANTES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'ANTES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA EXTERNA\\DESMALEZADO\\DESPUÉS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'DESPUÉS', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA EXTERNA', 'DESMALEZADO', 'DESPUÉS', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\COMPONENTES DE TRANSMISIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'COMPONENTES DE TRANSMISIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'COMPONENTES DE TRANSMISIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\LUMINARIA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'LUMINARIA EXTERIOR', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'LUMIMARIA EXTERIOR', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\PERIMETRO INTERNO\\IMPERMEABILIZACIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'IMPERMEABILIZACIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'PERIMETRO INTERNO', 'IMPERMEABILIZACIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\TORRE\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TORRE', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TORRE', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\BATERIAS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'BATERIAS', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'BATERIAS', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\CARGA CONECTADA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'CARGA CONECTADA', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'CARGA CONECTADA', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\GABINETES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'GABINETES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'GABINETES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\LIMPIEZA DE RECTIFICADORES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'LIMPIEZA DE RECTIFICADORES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'LIMPIEZA DE RECTIFICADORES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\LUMINARIA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'LUMINARIA INTERIOR', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'LUMINARIA INTERIOR', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\PUESTA A TIERRA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'PUESTA A TIERRA', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'PUESTA A TIERRA', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\ROUTER Y SWITCH\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'ROUTER Y SWITCH', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'ROUTER Y SWITCH', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\TABLERO PRINCIPAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'TABLERO PRINCIPAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'ESPACIO INTERNO (SHELTER)', 'TABLERO PRINCIPAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\TABLERO PRINCIPAL\\TENSIONES FASE-FASE\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-FASE', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-FASE', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSEIONES FASE-FASE', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\TABLERO PRINCIPAL\\TENSIONES FASE-NEUTRO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-NEUTRO', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSIONES FASE-NEUTRO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'TENSEIONES FASE-NEUTRO', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\TABLERO PRINCIPAL\\CORRIENTES DE FASE\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTES DE FASE', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTES DE FASE', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTES DE FASE', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\ESPACIO INTERNO (SHELTER)\\TABLERO PRINCIPAL\\CORRIENTE Y TENSIÓN DE NEUTRO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTE Y TENSIÓN DE NEUTRO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'TABLERO PRINCIPAL', 'CORRIENTE Y TENSIÓN DE NEUTRO', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', '', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', '', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 1\\TENSIÓN GENERAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'TENSIÓN GENERAL', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'TENSIÓN GENERAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'TENSIÓN GENERAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 1\\CORRIENTE GENERAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'CORRIENTE GENERAL', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'CORRIENTE GENERAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'CORRIENTE GENERAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 1\\CORRIENTES DEL COMPRESOR\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'CORRIENTES DEL COMPRESOR', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'CORRIENTES DEL COMPRESOR', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'CORRIENTES DEL COMPRESOR', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 1\\PRESIONES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'PRESIONES', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'PRESIONES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'PRESIONES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 1\\LAVADO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'LAVADO', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'LAVADO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 1', 'LAVADO', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 2\\TENSIÓN GENERAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'TENSIÓN GENERAL', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'TENSIÓN GENERAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'TENSIÓN GENERAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 2\\CORRIENTE GENERAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'CORRIENTE GENERAL', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'CORRIENTE GENERAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'CORRIENTE GENERAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 2\\CORRIENTES DEL COMPRESOR\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'CORRIENTES DEL COMPRESOR', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'CORRIENTES DEL COMPRESOR', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'CORRIENTES DEL COMPRESOR', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 2\\PRESIONES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'PRESIONES', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'PRESIONES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'PRESIONES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 2\\LAVADO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'LAVADO', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'LAVADO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 2', 'LAVADO', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 3\\TENSIÓN GENERAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'TENSIÓN GENERAL', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'TENSIÓN GENERAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'TENSIÓN GENERAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 3\\CORRIENTE GENERAL\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'CORRIENTE GENERAL', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'CORRIENTE GENERAL', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'CORRIENTE GENERAL', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 3\\CORRIENTES DEL COMPRESOR\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'CORRIENTES DEL COMPRESOR', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'CORRIENTES DEL COMPRESOR', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'CORRIENTES DEL COMPRESOR', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 3\\PRESIONES\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'PRESIONES', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'PRESIONES', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'PRESIONES', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\AIRES ACONDICIONADOS\\AIRE 3\\LAVADO\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 3 == 0:
				fot1 = files[0]
				fot2 = files[1]
				fot3 = files[2]
				diap3(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'LAVADO', path + fot1, path + fot2, path + fot3)
				del files[0:3]
			elif len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'LAVADO', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'AIRES ACONDICIONADOS', 'AIRE 3', 'LAVADO', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 1\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 1\\BATERIA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'BATERIA', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'BATERIA', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 1\\FLUIDOS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'FLUIDOS', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'FLUIDOS', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 1\\HORAS DE OPERACIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'HORAS DE OPERACIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'HORAS DE OPERACIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 1\\NIVELES DE OPERACIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'NIVELES DE OPERACIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 1', 'NIVELES DE OPERACIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 2\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', '', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', '', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 2\\BATERIA\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'BATERIA', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'BATERIA', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 2\\FLUIDOS\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'FLUIDOS', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'FLUIDOS', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 2\\HORAS DE OPERACIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'HORAS DE OPERACIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'HORAS DE OPERACIÓN', path + fot1)
				del files[0]

		path = 'FOTOS\\PLANTA INTERNA\\MOTORGENERADOR\\MOTORGENERADOR 2\\NIVELES DE OPERACIÓN\\'
		path1 = i + '\\' + path
		files = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
		while len(files) > 0:
			if len(files) % 2 == 0:
				fot1 = files[0]
				fot2 = files[1]
				diap2(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'NIVELES DE OPERACIÓN', path + fot1, path + fot2)
				del files[0:2]
			else:
				fot1 = files[0]
				diap1(i, 'PLANTA INTERNA', 'MOTORGENERADOR 2', 'NIVELES DE OPERACIÓN', path + fot1)
				del files[0]
				
		with open(i + '\\rf.tex', 'a', encoding="utf-8") as file:
			file.write('\\end{document}')
			file.close()

		logging.info('Informe de ' + i + ' generado.')	

def rename():
	carps = [f for f in os.listdir() if os.path.isdir(f)]
	a = 1

	for i in carps:
		os.rename( i + "/rf.tex", i + "/MP-" + i.split('-')[0] + "-07-2024-" + str(a) + ".tex")
		a = a + 1

if __name__ == '__main__':
	
	compress()
	completadas = analisis()
	portada()
	cuerpo(completadas)
	rename()
