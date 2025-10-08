import math
from typing import List, Optional, Union

# A small constant for floating-point comparisons to handle precision errors.
EPSILON = 1e-9

# ==============================================================================
# 1. GEOMETRIC OBJECT DEFINITIONS
# ==============================================================================

class Point:
    """Represents a point in a 2D Cartesian coordinate system."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x:.2f}, {self.y:.2f})"
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return math.isclose(self.x, other.x, abs_tol=EPSILON) and \
               math.isclose(self.y, other.y, abs_tol=EPSILON)

    def distance_to(self, other: 'Point') -> float:
        """Calculates the Euclidean distance to another point."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def translate(self, dx: float, dy: float) -> 'Point':
        """Translates the point by (dx, dy)."""
        return Point(self.x + dx, self.y + dy)

    def scale(self, factor: float, origin: 'Point') -> 'Point':
        """Scales the point by a factor relative to an origin point."""
        new_x = origin.x + (self.x - origin.x) * factor
        new_y = origin.y + (self.y - origin.y) * factor
        return Point(new_x, new_y)

    def rotate(self, angle_rad: float, origin: 'Point') -> 'Point':
        """Rotates the point by an angle in radians around an origin."""
        x_rel = self.x - origin.x
        y_rel = self.y - origin.y
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        new_x_rel = x_rel * cos_a - y_rel * sin_a
        new_y_rel = x_rel * sin_a + y_rel * cos_a
        
        return Point(origin.x + new_x_rel, origin.y + new_y_rel)

class Line:
    """Represents a line defined by two points or by ax + by + c = 0."""
    def __init__(self, p1: Point, p2: Point):
        if p1 == p2:
            raise ValueError("A line must be defined by two distinct points.")
        self.p1 = p1
        self.p2 = p2
        
        # Coefficients for the general form ax + by + c = 0
        self.a = p2.y - p1.y
        self.b = p1.x - p2.x
        self.c = -self.a * p1.x - self.b * p1.y

    def __repr__(self) -> str:
        return f"Line from {self.p1} to {self.p2}"

    def intersection_line(self, other: 'Line') -> Optional[Point]:
        """Calculates the intersection point with another line."""
        det = self.a * other.b - other.a * self.b
        if math.isclose(det, 0, abs_tol=EPSILON):
            # Lines are parallel or coincident
            return None
        
        x = (self.b * other.c - other.b * self.c) / det
        y = (other.a * self.c - self.a * other.c) / det
        return Point(x, y)

    def intersection_circle(self, circle: 'Circle') -> List[Point]:
        """Calculates intersection points with a circle."""
        # Find the foot of the perpendicular from the circle's center to the line
        foot = foot_of_perpendicular(self, circle.center)
        dist_center_to_line = circle.center.distance_to(foot)
        
        # Case 1: No intersection
        if dist_center_to_line > circle.radius + EPSILON:
            return []
        
        # Case 2: One intersection (tangent)
        if math.isclose(dist_center_to_line, circle.radius, abs_tol=EPSILON):
            return [foot]
            
        # Case 3: Two intersections
        # Use Pythagorean theorem to find distance from foot to intersection points
        dist_foot_to_intersection = math.sqrt(circle.radius**2 - dist_center_to_line**2)
        
        # Direction vector of the line
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        line_length = self.p1.distance_to(self.p2)
        
        # Unit direction vector
        ux = dx / line_length
        uy = dy / line_length
        
        # Calculate the two intersection points
        p_intersect1 = Point(foot.x + dist_foot_to_intersection * ux, 
                             foot.y + dist_foot_to_intersection * uy)
        p_intersect2 = Point(foot.x - dist_foot_to_intersection * ux, 
                             foot.y - dist_foot_to_intersection * uy)
                             
        return [p_intersect1, p_intersect2]
    
    def translate(self, dx: float, dy: float) -> 'Line':
        return Line(self.p1.translate(dx, dy), self.p2.translate(dx, dy))

    def scale(self, factor: float, origin: Point) -> 'Line':
        return Line(self.p1.scale(factor, origin), self.p2.scale(factor, origin))

    def rotate(self, angle_rad: float, origin: Point) -> 'Line':
        return Line(self.p1.rotate(angle_rad, origin), self.p2.rotate(angle_rad, origin))

