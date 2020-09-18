#!/usr/bin/env python

# Copyright (c) 2020 Stanford University
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR(S) DISCLAIM ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL AUTHORS BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Usage: ttinspect.py <file> <start_string> 

Options:
    -h, --help              Show this screen
"""

from docopt import docopt
from collections import namedtuple
import re
import string

Event = namedtuple('Event', ['timestamp', 'message'])
Trace = namedtuple('Trace', ['trace', 'cyclesPerSecond', 'startCycles'])
def parseTrace(f):
  traceOutput = []
  cyclesPerSecond = 0
  startCycles = 0
  with open(f) as trace:
      for line in trace:
        if 'CYCLES_PER_SECOND' in line:
            cyclesPerSecond = float(line.strip().split()[1])
            continue
        if 'START_CYCLES' in line:
            startCycles = int(line.strip().split()[1])
            continue
        match = re.match(' *([0-9.]+) ns \(\+ *([0-9.]+) ns\): (.*)', line)
        if not match: continue
        thisEventTime = float(match.group(1))
        thisEvent = match.group(3)
        traceOutput.append(Event(thisEventTime, thisEvent))
  return Trace(traceOutput, cyclesPerSecond, startCycles)

def main(args):
    trace = parseTrace(args['<file>'])
    start_string = args['<start_string>']
    prevTime = 0
    startTime = 0
    for event in trace[0]:
        if string.find(event.message, start_string) >= 0:
            startTime = event.timestamp
        print('%8.1f ns (+%6.1f ns): %s' % (event.timestamp - startTime, \
            event.timestamp - prevTime, event.message))
        prevTime = event.timestamp

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
