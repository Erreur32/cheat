Original project https://github.com/chrisallenlane/cheat 

----

Fork Verion [![cheapy](https://img.shields.io/badge/V%20-2.2.32-brightgreen.svg)](https://github.com/Erreur32/cheat)   

Features added by by 🅴🆁🆁🅴🆄🆁32 : 
 - Add color seach and prompt
 - Add Subdir creation and search
 - Add remove sheet file (-r) with confirmation
 - Add color help text


Origin repo https://github.com/Erreur32/cheat.git

Mirror repo https://git.echosystem.fr/Erreur32/cheat.git 

----


Put in your bashrc

```sh
function _cheat_autocomplete {
    sheets=$(cheat -l | cut -d' ' -f1)
    COMPREPLY=()
    if [ $COMP_CWORD = 1 ]; then
	COMPREPLY=(`compgen -W "$sheets" -- $2`)
    fi
}

complete -F _cheat_autocomplete cheat
```

Installing
----------

### manually ###
First, install the dependencies:

```sh
[sudo] pip install docopt pygments appdirs
```

Then clone this repository:
```sh
git clone https://github.com/Erreur32/cheat.git
```

Lastly, `cd` into the cloned directory, then run:

```sh
[sudo] python setup.py install
```

cheat
=====
`cheat` allows you to create and view interactive cheatsheets on the
command-line. It was designed to help remind \*nix system administrators of
options for commands that they use frequently, but not frequently enough to
remember.

 

Example
-------
The next time you're forced to disarm a nuclear weapon without consulting
Google, you may run:

```sh
cheat tar
```

You will be presented with a cheatsheet resembling:

```sh
# To extract an uncompressed archive: 
tar -xvf '/path/to/foo.tar'

# To extract a .gz archive:
tar -xzvf '/path/to/foo.tgz'

# To create a .gz archive:
tar -czvf '/path/to/foo.tgz' '/path/to/foo/'

# To extract a .bz2 archive:
tar -xjvf '/path/to/foo.tgz'

# To create a .bz2 archive:
tar -cjvf '/path/to/foo.tgz' '/path/to/foo/'
```

To see what cheatsheets are available, run `cheat -l`.

Note that, while `cheat` was designed primarily for \*nix system administrators,
it is agnostic as to what content it stores. If you would like to use `cheat`
to store notes on your favorite cookie recipes, feel free.

 

Modifying Cheatsheets
---------------------
The value of `cheat` is that it allows you to create your own cheatsheets - the
defaults are meant to serve only as a starting point, and can and should be
modified.

Cheatsheets are stored in the `~/.cheat/` directory, and are named on a
per-keyphrase basis. In other words, the content for the `tar` cheatsheet lives
in the `~/.cheat/tar` file.

Provided that you have a `CHEAT_EDITOR`, `VISUAL`, or `EDITOR` environment
variable set, you may edit cheatsheets with:

```sh
cheat -e foo
```

If the `foo` cheatsheet already exists, it will be opened for editing.
Otherwise, it will be created automatically.

After you've customized your cheatsheets, I urge you to track `~/.cheat/` along
with your [dotfiles][].


Configuring
-----------

### Setting a DEFAULT_CHEAT_DIR ###
Personal cheatsheets are saved in the `~/.cheat` directory by default, but you
can specify a different default by exporting a `DEFAULT_CHEAT_DIR` environment
variable:

```sh
export DEFAULT_CHEAT_DIR='/path/to/my/cheats'
```

### Setting a CHEATPATH ###
You can additionally instruct `cheat` to look for cheatsheets in other
directories by exporting a `CHEATPATH` environment variable:

```sh
export CHEATPATH='/path/to/my/cheats'
```

You may, of course, append multiple directories to your `CHEATPATH`:

```sh
export CHEATPATH="$CHEATPATH:/path/to/more/cheats"
```

You may view which directories are on your `CHEATPATH` with `cheat -d`.

### Enabling Syntax Highlighting ###
`cheat` can optionally apply syntax highlighting to your cheatsheets. To enable
syntax highlighting, export a `CHEATCOLORS` environment variable:

```sh
export CHEATCOLORS=true
```

#### Specifying a Syntax Highlighter ####
You may manually specify which syntax highlighter to use for each cheatsheet by
wrapping the sheet's contents in a [Github-Flavored Markdown code-fence][gfm].

Example:

<pre>
```sql
-- to select a user by ID
SELECT *
FROM Users
WHERE id = 100
```
</pre>

If no syntax highlighter is specified, the `bash` highlighter will be used by
default.


See Also:
---------
- [Enabling Command-line Autocompletion][autocompletion]
- [Related Projects][related-projects]


[autocompletion]:   https://github.com/chrisallenlane/cheat/wiki/Enabling-Command-line-Autocompletion
[dotfiles]:         http://dotfiles.github.io/
[gfm]:              https://help.github.com/articles/creating-and-highlighting-code-blocks/
[installing]:       https://github.com/chrisallenlane/cheat/wiki/Installing
[related-projects]: https://github.com/chrisallenlane/cheat/wiki/Related-Projects
