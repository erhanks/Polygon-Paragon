# Name: Pen Hanks

""" 
Polygon Paragon

I've made what essentially operates as a merge game; you click on matching shapes to make them into a bigger one. 
You need to combine as many shapes as the number says in the middle; 
for example, you need to combine 3 triangles to make a square, 4 squares to make a pentagon, etc
It'll make a bit more sense once you start up the game; I have a rules screen with a demonstration
There is a little bit of lag between when you click on enough shapes and when they combine, just wait a half second and it'll work


"""



from pgl import GWindow, GRect, GPolygon, GPolygon, GLine, GLabel, GCompound, GOval
from math import pi, sin, cos
from random import randint

#Starting (aka editable) constants
GW_HEIGHT = 800 #anything smaller than 500, the rules screen starts to get cut off, recommended size is 800 x 800 
GW_WIDTH = 800
GRIDX, GRIDY = 10, 10 # max recommended grid size for 800 x 800 is 15, you can do ~20, but the shapes turn into blobs very quickly
START_POLY_MIN = 3 #degree of minimum starting polygon, can't be less than 3
START_POLY_MAX = 8 #degree of maximum starting polygon; I don't recommend going over ~10ish, but I have distinct colors for up to 18
POLY_BOX_DISTANCE = 5 #distance between grid lines and polygon

#Derived constants
SQUARE_WIDTH = GW_WIDTH/GRIDX
HALF_SQUARE_W = SQUARE_WIDTH / 2
SQUARE_HEIGHT = GW_HEIGHT/GRIDY
HALF_SQUARE_H = SQUARE_HEIGHT / 2


