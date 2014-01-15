'''
Este modulo en Python fue diseñado para crear los personajes y sus disparos y poderes del juego SpiderMan Vs Green Goblin.
Permite crear mapas de bits de forma muy sencilla gracias a que en la interfaz
grafica se muestra una cuadricula de 32 * 32 cuadros cada uno de ellos representando un bit, en la cual solamente
se tiene que hacer click sobre el recuadro para pintarlo del color elejido por el usuario los cuales se pueden cambiar
pusando cualquiera de las teclas numricas del 0 - 9 y las teclas de funciones F1 - F9 o pulsando uno de los botones de color.
Al terminar el diseño del mapa de bits se tiene que guardar el archivo de salida y generar los archivos .txt
con los datos correspondientes.
Tambien existe la posibilidad de cargar nuevamente el archivo generado para continuar con el diseño en caso
de no finalizarlo antes.

Pix Map Generator
Created by: Jassael Ruiz
Version: 1.0
'''

# librerias a usar
import sys
sys.path.append('..')
import simplegui as sg

# global variables
width = 500
height = 500
lado = 13
x1i = 10
y1i = 10
x2i = x1i + lado
y2i = y1i + lado
squares_list = []
pix_map = []
size = [32, 32]
sep = 2
h = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]
pix_map_colors = []
colors = ['#000000', '#FFFFFF', '#0F1385', '#6165C5', '#739AF5', '#9B2121', '#CA1C1C', '#ED7171', '#B1B3B9']
colors_green_globin = ['#810872', '#C33C97', '#33972E', '#2AC124', '#E4CA2A']
colors_pumpking = ['#39A874', '#66FFB8', '#D6891C', '#FBD39C']
power_spider = ['#87ECFF'] # 18
colors.extend(colors_green_globin)
colors.extend(colors_pumpking)
colors.extend(power_spider)
ind_colors = 8
file_text_saved = 'colors'
pix_map_saved = 'pix map'
matrix_colors_saved = 'matrix colors'
load_file_name = 'colors'

def pix_map_to_hex():
    '''
    Convierte el mapa de pixeles de la figura creada que contiene valores 0 si no esta activo ese pixel
    o 1 si esta activo ese pixel a un mapa hexadecimal que contiene cada uno de los
    renglones de la matriz del mapa de bits
    '''
    
    hex_pix_map = ''
    hex_pix_map = []
    num_hex = ''
    num = ''
    serie = ''
    ind = 1
    for ren in range(0, size[0]):
        for col in range(0, size[1]):
            num += pix_map[ren][col]
            if(ind == 4 and col != 0):
                num_hex = dec_to_hex(bin_dec(num))
                serie += num_hex
                num = ''
                ind = 0
            if(len(serie) == 8):
                hex_pix_map.append('0x' + serie)
                serie = ''
                num = ''
                ind = 0
            ind += 1
        ind = 1
    return hex_pix_map

def bin_dec(n):
    # Convierte un numero binario a decimal

    bin_num = n[::-1]
    d = 0
    for ind in range(0, len(bin_num)):
        d += int(bin_num[ind]) * (2 ** ind)
    return d
                
def dec_to_hex(n):
    # Convierte un numero decimal a hexadecimal
    
    first = h[n % 16]
    return str(first)

def distancia(pos, x1, x2, y1, y2):
    # Retorna verdadero si la posicion del click hecho esta dentro de los limites del cuadro gris
    
    x = pos[0]
    y = pos[1]

    if(x1 <= x <= x2 and y1 <= y <= y2):
       return True

def change_value(ren, col, value):
    # Cambia el valor del mapa de pixeles al indicado por value
    
    pix_map[ren][col] = value

def change_color(ren, col, value):
    # Cambia el valor del color del mapa de pixeles al indicado por value
    
    pix_map_colors[ren][col] = value

def updateClickColor(p):
    '''
    Actualiza el color del mapa de pixeles de cada uno de los cuadros sobre los que se hizo click
    al color seleccionado por el usuario
    '''
    
    pos = p
    for ren in range(size[0]):
        for col in range(size[1]):
            square = squares_list[ren][col]
            x1 = square[0]
            x2 = square[1]
            y1 = square[2]
            y2 = square[3]
            dist = distancia(pos, x1, x2, y1, y2)
            if(dist):
                color = colors[ind_colors]
                if(ind_colors == 8):
                    change_value(ren, col, '0')
                else:
                    change_value(ren, col, '1')
                change_color(ren, col, ind_colors)
                square[-1] = color
                
