from enum import Enum
from math import atan2, sqrt, pow, sin, cos, pi
from matplotlib import pyplot as plt

class InexistentCoordinateTypeError(Exception):
    def __init__(self : Exception) -> None:
        super().__init__()
        self.message = "Inexistent Coordinate Type: is your type a valid item of CoordinateType enumerator?"
        self.error_code = -1


    def __str__(self) -> str:
        return f"{self.message} (Error Code: {self.error_code})"


class CoordinateType(Enum):
    POLAR : int = 0
    CARTESIAN : int = 1 


class Complex:

    real : float = None
    imaginary : float = None

    magnitude : float = None
    phase : float = None

    default_coordinate_type : CoordinateType = None


    def __init__(
        self : Complex, 
        _a : float, 
        _b : float, 
        _coordinate_type : CoordinateType
    ) -> None:
        if _coordinate_type not in (CoordinateType.POLAR, CoordinateType.CARTESIAN):
            raise InexistentCoordinateTypeError()
        self.default_coordinate_type = _coordinate_type
        if _coordinate_type is CoordinateType.CARTESIAN:
            self.real = _a
            self.imaginary = _b
            self.to_polar()
        elif _coordinate_type is CoordinateType.POLAR:
            self.magnitude = _a
            self.phase = _b
            self.to_cartesian()


    def __str__(self) -> str:
        if self.default_coordinate_type is CoordinateType.CARTESIAN:
            return f"Re: {self.real:.2f}, Im: {self.imaginary:.2f}"
        if self.default_coordinate_type is CoordinateType.POLAR:
            return f"|•|: {self.magnitude:.2f}, ∠: {self.phase:.2f}"
        return ""


    def to_polar(self : Complex) -> None:
        if (
            not self.real is None 
            and not self.imaginary is None 
        ):
            self.phase = atan2(self.imaginary, self.real)
            self.magnitude = sqrt(pow(self.real, 2) + pow(self.imaginary, 2))


    def to_cartesian(self : Complex) -> None:
        if (
            not self.magnitude is None 
            and not self.phase is None
        ):
            self.real = cos(self.phase) * self.magnitude
            self.imaginary = sin(self.phase) * self.magnitude

    
    def to_default_polar(self : Complex) -> None:
        self.to_polar()
        self.default_coordinate_type = CoordinateType.POLAR


    def to_default_cartesian(self : Complex) -> None:
        self.to_cartesian()
        self.default_coordinate_type = CoordinateType.CARTESIAN


    def _root_phase(self : Complex, angle : float, n : int, k : int) -> float:
        return (angle + 2 * k * pi) / n


    def calculate_complex_roots(self : Complex, roots_number : int) -> list[Complex]:
        self.to_polar()
        root_modulus : float = pow(self.magnitude, 1 / roots_number)
        return [
            Complex(
                root_modulus, 
                self._root_phase(self.phase, roots_number, k), 
                CoordinateType.POLAR
            ) for k in range(roots_number)
        ]


    def plot_complex_roots(self, root_count: int, show_circle: bool = True) -> list[Complex]:
        if root_count < 1:
            raise ValueError("Root number must be at least 1")

        roots = self.calculate_complex_roots(root_count)

        xs, ys = [], []
        for r in roots:
            r.to_cartesian()
            xs.append(r.real)
            ys.append(r.imaginary)

        fig, ax = plt.subplots(figsize=(6, 6))

        if show_circle:
            radius = abs(roots[0].magnitude)
            circle = plt.Circle(
                (0, 0), radius,
                fill=False, color="gray", linestyle="--", linewidth=1
            )
            ax.add_patch(circle)

        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)

        ax.scatter(xs, ys, s=80, color="crimson", zorder=5)

        for i, (x, y) in enumerate(zip(xs, ys)):
            ax.annotate(
                f"z{i}",
                (x, y),
                textcoords="offset points",
                xytext=(8, 8),
                fontsize=11,
            )
            ax.plot([0, x], [0, y], color="steelblue", linewidth=1, alpha=0.6)

        self.to_cartesian()
        ax.scatter([self.real], [self.imaginary], s=120, marker="*",
                   color="green", zorder=5, label="z")
        ax.annotate("Starting number", (self.real, self.imaginary),
                    textcoords="offset points", xytext=(8, 8),
                    fontsize=12, color="green")

        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("Re")
        ax.set_ylabel("Im")
        ax.set_title(f"Radici {root_count}-esime di z  (|z| = {z.magnitude:.2f}, ∠z = {z.phase:.2f} rad)")
        print(f"Radici {root_count}-esime di z  (|z| = {z.magnitude:.2f}, ∠z = {z.phase:.2f} rad)")
        
        ax.grid(True, linestyle=":", alpha=0.5)

        lim = max(max(abs(v) for v in xs + ys), abs(z.real), abs(z.imaginary)) * 1.3
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

        fig.savefig("roots.png", dpi=150, bbox_inches="tight")

        return roots


if __name__ == "__main__":
    z = Complex(1, pi / 4, CoordinateType.POLAR)
    z.plot_complex_roots(5)
