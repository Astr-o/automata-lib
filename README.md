# automata-lib Library 

Simple finite state automata library providing:

* FSA parser (*partially complete*)
* FSA simulator 
* FSA graph model (*early stage*)
* Basic command line interface

## Installation 

Requires Python 2.7+, not tested with Python 3

To use in your projects simply include `/automata-core-lib` in your python module path

## Usage 
	
From your command prompt with python configured run

	python automata-cli.py [machine_file] [strings]


`machine_file` - supported descripton file

`strings` - space seperated list of strings to test on machine

### Example Files 

Look in `/examples` for example fsa description files.

To get started try

	python automata-cli.py examples/plaintextmachine "aaa"


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History



## Credits



## License

**Avaliable under GNU GPL 3.0**

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