def updateDragColor(p):
    '''
    Actualiza el color del mapa de pixeles de cada uno de los cuadros sobre los que se arrastro el mouse
    al color seleccionado por el usuario
    '''
    
    pos = p
    for ren in range(size[0]):
        for col in range(size[1]):
            square = squares_list[ren][col]
            x1 = square[0]
            x2 = square[1]
            y1 = square[2]
            y2 = square[3]
            color = square[-1]
            dist = distancia(pos, x1, x2, y1, y2)
            if(dist):
                color = colors[ind_colors]
                change_value(ren, col, '1')
                change_color(ren, col, ind_colors)
                square[-1] = color
                
def click(p):
    # Click Handler
    
    updateClickColor(p)

def drag(p):
    # Drag Handler
    
    updateDragColor(p)

def llenar():
    # Inicializa el mapa de bits, la matriz de cuadros a dibujar en el canvas y los colores del mapa de bits
    
    global x1i, x2i, y1i, y2i
    x1 =  x1i
    x2 =  x2i
    y1 =  y1i
    y2 =  y2i
    pix_ren = []
    squares_ren = []
    colors_ren = []
    for ren in range(size[0]):
        for col in range(size[1]):
            new_square = [x1, x2, y1, y2, colors[8]]
            squares_ren.append(new_square)
            x1 += lado + sep
            x2 += lado + sep
            pix_ren.append('0')
            colors_ren.append(ind_colors)
        y1 += lado + sep
        y2 += lado + sep
        x1 =  x1i
        x2 =  x2i
        pix_map.append(pix_ren)
        pix_ren = []
        squares_list.append(squares_ren)
        squares_ren = []
        pix_map_colors.append(colors_ren)
        colors_ren = []
        
def draw(c):
    # Draw Handler, aqui se dibuja la matriz de cuadros en el canvas
    
    for ren in range(size[0]):
        for col in range(size[1]):
            square = squares_list[ren][col]
            color = square[-1]
            x1 = square[0]
            x2 = square[1]
            y1 = square[2]
            y2 = square[3]
            c.draw_polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], 1, color, color)

def pixm():
    # Guarda los archivos con los nombres indicados del diseño realizado
    
    save_pix_map(pix_map_saved)
    save_matrix_colors(matrix_colors_saved)
    save_file_colors(file_text_saved)

def save_file_colors(name):
    # Guarda en el archivo el conjunto de colores correspondientes al diseño hecho, este es usado
    # para continuar el diseño despues
    
    with open(name+'.txt', 'w') as file:
        archivo = ''
        for ren in range(len(pix_map_colors)):
            for col in range(len(pix_map_colors[ren])):
                archivo += str(pix_map_colors[ren][col])
                if(col < len(pix_map_colors[ren]) - 1):
                    archivo += ','
            archivo += '\n'
        file.write(archivo)

    print('File created: ' + name + '.txt')
    

def save_pix_map(name):
    # Guarda en el archivo el mapa de bits con los valores hexadecimales correspondiente al diseño hecho
    
    matriz = pix_map_to_hex()
    with open(name + '.txt', 'w') as file:
        file.write('{\n')
        for ind in range(len(matriz)):
            ren = matriz[ind]
            file.write(ren)
            if(ind < (len(matriz) - 1)):
                file.write(',')
            file.write('\n')
        file.write('};')
    print('File created: ' + name + '.txt')

def save_matrix_colors(name):
    # Guarda en el archivo la matriz de colores con los valores decimales correspondiente al diseño hecho
    
    with open(name + '.txt', 'w') as file:
        file.write('{\n')
        colors = ''
        for ren in range(len(pix_map_colors)):
            colors += '{'
            for col in range(len(pix_map_colors[ren])):
                colors += str(pix_map_colors[ren][col])
                if(col < len(pix_map_colors[ren]) - 1):
                    colors += ', '
            colors += '}'
            if(ren < len(pix_map_colors) - 1):
                colors += ','
            colors += '\n'
        file.write(colors)
        file.write('};')
    print('File created: ' + name + '.txt')

