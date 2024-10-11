# JSON parser
## Synopsis
A JSON parser implemented in pure python.

This is a learning project. For real-world use cases, consider [python's
built in json module](https://docs.python.org/3/library/json.html).

For a pure python implementation, consider 
[json-stream](https://github.com/daggaz/json-stream)


## Quick Start
This project project has no dependencies except for python itself
1. Clone this repo
2. `python3 main.py` to see it in action


## Structure
I divided this parser into the following 2 parts

### Lexer / Tokenizer
This is the first parsing step. It turns the list of characters (json file)
into slightly larger datatypes, defined in lexer.py. It also checks for some
basic errors, and saves the position of each "token" for future error handling

### Analyzer
This is 2nd, and hardest part. It involved writing recursive functions to parse 
the tree-like JSON structure.


## Further Learning
There are 2 big concepts that I want to try incorporating into the parser code. 
I think the tokenizer is OK as-is.

- State Machines
  - This seems to be a useful tool for modelling more complex grammars in code
    form

- Iterative alternative to recursive parser
  - Having no recursion would suggest that a stack is implemented into the
    *program* itself, as opposed to being managed by the python runtime. This
    would allow for a depth-limit to be specified in the code, or to be 
    exposed as an option for the library's end-user. In my opinion, this is 
    better than than the recursion depth being dependent on the system's python
    implementation.
  - Complex iterative logic is one of my weak-points. This would make great 
    practice


## What could I have done differently?
### Make an interface for getting and consuming single tokens
I found that in the analyzer, I only ever had to increment the token list counter
by 1. I thought that maybe I would need to increment by more in the future, but 
this never ended up true, at least for this JSON parser. It would be very helpful
to have a function to "consume" a token, aka: increment the token list counter.

Furthermore, I only ever had to get the current token's value using 
`ParserData.safeget(ParserData.head)`. That whole line could have been a single
function. This may be different for other grammars, but for json, I only ever
needed to get the current head's position.


### Implement state machines.
Although complex for a small parser like this one, State Machines seem to be a 
useful abstraction for modelling grammar in code form. This may end up cleaner 
than the chains of if-statements found in `analyzer.py`.