def merge_game():
    #starting values and the like
    gw = GWindow(GW_WIDTH,GW_HEIGHT)
    color_list = ['#FF0000', '#FFA500','#FFFF00','#32CD32', '#0000FF', '#BA55D3', '#FFC0CB', '#800000', '#D2691E', '#DAA520', '#006400', '#000080', '#4B0082','#FFC0CB', '#C71585', '#FF1493']
    gw.current_shape = None
    gw.current_color = None
    gw.ngon_tracker = 0
    gw.shape_list = []
    gw.started = False

    #functions!! 
    def generate_grid(): 
        for i in range(GRIDX):
            vert_line = GLine(i*SQUARE_WIDTH,0,i*SQUARE_WIDTH,GW_HEIGHT)
            gw.add(vert_line)
        for j in range(GRIDY):
            horiz_line = GLine(0,j*SQUARE_HEIGHT,GW_WIDTH,j*SQUARE_HEIGHT)
            gw.add(horiz_line)

    #def generate_polygon(n_gon): 
       # shape = GPolygon()
      #  first_vert = (HALF_SQUARE_H) - POLY_BOX_DISTANCE
       # side_length = 2*(first_vert) * sin(pi/n_gon)
        #shape.add_vertex(first_vert,0)
        #angle = ((n_gon-2)*180)/n_gon
        #shape.add_polar_edge(side_length, angle)
        #shape.add_polar_edge(side_length, -angle)
        #shape.set_line_width(5)
        #print(first_vert)
        #return shape
    
    def generate_polygon_again(n_gon): #to generate a regular polygon with its corresponding color
        shape = GPolygon()
        radius = (min(HALF_SQUARE_H,HALF_SQUARE_W)) - POLY_BOX_DISTANCE
        shape.add_vertex(0,-radius)
        for i in range(n_gon-1):
            coord = rect(radius, ((i+1) * ((2*pi)/n_gon))-(pi / 2))
            shape.add_vertex(coord[0],coord[1])
        shape.set_line_width(5)
        shape.set_color(color_list[n_gon-3])
        return shape

    def generate_outline(n_gon): # to generate the outline for the given regular polygon
        shape = GPolygon()
        radius = (HALF_SQUARE_H) - POLY_BOX_DISTANCE
        shape.add_vertex(0,-radius)
        for i in range(n_gon-1):
            coord = rect(radius+3, ((i+1) * ((2*pi)/n_gon))-(pi / 2))
            shape.add_vertex(coord[0],coord[1])
        shape.set_line_width(2)
        shape.set_color(color_list[n_gon-3])
        return shape

    def game_shape(n_gon,x,y): #adding the rest of the game components together in a GCompound
        game_piece = GCompound()
        game_piece.add (generate_polygon_again(n_gon))
        number = GLabel(str(n_gon))
        number.set_font("10pt serif")
        if n_gon < 10:
            game_piece.add(number,-2.5,5)
        else: 
            game_piece.add(number,-6,5)
        gw.add(game_piece,x,y)
        game_piece.set_color(color_list[n_gon-3]) #although this doesn't change anything visually, it makes shape identification much easier

    def rect(r,theta): #coordinate function
        x = r * cos(theta)
        y = r * sin(theta)
        return (x,y)
    
    def merge_shape(event): #What happens when you click! 
        ex = event.get_x()
        ey = event.get_y()

        if gw.started == False: #Clears rules screen and starts the game
            gw.clear()
            generate_grid()
            filler_circle = GOval(((HALF_SQUARE_W) - POLY_BOX_DISTANCE)*2,((HALF_SQUARE_H) - POLY_BOX_DISTANCE)*2) #this is the "refill" circle
            filler_circle.set_filled(True)
            filler_circle.set_color("#795548")
            gw.add(filler_circle, 5,5)
            starting_board()
            gw.started = True

        if gw.current_color == None and gw.started == True: #confirming we started the game and we don't have a current shape/color
            gw.current_shape = gw.get_element_at(ex,ey) 
            if gw.current_shape is not None: # just in case if when you clicked on it, it was nothing
                color = gw.current_shape.get_color()
                if color == "#795548": # if you've clicked on the regenerate circle
                    starting_board()
                elif color != 'Black':  #making sure you haven't clicked the grid
                    gw.ngon_tracker+=1
                    ind = color_list.index(color)
                    gw.current_color = color
                #outline = generate_outline(ind+3)
                #outline.set_color("black")
                #gw.current_shape.add(outline)

        else: #if there is a color currently assigned to gw.current_color
            second_shape = gw.get_element_at(ex,ey)
            if second_shape is not None: #again, making sure it doesnt explode when you try and take stuff from it
                sx,sy = second_shape.get_x(), second_shape.get_y()
                cx,cy = gw.current_shape.get_x(), gw.current_shape.get_y()
                if sx != cx or sy != cy: #if at least one coordinate is different
                    second_color = second_shape.get_color()
                    index = color_list.index(gw.current_color)
                    if second_color == gw.current_color and gw.ngon_tracker == (index+2): #if you clicked on the right guy and its the last one needed
                        gw.remove(second_shape)
                        gw.remove(gw.current_shape)
                        for j in range(len(gw.shape_list)):
                            gw.remove(gw.shape_list[j]) #removes all the shapes we stored
                        gw.current_shape = None
                        gw.current_color = None
                        gw.ngon_tracker = 0
                        nx_coeff = round((ex - (HALF_SQUARE_W))/SQUARE_WIDTH)
                        ny_coeff = round((ey - (HALF_SQUARE_H))/SQUARE_HEIGHT)
                        nx = (HALF_SQUARE_W)+ (SQUARE_WIDTH*nx_coeff)
                        ny = (HALF_SQUARE_H)+ (SQUARE_HEIGHT*ny_coeff)
                        game_shape(index + 4,nx,ny)
                        shape_list=[]
                    elif second_color == gw.current_color and gw.ngon_tracker < (index+3): #if you clicked on the right shape but still need more shapes
                        gw.ngon_tracker += 1
                        gw.shape_list.append(second_shape)

                    else: #you clicked on the wrong shape
                        gw.current_shape = None
                        gw.current_color = None
    def starting_board(): 
        for i in range(GRIDX):
            for j in range(GRIDY):
                if gw.get_element_at(HALF_SQUARE_W + (i * SQUARE_WIDTH), HALF_SQUARE_H + (j*SQUARE_HEIGHT)) == None:
                    vert = randint(START_POLY_MIN,START_POLY_MAX)
                    game_shape(vert, HALF_SQUARE_W + (i * SQUARE_WIDTH), HALF_SQUARE_H + (j*SQUARE_HEIGHT))

    def rules_screen():
        #labels
        title = GLabel("Polygon Paragon")
        objective = GLabel("Objective: combine polygons to make polygons of higher degree")
        rules_1 = GLabel("Rules: You can only combine polygons of the same degree")
        rules_2 = GLabel("You need as many polygons as the number in the center of the polygons")
        tip = GLabel("Tip: if you get stuck, hit the brown circle and the board will refill with shapes")
        equal = GLabel("=")
        start = GLabel("Click anywhere to start!")
        #fonts
        title.set_font("40pt serif")
        title.set_color("#795548")
        objective.set_font("13pt serif")
        rules_1.set_font("13pt serif")
        rules_2.set_font("11pt serif")
        tip.set_font("10pt serif")
        start.set_font("30pt serif")
        start.set_color("#795548")
        equal.set_font("30pt serif")
        #adding to window
        gw.add(title,GW_WIDTH * .1, GW_HEIGHT *.3)
        gw.add(objective, GW_WIDTH * .05, GW_HEIGHT*.4)
        gw.add(rules_1, GW_WIDTH * .05, GW_HEIGHT*.45)
        gw.add(rules_2, GW_WIDTH * .05, GW_HEIGHT*.5)
        gw.add(tip, GW_WIDTH * .05, GW_HEIGHT*.55)
        gw.add(start, GW_WIDTH * .15, GW_HEIGHT*.8)
        gw.add(equal,GW_WIDTH* .57,GW_HEIGHT *.675 )
        game_shape(3, GW_WIDTH * .3,GW_HEIGHT *.65)
        game_shape(3,GW_WIDTH *.4,GW_HEIGHT *.65 )
        game_shape(3 ,GW_WIDTH * .5 , GW_HEIGHT *.65)
        game_shape(4,GW_WIDTH* .7 ,GW_HEIGHT *.65 )



    rules_screen()
    gw.add_event_listener("click", merge_shape)



if __name__ == '__main__':
    merge_game()