def down(key):
    # Key Handler, permite al usuario seleccionar un color distinto de los listados abajo
    
    global ind_colors, label
    if(key == sg.KEY_MAP['0']):
        ind_colors = 0
    if(key == sg.KEY_MAP['1']):
        ind_colors = 1
    if(key == sg.KEY_MAP['2']):
        ind_colors = 2
    if(key == sg.KEY_MAP['3']):
        ind_colors = 3
    if(key == sg.KEY_MAP['4']):
        ind_colors = 4
    if(key == sg.KEY_MAP['5']):
        ind_colors = 5
    if(key == sg.KEY_MAP['6']):
        ind_colors = 6
    if(key == sg.KEY_MAP['7']):
        ind_colors = 7
    if(key == sg.KEY_MAP['8']):
        ind_colors = 8
    if(key == sg.KEY_MAP['9']):
        ind_colors = 9
    if(key == sg.KEY_MAP['F1']):
        ind_colors = 10
    if(key == sg.KEY_MAP['F2']):
        ind_colors = 11
    if(key == sg.KEY_MAP['F3']):
        ind_colors = 12
    if(key == sg.KEY_MAP['F4']):
        ind_colors = 13
    if(key == sg.KEY_MAP['F5']):
        ind_colors = 14
    if(key == sg.KEY_MAP['F6']):
        ind_colors = 15
    if(key == sg.KEY_MAP['F7']):
        ind_colors = 16
    if(key == sg.KEY_MAP['F8']):
        ind_colors = 17
    if(key == sg.KEY_MAP['F9']):
        ind_colors = 18
    label.set_text("Color:"+' '+str(ind_colors))

def set_file_name(txt):
    # Establece el nombre del archivo a cargar que contiene los colores del diseño
    
    global load_file_name
    if(len(txt) > 0):
        load_file_name = txt

def set_sfile_name(txt):
    # Establece el nombre del archivo a guardar que contiene los valores decimales de los colores del diseño
    
    global file_text_saved
    if(len(txt) > 0):
        file_text_saved = txt        

def set_pix_map_name(txt):
    # Establece el nombre del archivo a guardar que contiene los valores hexadecimales del diseño
    
    global pix_map_saved
    if(len(txt) > 0):
        pix_map_saved = txt

def set_matrix_colors_name(txt):
    # Establece el nombre del archivo a guardar que contiene la matriz de colores del diseño
    
    global matrix_colors_saved
    if(len(txt) > 0):
        matrix_colors_saved = txt

# Button Pressed Handler, cambia el color con el que se pintan los cuadros
    
def set_color_black():
    global ind_colors, label
    ind_colors = 0
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_white():
    global ind_colors, label
    ind_colors = 1
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_blue1():
    global ind_colors, label
    ind_colors = 2
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_blue2():
    global ind_colors, label
    ind_colors = 3
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_blue3():
    global ind_colors, label
    ind_colors = 4
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_red1():
    global ind_colors, label
    ind_colors = 5
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_red2():
    global ind_colors, label
    ind_colors = 6
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_red3():
    global ind_colors, label
    ind_colors = 7
    label.set_text("Color:"+' '+str(ind_colors))
    
def set_color_gray():
    global ind_colors, label
    ind_colors = 8
    label.set_text("Color:"+' '+str(ind_colors))

def set_color_purple1():
    global ind_colors, label
    ind_colors = 9
    label.set_text("Color:"+' '+str(ind_colors))

def set_color_purple2():
    global ind_colors, label
    ind_colors = 10
    label.set_text("Color:"+' '+str(ind_colors))

def set_color_green1():
    global ind_colors, label
    ind_colors = 11
    label.set_text("Color:"+' '+str(ind_colors))

def set_color_green2():
    global ind_colors, label
    ind_colors = 12
    label.set_text("Color:"+' '+str(ind_colors))

def set_color_yellow1():
    global ind_colors, label
    ind_colors = 13
    label.set_text("Color:"+' '+str(ind_colors))

