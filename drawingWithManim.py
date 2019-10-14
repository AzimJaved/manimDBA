from manimlib.imports import *

class RotaCompass(Rotating):
    CONFIG = {
        "rate_func": smooth,
        "run_time": 2
    }
class Compass(VGroup):
    CONFIG = {
        "height": 2.5,
        "stroke_material": 0.7,
        "esparrago_width": 0.06,
        "needle_height": 0.1,
        "hinge_radius_1": 0.06,
        "hinge_width": 0.3,
        "hinge_height": 0.7,
        "hinge_support_width": 0.1,
        "hinge_support_height": 0.3,
    }
    def __init__(self,start=ORIGIN,gap=1.5,**kwargs):
        digest_config(self,kwargs)
        super().__init__()
        # Points of compass
        needle_start_a = start
        needle_end_a = start+UP*self.needle_height
        p3 = start+RIGHT*gap/2+UP*self.height
        p2 = start+RIGHT*gap+UP*self.needle_height
        p1 = start+p3+UP*self.stroke_material
        needle_start_b = p2
        needle_end_b = needle_start_b+DOWN*self.needle_height
        hinge_coord = (p1-p3)/3+p3
        # needles
        needle_a = Line(needle_start_a,needle_end_a,buff=0,stroke_width=2)
        needle_b = Line(needle_start_b,needle_end_b,buff=0,stroke_width=2)
        needle_a.set_color(color=[WHITE,WHITE])
        needle_b.set_color(color=[WHITE,WHITE])
        # body
        body = Polygon(needle_end_a,p1,p2,p3).set_fill(BLUE,1)
        body.set_color(color=[interpolate_color(GRAY,BLACK,0.5),GRAY,interpolate_color(GRAY,BLACK,0.5)])
        body.set_sheen_direction(UP)
        # hinge
        hinge_rectangle = Rectangle(width=self.hinge_width,height=self.hinge_height,fill_opacity=1)
        h_p1 = hinge_rectangle.get_corner(DL)
        h_p2 = hinge_rectangle.get_corner(UL)
        h_p3 = h_p2+RIGHT*(self.hinge_width-self.hinge_support_width)/2
        h_p4 = h_p3 + UP*self.hinge_support_height
        h_p5 = h_p4 + RIGHT*self.hinge_support_width
        h_p6 = h_p5 + DOWN*self.hinge_support_height
        h_p7 = hinge_rectangle.get_corner(UR)
        h_p8 = hinge_rectangle.get_corner(DR)
        hinge_support = Polygon(h_p1,h_p2,h_p3,h_p4,h_p5,h_p6,h_p7,h_p8,fill_opacity=1)
        hinge_support.set_color(color=[ORANGE,RED])
        hinge_support.set_sheen_direction(UP)
        hinge = VGroup(
            hinge_support,
            Dot(radius=self.hinge_radius_1*1.2,color=interpolate_color(GRAY,BLACK,0.5)),
            Dot(radius=self.hinge_radius_1,color=GRAY),
            )
        hinge.move_to(hinge_coord)
        self.gap=gap
        self.needle_a=needle_start_a
        self.needle_b=needle_end_b
        self.needle_a_line = needle_a
        self.needle_b_line = needle_b
        self.draws=VGroup()
        self.add(body,hinge,needle_a,needle_b)

    def get_needle_a_coord(self):
        return self.needle_a_line.get_start()

    def get_needle_b_coord(self):
        return self.needle_b_line.get_end()

    def Draw(self,angle,needle="A",arc_color=RED,arc_start=0,**anim_kwargs):
        if needle == "A":
            point = self.get_needle_a_coord()
            start_angle = 0 + arc_start
        if needle == "B":
            point = self.get_needle_b_coord()
            start_angle = PI + arc_start
            angle=-angle
        ratate_compass = RotaCompass(self,radians=angle,about_point=point,**anim_kwargs)
        arc = Arc(angle=angle,radius=self.gap,arc_center=point,start_angle=start_angle,color=arc_color)
        draw = ShowCreation(arc,**anim_kwargs)
        self.draws.add(arc)
        return [ratate_compass,draw]
        

class CompassScene(Scene):
    def construct(self):
        #self.show_compass()
        self.simple_animation()
        
    def show_compass(self):
        compas = Compas()
        self.add(compas)
        
    def simple_animation(self):
        arc = PI*2
        compass = Compass()
        compass2 = Compass(gap=3,stroke_material=0.4)
        dot = Dot(radius=0.05)

        self.play(GrowFromCenter(dot))
        self.add_foreground_mobject(compass)

        self.play(FadeInFrom(compass,UP))
        self.play(
            *compass.Draw(arc,needle="B",arc_color=BLUE),
            run_time=3
            )
        self.play(ReplacementTransform(compass,compass2))
        self.add_foreground_mobject(compass2)
        self.play(
            *compass2.Draw(PI),
            run_time=3
            )
        self.play(
            *compass2.Draw(PI,needle="B",arc_start=-PI),
            run_time=3
            )
        self.play(compass.draws[0].set_color,PINK)
        self.play(compass2.draws[0].set_color,YELLOW)
        self.play(compass2.draws[1].set_color,PURPLE)
        self.wait()