This program parses yardsalesearch.com for yard sales and lists them out. Arguments can manipulate the given information. Currently the location and radius is hard coded into the url, but this can be changed by just aquiring a new url with location and radius selected.

###arguments
give all information

    python search.py
list help arguments

    python search.py --help
remove link from output

    python search.py -l
remove description from output

    python search.py -d
remove date and time from output

    python search.py -t
remove separator from output

    python search.py -s
remove address from output

    python search.py -a
remove total sales count from output

    python search.py -e
combine removals, only show address

    python search.py -ldts
select number of pages to parse

    python search -p 2
output to filename

    python search -o sales.txt
    
Any combination of arguments can be given to give the desired output. 
    


usage: search.py [-h] [-l] [-d] [-t] [-s] [-a] [-e] [-p PAGE] [-o OUTPUT]

Arguments

optional arguments:
  -h, --help            show this help message and exit
  -l, --link            Remove links from output
  -d, --desc            Remove descriptions from output
  -t, --time            Remove date and time from output
  -s, --sep             Remove separator from output
  -a, --address         Remove address from output
  -e, --entire          Remove entire total sales number from output
  -p PAGE, --page PAGE  number of pages to parse
  -o OUTPUT, --output OUTPUT
                        output to filename given
