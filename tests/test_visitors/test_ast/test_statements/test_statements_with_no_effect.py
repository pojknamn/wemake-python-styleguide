import pytest

from wemake_python_styleguide.violations.best_practices import (
    StatementHasNoEffectViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    StatementsWithBodiesVisitor,
)

# Modules:

module_template = """
{0}
"""

module_attribute_docs_template = """
x: int = 1
{0}
"""

# Simple conditions:

if_template = """
if some:
    {0}
"""

if_elif_template = """
if some:
    print()
elif not some:
    {0}
"""

if_else_template = """
if some:
    print()
else:
    {0}
"""

# Loops:

for_template = """
for some in []:
    {0}
"""

for_else_template = """
for some in []:
    print()
else:
    {0}
"""

while_template = """
while True:
    {0}
"""

while_else_template = """
while True:
    print()
else:
    {0}
"""

# Exception handling:

try_template = """
try:
    {0}
except Exception:
    print()
"""

try_except_template = """
try:
    print()
except Exception:
    {0}
"""

try_else_template = """
try:
    print()
except Exception:
    print()
else:
    {0}
"""

try_finally_template = """
try:
    print()
finally:
    {0}
"""

# Context managers:

with_template = """
with some:
    {0}
"""

# Functions:

function_template = """
def function():
    {0}
"""

function_extra_template = """
def function():
    x = 1
    {0}
"""

# Classes:

class_template = """
class Test:
    {0}
"""

class_extra_template = """
class Test:
    def some(self):
        pass
    {0}
"""

class_attribute_docs_template = """
class Test:
    x = 1
    {0}
"""

# Async:

async_function_template = """
async def function():
    {0}
"""

async_with_template = """
async def container():
    async with some:
        {0}
"""

async_for_template = """
async def container():
    async for some in []:
        {0}
"""

async_for_else_template = """
async def container():
    async for some in []:
        print()
    else:
        {0}
"""

# PM:

pattern_matching = """
match some:
    case other:
        {0}
"""


@pytest.mark.parametrize(
    'code',
    [
        module_template,
        module_attribute_docs_template,
        if_template,
        if_elif_template,
        if_else_template,
        for_template,
        for_else_template,
        while_template,
        while_else_template,
        try_template,
        try_except_template,
        try_else_template,
        try_finally_template,
        with_template,
        function_template,
        function_extra_template,
        class_template,
        class_attribute_docs_template,
        class_extra_template,
        async_function_template,
        async_with_template,
        async_for_template,
        async_for_else_template,
        pattern_matching,
    ],
)
@pytest.mark.parametrize(
    'statement',
    [
        'print',
        'object.mro',
        '3 > 4',
        '1 + 2',
        '-100',
    ],
)
def test_statement_with_no_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that unreachable code is detected."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StatementHasNoEffectViolation])


@pytest.mark.parametrize(
    'code',
    [
        module_template,
        module_attribute_docs_template,
        if_template,
        if_elif_template,
        if_else_template,
        for_template,
        for_else_template,
        while_template,
        while_else_template,
        try_template,
        try_except_template,
        try_else_template,
        try_finally_template,
        with_template,
        function_template,
        function_extra_template,
        class_template,
        class_attribute_docs_template,
        class_extra_template,
        async_function_template,
        async_with_template,
        async_for_template,
        async_for_else_template,
        pattern_matching,
    ],
)
@pytest.mark.parametrize(
    'statement',
    [
        'some_name = 1 + 2',
        'call()',
        'object.mro()',
        'del some',
        'some_var: int',
        'x += 2',
        'x += y + 2',
        'x += check(2)',
        'x -= 1',
        'x *= 1',
        'x **= 1',
        'x /= 1',
        'x ^= 1',
        'x %= 1',
        'x >>= 1',
        'x <<= 1',
        'x &= 1',
        'x |= 1',
        'x -= x.attr("a")',
        'x -= test(x)',
        'x -= x.method()',
        'x -= x.attr + 1',
        'x -= test(x) + 1',
        'x = 2 + x',
    ],
)
def test_statement_with_regular_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing functions, methods, and assignment works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        function_template,
    ],
)
@pytest.mark.parametrize(
    'statement',
    [
        'return',
        'yield',
        'yield from some',
        'raise TypeError()',
    ],
)
def test_statement_with_function_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that `return` and `yield` works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        async_function_template,
    ],
)
@pytest.mark.parametrize(
    'statement',
    [
        'await some',
        'return',
        'yield',
        'raise TypeError()',
    ],
)
def test_statement_with_await_effect(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that `await` works."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        function_template,
        async_function_template,
        class_template,
        class_attribute_docs_template,
        module_template,
        module_attribute_docs_template,
    ],
)
@pytest.mark.parametrize(
    'statement',
    [
        '"docstring"',
        '"""docstring"""',
    ],
)
def test_statement_with_docstring_definition(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that docstrings work."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        function_template,
        async_function_template,
        class_template,
    ],
)
def test_statement_with_ellipsis_definition(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that `...` works."""
    tree = parse_ast_tree(code.format('...'))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        if_template,
        if_elif_template,
        if_else_template,
        for_template,
        for_else_template,
        while_template,
        while_else_template,
        try_template,
        try_except_template,
        try_else_template,
        try_finally_template,
        with_template,
        async_with_template,
        async_for_template,
        async_for_else_template,
        function_extra_template,
        class_extra_template,
        pattern_matching,
    ],
)
@pytest.mark.parametrize(
    'statement',
    [
        '"docstring"',
        '...',
        'some_name',
    ],
)
def test_statement_useless_special_statements(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    default_options,
):
    """Testing that errors are correctly detected."""
    tree = parse_ast_tree(code.format(statement))

    visitor = StatementsWithBodiesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StatementHasNoEffectViolation])
