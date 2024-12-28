from manim import *

class ParabolaMidpoint(Scene):
    def construct(self):
        # Create axes
        axes = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 1], axis_config={"include_numbers": True})
        self.play(Create(axes))

        # Define the parabola
        parabola = axes.plot(lambda x: x**2, color=BLUE)
        self.play(Create(parabola))

        # Define two points on the parabola with the same y-coordinate (e.g., y=4)
        point1 = Dot(axes.coords_to_point(-2, 4), color=RED)
        point2 = Dot(axes.coords_to_point(2, 4), color=RED)
        self.play(FadeIn(point1), FadeIn(point2))

        # Draw lines from these points to the x-axis
        line1 = axes.get_vertical_line(axes.input_to_graph_point(-2, parabola), color=YELLOW)
        line2 = axes.get_vertical_line(axes.input_to_graph_point(2, parabola), color=YELLOW)
        self.play(Create(line1), Create(line2))

        # Calculate the midpoint
        midpoint_x = (-2 + 2) / 2
        midpoint_y = 4
        midpoint = Dot(axes.coords_to_point(midpoint_x, midpoint_y), color=GREEN)
        self.play(FadeIn(midpoint))

        # Show labels for points and midpoint
        label1 = MathTex("(-2, 4)").next_to(point1, LEFT)
        label2 = MathTex("(2, 4)").next_to(point2, RIGHT)
        label_mid = MathTex("(0, 4)").next_to(midpoint, UP)
        self.play(Write(label1), Write(label2), Write(label_mid))

        # Add explanation text
        explanation = Tex("The midpoint is calculated as:").to_edge(UP)
        midpoint_formula = MathTex("\\left(\\frac{x_1 + x_2}{2}, \\frac{y_1 + y_2}{2}\\right)").next_to(explanation, DOWN)
        self.play(Write(explanation), Write(midpoint_formula))
        self.wait(3)