def reverse_matrix():
    '''
    Una vez que tenemos cargado el archivo que contiene los colores del diseño podemos invertir la matriz de
    colores de izquierda a derecha con este metodo
    '''
    
    global squares_list, pix_map_colors
    matriz_colores = []

    try:
        
        with open(load_file_name + '.txt', 'r') as file:
            for line in file:
                matriz_colores.append(line.strip('\n').split(','))
        print('File loaded:' + load_file_name )
    
        for ren in range(len(matriz_colores)):
            for col in range(len(matriz_colores[ren]) // 2):
                matriz_colores[ren][col], matriz_colores[ren][-(col+1)] = matriz_colores[ren][-(col+1)], matriz_colores[ren][col]
    
        for ren in range(len(squares_list)):
            for col in range(len(squares_list[ren])):
                square = squares_list[ren][col]
                ind_color = int(matriz_colores[ren][col])
                square[-1] = colors[ind_color]
                if(ind_color == 8):
                    change_value(ren, col, '0')
                else:
                    change_value(ren, col, '1')
                change_color(ren, col, ind_color)
                
    except FileNotFoundError:
        print("No se pudo cargar el archivo: " + load_file_name + '.txt')    

def load_file_colors():
    # Permite cargar el archivo de colores con el nombre indicado, para seguir modificandolo
    
    global squares_list, pix_map_colors
    matriz_colores = []

    try:
        
        with open(load_file_name + '.txt', 'r') as file:
            for line in file:
                matriz_colores.append(line.strip('\n').split(','))
        print('File loaded:' + load_file_name )
    
        for ren in range(len(squares_list)):
            for col in range(len(squares_list[ren])):
                square = squares_list[ren][col]
                ind_color = int(matriz_colores[ren][col])
                square[-1] = colors[ind_color]
                if(ind_color == 8):
                    change_value(ren, col, '0')
                else:
                    change_value(ren, col, '1')
                change_color(ren, col, ind_color)
                
    except FileNotFoundError:
        print("No se pudo cargar el archivo: " + load_file_name + '.txt')

def delete_all():
    # Borra todos los cuadros pintados estableciendo el color predeterminado el gris
    
    for ren in range(len(squares_list)):
        for col in range(len(squares_list[ren])):
            square = squares_list[ren][col]
            square[-1] = colors[8]

#create frame    
f =  sg.create_frame("Pix map Generator", width, height)
#register event handler´s for control elements
f.set_draw_handler(draw)
f.set_mouseclick_handler(click)
f.set_mousedrag_handler(drag)
f.add_button("Invertir matriz de colores", reverse_matrix, 80)
f.add_button("Guardar archivos.txt", pixm, 80)
f.add_button("Cargar archivo colores", load_file_colors, 80)
input4 = f.add_input("File´s name to load", set_file_name, 80)
input4.set_text(load_file_name)
input1 = f.add_input("Save file colors as", set_sfile_name, 80)
input1.set_text(file_text_saved)
input2 = f.add_input("Save pix map as", set_pix_map_name, 80)
input2.set_text(pix_map_saved)
input3 = f.add_input("Save colors matrix as", set_matrix_colors_name, 80)
input3.set_text(matrix_colors_saved)
f.add_button("Borrar todo", delete_all, 70)
f.add_button("Black: 0", set_color_black, 70)
f.add_button("White: 1", set_color_white, 70)
f.add_button("Blue1: 2", set_color_blue1, 70)
f.add_button("Blue2: 3", set_color_blue2, 70)
f.add_button("Blue3: 4", set_color_blue3, 70)
f.add_button("Red1: 5", set_color_red1, 70)
f.add_button("Red2: 6", set_color_red2, 70)
f.add_button("Red3: 7", set_color_red3, 70)
f.add_button("Gray: 8", set_color_gray, 70)
f.add_button("Purple1: 9", set_color_purple1, 70)
f.add_button("Purple2: 10", set_color_purple2, 70)
f.add_button("Green1: 11", set_color_green1, 70)
f.add_button("Green2: 12", set_color_green2, 70)
f.add_button("Yellow1: 13", set_color_yellow1, 70)
label = f.add_label("Color:"+' '+str(ind_colors))
f.set_keydown_handler(down)
# set canvas background
f.set_canvas_background('#D1E3EC')
llenar()
# start frame
f.start()