class Circle:
    """Represents a circle defined by a center point and a radius."""
    def __init__(self, center: Point, radius: float):
        if radius <= 0:
            raise ValueError("Radius must be a positive number.")
        self.center = center
        self.radius = radius

    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius:.2f})"

    def intersection_circle(self, other: 'Circle') -> List[Point]:
        """Calculates intersection points with another circle."""
        d = self.center.distance_to(other.center)

        # Non-intersecting cases
        if d > self.radius + other.radius or d < abs(self.radius - other.radius):
            return []
        
        # Coincident circles (infinite intersections, not handled)
        if d == 0 and self.radius == other.radius:
            return []

        # The radical axis equation: 2(h2-h1)x + 2(k2-k1)y + (h1^2-h2^2+k1^2-k2^2+r2^2-r1^2) = 0
        a_rad = 2 * (other.center.x - self.center.x)
        b_rad = 2 * (other.center.y - self.center.y)
        c_rad = self.center.x**2 - other.center.x**2 + \
                self.center.y**2 - other.center.y**2 + \
                other.radius**2 - self.radius**2

        # Create two dummy points to define the radical line
        if abs(b_rad) > EPSILON: # If not a vertical line
            p1_rad = Point(0, -c_rad / b_rad)
            p2_rad = Point(1, (-c_rad - a_rad) / b_rad)
        else: # Vertical line
            p1_rad = Point(-c_rad / a_rad, 0)
            p2_rad = Point(-c_rad / a_rad, 1)

        radical_line = Line(p1_rad, p2_rad)
        
        # Intersect the radical line with the first circle
        return radical_line.intersection_circle(self)

    def translate(self, dx: float, dy: float) -> 'Circle':
        return Circle(self.center.translate(dx, dy), self.radius)

    def scale(self, factor: float, origin: Point) -> 'Circle':
        # Radius scales directly with the factor
        return Circle(self.center.scale(factor, origin), self.radius * factor)

    def rotate(self, angle_rad: float, origin: Point) -> 'Circle':
        return Circle(self.center.rotate(angle_rad, origin), self.radius)

class Triangle:
    """Represents a triangle defined by three vertex points."""
    def __init__(self, v1: Point, v2: Point, v3: Point):
        self.v1, self.v2, self.v3 = v1, v2, v3
        # Check for collinearity
        area = 0.5 * abs(v1.x*(v2.y-v3.y) + v2.x*(v3.y-v1.y) + v3.x*(v1.y-v2.y))
        if area < EPSILON:
            raise ValueError("The three points are collinear and do not form a triangle.")

    def __repr__(self) -> str:
        return f"Triangle(v1={self.v1}, v2={self.v2}, v3={self.v3})"

    def translate(self, dx: float, dy: float) -> 'Triangle':
        return Triangle(self.v1.translate(dx, dy), 
                        self.v2.translate(dx, dy), 
                        self.v3.translate(dx, dy))

    def scale(self, factor: float, origin: Point) -> 'Triangle':
        return Triangle(self.v1.scale(factor, origin),
                        self.v2.scale(factor, origin),
                        self.v3.scale(factor, origin))

    def rotate(self, angle_rad: float, origin: Point) -> 'Triangle':
        return Triangle(self.v1.rotate(angle_rad, origin),
                        self.v2.rotate(angle_rad, origin),
                        self.v3.rotate(angle_rad, origin))

# ==============================================================================
# 3. PERPENDICULAR LINE CALCULATION
# ==============================================================================

def foot_of_perpendicular(line: Line, point: Point) -> Point:
    """Calculates the foot of the perpendicular from a point to a line."""
    a, b, c = line.a, line.b, line.c
    x0, y0 = point.x, point.y
    
    # Using the direct formula derived from vector projection
    # k = -(a*x0 + b*y0 + c) / (a^2 + b^2)
    # x_foot = x0 + k * a
    # y_foot = y0 + k * b
    # A small refactor to avoid division by zero if a=b=0 (handled by Line class)
    # and to match the formula x' = x0 - a*k, y' = y0 - b*k
    # k = (a*x0 + b*y0 + c) / (a^2 + b^2)
    
    denom = a**2 + b**2
    k = (a * x0 + b * y0 + c) / denom
    
    x_foot = x0 - a * k
    y_foot = y0 - b * k
    
    return Point(x_foot, y_foot)
    
# ==============================================================================
# 4. PYTHAGOREAN THEOREM VERIFICATION
# ==============================================================================

