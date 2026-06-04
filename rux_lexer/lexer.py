from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

class RuxLexer(RegexLexer):
    name = "Rux"
    aliases = ["rux"]
    filenames = ["*.rux"]

    tokens = {
        "root": [
            # Comments
            (r'///.*?$', Comment.Special),
            (r'//.*?$', Comment.Single),
            (r'/\*[\s\S]*?\*/', Comment.Multiline),

            # Strings
            (r'(c8|c16|c32)"', String, "string"),
            (r'"', String, "string"),
            (r"(c8|c16|c32)'", String.Char, "char"),
            (r"'", String.Char, "char"),

            # Attributes
            (r'@\[[^\]]*\]', Name.Decorator),

            # Compile-time intrinsics
            (
                r'(#)(module|file|function|line|column|date|time)\b',
                bygroups(Punctuation, Name.Constant)
            ),

            # Keywords
            (
                r'\b('
                r'break|continue|do|else|for|if|in|loop|match|return|while|'
                r'const|let|pub|var|'
                r'asm|async|extend|extern|import|export|module|'
                r'as|is'
                r')\b',
                Keyword
            ),

            # Type declarations
            (
                r'\b(interface|enum|struct|union|type)\b',
                Keyword.Declaration
            ),

            # Boolean/null
            (
                r'\b(true|false|null)\b',
                Keyword.Constant
            ),

            # Types
            (
                r'\b('
                r'int|int8|int16|int32|int64|int128|int256|int512|'
                r'uint|uint8|uint16|uint32|uint64|uint128|uint256|uint512|'
                r'float|float8|float16|float32|float64|float80|float128|float256|float512|'
                r'char|char8|char16|char32|char64|char128|char256|char512|'
                r'bool|bool8|bool16|bool32|bool64|bool128|bool256|bool512|'
                r'opaque'
                r')\b',
                Keyword.Type
            ),

            # Function definitions
            (
                r'\b(func)(\s+)([A-Za-z_][A-Za-z0-9_]*)',
                bygroups(Keyword, Whitespace, Name.Function)
            ),

            # Numbers
            (r'0x[\da-fA-F_]+', Number.Hex),
            (r'0o[0-7_]+', Number.Oct),
            (r'0b[01_]+', Number.Bin),
            (r'\d[\d_]*(\.\d[\d_]*)?([eE][+-]?\d+)?', Number),

            # Operators
            (
                r'(==|!=|<=|>=|=>|<<=|>>=|\+=|-=|\*=|/=|%=|&=|\|=|\^=)',
                Operator
            ),
            (
                r'(\+\+|--|\+|-|\*|/|%|&&|\|\||!|~|\^|<<|>>|=)',
                Operator
            ),

            # Punctuation
            (r'(::|\.\.=|\.\.\.|\.\.|[{}()\[\],;:.<>])', Punctuation),

            # Identifiers
            (r'[A-Za-z_][A-Za-z0-9_]*', Name),

            (r'\s+', Whitespace),
        ],

        "string": [
            (r'\\.', String.Escape),
            (r'"', String, "#pop"),
            (r'[^"\\]+', String),
        ],

        "char": [
            (r'\\.', String.Escape),
            (r"'", String.Char, "#pop"),
            (r"[^'\\]+", String.Char),
        ],
    }