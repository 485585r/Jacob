from manim import *

class MidpointBetweenPointsOnParabola(Scene):
    def construct(self):
        # Axes setup
        axes = Axes(x_range=[-5, 5, 1], y_range=[-1, 9, 1], axis_config={"include_tip": False})
        self.play(Create(axes))

        # Parabola equation y = x^2
        parabola = axes.plot(lambda x: x**2, color=BLUE)
        self.play(Create(parabola))

        # Points A and B on the parabola
        A = axes.coords_to_point(-2, 4)
        B = axes.coords_to_point(2, 4)
        point_A = Dot(A, color=RED)
        point_B = Dot(B, color=RED)
        label_A = MathTex("A(-2, 4)").next_to(point_A, UP)
        label_B = MathTex("B(2, 4)").next_to(point_B, UP)

        self.play(FadeIn(point_A, label_A), FadeIn(point_B, label_B))

        # Midpoint C calculation
        C_x = (-2 + 2) / 2
        C_y = (4 + 4) / 2
        C = axes.coords_to_point(C_x, C_y)
        point_C = Dot(C, color=GREEN)
        label_C = MathTex("C(0, 4)").next_to(point_C, UP)

        self.play(FadeIn(point_C, label_C))

        # Line connecting A, C, and B
        line = Line(A, B, color=YELLOW)
        self.play(Create(line))

        # Explanation text
        explanation = Text("Midpoint C is calculated as:\\nC_x = (A_x + B_x) / 2\\nC_y = (A_y + B_y) / 2", font_size=24).to_edge(DOWN)
        self.play(Write(explanation))

        self.wait(3)