def verify_pythagorean(line: Line, external_point: Point):
    """
    Forms a right-angled triangle and verifies the Pythagorean theorem.
    Points: A (external_point), B (foot_of_perpendicular), C (arbitrary point on line).
    """
    print("--- Pythagorean Theorem Verification ---")
    
    # A = The external point
    point_A = external_point
    print(f"Point A (External): {point_A}")

    # B = The foot of the perpendicular (forms the right angle)
    point_B = foot_of_perpendicular(line, point_A)
    print(f"Point B (Foot of Perpendicular): {point_B}")
    
    # C = An arbitrary point on the line (we'll use one of its defining points)
    # Ensure point C is distinct from point B for a valid triangle
    point_C = line.p1 if not line.p1 == point_B else line.p2
    print(f"Point C (On Line): {point_C}")
    
    if point_A == point_B or point_B == point_C or point_A == point_C:
        print("Points are not distinct. Cannot form a triangle for verification.")
        return

    # Calculate the lengths of the three sides
    # a = length of side opposite A (BC)
    # b = length of side opposite B (AC, the hypotenuse)
    # c = length of side opposite C (AB)
    # Standard notation is a^2 + b^2 = c^2 where c is hypotenuse.
    # Let's use more descriptive names.
    
    len_AB = point_A.distance_to(point_B) # one leg
    len_BC = point_B.distance_to(point_C) # other leg
    len_AC = point_A.distance_to(point_C) # hypotenuse
    
    print(f"Length of leg AB = {len_AB:.4f}")
    print(f"Length of leg BC = {len_BC:.4f}")
    print(f"Length of Hypotenuse AC = {len_AC:.4f}")
    
    # The sum of the squares of the two legs
    sum_sq_legs = len_AB**2 + len_BC**2
    sq_hypotenuse = len_AC**2
    
    print(f"(Leg AB)² + (Leg BC)² = {len_AB**2:.4f} + {len_BC**2:.4f} = {sum_sq_legs:.4f}")
    print(f"(Hypotenuse AC)² = {sq_hypotenuse:.4f}")
    
    # Verify using math.isclose for floating point comparison
    if math.isclose(sum_sq_legs, sq_hypotenuse, rel_tol=1e-9):
        print("✅ Verification successful: a² + b² ≈ c²")
    else:
        print("❌ Verification failed.")
    print("-" * 38 + "\n")


# ==============================================================================
# DEMONSTRATION
# ==============================================================================

if __name__ == "__main__":
    
    print("### GEOMETRY TOOLKIT DEMO ###\n")
    
    # --- Object Creation ---
    p1 = Point(1, 1)
    p2 = Point(7, 4)
    line1 = Line(p1, p2)
    
    p3 = Point(1, 6)
    p4 = Point(8, 2)
    line2 = Line(p3, p4)

    circle1 = Circle(Point(5, 5), 3)
    circle2 = Circle(Point(9, 5), 2)
    circle3 = Circle(Point(1, 1), 1)

    tri = Triangle(Point(0,0), Point(4,0), Point(2,3))

    print("--- 2. Intersection Calculations ---")
    print(f"Intersection of {line1} and {line2}: {line1.intersection_line(line2)}")
    print(f"Intersection of {line1} and {circle1}: {line1.intersection_circle(circle1)}")
    print(f"Intersection of {line2} and {circle1}: {line2.intersection_circle(circle1)}")
    print(f"Intersection of {circle1} and {circle2}: {circle1.intersection_circle(circle2)}")
    print(f"Intersection of {circle1} and {circle3}: {circle1.intersection_circle(circle3)}")
    print("-" * 36 + "\n")

    # --- Perpendicular Foot ---
    ext_point = Point(6, 9)
    print("--- 3. Perpendicular Foot Calculation ---")
    print(f"Line: {line1}")
    print(f"External Point: {ext_point}")
    print(f"Foot of Perpendicular: {foot_of_perpendicular(line1, ext_point)}")
    print("-" * 39 + "\n")

    # --- Pythagorean Verification ---
    verify_pythagorean(line1, ext_point)

    # --- Transformations ---
    print("--- 5. Geometric Transformations ---")
    print(f"Original Triangle: {tri}")
    # Translate
    tri_translated = tri.translate(2, 1)
    print(f"Translated (2,1):  {tri_translated}")
    # Scale
    scale_origin = Point(0,0)
    tri_scaled = tri.scale(2.0, scale_origin)
    print(f"Scaled by 2 from {scale_origin}: {tri_scaled}")
    # Rotate
    rotate_origin = Point(0,0)
    angle = math.pi / 2 # 90 degrees
    tri_rotated = tri.rotate(angle, rotate_origin)
    print(f"Rotated 90° from {rotate_origin}: {tri_rotated}")
    print("-" * 34 + "\n")