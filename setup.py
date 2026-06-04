from setuptools import setup

setup(
    name="rux-lexer",
    version="0.1",
    packages=["rux_lexer"],
    entry_points={
        "pygments.lexers": [
            "rux = rux_lexer.lexer:RuxLexer",
        ]
    }
)